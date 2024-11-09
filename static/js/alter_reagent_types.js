function mudar_div_reagents(id, btn, btns,) {
    var divs = document.querySelectorAll('.listReagents')

    divs.forEach(element => {
        element.classList.add('none')
    });
    
    btns.forEach(element => {
        element.classList.remove('active')
    });

    document.getElementById(id).classList.remove('none')
    btn.classList.add('active')
    console.log(document.getElementById(id))
}
var tab_btns = document.querySelectorAll('.tab2-btn')

tab_btns.forEach(element => {
    element.addEventListener("click", function(e) {
        var id = element.getAttribute('content-id')
        mudar_div_reagents(id, element, tab_btns)
    })
});