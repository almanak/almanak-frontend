$(document).ready(function() {

    // If evenly divisible by 4 and not evenly divisible by 100,
    // or is evenly divisible by 400, then a leap year
    function leap_year(year) {
        if ((!(year % 4) && year % 100) || !(year % 400)) {
            return "29";
        } else {
            return "28";
        }
    }

    var $form = $('#date-form');
    $form.on('submit', function() {
        // event.preventDefault();

        var year_from = $('input[name="year_from"]').val();
        var month_from = $('input[name="month_from"]').val();
        var day_from = $('input[name="day_from"]').val();
        var year_to = $('input[name="year_to"]').val();
        var month_to = $('input[name="month_to"]').val();
        var day_to = $('input[name="day_to"]').val();

        var date_from = '';
        var date_to = '';

        // If not 'year_from' present, skip whole 'date_from'
        if (year_from) {
            if (month_from) {
                if (month_from.length == 1) {
                    month_from = '0' + month_from;
                }
                date_from = year_from + month_from;
                if (day_from) {
                    if (day_from.length == 1) {
                        day_from = '0' + day_from;
                    }
                } else {
                    day_from = '01';
                }
                date_from += day_from;
            // No month present
            } else {
                date_from = year_from + '0101';
            }

            // If 'date_from' present, apply new value, else append to form with new 'date_from'-value
            if ($('input[name="date_from"]').length) {
                $('input[name="date_from"]').val(date_from);
            } else {
                $('<input>').attr('type', 'hidden').attr('name', 'date_from').attr('value', date_from).appendTo($form);
            }
        }

        // If not 'year_to' present, skip whole 'date_to'
        if (year_to) {
            if (month_to) {
                if (month_to.length == 1) {
                    month_to = '0' + month_to;
                }
                date_to = year_to + month_to;
                if (day_to) {
                    if (day_to.length == 1) {
                        day_to = '0' + day_to;
                    }
                } else {
                    // More complex than date_from, as we cannot always use '31'
                    if ($.inArray(month_to, [ "01", "03", "05", "07", "08", "10", "12"]) > -1) {
                        day_to = '31';
                    } else if ($.inArray(month_to, [ "04", "06", "09", "11"]) > -1) {
                        day_to = '30';
                    } else {
                        day_to = leap_year(year_to);
                        // day_to = '28';
                    }
                }
                date_to += day_to;
            } else {
                date_to = year_to + '1231';
            }

            // If 'date_to' present, apply new value, else append to form with new 'date_to'-value
            if ($('input[name="date_to"]').length) {
                $('input[name="date_to"]').val(date_to);
            } else {
                $('<input>').attr('type', 'hidden').attr('name', 'date_to').attr('value', date_to).appendTo($form);
            }
        }

        if (!date_from && !date_to) {
            return false;
        } else {
            // Presumes that everything is OK
            $('input[name="year_from"]').removeAttr('name');
            $('input[name="month_from"]').removeAttr('name');
            $('input[name="day_from"]').removeAttr('name');
            $('input[name="year_to"]').removeAttr('name');
            $('input[name="month_to"]').removeAttr('name');
            $('input[name="day_to"]').removeAttr('name');
            return true;
        }
    });
});
