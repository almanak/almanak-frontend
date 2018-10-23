// var structure = new Bloodhound({
//     datumTokenizer: Bloodhound.tokenizers.obj.whitespace('preferredTerm'),
//     queryTokenizer: Bloodhound.tokenizers.whitespace,
//     local: (series) ? series : {}
// });
// {
//     name: 'series',
//     display: 'preferredTerm',
//     source: structure,
//     templates: {
//         suggestion: function(data) {
//             return '<div><span class="pre-icon icon_bookmark">' + data.preferredTerm + '</span></div>';
//         }
//     }
// }

// Typeahead remote-request engine
var entities = new Bloodhound({
    // datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/autosuggest?q=',
        prepare: function (query, settings) {
            // console.log(query);
            settings.url = settings.url + encodeURIComponent(query);
            return settings;
        },
        transform: function (payload) {
            transformedHits = [];
            // transformedHits.push({domain: 'q'});

            $.each(payload, function(i, m) {
                // Apply icons
                var icon_string = "";
                if (m.domain == "organisations") {
                    m.icon = "far fa-building icon-left fa-sm";
                    if (m.sub_display.indexOf("Organisation,") > -1) {
                        m.sub_display = m.sub_display.replace("Organisation, ", "");
                    }
                    // } else {
                    //     m.sub_display = m.sub_display.replace("Organisation", "");
                    // }
                } else if (m.domain == "locations") {
                    m.icon = "fas fa-map-marker-alt icon-left fa-sm";
                    if (m.sub_display.indexOf("Sted,") > -1) {
                        m.sub_display = m.sub_display.replace("Sted, ", "");
                    }
                    // } else {
                    //     m.sub_display = m.sub_display.replace("Sted", "");
                    // }
                } else if (m.domain == "people") {
                    m.icon = "far fa-user icon-left fa-sm";
                    if (m.sub_display.indexOf("Person,") > -1) {
                        m.sub_display = m.sub_display.replace("Person, ", "");
                    }
                    // } else {
                    //     m.sub_display = m.sub_display.replace("Person", "");
                    // }
                } else if (m.domain == "events") {
                    m.icon = "far fa-calendar icon-left fa-sm";
                    if (m.sub_display.indexOf("Begivenhed,") > -1) {
                        m.sub_display = m.sub_display.replace("Begivenhed, ", "");
                    }
                    // } else {
                    //     m.sub_display = m.sub_display.replace("Begivenhed", "");
                    // }
                } else if (m.domain == "collections") {
                    // HACK - collections must be renamed to collection
                    m.domain = 'collection';
                    m.icon = "fas fa-archive icon-left fa-sm";
                } else {
                    m.icon = "";
                }
                transformedHits.push(m);
            });
            return transformedHits;
        }
    }
});

$(document).ready(function(){
    $('.global-search-field').typeahead({
        hint: false,
        highlight: true,
        minLength: 2
    },
    {
        name: 'entities',
        display: 'display',
        source: entities,
        limit: 10,
        templates: {
            pending: '<div class="auto-pending">Henter forslag...</div>',
            notFound: '<div class="auto-not-found">Ingen forslag. Tryk på søgeknappen for at fritekstsøge i stedet.</div>',
            header: '<div class="auto-header">Vælg et forslag nedenfor <strong>eller</strong> tryk på søgeknappen for at fritekstsøge.</div>',
            suggestion: function(data) {
                // if (data.domain === 'q') {
                //     // HACK: DOM -update to use on selecting fulltext-suggestion
                //     $('.typeahead-search-field').attr('data-query', data._query);
                //     return  '<p style="border-bottom: 2px solid #ececec;">Fritekstsøg...</p>';
                // }  else if (data.hasOwnProperty('sub_display')) {
                if (data.hasOwnProperty('sub_display')) {
                    return '<div><span class="' + data.icon + '"></span><span class="auto-display">' + data.display + '</span><br><span class="auto-sub-display">' + data.sub_display + '</span></div>';
                } else {
                    return '<div><span class="' + data.icon + '"></span><span>' + data.display + '</span></div>';
                }
            },
            footer: function(data) {
                console.log(data);
                if (data.suggestions.length === 10) {
                     return '<div class="auto-footer"><span>Flere end 10 forslag!</span><br><span>Skriv noget mere eller vælg fritekstsøgning.</span></div>';
                }
            }
        }
    })
    .on("typeahead:select", function(e, datum, dataset) {
        // console.log(dataset);
        var $form = $(this).closest('form');
        var $input = $form.find('.global-search-field').first();

        if (datum.domain === 'q') {
            val = $input.attr('data-query');
            $input.val(val);
        } else {
            $input.attr('name', datum.domain).val(datum.id);
        }
        // console.log($input);
        $form.submit();
    })
    .on("typeahead:render", function(e, suggestions, async, dataset) {
        // $('body #tt-helptext').remove();
        // console.log('registered: ' + 'render');
    })
    .on("typeahead:active", function(e, obj) {
        // $('.tt-dataset').prepend('<div id="tt-helptext" style="padding:.3rem;font-size:90%;color:#333;"><p>Brug * for at trunkere. Eks.: " skattemandtal* "</p></div>');
        // console.log('registered: ' + 'active');
    })
    .on("typeahead:idle", function(e, obj) {
        // $('body #tt-helptext').remove();
        // console.log('registered: ' + 'idle');
    })
    .on("typeahead:open", function(e, obj) {
        // console.log('registered: ' + 'open');
    })
    .on("typeahead:close", function(e, obj) {
        // console.log('registered: ' + 'close');
    })
    .on("typeahead:change", function(e) {
        // console.log('registered: ' + 'change');
    })
    .on("typeahead:select", function(e, datum, dataset) {
        console.log('registered: ' + 'select');
    })
    .on("typeahead:selected", function(e, datum, dataset) {
        console.log('registered: ' + 'selected');
    })

    .on('typeahead:selectableClicked', function(e) {
        console.log('registered: ' + 'selectableClicked');
    })
    .on('typeahead:asyncRequested', function(e) {
        console.log('registered: ' + 'asyncRequested');
    })
    .on('typeahead:asyncCanceled', function(e) {
        console.log('registered: ' + 'asyncCanceled');
    })
    .on('typeahead:asyncReceived', function(e) {
        console.log('registered: ' + 'asyncReceived');
    })
    .on('typeahead:datasetRendered', function(e) {
        console.log('registered: ' + 'datasetRendered');
    })
    .on('typeahead:datasetCleared', function(e) {
        console.log('registered: ' + 'datasetCleared');
    })


    .on("typeahead:autocomplete", function(e, datum, dataset) {
        // console.log('registered: ' + 'autocomplete');
    })
    .on("typeahead:cursorchange", function(e, datum, dataset) {
        // console.log('registered: ' + 'cursorchange');
    })
    .on("typeahead:asyncrequest", function(e, query, dataset) {
        // console.log('registered: ' + 'asyncrequest');
    })
    .on("typeahead:asynccancel", function(e, query, dataset) {
        // console.log('registered: ' + 'asynccancel');
    })
    .on("typeahead:asyncreceive", function(e, query, dataset) {
        // console.log('registered: ' + 'asyncreceive');
    });
});
