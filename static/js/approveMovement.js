var importUrl = document.currentScript.getAttribute('url');
const approveButtons = document.querySelectorAll('.approveRequestButton');

approveButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Obtém o ID da requisição de movimentação do atributo data-id
        const requestId = this.getAttribute('data-id');

        // Monta a URL dinamicamente de acordo com a url do django
        var url = `${importUrl}?id=${requestId}`;

        // Faz uma requisição GET para a API de aprovação usando Fetch
        fetch(url, {
            method: 'GET'
        })
        .then(response => response.json())  // Converte a resposta em JSON
        .then(data => {
            if (data.message) {
                alert('Requisição aprovada com sucesso!');
                this.parentElement.style.display = 'none';
            } else if (data.error) {
                alert('Erro: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao aprovar a requisição:', error);
            alert('Ocorreu um erro ao aprovar a requisição.');
        });
    });
});