from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CadastroTests(TestCase):
    def dados(self, **alteracoes):
        dados = {
            'username': 'nova',
            'first_name': 'Nova',
            'email': 'nova@exemplo.com',
            'password1': 'SenhaForte#2026',
            'password2': 'SenhaForte#2026',
        }
        dados.update(alteracoes)
        return dados

    def test_pagina_de_cadastro_carrega(self):
        resposta = self.client.get(reverse('cadastro'))
        self.assertEqual(resposta.status_code, 200)

    def test_cadastro_valido_cria_usuario_comum_e_faz_login(self):
        resposta = self.client.post(reverse('cadastro'), self.dados())
        self.assertRedirects(resposta, reverse('lista_eventos'))
        usuario = User.objects.get(username='nova')
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
        self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_cadastro_rejeita_senhas_diferentes(self):
        resposta = self.client.post(reverse('cadastro'), self.dados(password2='OutraSenha#2026'))
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(User.objects.filter(username='nova').exists())

    def test_cadastro_rejeita_email_repetido(self):
        User.objects.create_user('existente', email='nova@exemplo.com', password='x')
        resposta = self.client.post(reverse('cadastro'), self.dados())
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(User.objects.filter(username='nova').exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('maria', password='senha12345')

    def test_login_valido_redireciona_para_a_lista_de_eventos(self):
        resposta = self.client.post(
            reverse('login'), {'username': 'maria', 'password': 'senha12345'}
        )
        self.assertRedirects(resposta, reverse('lista_eventos'))

    def test_login_invalido_nao_autentica(self):
        resposta = self.client.post(
            reverse('login'), {'username': 'maria', 'password': 'errada'}
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_por_post_encerra_a_sessao(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(reverse('logout'))
        self.assertRedirects(resposta, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_por_get_nao_e_permitido(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse('logout'))
        self.assertEqual(resposta.status_code, 405)