function onlyAlphabets(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[a-z. ]/i);
    // var pattern = new RegExp(/^[a-zA-Z ]{2,30}$/);
    return pattern.test(value);    
}

// /^[a-z](?!.* {2})[ \w.-]{2,24}$/gmi

function alphaNumeric(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[a-z0-9.-_ ]/i);
    return pattern.test(value);    
}
// "^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$"
function onlyNumbers(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[0-9 ]/);
    return pattern.test(value);    
}

// function forEmail(event){
//     var value = String.fromCharCode(event.which);
//     var pattern = new RegExp(/[a-z0-9@._-]i/);
//     return pattern.test(value); 
// }

function noSpecial(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[A-Za-z0-9]/);
    // var newvalue = str.replace("  ", " ");
    return pattern.test(value);    
}

function money(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[0-9.]/);
    return pattern.test(value);    
}


function pan(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/[a-z0-9]/i);
    return pattern.test(value);   
    
}







 
