function open_movement_form_modal(){
    back = document.querySelector('#movement_form')
    var modal =  back.children[0]


    back.classList.remove('none')
    modal.classList.remove('none')
}

function close_movement_form_modal(){
    back = document.querySelector('#movement_form')
    var modal = back.children[0]
        
    modal.classList.add('slideUp');

    setTimeout(() => {
        back.classList.add('none');
        modal.classList.add('none');
        modal.classList.remove('slideUp');
    }, 500);
}

var buttons_card = document.querySelectorAll(".btn_show")

buttons_card.forEach(button => {
    button.addEventListener("click", () => {
        var card_id = button.getAttribute("card_id");
        var back = document.getElementById(card_id)

        var modal =  back.children[0]

        back.classList.remove('none')
        modal.classList.remove('none')
    });
});


var buttons_close = document.querySelectorAll(".btn_close")

buttons_close.forEach(button => {
    button.addEventListener("click", () => {
        var card_id = button.getAttribute("card_id");
        var back = document.getElementById(card_id)
        var modal = back.children[0]
        
        modal.classList.add('slideUp');

        setTimeout(() => {
            back.classList.add('none');
            modal.classList.add('none');
            modal.classList.remove('slideUp');
        }, 500);
    });
});