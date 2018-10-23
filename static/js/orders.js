$(document).ready(function() {

    $(document).on('click', '.order-handler', function(e) {
        e.preventDefault();
        var $this = $(this);
        var method, url, data;

        if ( $this.attr('data-action') === 'delete-order' ) {
            method = 'DELETE';
            url = '/users/me/orders/' + $this.attr('data-resource-id');

        } else if ( $this.attr('data-action') === 'create-order' ) {
            method = 'POST';
            url = '/users/me/orders';
            data = {
                "storage_id": $this.attr('data-storage-id'),
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
                    // If in orderlist-view, remove the listitem after deletion 
                    $('.userpage .order-handler[data-resource-id="' + resp.id + '"]').closest('.listitem').slideUp().remove();
                } else if (method === 'POST') {
                    // If in record-view, toggle 'order'-buttons after ordering the record 
                    $('.resourcepage .order-handler').toggleClass('hide');
                    // If in searchresult-view, remove 'order'-icon of the specific listitem
                    $('.searchpage [data-resource-id="' + resp.id + '"] .order-handler').toggleClass('hide');
                    // If ordering a cartitem, remove the order-button
                    $('.userpage .order-handler[data-resource-id="' + resp.id + '"]').fadeOut().remove();
                }
            }
        })
        .always(function(resp) {
            notify(resp);
        });
    });
});

    // $.fn.serializeObject = function() {
    //    var o = {};
    //    var a = this.serializeArray();
    //    $.each(a, function() {
    //        if (o[this.name]) {
    //            if (!o[this.name].push) {
    //                o[this.name] = [o[this.name]];
    //            }
    //            o[this.name].push(this.value || '');
    //        } else {
    //            o[this.name] = this.value || '';
    //        }
    //    });
    //    return o;
    // };
