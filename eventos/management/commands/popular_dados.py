from datetime import time, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from eventos.models import Categoria, Evento, Inscricao, Local

CATEGORIAS = [
    ('Tecnologia', 'Palestras, workshops e maratonas de programação.'),
    ('Música', 'Shows, festivais e apresentações musicais.'),
    ('Esportes', 'Campeonatos, corridas e atividades esportivas.'),
    ('Educação', 'Cursos, seminários e aulas abertas.'),
    ('Negócios', 'Networking, feiras e eventos empresariais.'),
    ('Arte e Cultura', 'Exposições, teatro e cinema.'),
]

LOCAIS = [
    ('Auditório Central', 'Av. Principal, 100 - Centro', 300),
    ('Centro de Convenções', 'Rua das Flores, 250 - Centro', 800),
    ('Ginásio Municipal', 'Av. dos Esportes, 50', 1200),
    ('Teatro Municipal', 'Praça da Matriz, 1', 400),
    ('Sala de Workshops', 'Rua do Saber, 75 - Sala 3', 30),
]

# (título, descrição, dias a partir de hoje, horário, local, categoria, vagas)
EVENTOS = [
    ('Semana de Tecnologia', 'Palestras e oficinas sobre desenvolvimento web, dados e IA.',
     7, time(9, 0), 'Auditório Central', 'Tecnologia', None),
    ('Workshop de Git e GitHub', 'Aprenda versionamento de código na prática. Vagas limitadas!',
     3, time(14, 0), 'Sala de Workshops', 'Tecnologia', 2),
    ('Festival de Música Universitária', 'Bandas da região em uma noite de música ao vivo.',
     15, time(19, 30), 'Teatro Municipal', 'Música', None),
    ('Corrida Solidária 5 km', 'Corrida de rua com renda destinada a instituições locais.',
     20, time(7, 0), 'Ginásio Municipal', 'Esportes', 500),
    ('Feira de Empreendedorismo', 'Estandes, palestras e networking para novos negócios.',
     25, time(10, 0), 'Centro de Convenções', 'Negócios', None),
    ('Mostra de Cinema Brasileiro', 'Exibição de filmes nacionais seguida de debate.',
     10, time(20, 0), 'Teatro Municipal', 'Arte e Cultura', 150),
    ('Seminário de Educação Aberta', 'Debates sobre recursos educacionais abertos.',
     12, time(8, 30), 'Auditório Central', 'Educação', None),
    ('Hackathon da Turma (encerrado)', 'Maratona de programação que já aconteceu.',
     -10, time(8, 0), 'Centro de Convenções', 'Tecnologia', None),
]


class Command(BaseCommand):
    help = 'Popula o banco com dados de exemplo (usuários, categorias, locais, eventos e inscrições).'

    def handle(self, *args, **options):
        hoje = timezone.localdate()

        # Administrador
        admin_user, criado = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@exemplo.com',
                'first_name': 'Administrador',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if criado:
            admin_user.set_password('admin123')
            admin_user.save()

        # Usuários comuns
        usuarios = {}
        for username, nome in [('maria', 'Maria'), ('joao', 'João'), ('ana', 'Ana')]:
            usuario, criado = User.objects.get_or_create(
                username=username,
                defaults={'first_name': nome, 'email': f'{username}@exemplo.com'},
            )
            if criado:
                usuario.set_password('senha12345')
                usuario.save()
            usuarios[username] = usuario

        # Categorias e locais
        categorias = {}
        for nome, descricao in CATEGORIAS:
            categorias[nome], _ = Categoria.objects.get_or_create(
                nome=nome, defaults={'descricao': descricao}
            )

        locais = {}
        for nome, endereco, capacidade in LOCAIS:
            locais[nome], _ = Local.objects.get_or_create(
                nome=nome, defaults={'endereco': endereco, 'capacidade': capacidade}
            )

        # Eventos
        eventos = {}
        for titulo, descricao, dias, horario, local, categoria, vagas in EVENTOS:
            eventos[titulo], _ = Evento.objects.get_or_create(
                titulo=titulo,
                defaults={
                    'descricao': descricao,
                    'data': hoje + timedelta(days=dias),
                    'horario': horario,
                    'local': locais[local],
                    'categoria': categorias[categoria],
                    'organizador': admin_user,
                    'vagas': vagas,
                },
            )

        # Inscrições (o Workshop de Git tem 2 vagas e fica esgotado)
        inscricoes = [
            ('maria', 'Workshop de Git e GitHub'),
            ('joao', 'Workshop de Git e GitHub'),
            ('maria', 'Semana de Tecnologia'),
            ('ana', 'Semana de Tecnologia'),
            ('joao', 'Festival de Música Universitária'),
            ('maria', 'Hackathon da Turma (encerrado)'),
        ]
        for username, titulo in inscricoes:
            Inscricao.objects.get_or_create(usuario=usuarios[username], evento=eventos[titulo])

        # Uma inscrição cancelada, para exemplificar o status
        Inscricao.objects.get_or_create(
            usuario=usuarios['ana'],
            evento=eventos['Mostra de Cinema Brasileiro'],
            defaults={'status': Inscricao.Status.CANCELADA},
        )

        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
        self.stdout.write('Administrador: admin / admin123')
        self.stdout.write('Usuários comuns: maria, joao e ana / senha12345')