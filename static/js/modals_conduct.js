function close_modal() {
    var div_backs = document.querySelectorAll('.back')

    div_backs.forEach(element => {
        element.classList.add('none')
    });
}

function open_movement_form_modal(){
    document.querySelector('#movement_form').classList.remove("none")
}

var buttons_card = document.querySelectorAll(".btn_show")

buttons_card.forEach(button => {
    button.addEventListener("click", () => {
        var card_id = button.getAttribute("card_id");
        var modal = document.getElementById(card_id)
        modal.classList.remove('none')
    });
});