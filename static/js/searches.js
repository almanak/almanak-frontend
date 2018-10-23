$(document).ready(function() {

    $(document).on('click', '.search-handler', function(e) {
        e.preventDefault();
        var $this = $(this);
        var method, url, data;

        if ( $this.attr('data-action') === 'create-search' ) {
            method = 'POST';
            url = '/users/me/searches';
            data = {
                "url": $this.attr('data-url'),
                "description": $this.siblings('[name="description"]').val()
            };

        } else if ( $this.attr('data-action') === 'delete-search' ) {
            method = 'DELETE';
            url = '/users/me/searches/' + $this.attr('data-created');

        } else if ( $this.attr('data-action') === 'update-search') {
            method = 'PUT';
            url = '/users/me/searches/' + $this.attr('data-created');
            data = {
                "description": $this.siblings('[name="description"]').val()
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
                if (method === 'DELETE') {
                    // Remove specific saved-search listitem after deletion
                    $('.userpage .listitem[data-created="' + resp.created + '"]').slideUp().remove();

                } else if (method === 'POST') {
                    // Close modal and remove 'save-search'-icon from searchpage
                    $('.searchpage #save-search-modal').foundation('close');
                    $('.searchpage #save-search-trigger').remove();

                } else if (method === 'PUT') {
                    // Close modal and update description-text of the specific saved search
                    $('.userpage .reveal[data-created="' + resp.created + '"]').foundation('close');
                    $('.userpage .listitem[data-created="' + resp.created + '"]').find('.search-description').text(resp.description);

                }
            }
        })
        .always(function(resp) {
            notify(resp);
        });
    });
});
