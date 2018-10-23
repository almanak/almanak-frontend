$(document).ready(function(){

    $('.typeahead-search-field').typeahead({
        // input: '.typeahead-search-form',
        minLength: 2,
        maxItem: 25,
        accent: true,
        emptyTemplate: 'Intet resultat for "{{query}}"',
        dynamic: true,
        // delay: 400,
        // backdrop: true,
        // resultContainer: '#typeahead__resultContainer',
        // href: "/search?{{domain}}={{id}}",
        // template: "{{display}}",
        // dynamicFilter: null,  // default value
        // resultContainer: null,  // default value
        // loadingAnimation: false,

        // IMPORTANT: Return a string
        // group: {
        //     key: "domain",
        //     template: function (item) {
        //         var domains = {
        //             "tags": "Tags",
        //             "people": "Personer",
        //             "organisations": "Organisationer",
        //             "events": "Begivenheder",
        //             "locations": "Steder",
        //             "collections": "Samlinger"
        //         };
        //         return domains[item.domain];
        //     }
        // },
        source: {
            ajax: {
                type: "GET",
                // TODO: change to q when problem solved
                url: "/autosuggest_v2?t={{query}}"
            }
        },
        template: "<div class='autosuggest_listitem'> \
                    <p class='autosuggest_item-header'>{{display}}</p> \
                    <p class='autosuggest_item-subheader'>{{sub_display}}</p> \
                    </div>",
        debug: true,
        callback: {
            onNavigateAfter: function (node, lis, a, item, query, event) {
                console.log('onNavigateAfter function triggered');
                if (~[38,40].indexOf(event.keyCode)) {
                    var resultList = node.closest("form").find("ul.typeahead__list"),
                    // var resultList = $("#typeahead__resultContainer").find("ul.typeahead__list"),
                        activeLi = lis.filter("li.active"),
                        offsetTop = activeLi[0] && activeLi[0].offsetTop - (resultList.height() / 2) || 0;
                    resultList.scrollTop(offsetTop);
                }
            },
            onResult: function (node, query, result, resultCount) {
                // if (query === "") return;
     
                // var text = "";
                // if (result.length > 0 && result.length < resultCount) {
                //     text = "Showing <strong>" + result.length + "</strong> of <strong>" + resultCount + '</strong> elements matching "' + query + '"';
                // } else if (result.length > 0) {
                //     text = 'Showing <strong>' + result.length + '</strong> elements matching "' + query + '"';
                // } else {
                //     text = 'No results matching "' + query + '"';
                // }
                // $('#result-container').html(text);

                console.log(result);
                console.log("resultCount:" + resultCount);
                console.log('onResult function triggered');
            },
            onClick: function (node, a, item, event) {
                console.log('onClick function triggered. Input-field name and value updated.');
                node.attr('name', item.domain);
                node.val(item.id);
                node.closest('form').submit();
            },
            onShowLayout: function (node, query) {
                console.log('onShowLayout triggered');
            },
            onHideLayout: function (node, query) {
                console.log('onHideLayout triggered');
                // $('#typeahead__resultContainer').toggleClass('hide');
            },
            // onSubmit: function (node, form, item, event) {
            //     // console.log(node);
            //     console.log(form);
            //     console.log("item:" + item);
            //     // console.log("event:" + event);
            //     console.log('onSubmit override function triggered');
            //     //form.submit();
            //     event.preventDefault();
            // }
        }
    });

    $('.global-search-form').on('submit', function(e) {
        console.log($(this));
        // e.preventDefault();
    });
});
