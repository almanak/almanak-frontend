$(document).ready( function () {
    $('#available-orders-table, #initialized-orders-table, #terminated-orders-table').DataTable( {
        "columnDefs": [
            { "orderable": false, "targets": 4 },
            { "orderable": false, "targets": 5 },
            { "orderable": false, "targets": 6 },
            { "orderable": false, "targets": 7 },
        ]
    });
} );