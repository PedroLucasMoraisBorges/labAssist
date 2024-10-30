const buttons = document.querySelectorAll('.actionButtons');

function del_card(element) {
    var new_element = element
    while(true) {
        if (new_element.classList.contains("card_request")) {
            new_element.style.display = 'none';
            break
        }
        else {
            new_element = new_element.parentElement
        }
    }
}
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
                del_card(this)
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