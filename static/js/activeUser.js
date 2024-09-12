const approveUserButtons = document.querySelectorAll('.approveUserButton');
var importUserUrl = document.currentScript.getAttribute('url');

approveUserButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Obtém o ID da requisição de movimentação do atributo data-id
        const userId = this.getAttribute('data-id');

        console.log(importUserUrl)
        // Monta a URL dinamicamente de acordo com a url do django
        var url = `${importUserUrl}?id=${userId}`;

        fetch(url, {
            method: 'GET'
        })
        .then(response => response.json())  // Converte a resposta em JSON
        .then(data => {
            if (data.message) {
                alert('Usuário ativado com sucesso!');
                this.parentElement.style.display = 'none';
            } else if (data.error) {
                alert('Erro: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao aprovar a requisição:', error);
            alert('Ocorreu um erro ao ativar o usuário.');
        });
    });
});