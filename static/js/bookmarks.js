$(document).ready(function() {

    $(document).on('click', '.bookmark-handler', function(e) {
        e.preventDefault();
        var $this = $(this);
        var method, url, data;

        if ( $this.attr('data-action') === 'delete-bookmark' ) {
            method = 'DELETE';
            url = '/users/me/bookmarks/' + $this.attr('data-resource-id');

        } else if ( $this.attr('data-action') === 'create-bookmark' ) {
            method = 'POST';
            url = '/users/me/bookmarks';
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
                if (method === 'DELETE') {
                    // If in bookmarklist-view, remove the listitem after deletion 
                    $('.userpage .bookmark-handler[data-resource-id="' + resp.id + '"]').closest('.listitem').slideUp().remove();
                } else if (method === 'POST') {
                    // If in searchresult-view, remove 'bookmark'-icon of the specific listitem
                    $('.searchpage [data-resource-id="' + resp.id + '"] .bookmark-handler').toggleClass('hide');
                    // If bookmarking a cartitem, remove the bookmark-button
                    $('.userpage .bookmark-handler[data-resource-id="' + resp.id + '"]').fadeOut().remove();
                }
                // If in record-view, toggle 'bookmark'-buttons after bookmarking the record, no matter method
                $('.resourcepage .bookmark-handler').toggleClass('hide');
            }
        })
        .always(function(resp) {
            notify(resp);
        });
    });
});
