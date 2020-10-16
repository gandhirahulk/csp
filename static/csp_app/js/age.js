$(document).ready(function(){
    // days
    $(function(){
        var dtToday = new Date(); 
        var month = dtToday.getMonth() + 1;
        var day = dtToday.getDate();
        var year = dtToday.getFullYear();
        if(month < 10)
            month = '0' + month.toString();
        if(day < 10)
            day = '0' + day.toString();          
        var minDate= year + '-' + month + '-' + day; 
        var adminDate = new Date(minDate);
        adminDate.setDate(adminDate.getDate() - 30);
        var m = adminDate.getMonth() + 1;
        var d = adminDate.getDate();
        var y = adminDate.getFullYear();
        if(m < 10)
            m = '0' + m.toString();
        if(d < 10)
            d = '0' + d.toString();          
        var admin_date= y + '-' + m + '-' + d; 
        var maxDate = new Date(minDate);
        maxDate.setDate(maxDate.getDate() + 90);
        var m = maxDate.getMonth() + 1;
        var d = maxDate.getDate();
        var y = maxDate.getFullYear();
        if(m < 10)
            m = '0' + m.toString();
        if(d < 10)
            d = '0' + d.toString();          
        var max_date= y + '-' + m + '-' + d; 
        $('#False').attr('min', minDate);
        $('#True').attr('min', admin_date);
        $('#True').attr('max', max_date);
        $('#False').attr('max', max_date);
    });
    //years
    $(function(){
        var dtToday = new Date(); 
        var month = dtToday.getMonth() + 1;
        var day = dtToday.getDate();
        var maxYear = dtToday.getFullYear() - 45;
        var minYear = dtToday.getFullYear() - 18;
        if(month < 10)
            month = '0' + month.toString();
        if(day < 10)
            day = '0' + day.toString();          
        var maxAge= maxYear + '-' + month + '-' + day;     
        var minAge= minYear + '-' + month + '-' + day;
        $('#c_dob').attr('min', maxAge);
        $('#c_dob').attr('max', minAge);

        $('#firstname').bind('keypress', onlyAlphabets);
        $('#lastname').bind('keypress', onlyAlphabets); 
    });
});