function getPDF(){
    // alert("save me");
    var HTML_Width = 450;
    var HTML_Height = HTML_Width * 1.3;
    var top_left_margin = 45 ;
    var PDF_Width = 450 +(top_left_margin*2);
    // var PDF_Width = HTML_Width+(top_left_margin*2);

    var PDF_Height = (PDF_Width)+(top_left_margin*2);
    // var PDF_Height = (PDF_Width)+(top_left_margin*2);

    var canvas_image_width = HTML_Width ;
    var canvas_image_height = HTML_Height / 2;



    var totalPDFPages = Math.ceil(HTML_Height/PDF_Height)-1;
    
    
    
    html2canvas($(".canvas_div_pdf")[0],{allowTaint:true, quality: 4, scale : 5}).then(function(canvas) {
    canvas.getContext('2d');
    

    
    // console.log(canvas.height+"  "+canvas.width);
    
    
    var imgData = canvas.toDataURL("image/jpeg", 1.0);
    var pdf = new jsPDF('p', 'pt',  [PDF_Width, PDF_Height]);
    // var pdf = new jsPDF('p', 'pt','a4',true);
    pdf.addImage(imgData, 'PNG', top_left_margin, top_left_margin,canvas_image_width,canvas_image_height);
    // pdf.addImage(imgData, 'PNG', 0, 0, 485, 270, undefined,'FAST');
    
    // for (var i = 1; i <= totalPDFPages; i++) { 
    //     pdf.addPage(PDF_Width, PDF_Height);
    //     pdf.addImage(imgData, 'PNG', top_left_margin, -(PDF_Height*i)+(top_left_margin*4),canvas_image_width,canvas_image_height);
    // }
    
    pdf.save("salary-structure.pdf");
    });
    };

