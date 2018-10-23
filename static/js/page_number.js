$(document).ready(function() {

    var $form = $('#page-form');

    $form.on('submit', function() {
        var size = $form.attr('data-size');
        var start_value = $('input[name="start"]').val() - 1;
        $('input[name="start"]').val(start_value * size);
        // var query_string = $form.serialize();
        $form.attr('action', '/search?' + $form.serialize());
        return true;
    });
});
