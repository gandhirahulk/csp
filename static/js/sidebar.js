function showMe(id, caretid){
    var active_tab = document.getElementsByClassName('active');
    for(var i=0; i < active_tab.length; i++){
        active_tab[i].classList.remove("active"); 
    }
    var tab_item = document.getElementById(id);
    tab_item.classList.toggle('active');
    var up_caret = document.getElementsByClassName('fa-caret-up');
    for(var i=0; i< up_caret.length; i++){
        up_caret[i].classList.remove("fa-caret-up");
        up_caret[i].classList.add("fa-caret-right");
    }
    var change_caret = document.getElementById(caretid);
    change_caret.classList.add("fa-caret-up");

    // alert("yep");
}

$(function() {
    $('input,select').on('keypress', function(e) {
        e.which !== 13 || $('[tabIndex=' + (+this.tabIndex + 1) + ']')[0].focus();
    });
});