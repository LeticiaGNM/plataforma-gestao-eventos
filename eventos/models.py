from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    # Tipo do evento (ex.: Tecnologia, Música, Esportes).
    nome = models.CharField(max_length=80, unique=True)
    descricao = models.TextField('descrição', blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Local(models.Model):
    # Lugar físico onde os eventos acontecem.
    nome = models.CharField(max_length=120)
    endereco = models.CharField('endereço', max_length=255)
    capacidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Número máximo de pessoas que o local comporta.',
    )

    class Meta:
        ordering = ['nome']
        verbose_name = 'local'
        verbose_name_plural = 'locais'

    def __str__(self):
        return f'{self.nome} (capacidade: {self.capacidade})'


class Evento(models.Model):
    titulo = models.CharField('título', max_length=150)
    descricao = models.TextField('descrição', blank=True)
    data = models.DateField()
    horario = models.TimeField('horário')
    local = models.ForeignKey(Local, on_delete=models.PROTECT, related_name='eventos')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='eventos')
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='eventos_organizados',
        limit_choices_to={'is_staff': True},
    )
    vagas = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text='Opcional. Se ficar em branco, vale a capacidade do local.',
    )
    imagem = models.ImageField('imagem de capa', upload_to='eventos/', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data', 'horario']

    def __str__(self):
        return f'{self.titulo} ({self.data:%d/%m/%Y})'

    def clean(self):
        # Regra de negócio: o limite de vagas não pode passar da capacidade do local.
        super().clean()
        if self.vagas is not None and self.local_id and self.vagas > self.local.capacidade:
            raise ValidationError({
                'vagas': f'O número de vagas ({self.vagas}) não pode ser maior '
                         f'que a capacidade do local ({self.local.capacidade}).'
            })

    @property
    def data_hora(self):
        return timezone.make_aware(datetime.combine(self.data, self.horario))

    @property
    def encerrado(self):
        return self.data_hora < timezone.now()

    @property
    def limite_vagas(self):
        return self.vagas if self.vagas is not None else self.local.capacidade

    @property
    def vagas_ocupadas(self):
        return self.inscricoes.filter(status=Inscricao.Status.CONFIRMADA).count()

    @property
    def vagas_disponiveis(self):
        return max(self.limite_vagas - self.vagas_ocupadas, 0)

    @property
    def esgotado(self):
        return self.vagas_disponiveis == 0


class Inscricao(models.Model):
    class Status(models.TextChoices):
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscricoes',
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField('data da inscrição', auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONFIRMADA)

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        ordering = ['-data_inscricao']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'evento'],
                name='inscricao_unica_por_usuario_evento',
            ),
        ]

    def __str__(self):
        return f'{self.usuario} em {self.evento.titulo} ({self.get_status_display()})'

    @property
    def confirmada(self):
        return self.status == self.Status.CONFIRMADA

    @property
    def pode_cancelar(self):
        return self.confirmada and not self.evento.encerrado