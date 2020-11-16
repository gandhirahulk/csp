
      $(document).ready(function(){
        $(".sidebar").click(function () {
            $(".wrapper").toggleClass("collapse");
        });
        // $(".sidebar").hover(function () {
        //     $(".wrapper").toggleClass("collapse");
        // });
        $('#entity-table').DataTable({
            "order": [[ 2, "desc" ],[ 3, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"},{"targets":3, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
            
        });
        $('#vendor-table').DataTable({          
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        
        $('#department-table').DataTable({
            
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
     
        $('#function-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
            
        });
        $('#team-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#subteam-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#designation-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#region-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#state-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#city-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#location-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#user-table').DataTable({
            "order": [[ 3, "desc" ]], //or asc 
            "columnDefs" : [{"targets":3, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        
        $('#candidate-table').DataTable({
            scrollX : "true",
            "order": [[ 22, "desc" ],[ 23, "desc" ]], 
            "columnDefs" : [{"targets":22, "type":"date-eu"},{"targets":23, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
            "autoWidth": true
        } );
        $('#pending-candidate-table').DataTable();
        $('#joined-candidate-table').DataTable();
        $('#future-candidate-table').DataTable();
        $('#dropout-candidate-table').DataTable();
        $('#request-candidate-table').DataTable();



    
        $('#document-table').DataTable();
        $('#nocandidate-table').DataTable({
            scrollX: true,
        });
        $('#wages-table').DataTable({
            "order": [[ 1, "desc" ],[ 2, "desc" ]], 
            "columnDefs" : [{"targets":1, "type":"date-eu"},{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });

    });