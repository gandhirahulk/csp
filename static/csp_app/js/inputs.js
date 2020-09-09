function onlyAlphabets(event) {
    // checkDOJ();
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[a-z ]/i);
    // var newvalue = str.replace("  ", " ");
    return pattern.test(value);    
}
// "^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$"
function onlyNumbers(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[0-9]/);
    return pattern.test(value);    
}

function money(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[0-9.]/);
    return pattern.test(value);    
}


function pan(event) {
    var value = String.fromCharCode(event.which);
    // alert(value)
    var pattern = new RegExp(/[A-Z]{5}[0-9]{4}[A-Z]{1}/);
    return pattern.test(value);
    
}


function sameNumber(c, e, textbox){
    var contact = document.getElementById(c).value;
    var emergency = document.getElementById(e).value;
    if (contact === emergency){
        textbox.setCustomValidity("Contact No. and Emergency No. Cannot Be Same");
        return false;
    } 
}


function checkDOJ(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    var yyyy = today.getFullYear();
    if(dd<10){
            dd='0'+dd
        } 
        if(mm<10){
            mm='0'+mm
        } 

    today = yyyy+'-'+mm+'-'+dd;
    document.getElementById("datefield").setAttribute("max", today);
}

 
