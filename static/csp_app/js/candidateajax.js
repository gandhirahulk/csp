$(document).ready(function(){ 
    var okay = -1;
    $('#c_aadhaar').keyup(function(){
        aadhaar = $('#c_aadhaar').val()
        pan = ''
        contact = 0
        fathername = ''
        firstname = ''
        dob = ''
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'aadhaar': aadhaar, 
                'pan':pan,
                'contact':contact,
                'fathername': fathername,
                'dob': dob,
                'email': email,       
                'firstname': firstname,       
            },
            dataType: 'Json',
            success: function(data){
                console.log(data['adhaar']);
                if (data['adhaar'] != ''){
                    var duplicate_msg = 'Adhaar Number Already Exist With Candidate ID : ' + data['adhaar'] ;
                    $('#adhaarmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');
                    
                } 
                if (data['adhaar'] == ''){
                    $('#adhaarmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    $('#detailsmsg').html('').css('color','red');

                }
            }
        });
    });
    
    $('#calculate').mouseenter(function(){
        aadhaar = $('#c_aadhaar').val()
        pan = $('#c_pan').val();
        contact = $('#c_contact').val()
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        email = $('#email').val();
        
        middlename = $('#c_middlename').val();
        lastname = $('#c_lastname').val();
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
                'dob':dob,     
                'middlename' : middlename,
                'lastname' : lastname,
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'email': email,       
            },
            dataType: 'Json',
            success: function(data){
            
                if (data['adhaar'] != '' || data['contact'] != '' || data['pan'] != '' || data['email'] != '' || data['details'] != '' || data['invalid_domain'] != ''){
                  
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');

                    
                } 
                if (data['adhaar'] == '' && data['contact'] == '' && data['pan'] == '' && data['email'] == '' && data['details'] == '' && data['invalid_domain'] == ''){

                   
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    $('#detailsmsg').html('').css('color','red');

                }
            }
        });
    });
    

    $('#c_contact').keyup(function(){
        contact = $('#c_contact').val()
        pan = ''
        aadhaar = 000000
        fathername = ''
        firstname = ''
        dob = ''
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'fathername': fathername,
                'dob': dob,
                'email': email,     
                'firstname': firstname,                   
            },
            dataType: 'Json',
            success: function(data){
                if (data['contact'] != ''){
                    var duplicate_msg = 'Contact Number Already Exist With Candidate ID : ' + data['contact'] ;
                    $('#contactmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');

                } 
                if (data['contact'] == ''){
                    $('#contactmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    $('#detailsmsg').html('').css('color','red');

                }
            }
        });
    });
    $('#c_pan').keyup(function(){
        pan = $('#c_pan').val();
        contact = 0
        aadhaar = 000000
        fathername = ''
        firstname = ''
        dob = ''
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'pan': pan, 
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'fathername': fathername,
                'dob': dob,
                'email': email,     
                'firstname': firstname,                 
            },
            dataType: 'Json',
            success: function(data){
                if (data['pan'] != ''){
                    var duplicate_msg = 'PAN Number Already Exist With Candidate ID : ' + data['pan'] ;
                    $('#panmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');

                } 
                if (data['pan'] == ''){
                    $('#panmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    $('#detailsmsg').html('').css('color','red');

                }
            }
        });
    });
    $('#email').keyup(function(){
        email = $('#email').val();
        contact = 0
        aadhaar = 000000
        fathername = ''
        firstname = ''
        dob = ''
        pan = 0
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'email': email,     
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'fathername': fathername,
                'dob': dob,
                'firstname': firstname,             
            },
            dataType: 'Json',
            success: function(data){
                if (data['invalid_domain'] != ''){
                    $('#emailmsg').html(data['invalid_domain']).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');

                } else {
                    $('#emailmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    if (data['email'] != ''){
                        var duplicate_msg = 'Email ID Already Exist With Candidate ID : ' + data['email'] ;
                        $('#emailmsg').html(duplicate_msg).css('color','red');
                        $('#new-candidate').attr('onsubmit','return false;');
                        $('#calculate').attr('title', 'Please Recheck Entered Data');
                        $('#detailsmsg').html('Please Fix All The Errors').css('color','red');
                    } 
                    if (data['email'] == ''){
                        $('#emailmsg').html('');
                        $('#new-candidate').attr('onsubmit','return true;');
                        $('#calculate').attr('title', 'Calculate Salary Structure');
                        $('#detailsmsg').html('').css('color','red');

                    }
                }
                
            }
        });
    });
    
    $('#c_firstname').keyup(function(){
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        middlename = $('#c_middlename').val();
        lastname = $('#c_lastname').val();
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
                'middlename' : middlename,
                'lastname' : lastname,
                'dob':dob,     
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'email': email,       
            },
            dataType: 'Json',
            success: function(data){
                if (data['details'] != ''){
                    var duplicate_msg = 'Candidate Already Exist with Candidate ID : ' + data['details'] ;
                    $('#detailsmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');

                } 
                if (data['details'] == ''){
                    $('#detailsmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                }
            }
        });
    });
    $('#c_dob').change(function(){
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        middlename = $('#c_middlename').val();
        lastname = $('#c_lastname').val();
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
                'middlename' : middlename,
                'lastname' : lastname,
                'dob':dob,     
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'email': email,      
            },
            dataType: 'Json',
            success: function(data){
                if (data['details'] != ''){
                    var duplicate_msg = 'Candidate Already Exist with Candidate ID : ' + data['details'] ;
                    $('#detailsmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                } 
                if (data['details'] == ''){
                    $('#detailsmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                }
            }
        });
    });
    $('#c_fathername').keyup(function(){
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        middlename = $('#c_middlename').val();
        lastname = $('#c_lastname').val();
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
                'middlename' : middlename,
                'lastname' : lastname,
                'dob':dob,     
                'contact_no': contact,    
                'aadhaar': aadhaar, 
                'pan':pan,
                'email': email,    
            },
            dataType: 'Json',
            success: function(data){
                if (data['details'] != ''){
                    var duplicate_msg = 'Candidate Already Exist with Candidate ID : ' + data['details'] ;
                    $('#detailsmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                } 
                if (data['details'] == ''){
                    $('#detailsmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                }
            }
        });
    });
   
    $('#reporting_manager_email').keyup(function(){
        email = $('#reporting_manager_email').val();
        $.ajax({
            url: '/csp_candidates/check_rm_email/',
            data: {
                'email': email,     
                          
            },
            dataType: 'Json',
            success: function(data){
                // print(data['result'] );
                if (data['result'] != ''){
                    $('#rmemailmsg').html(data['result']).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    $('#detailsmsg').html('Please Fix All The Errors').css('color','red');
                    $('#calculate').attr('disabled',true);


                } else {
                    $('#rmemailmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                    $('#detailsmsg').html('').css('color','red');
                    $('#calculate').attr('disabled',false);

                }
                
            }
        });
    });
    
  

});