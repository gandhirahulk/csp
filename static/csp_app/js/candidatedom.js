document.addEventListener('DOMContentLoaded', function() {        
var input = document.getElementById('c_contact');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32) {
        e.preventDefault();
        return false;
    }     
});
var input = document.getElementById('c_emergency');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32) {
        e.preventDefault();
        return false;
    }     
});
var input = document.getElementById('spocemail');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32) {
        e.preventDefault();
        return false;
    }     
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
    
        e.preventDefault();
        return false;
    } 
    if(e.keyCode == 219 || e.keyCode == 221) {
        
        e.preventDefault();
        return false;
    }  
});

var input = document.getElementById('email');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
    
        e.preventDefault();
        return false;
    } 
    if(e.keyCode == 219 || e.keyCode == 221) {
        
        e.preventDefault();
        return false;
    }      
});
var input = document.getElementById('c_aadhaar');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32) {
        e.preventDefault();
        return false;
    }
});
var input = document.getElementById('reporting_manager');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
            
});
var input = document.getElementById('reporting_manager_email');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
    
        e.preventDefault();
        return false;
    } 
    if(e.keyCode == 219 || e.keyCode == 221) {
        
        e.preventDefault();
        return false;
    } 
        
});
var input = document.getElementById('c_firstname');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
            
});
var input = document.getElementById('c_mothername');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
            
});
var input = document.getElementById('c_middlename');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    } 
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    }   
            
});
var input = document.getElementById('c_lastname');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
            
});
var input = document.getElementById('c_fathername');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
    if(e.keyCode == 32 && (val[end - 1] == " " || val[end] == " ")) {
        e.preventDefault();
        return false;
    }   
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
        
});
var input = document.getElementById('c_salary');
input.addEventListener('keydown', function(e){      
    var input = e.target;
    var val = input.value;
    var end = input.selectionEnd;
        
    if(e.keyCode == 190 && (val[end - 1] == "." || val[end] == ".")) {
        e.preventDefault();
        return false;
    } 
        
});


});
