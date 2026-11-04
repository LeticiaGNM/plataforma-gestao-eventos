from django.contrib import admin, messages
from django.db.models import Count
from django.utils import timezone

from .models import Categoria, Evento, Inscricao, Local


class PeriodoFilter(admin.SimpleListFilter):
    # Filtro personalizado: separa os eventos por período.
    title = 'período'
    parameter_name = 'periodo'

    def lookups(self, request, model_admin):
        return [
            ('proximos', 'Próximos eventos'),
            ('hoje', 'Hoje'),
            ('passados', 'Já realizados'),
        ]

    def queryset(self, request, queryset):
        hoje = timezone.localdate()
        if self.value() == 'proximos':
            return queryset.filter(data__gte=hoje)
        if self.value() == 'hoje':
            return queryset.filter(data=hoje)
        if self.value() == 'passados':
            return queryset.filter(data__lt=hoje)
        return queryset


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'total_eventos')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_total=Count('eventos'))

    @admin.display(description='Eventos', ordering='_total')
    def total_eventos(self, obj):
        return obj._total


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'capacidade')
    list_filter = ('capacidade',)
    search_fields = ('nome', 'endereco')
    ordering = ('nome',)


class InscricaoInline(admin.TabularInline):
    # Permite ver e editar as inscrições dentro da página do evento.
    model = Inscricao
    extra = 0
    fields = ('usuario', 'status', 'data_inscricao')
    readonly_fields = ('data_inscricao',)
    autocomplete_fields = ('usuario',)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'horario', 'categoria', 'local', 'organizador', 'ocupacao')
    list_filter = (PeriodoFilter, 'categoria', 'local', 'data')
    search_fields = ('titulo', 'descricao', 'local__nome', 'categoria__nome')
    date_hierarchy = 'data'
    ordering = ('data', 'horario')
    list_select_related = ('categoria', 'local', 'organizador')
    readonly_fields = ('criado_em',)
    inlines = [InscricaoInline]
    fieldsets = (
        ('Informações gerais', {'fields': ('titulo', 'descricao', 'imagem')}),
        ('Data e local', {'fields': ('data', 'horario', 'local', 'vagas')}),
        ('Organização', {'fields': ('categoria', 'organizador', 'criado_em')}),
    )

    @admin.display(description='Ocupação')
    def ocupacao(self, obj):
        return f'{obj.vagas_ocupadas}/{obj.limite_vagas}'

    def get_changeform_initial_data(self, request):
        # Ao criar um evento, o organizador já vem preenchido com quem está logado.
        dados = super().get_changeform_initial_data(request)
        dados['organizador'] = request.user.pk
        return dados


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'status', 'data_inscricao')
    list_filter = ('status', 'evento__categoria', 'evento')
    search_fields = ('usuario__username', 'usuario__email', 'evento__titulo')
    date_hierarchy = 'data_inscricao'
    list_select_related = ('usuario', 'evento')
    autocomplete_fields = ('usuario', 'evento')
    readonly_fields = ('data_inscricao',)
    actions = ['cancelar_inscricoes']

    @admin.action(description='Cancelar inscrições selecionadas')
    def cancelar_inscricoes(self, request, queryset):
        total = queryset.update(status=Inscricao.Status.CANCELADA)
        self.message_user(request, f'{total} inscrição(ões) cancelada(s).', messages.SUCCESS)