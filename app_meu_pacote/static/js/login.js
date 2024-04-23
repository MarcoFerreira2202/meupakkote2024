// meu_app/static/js/login.js
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api-token-auth/', {  // Ajuste o endpoint conforme necessário
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            alert('Login bem-sucedido!');
            window.location.href = '/buscar_encomendas/';  // Redireciona para a página de busca de encomendas
        } else {
            alert('Login falhou! Verifique suas credenciais.');
        }
    })
    .catch(error => console.error('Erro:', error));
});
