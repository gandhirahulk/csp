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
                    
                } 
                if (data['adhaar'] == ''){
                    $('#adhaarmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                }
            }
        });
    });
    
    
    $('#calculate').mouseover(function(){
        aadhaar = $('#c_aadhaar').val()
        pan = $('#c_pan').val();
        contact = $('#c_contact').val()
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        email = $('#email').val();
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
            
                if (data['adhaar'] != '' || data['contact'] != '' || data['pan'] != '' || data['email'] != '' || data['details'] != ''){
                  
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                    
                } 
                if (data['adhaar'] == '' || data['contact'] == '' || data['pan'] == '' || data['email'] == '' || data['details'] == ''){

                   
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
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
                } 
                if (data['contact'] == ''){
                    $('#contactmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
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
                } 
                if (data['pan'] == ''){
                    $('#panmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
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
                if (data['email'] != ''){
                    var duplicate_msg = 'Email ID Already Exist With Candidate ID : ' + data['email'] ;
                    $('#emailmsg').html(duplicate_msg).css('color','red');
                    $('#new-candidate').attr('onsubmit','return false;');
                    $('#calculate').attr('title', 'Please Recheck Entered Data');
                } 
                if (data['email'] == ''){
                    $('#emailmsg').html('');
                    $('#new-candidate').attr('onsubmit','return true;');
                    $('#calculate').attr('title', 'Calculate Salary Structure');
                }
            }
        });
    });
    $('#c_firstname').keyup(function(){
        fathername = $('#c_fathername').val();
        firstname = $('#c_firstname').val();
        dob = $('#c_dob').val();
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
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
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
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
      
        contact = 0
        aadhaar = 000000
        pan = 0
        email = ''
        $.ajax({
            url: '/csp_candidates/check_duplicacy_new/',
            data: {
                'fathername': fathername,
                'firstname': firstname,
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

  

});