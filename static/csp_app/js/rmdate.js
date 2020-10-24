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
        maxDate.setDate(maxDate.getDate() + 30);
        var m = maxDate.getMonth() + 1;
        var d = maxDate.getDate();
        var y = maxDate.getFullYear();
        if(m < 10)
            m = '0' + m.toString();
        if(d < 10)
            d = '0' + d.toString();          
        var max_date= y + '-' + m + '-' + d; 
        $('#calendar_inp').attr('max', minDate);
        $('#calendar_inp').attr('min', admin_date);
        $('#calendar_inp_future').attr('min', minDate);
        $('#calendar_inp_future').attr('max', max_date);
        
    });
   
    $('#calendar_li').click(function(){
        $('#calendar_input').addClass("show_me");
        $('#calender').attr("checked", true);
        $('#choice').attr("value", 5);

        $('#calendar_input_future').removeClass("show_me");
        $('#future').attr("checked", false);
        $('#notjoined').attr("checked", false);
       
  
       
    });
    
    $("#nor").on("click", function () {
        if (this.checked) {
            $("#calendar_inp").val("");
            $('#remark').addClass("show_me");
            $('#remark').attr("disabled", false);
        } else {
            $('#remark').removeClass("show_me");
            $('#remark').attr("disabled", true);

        }
    });

   
    $('#notjoined_li').click(function(){
        $('#notjoined').attr("checked", true);
        $('#calendar_input_future').removeClass("show_me");
        $('#choice').attr("value", 6);
        $('#future').attr("checked", false);
        $('#calendar_input').removeClass("show_me");
        $('#calender').attr("checked", false);
    });
    $('#future_li').click(function(){
        $('#calendar_input_future').addClass("show_me");
        $('#future').attr("checked", true);
        $('#choice').attr("value", 7);
        $('#calendar_input').removeClass("show_me");
        $('#calender').attr("checked", false);
        $('#notjoined').attr("checked", false);

    });


});