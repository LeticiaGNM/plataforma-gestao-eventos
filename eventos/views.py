from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Categoria, Evento, Inscricao


def home(request):
    return render(request, 'eventos/home.html')


@login_required
def lista_eventos(request):
    termo = request.GET.get('q', '').strip()
    categoria_param = request.GET.get('categoria', '')

    # Apenas eventos que ainda vão acontecer (hoje ou depois).
    eventos = (
        Evento.objects
        .select_related('local', 'categoria')
        .filter(data__gte=timezone.localdate())
    )

    # Pesquisa por texto no título, na descrição ou no nome do local.
    if termo:
        eventos = eventos.filter(
            Q(titulo__icontains=termo)
            | Q(descricao__icontains=termo)
            | Q(local__nome__icontains=termo)
        )

    # Filtro por categoria (só aceita números, ignorando valores estranhos na URL).
    categoria_selecionada = None
    if categoria_param.isdigit():
        categoria_selecionada = int(categoria_param)
        eventos = eventos.filter(categoria_id=categoria_selecionada)

    paginator = Paginator(eventos, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Mantém a busca e o filtro nos links da paginação (tudo, menos o número da página).
    parametros = request.GET.copy()
    parametros.pop('page', None)

    contexto = {
        'page_obj': page_obj,
        'paginator': paginator,
        'categorias': Categoria.objects.all(),
        'q': termo,
        'categoria_selecionada': categoria_selecionada,
        'querystring': parametros.urlencode(),
    }
    return render(request, 'eventos/lista.html', contexto)


@login_required
def detalhe_evento(request, pk):
    evento = get_object_or_404(
        Evento.objects.select_related('local', 'categoria', 'organizador'),
        pk=pk,
    )
    inscricao = Inscricao.objects.filter(usuario=request.user, evento=evento).first()
    contexto = {
        'evento': evento,
        'inscricao': inscricao,
        'inscrito': inscricao is not None and inscricao.confirmada,
    }
    return render(request, 'eventos/detalhe.html', contexto)


@login_required
@require_POST
def inscrever(request, pk):
    # A transação + o bloqueio da linha do evento evitam que duas pessoas
    # peguem a última vaga ao mesmo tempo.
    with transaction.atomic():
        evento = get_object_or_404(Evento.objects.select_for_update(), pk=pk)
        inscricao = Inscricao.objects.filter(usuario=request.user, evento=evento).first()

        if inscricao and inscricao.confirmada:
            messages.info(request, 'Você já está inscrito neste evento.')
        elif evento.encerrado:
            messages.error(request, 'Este evento já foi encerrado.')
        elif evento.esgotado:
            messages.error(request, 'Não há mais vagas disponíveis para este evento.')
        else:
            if inscricao:
                # Estava cancelada: reativa a mesma inscrição (a restrição única impede duplicar).
                inscricao.status = Inscricao.Status.CONFIRMADA
                inscricao.save(update_fields=['status'])
            else:
                Inscricao.objects.create(usuario=request.user, evento=evento)
            messages.success(request, 'Inscrição realizada com sucesso!')

    return redirect('detalhe_evento', pk=pk)


@login_required
@require_POST
def cancelar_inscricao(request, pk):
    # Filtra por usuario=request.user: ninguém cancela a inscrição de outra pessoa.
    inscricao = get_object_or_404(
        Inscricao.objects.select_related('evento'),
        usuario=request.user,
        evento_id=pk,
    )

    if inscricao.pode_cancelar:
        inscricao.status = Inscricao.Status.CANCELADA
        inscricao.save(update_fields=['status'])
        messages.success(request, 'Inscrição cancelada com sucesso.')
    else:
        messages.error(request, 'Esta inscrição não pode ser cancelada.')

    if request.POST.get('origem') == 'minhas':
        return redirect('minhas_inscricoes')
    return redirect('detalhe_evento', pk=pk)


@login_required
def minhas_inscricoes(request):
    inscricoes = (
        Inscricao.objects
        .filter(usuario=request.user)
        .select_related('evento', 'evento__local', 'evento__categoria')
    )
    return render(request, 'eventos/minhas_inscricoes.html', {'inscricoes': inscricoes})

@login_required
def painel(request):
    # Somente a equipe (is_staff) acessa o painel; os demais recebem erro 403.
    if not request.user.is_staff:
        raise PermissionDenied

    hoje = timezone.localdate()
    confirmada = Inscricao.Status.CONFIRMADA

    eventos_por_categoria = Categoria.objects.annotate(total=Count('eventos')).order_by('nome')
    mais_procurados = (
        Evento.objects
        .annotate(total=Count('inscricoes', filter=Q(inscricoes__status=confirmada)))
        .order_by('-total', 'titulo')[:5]
    )

    contexto = {
        'total_eventos': Evento.objects.count(),
        'proximos_eventos': Evento.objects.filter(data__gte=hoje).count(),
        'total_inscricoes': Inscricao.objects.filter(status=confirmada).count(),
        'total_participantes': get_user_model().objects.filter(is_staff=False).count(),
        'grafico_categorias': {
            'labels': [c.nome for c in eventos_por_categoria],
            'valores': [c.total for c in eventos_por_categoria],
        },
        'grafico_eventos': {
            'labels': [e.titulo for e in mais_procurados],
            'valores': [e.total for e in mais_procurados],
        },
    }
    return render(request, 'eventos/painel.html', contexto)