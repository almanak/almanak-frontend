$(document).ready(function() {

    // If on a searchpage with splitview activated
    if ( $('#splitlist').length ) {
        // Fetch first record and show in record-container
        var first_url = $('.listitem').attr('href');
        // console.log('found splitview');
        $.get( first_url, function( data ) {
            $( "#record-container" ).html( data );
        });
    }

// Clicking a listitem, if in splitview, shows it in the record-container
    $('.listitem').on('click', function(e) {
        if ( $('#splitlist').length ) {
            e.preventDefault();
            var url = $(this).attr('href');
            $.get( url, function( data ) {
                $( "#record-container" ).html( data );
            });
            // $('#record-container').foundation('scrollToLoc');

        }
    });
});
