$(document).ready(function() {

    $(document).on('click', '.cart-handler', function(e) {
        e.preventDefault();
        var $this = $(this);
        var method, url, data;

        if ( $this.attr('data-action') === 'remove-from-cart' ) {
            method = 'DELETE';
            url = '/cart/' + $this.attr('data-resource-id');

        } else if ( $this.attr('data-action') === 'add-to-cart' ) {
            method = 'POST';
            url = '/cart';
            data = {
                "resource_id": $this.attr('data-resource-id')
            };

        } else {
            return false;
        }

        $.ajax({
            type : method,
            url : url,
            dataType: 'json',
            data: JSON.stringify( data ),
            contentType: 'application/json;charset=UTF-8'
        })
        .done(function(resp) {
            if (!resp.error) {
                console.log(resp);
                // Get value from any (the first) of potentially multiple badges
                var currentSize = $('.cart-badge').text()[0];
                var cartSize;

                if (method === 'DELETE') {
                    cartSize = parseInt(currentSize) - 1;
                    // If cart is emptied, hide the badge-counter. Foundation uses .hide
                    if (cartSize === 0) { $('.cart-badge').addClass('hide'); }

                    // If deleting in cartlist-view, remove the relevant listitem after deletion 
                    $('.userpage .cart-handler[data-resource-id="' + resp.id + '"]').closest('.listitem').slideUp().remove();
                    $('.cart .cart-handler[data-resource-id="' + resp.id + '"]').closest('.listitem').slideUp().remove();

                } else if (method === 'POST') {
                    cartSize = parseInt(currentSize) + 1;
                    // No matter cartsize, it must now be positive
                    $('.cart-badge').removeClass('hide');
                }

                // Replace both on- and offline-viewable badges
                $('.cart-badge').each(function() {
                    $(this).text(cartSize);
                });

                // Toggle visibility of both cart-handler-buttons on a resourcepage, whether DELETE or POST
                // No need to specify data-resource-id
                $('.resourcepage .cart-handler').toggleClass('hide');
                // Toggle visibility of both cart-handler-icons of a given listitem on a searchpage, whether DELETE or POST
                $('.searchpage [data-resource-id="' + resp.id + '"] .cart-handler').toggleClass('hide');
            }
        })
        .always(function(resp) {
            notify(resp);
        });
    });

    // Special event-handler for cart
    $(document).on('click', '.cart-link', function(e) {
        if ( !$('.cart-badge').is(':visible') ) {
            e.preventDefault();
            alert('KURVEN ER TOM\n\nKurven fungerer som en huskeliste, hvortil man kan tilføje eller fjerne materialer. Hvis man er logget ind, kan man også bogmærke og bestille materialer fra kurven.');
        }
    });

});
