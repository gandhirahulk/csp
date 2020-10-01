$(document).ready(function(){ 



    showMe('Candidate', 'can-expand');

    $('#close_delete').click(function(){
        $("#salary_structure").css("display", "none");
        $("#crumbs").css("z-index", "100");
    });  

    $('#hiring').change(function() {
        var selectedvalue = $(this).val();
        if (selectedvalue == '1'){
            $('#c_replacement').attr("disabled", false);
        } else {
            $('#c_replacement').prop("value", '');                
            $('#c_replacement').attr("disabled", true);
        }
    });
    $('#referral').change(function() {
        var selectedvalue = $(this).val();
        if (selectedvalue == '1'){
            $('#c_referral').attr("disabled", false);
        } else {
            $('#c_referral').prop("value", '');
            $('#c_referral').attr("disabled", true);
        }
    });
    $('#c_contact, #c_emergency').on('keyup', function () {
    if ($('#c_contact').val() == $('#c_emergency').val()) {
        $('#message').html('Contact No. and Emergency No. Cannot be same.').css('color', 'red');
    } else 
        $('#message').html('').css('color', 'green');
    });

    $('#c_entity').change(function() {
        var filter = $(this).val();
        var total = $('#c_dept option').length;
        var count = 0;
        $('#c_dept option').each(function() {
            if ($(this).text() == filter) {
            $('#c_dept').attr("disabled", false);
                $(this).show();
            } else {
                $(this).hide();
                count += 1;
            }
            $('#c_dept').val(filter);
        });
     
        var vcount = 0;
        var vtotal = $('#c_vendor option').length;
        $('#c_vendor option').each(function() {
            if ($(this).text() == filter) {
            $('#c_vendor').attr("disabled", false);
                $(this).show();
            } else {
                $(this).hide();
                vcount += 1;
            }
            $('#c_vendor').val(filter);
        });
        var rcount = 0;
        var rtotal = $('#c_region option').length;
        $('#c_region option').each(function() {
        if ($(this).text() == filter) {
            $('#c_region').attr("disabled", false);
                $(this).show();
            } else {
                $(this).hide();
                rcount += 1;
            }
            $('#c_region').val(filter);
        });
        if (vcount === vtotal){
            $('#c_vendor').attr("disabled", true);
            $('#c_vendor').append($('<option>', {
            value: '',
            text: '',
            label: '',
            selected: true,
            selected: "true"
            }));
        } else {
            $('#c_vendor .empty').css("display", "");
            $('#c_vendor .empty').prop("selected", true);
        }
        if (count === total){
            $('#c_dept').attr("disabled", true);
           
        } else {
            $('#c_dept .empty').css("display", "");
            $('#c_dept .empty').prop("selected", true);
        }
        if (rcount === rtotal){
            $('#c_region').attr("disabled", true);
           
        } else {
            $('#c_region .empty').css("display", "");
            $('#c_region .empty').prop("selected", true);
        }

    });
  
    $('#c_region').change(function() {
        var filter = $(this).val();
        var total = $('#c_state option').length;
        var count = 0;
        $('#c_state option').each(function() {
        if ($(this).text() == filter) {
        $('#c_state').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_state').val(filter);
        });
        if (count === total){
            $('#c_state').attr("disabled", true)
           
        } else {
            $('#c_state .empty').attr("selected", true);
            $('#c_state .empty').css("display", "");
            $('#c_state .empty').prop("selected", true);
        }
    });
    
    $('#c_state').change(function() {
        var filter = $(this).val();
        var total = $('#c_city option').length;
        var count = 0;
        $('#c_city option').each(function() {
        if ($(this).text() == filter) {
            
        $('#c_city').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_city').val(filter);
        });
        if (count === total){
            $('#c_city').attr("disabled", true)
           
        } else {
            $('#c_city .empty').attr("selected", true);
            $('#c_city .empty').css("display", "");
            $('#c_city .empty').prop("selected", true);
        }
    });
    
    $('#c_city').change(function() {
        var filter = $(this).val();
        var total = $('#c_location option').length;
        var count = 0;
        $('#c_location option').each(function() {
        if ($(this).text() == filter) {
            
        $('#c_location').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_location').val(filter);
        });
        if (count === total){
            $('#c_location').attr("disabled", true)
           
        } else {
            $('#c_location .empty').attr("selected", true);
            $('#c_location .empty').css("display", "");
            $('#c_location .empty').prop("selected", true);
        }
    });

    $('#c_dept').change(function() {
        var filter = $(this).val();
        var total = $('#c_function option').length;
        var count = 0;
        $('#c_function option').each(function() {
        if ($(this).text() == filter) {
            
        $('#c_function').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_function').val(filter);
        });
        if (count === total){
            $('#c_function').attr("disabled", true);
           
        } else {
            $('#c_function .empty').attr("selected", true);
            $('#c_function .empty').css("display", "");
            $('#c_function .empty').prop("selected", true);
        }
    });
    $('#c_function').change(function() {
        var filter = $(this).val();
        var total = $('#c_team option').length;
        var count = 0;
        $('#c_team option').each(function() {
        if ($(this).text() == filter) {
           
        $('#c_team').attr("disabled", false);
            $(this).show();
            
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_team').val(filter);
        });
        if (count === total){
            $('#c_team').attr("disabled", true)
           
        } else {
            $('#c_team .empty').attr("selected", true);
            $('#c_team .empty').css("display", "");
            $('#c_team .empty').prop("selected", true);
        }
    });

    $('#c_team').change(function() {
        var filter = $(this).val();
        var total = $('#c_subteam option').length;
        var count = 0;
        $('#c_subteam option').each(function() {
        if ($(this).text() == filter) {
            
        $('#c_subteam').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_subteam').val(filter);
        });
        if (count === total){
            $('#c_subteam').attr("disabled", true)
            
        } else {
            $('#c_subteam .empty').attr("selected", true);
            $('#c_subteam .empty').css("display", "");
            $('#c_subteam .empty').prop("selected", true);
        }
    });

    $('#c_subteam').change(function() {
        var filter = $(this).val();
        var total = $('#c_desg option').length;
        var count = 0;
        $('#c_desg option').each(function() {
        if ($(this).text() == filter) {
            
        $('#c_desg').attr("disabled", false);
            $(this).show();
        } else {
            $(this).hide();
            count += 1;
        }
        $('#c_desg').val(filter);
        });
        if (count === total){
            $('#c_desg').attr("disabled", true)
           
        } else {
            $('#c_desg .empty').attr("selected", true);
            $('#c_desg .empty').css("display", "");
            $('#c_desg .empty').prop("selected", true);
        }
    });


})