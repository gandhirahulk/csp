
      $(document).ready(function(){
        $(".sidebar").click(function () {
            $(".wrapper").toggleClass("collapse");
        });
        // $(".sidebar").hover(function () {
        //     $(".wrapper").toggleClass("collapse");
        // });
        $('#entity-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#vendor-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#department-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#function-table').DataTable({
            "bPaginate" : true,
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            
        });
        $('#team-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#subteam-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#designation-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#region-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#state-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#city-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#location-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#user-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });
        $('#candidate-table').DataTable();
        $('#document-table').DataTable();
        $('#wages-table').DataTable({
            "order": [[ 2, "desc" ]], //or asc 
            "columnDefs" : [{"targets":2, "type":"date-eu"}],
            "pagingType": "full_numbers",
            "paging": true,
            "lengthMenu": [10, 25, 50, 75, 100],
        });

    });