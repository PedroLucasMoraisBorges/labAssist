const buttons = document.querySelectorAll('.actionButtons');

buttons.forEach(button => {
    button.addEventListener('click', function() {
        // Obtém o ID da requisição de movimentação do atributo data-id
        console.log(this)
        const id = this.getAttribute('data-id');
        const importedUrl = this.getAttribute('url');

        // Monta a URL dinamicamente de acordo com a url do django
        var url = `${importedUrl}?id=${id}`;

        fetch(url, {
            method: 'GET'
        })
        .then(response => response.json())  // Converte a resposta em JSON
        .then(data => {
            if (data.message) {
                alert('Ação feita com sucesso');
                this.parentElement.style.display = 'none';
            } else if (data.error) {
                alert('Erro: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao aprovar a requisição:', error);
            alert('Ocorreu um erro ao enviar a requisição');
        });
    });
});