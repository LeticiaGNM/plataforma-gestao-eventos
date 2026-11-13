from datetime import time, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Categoria, Evento, Inscricao, Local


def criar_evento(titulo='Evento de Teste', dias=5, capacidade=10, vagas=None, categoria='Tecnologia'):
    # Função auxiliar: cria um evento com tudo de que ele depende.
    categoria_obj, _ = Categoria.objects.get_or_create(nome=categoria)
    organizador, _ = User.objects.get_or_create(username='organizador', defaults={'is_staff': True})
    local = Local.objects.create(nome=f'Local de {titulo}', endereco='Rua A, 100', capacidade=capacidade)
    return Evento.objects.create(
        titulo=titulo,
        descricao='Descrição do evento.',
        data=timezone.localdate() + timedelta(days=dias),
        horario=time(19, 0),
        local=local,
        categoria=categoria_obj,
        organizador=organizador,
        vagas=vagas,
    )


class EventoModelTests(TestCase):
    def test_vagas_disponiveis_desconta_apenas_inscricoes_confirmadas(self):
        evento = criar_evento(capacidade=3)
        u1 = User.objects.create_user('u1', password='x')
        u2 = User.objects.create_user('u2', password='x')
        Inscricao.objects.create(usuario=u1, evento=evento)
        Inscricao.objects.create(usuario=u2, evento=evento, status=Inscricao.Status.CANCELADA)
        self.assertEqual(evento.vagas_ocupadas, 1)
        self.assertEqual(evento.vagas_disponiveis, 2)

    def test_vagas_do_evento_tem_prioridade_sobre_a_capacidade_do_local(self):
        evento = criar_evento(capacidade=100, vagas=5)
        self.assertEqual(evento.limite_vagas, 5)

    def test_vagas_maiores_que_a_capacidade_sao_rejeitadas(self):
        evento = criar_evento(capacidade=10)
        evento.vagas = 11
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_evento_passado_esta_encerrado(self):
        self.assertTrue(criar_evento(dias=-1).encerrado)

    def test_evento_futuro_nao_esta_encerrado(self):
        self.assertFalse(criar_evento(dias=3).encerrado)

    def test_usuario_nao_pode_ter_duas_inscricoes_no_mesmo_evento(self):
        evento = criar_evento()
        usuario = User.objects.create_user('u1', password='x')
        Inscricao.objects.create(usuario=usuario, evento=evento)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Inscricao.objects.create(usuario=usuario, evento=evento)


class AcessoAnonimoTests(TestCase):
    def test_paginas_da_area_do_usuario_exigem_login(self):
        evento = criar_evento()
        for nome, args in [
            ('lista_eventos', []),
            ('detalhe_evento', [evento.pk]),
            ('minhas_inscricoes', []),
            ('painel', []),
        ]:
            url = reverse(nome, args=args)
            resposta = self.client.get(url)
            self.assertRedirects(resposta, f"{reverse('login')}?next={url}")

    def test_inscrever_exige_login(self):
        evento = criar_evento()
        url = reverse('inscrever', args=[evento.pk])
        resposta = self.client.post(url)
        self.assertRedirects(resposta, f"{reverse('login')}?next={url}")
        self.assertEqual(Inscricao.objects.count(), 0)


class ListaEventosTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('maria', password='senha12345')
        self.client.force_login(self.usuario)
        self.evento = criar_evento(titulo='Semana de Tecnologia')

    def test_lista_mostra_eventos_futuros(self):
        resposta = self.client.get(reverse('lista_eventos'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Semana de Tecnologia')

    def test_lista_nao_mostra_eventos_encerrados(self):
        criar_evento(titulo='Evento Antigo', dias=-3)
        resposta = self.client.get(reverse('lista_eventos'))
        self.assertNotContains(resposta, 'Evento Antigo')

    def test_busca_por_titulo(self):
        criar_evento(titulo='Maratona de Programação')
        resposta = self.client.get(reverse('lista_eventos'), {'q': 'Maratona'})
        self.assertContains(resposta, 'Maratona de Programação')
        self.assertNotContains(resposta, 'Semana de Tecnologia')

    def test_filtro_por_categoria(self):
        show = criar_evento(titulo='Show de Jazz', categoria='Música')
        resposta = self.client.get(reverse('lista_eventos'), {'categoria': show.categoria_id})
        self.assertContains(resposta, 'Show de Jazz')
        self.assertNotContains(resposta, 'Semana de Tecnologia')


class InscricaoTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('maria', password='senha12345')
        self.client.force_login(self.usuario)
        self.evento = criar_evento(titulo='Semana de Tecnologia', capacidade=2)
        self.url_inscrever = reverse('inscrever', args=[self.evento.pk])
        self.url_cancelar = reverse('cancelar_inscricao', args=[self.evento.pk])

    def test_inscrever_cria_inscricao_confirmada(self):
        resposta = self.client.post(self.url_inscrever)
        self.assertRedirects(resposta, reverse('detalhe_evento', args=[self.evento.pk]))
        inscricao = Inscricao.objects.get(usuario=self.usuario, evento=self.evento)
        self.assertEqual(inscricao.status, Inscricao.Status.CONFIRMADA)

    def test_inscrever_por_get_nao_e_permitido(self):
        resposta = self.client.get(self.url_inscrever)
        self.assertEqual(resposta.status_code, 405)
        self.assertEqual(Inscricao.objects.count(), 0)

    def test_nao_duplica_inscricao(self):
        self.client.post(self.url_inscrever)
        self.client.post(self.url_inscrever)
        self.assertEqual(Inscricao.objects.filter(usuario=self.usuario).count(), 1)

    def test_nao_inscreve_em_evento_esgotado(self):
        for nome in ('ana', 'joao'):
            outro = User.objects.create_user(nome, password='x')
            Inscricao.objects.create(usuario=outro, evento=self.evento)
        self.client.post(self.url_inscrever)
        self.assertFalse(Inscricao.objects.filter(usuario=self.usuario).exists())

    def test_nao_inscreve_em_evento_encerrado(self):
        passado = criar_evento(titulo='Evento Passado', dias=-1)
        self.client.post(reverse('inscrever', args=[passado.pk]))
        self.assertFalse(Inscricao.objects.filter(usuario=self.usuario).exists())

    def test_cancelar_inscricao(self):
        Inscricao.objects.create(usuario=self.usuario, evento=self.evento)
        self.client.post(self.url_cancelar)
        inscricao = Inscricao.objects.get(usuario=self.usuario, evento=self.evento)
        self.assertEqual(inscricao.status, Inscricao.Status.CANCELADA)

    def test_reinscricao_reativa_a_inscricao_cancelada(self):
        Inscricao.objects.create(
            usuario=self.usuario, evento=self.evento, status=Inscricao.Status.CANCELADA
        )
        self.client.post(self.url_inscrever)
        self.assertEqual(Inscricao.objects.filter(usuario=self.usuario).count(), 1)
        inscricao = Inscricao.objects.get(usuario=self.usuario)
        self.assertEqual(inscricao.status, Inscricao.Status.CONFIRMADA)

    def test_usuario_nao_cancela_inscricao_de_outro(self):
        outro = User.objects.create_user('joao', password='x')
        Inscricao.objects.create(usuario=outro, evento=self.evento)
        resposta = self.client.post(self.url_cancelar)
        self.assertEqual(resposta.status_code, 404)
        inscricao = Inscricao.objects.get(usuario=outro)
        self.assertEqual(inscricao.status, Inscricao.Status.CONFIRMADA)

    def test_minhas_inscricoes_mostra_apenas_as_do_usuario(self):
        outro = User.objects.create_user('joao', password='x')
        outro_evento = criar_evento(titulo='Evento do Joao')
        Inscricao.objects.create(usuario=self.usuario, evento=self.evento)
        Inscricao.objects.create(usuario=outro, evento=outro_evento)
        resposta = self.client.get(reverse('minhas_inscricoes'))
        self.assertContains(resposta, 'Semana de Tecnologia')
        self.assertNotContains(resposta, 'Evento do Joao')


class PainelTests(TestCase):
    def test_usuario_comum_recebe_403(self):
        usuario = User.objects.create_user('maria', password='senha12345')
        self.client.force_login(usuario)
        resposta = self.client.get(reverse('painel'))
        self.assertEqual(resposta.status_code, 403)

    def test_equipe_acessa_o_painel(self):
        gestor = User.objects.create_user('gestor', password='senha12345', is_staff=True)
        self.client.force_login(gestor)
        resposta = self.client.get(reverse('painel'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Painel de gestão')
