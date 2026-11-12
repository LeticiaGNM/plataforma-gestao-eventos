document.addEventListener('DOMContentLoaded', function () {
    var botao = document.getElementById('botao-tema');
    var icone = document.getElementById('icone-tema');
    var html = document.documentElement;

    if (!botao) {
        return;
    }

    function atualizarBotao() {
        var escuro = html.getAttribute('data-bs-theme') === 'dark';
        icone.className = escuro ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        botao.setAttribute('aria-label', escuro ? 'Mudar para o tema claro' : 'Mudar para o tema escuro');
    }

    botao.addEventListener('click', function () {
        var novo = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-bs-theme', novo);
        localStorage.setItem('tema', novo);
        atualizarBotao();
        window.dispatchEvent(new CustomEvent('tema-alterado'));
    });

    atualizarBotao();
});