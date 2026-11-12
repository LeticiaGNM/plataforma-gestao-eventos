<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=8E5BA5&height=120&section=header" width="100%" alt="">

<img src="docs/img/logo1.png" alt="Lumipass, por Lume" width="400">

### ✨ Plataforma de Gestão de Eventos ✨
*Descubra, inscreva-se e organize eventos em um só lugar.*

![Python](https://img.shields.io/badge/Python-3.12+-8E5BA5?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-C3A3D6?style=for-the-badge&logo=django&logoColor=white)
![Jazzmin](https://img.shields.io/badge/Admin-Jazzmin-FFC266?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Checkpoint%202-8E5BA5?style=for-the-badge)

**Lumipass** é um produto da **Lume** · Projeto da disciplina **GAC116 – Programação Web** · UFLA

[Contexto](#-contexto) · [Problema](#-o-problema) · [Solução](#-a-solução) · [História de uso](#-história-de-uso) · [Funcionalidades](#-funcionalidades) · [Instalação](#-instalação) · [Equipe](#-equipe)

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🌌 Contexto

Eventos acontecem o tempo todo em ambientes acadêmicos e comunitários: palestras, oficinas, semanas
acadêmicas, encontros e feiras. Mas as informações ficam espalhadas em cartazes, grupos de mensagens e
redes sociais. Quem organiza precisa controlar inscrições e vagas, e quem participa precisa descobrir
o que está acontecendo e garantir sua presença.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🧩 O problema

- **Divulgação dispersa:** as informações de um evento ficam em vários canais e se perdem.
- **Inscrições manuais:** listas de papel, planilhas e formulários soltos geram erro, duplicidade e retrabalho.
- **Falta de controle de vagas:** é fácil lotar um local além da capacidade ou perder a conta de quem confirmou.
- **Pouca visibilidade para quem participa:** sem um lugar único, a pessoa não consegue pesquisar, filtrar
  por interesse nem acompanhar suas inscrições.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 💜 Motivação

Organizar e participar de eventos ainda depende de processos manuais e de informação espalhada.
Queríamos um sistema **simples para quem participa** e **prático para quem organiza**, com uma
interface acolhedora e acessível, e que ao mesmo tempo nos permitisse aplicar, de ponta a ponta, o que
aprendemos em Programação Web: modelagem, regras de negócio, autenticação, painel administrativo e
interface.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🌱 Impacto social esperado

- **Mais acesso à informação:** todos os eventos em um único lugar, com busca e filtro por categoria.
- **Mais participação:** inscrever-se e cancelar em poucos cliques reduz a barreira para participar.
- **Menos desperdício e mais organização:** o controle automático de vagas evita superlotação e
  facilita o planejamento de quem organiza.
- **Fortalecimento da comunidade:** eventos acadêmicos, culturais e de extensão ganham alcance e visibilidade.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🌟 A solução

O **Lumipass** é uma aplicação web feita com **Django** onde:

- **Participantes** criam uma conta, exploram eventos, pesquisam, filtram por categoria, se inscrevem,
  cancelam e acompanham suas inscrições.
- **Administradores** cadastram eventos, categorias e locais, acompanham inscrições e gerenciam
  usuários em um ambiente administrativo personalizado (tema **Jazzmin**), com filtros, buscas e
  navegação por data, além de um **painel com gráficos** sobre os eventos e as inscrições.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 📖 História de uso

> [!NOTE]
> **Ana**, estudante de Ciência da Computação, quer participar de uma oficina, mas nunca sabe onde
> encontrar as informações.

1. Ana abre o **Lumipass** e cria sua conta em menos de um minuto.
2. Na lista de eventos, filtra pela categoria **Tecnologia** e busca por "oficina".
3. Abre os detalhes do evento: data, horário, local, descrição e **vagas disponíveis**.
4. Clica em **Inscrever-se**. A inscrição é confirmada e o número de vagas é atualizado.
5. Em **Minhas inscrições**, acompanha tudo e, se a agenda apertar, **cancela** com um clique,
   liberando a vaga para outra pessoa.

> [!TIP]
> **Maria**, organizadora, acessa o ambiente administrativo, cadastra o evento com local e vagas e
> acompanha as inscrições e os números do evento no painel com gráficos.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## ✅ Funcionalidades

### Área do participante (usuário logado)

- Cadastro, login e logout por usuário e senha
- Lista de eventos futuros com busca por texto, filtro por categoria e paginação
- Página de detalhes do evento, com informações do local e barra de vagas
- Inscrição e cancelamento da inscrição
- Página **Minhas inscrições**, com o status de cada uma
- Interface responsiva, com tema claro e escuro (a escolha fica salva no navegador)
- Páginas de erro 403 e 404 personalizadas

### Administração (equipe)

- CRUD de eventos, categorias e locais, com upload de imagem de capa
- Gerenciamento de inscrições (cancelamento em lote) e inscrições dentro da página do evento
- Gerenciamento de usuários, grupos e permissões
- Ambiente administrativo com tema **Jazzmin**, com filtros por período, categoria, local e data, buscas e
  navegação por data
- **Painel com gráficos** (Chart.js): total de eventos, próximos eventos, inscrições confirmadas,
  participantes, eventos por categoria e eventos mais procurados
- Comando que popula o banco com dados de exemplo

### Regras de negócio

> [!IMPORTANT]
> - O limite de vagas de um evento **não pode ultrapassar a capacidade do local**.
> - Cada usuário só pode ter **uma inscrição por evento**.
> - Locais e categorias com eventos **não podem ser excluídos**.
> - Não é possível se inscrever em eventos **encerrados** ou **esgotados**.
> - Cada usuário só acessa e cancela **as próprias inscrições**.
> - Inscrever e cancelar só funcionam por formulário (método POST) e com o usuário logado.
> - O painel e o admin são restritos à equipe; participantes recebem erro 403.

### Perfis de acesso

| Perfil | Acesso |
|---|---|
| **Administrador** | Tudo: eventos, categorias, locais, inscrições, usuários, grupos e painel com gráficos |
| **Gestor de eventos** | Cria e edita eventos, categorias e locais, apenas visualiza inscrições e acessa o painel |
| **Usuário comum** | Área do participante: lista e detalhes de eventos, inscrição, cancelamento e "Minhas inscrições". Não acessa o admin nem o painel |

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🗂️ Modelagem do banco de dados

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#EFE8F5','primaryBorderColor':'#8E5BA5','lineColor':'#8E5BA5','primaryTextColor':'#3b2a4a','tertiaryColor':'#FFF8EC'}}}%%
erDiagram
    USUARIO ||--o{ INSCRICAO : faz
    EVENTO ||--o{ INSCRICAO : recebe
    LOCAL ||--o{ EVENTO : sedia
    CATEGORIA ||--o{ EVENTO : classifica
    USUARIO ||--o{ EVENTO : organiza

    USUARIO {
        int id PK
        string username
        string email
        bool is_staff
    }
    CATEGORIA {
        int id PK
        string nome
        text descricao
    }
    LOCAL {
        int id PK
        string nome
        string endereco
        int capacidade
    }
    EVENTO {
        int id PK
        string titulo
        text descricao
        date data
        time horario
        int vagas
        string imagem
        int local_id FK
        int categoria_id FK
        int organizador_id FK
    }
    INSCRICAO {
        int id PK
        datetime data_inscricao
        string status
        int usuario_id FK
        int evento_id FK
    }
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🧰 Tecnologias

* **Python 3.12+** e **Django 6.1**
* **SQLite** (banco de dados relacional)
* **Bootstrap 5.3** e **Bootstrap Icons** (interface responsiva, com tema claro e escuro)
* **django-jazzmin** (tema do ambiente administrativo)
* **Chart.js** (gráficos do painel)
* **Pillow** (upload de imagens) e **WhiteNoise** (arquivos estáticos)
* **Git** e **GitHub** (versionamento com branches e Pull Requests)

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 🚀 Instalação

Pré-requisitos: Python 3.12 ou superior e Git. No Linux e no macOS, use `python3` no lugar de `python`.

```bash
git clone https://github.com/LeticiaGNM/plataforma-gestao-eventos.git
cd plataforma-gestao-eventos
python -m venv venv
```

Ative o ambiente virtual:

* Windows (PowerShell): `venv\Scripts\Activate.ps1`
* Windows (Git Bash): `source venv/Scripts/activate`
* Linux/macOS: `source venv/bin/activate`

Instale as dependências, crie o banco e popule com dados de exemplo:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py popular_dados
```

## ▶️ Execução

```bash
python manage.py runserver
```

Acesse o site em [http://127.0.0.1:8000/](http://127.0.0.1:8000/). O ambiente administrativo fica em
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) e o painel com gráficos em
[http://127.0.0.1:8000/painel/](http://127.0.0.1:8000/painel/) (apenas para a equipe).

> O site usa Bootstrap, Bootstrap Icons e Chart.js por CDN, então é preciso ter conexão com a internet.

**Usuários de exemplo (apenas desenvolvimento):**

| Usuário | Senha | Perfil |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `gestor` | `senha12345` | Gestor de eventos |
| `maria`, `joao`, `ana` | `senha12345` | Usuários comuns (sem acesso ao admin) |

## 🧪 Testes

O projeto tem testes automatizados para as regras de negócio, o controle de acesso, a lista de eventos,
as inscrições, o painel, o cadastro e o login/logout. Para executá-los:

```bash
python manage.py test
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 📁 Estrutura do projeto

```text
plataforma-gestao-eventos/
├── gestao_eventos/        # configurações do projeto (settings, urls)
├── usuarios/              # app de usuários: cadastro, login e logout
│   ├── forms.py           # formulários de cadastro e login
│   ├── views.py
│   ├── urls.py
│   └── templates/usuarios/
├── eventos/               # app: categorias, locais, eventos e inscrições
│   ├── models.py          # modelos e regras de negócio
│   ├── admin.py           # configuração do ambiente administrativo
│   ├── views.py           # lista, detalhes, inscrição, cancelamento e painel
│   ├── urls.py
│   ├── tests.py           # testes automatizados
│   ├── templates/eventos/ # páginas da área do participante e do painel
│   └── management/
│       └── commands/
│           └── popular_dados.py   # comando de dados de exemplo
├── templates/             # templates compartilhados (base, navbar, páginas de erro)
├── static/                # CSS e JavaScript (estilo e alternância de tema)
├── docs/img/              # logo e imagens do README
├── LICENSE
├── requirements.txt
└── manage.py
```

## 🔀 Fluxo de versionamento

Branches: `main` (versões entregues), `develop` (integração) e `feature/*` (uma por funcionalidade),
integradas por Pull Requests.

<img src="https://capsule-render.vercel.app/api?type=rect&color=C3A3D6&height=3" width="100%" alt="">

## 👩‍💻 Equipe

<div align="center">

<table>
  <tr>
    <td align="center" width="220">
      <a href="https://github.com/LeticiaGNM">
        <img src="https://github.com/LeticiaGNM.png?size=140" width="140" alt="Leticia Gabriella Nascimento de Morais">
      </a><br>
      <b>Leticia Gabriella Nascimento de Morais</b><br>
      <a href="https://github.com/LeticiaGNM">@LeticiaGNM</a>
    </td>
    <td align="center" width="220">
      <a href="https://github.com/tainarafms">
        <img src="https://github.com/tainarafms.png?size=140" width="140" alt="Tainara de Fátima Matias Souza">
      </a><br>
      <b>Tainara de Fátima Matias Souza</b><br>
      <a href="https://github.com/tainarafms">@tainarafms</a>
    </td>
  </tr>
</table>

*Lumipass · Lume · Projeto da disciplina GAC116 · UFLA*

<img src="https://capsule-render.vercel.app/api?type=waving&color=C3A3D6&height=100&section=footer" width="100%" alt="">

</div>
