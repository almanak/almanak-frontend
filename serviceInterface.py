import os
import json
import requests
import boto3


class Service():
    def __init__(self, api_key):

        self.OAWS_API_KEY = api_key
        self.OAWS_BASE_URL = 'https://openaws.appspot.com'
        self.FILTERS = {
            'creators': {
                "label": "Ophavsretsholder",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'locations': {
                "label": "Stedsangivelse",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'events': {
                "label": "Begivenhed",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'people': {
                "label": "Person",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'organisations': {
                "label": "Organisation",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'collection': {
                "label": "Samling",
                "repeatable": False,
                "type": "object",
                "negatable": True
            },
            'date_from': {
                "label": "Tidligste dato",
                "repeatable": False,
                "type": "date",
                "negatable": False
            },
            'date_to': {
                "label": "Seneste dato",
                "repeatable": False,
                "type": "date",
                "negatable": False
            },
            'subjects': {
                "label": "Emnekategori",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'series': {
                "label": "Arkivserie",
                "repeatable": False,
                "type": "string",
                "negatable": False
            },
            'admin_tags': {
                "label": "Administrativt tag",
                "repeatable": True,
                "type": "string",
                "negatable": True
            },
            'collection_tags': {
                "label": "Samlingstags",
                "repeatable": True,
                "type": "string",
                "negatable": True
            },
            'content_types': {
                "label": "Materialetype",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'collectors': {
                "label": "Arkivskaber",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'curators': {
                "label": "Kurator",
                "repeatable": True,
                "type": "object",
                "negatable": True
            },
            'availability': {
                "label": "Tilgængelighed",
                "repeatable": False,
                "type": "object",
                "negatable": True
            },
            'usability': {
                "label": "Brugslicens",
                "repeatable": False,
                "type": "object",
                "negatable": True
            },
            'registration_id': {
                'label': 'RegistreringsID',
                'repeatable': False,
                'type': 'integer',
                'negatable': False
            }
        }
        self.SEARCH_ENGINE = boto3.client(
            'cloudsearchdomain',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION_NAME"),
            endpoint_url=os.environ.get("AWS_CLOUDSEARCH_ENDPOINT")
        )

    #######################
    # PUBLIC BASE METHODS #
    #######################
    def list_facets(self):
        # Baseline
        facet_options = {
            "availability": {},
            "usability": {},
            "content_types": {"size": 100},
            "subjects": {"size": 100},
        }

        key_args = {}
        key_args['facet'] = json.dumps(facet_options)
        key_args['returnFields'] = '_no_fields'
        key_args['size'] = 1
        key_args['queryParser'] = 'structured'
        key_args['query'] = "matchall"

        response = self.SEARCH_ENGINE.search(**key_args)
        return response.get('facets')

    def list_collection_structures(self, collection_id):
        # Used to fetch series and collection_tags as facets (incl. count) when requesting a collection
        # def sort_by_value(sort_key, list_of_dicts):
        #     decorated = [(dict_.get(sort_key), dict_) for dict_ in list_of_dicts]
        #     decorated.sort()
        #     return [dict_ for (key, dict_) in decorated]

        def _generate_hierarchical_structure(dict_list):
            # Takes a list of strings with possible '/' as hierarchical seperators
            # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

            def addHierItem(key, hierStruct, hierList, parent):
                if parent != "":
                    path = parent + "/" + key
                else:
                    path = key

                hierItem = {"label": key, "path": path}

                childrenList = []
                children = hierStruct.get(key)
                for childKey in sorted(children):
                    addHierItem(childKey, children, childrenList, path)

                if len(childrenList) > 0:
                    hierItem["children"] = childrenList

                hierList.append(hierItem)

            # hierarchical = False
            hierList = []
            hierStruct = {}
            # Extra conversion (relative to the clientInterface-function), as amazon returns list of dicts,
            # not just list of strings
            string_list = [e.get('value') for e in dict_list]

            for item in sorted(string_list):
                splitList = item.split("/")
                # if len(splitlist) > 1:
                #     hierarchical = True

                curLevel = hierStruct
                for key in splitList:
                    hierData = curLevel.get(key, {})
                    curLevel[key] = hierData
                    curLevel = hierData

            for key in sorted(hierStruct):
                addHierItem(key, hierStruct, hierList, "")

            return hierList

        facet_options = {
            "collection_tags": {"sort": "count", "size": 7000},
            "series": {"sort": "count", "size": 2000},
        }

        key_args = {}
        key_args['query'] = "matchall"
        key_args['facet'] = json.dumps(facet_options)
        key_args['returnFields'] = '_no_fields'
        key_args['size'] = 1
        key_args['queryParser'] = 'structured'
        key_args['query'] = "matchall"
        key_args['filterQuery'] = "collection:'" + str(collection_id) +  "'"

        api_response = self.SEARCH_ENGINE.search(**key_args)

        # Convert to dict with label, id and children keys, like the classic 'series'
        facets = api_response.get('facets')

        series = []
        if facets.get('series'):
            series_list = facets['series'].get('buckets')
            series = _generate_hierarchical_structure(series_list)

        collection_tags = []
        if facets.get('collection_tags'):
            collection_tags_list = facets['collection_tags'].get('buckets')
            collection_tags = _generate_hierarchical_structure(collection_tags_list)

        return series, collection_tags
        
    def list_resources_v2(self, query_params):
        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/search-api.html#structured-search-syntax
        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/searching-compound-queries.html

        ############
        # BASELINE #
        ############
        # Kwargs to send to all bobo3-cloudsearch-calls.
        key_args = {}
        key_args['queryParser'] = 'structured'
        key_args['queryOptions'] = json.dumps({
            "fields": ["label^4", "summary^2", "description"],
        })

        date_from = query_params.get("date_from")
        date_to = query_params.get("date_to")
        q = query_params.get("q")
        sort = query_params.get("sort", "date_from")
        direction = query_params.get("direction", "asc")

        ####################
        # SORT + DIRECTION #
        ####################
        # Extra sorting-tests, if no explicit sort is selected.
        if not query_params.get("sort"):
            # If fulltext-search, then rank by relevance
            if q:
                sort = "_score"
                direction = "desc"
            # If date_to is set, override relevance-sorting 
            if date_to:
                sort = "date_to"
                direction = "desc"
            # If date_from is set, overrides relevance and date_to
            if date_from:
                sort = "date_from"
                direction = "asc"

        key_args['sort'] = ' '.join([sort, direction])  # aws-convention

        ###########
        # Q-PARAM #
        ###########
        # Fulltext query - wrap value in single-quotes or if empty use
        # "matchall" to enable filtered searches without a q-param
        if q and q.strip():
            # tokens = q.strip().split(' ')
            tokens = q.split(" ")
            if tokens:
                strs = []
                phrase = None
                phrase_strs = []

                for s in tokens:
                    # no need to bother
                    if len(s) < 2:
                        continue

                    # If single-word phrase
                    if not phrase and s.startswith('"') and s.endswith('"'):
                        strs.append("'" + s[1:-1] + "'")

                    # Elif single-word negative phrase
                    elif not phrase and s.startswith('-"') and s.endswith('"'):
                        strs.append("'" + s[2:-1] + "'")

                    # Elif a phrase is active, add token if not the ending
                    elif phrase and not (s.endswith('"') or s.startswith('"')):
                        phrase_strs.append(s)

                    elif s.startswith('-"') and not phrase:
                        # start a new phrase and append string
                        phrase = 'negated'
                        # s = re.sub('*', '', s)
                        phrase_strs.append(s[2:])

                    elif s.startswith('"') and not phrase:
                        # start a new phrase and append string
                        phrase = 'positive'
                        phrase_strs.append(s[1:])

                    elif s.endswith('"') and phrase:
                        # append string and close phrase
                        phrase_strs.append(s[:-1])
                        if phrase == 'positive':
                            strs.append("(phrase '" + ' '.join(phrase_strs) + "')")
                        else:
                            strs.append("(not (phrase '" + ' '.join(phrase_strs) + "'))")
                        # Ready for new phrase
                        phrase = None
                        phrase_strs = []

                    elif s.startswith('-'):
                        if s.endswith('*'):
                            strs.append("(not (prefix '" + s[:-1] + "'))")
                        else:
                            strs.append("(not '" + s[1:] + "')")

                    elif s.endswith('*'):
                        strs.append("(prefix '" + s[:-1] + "')")

                    else:
                        strs.append("'" + s + "'")

            if len(tokens) > 1:
                key_args['query'] = "(and " + ' '.join(strs) + ")"
            else:
                # key_args['query'] = "'" + strs[0] + "'"
                key_args['query'] = strs[0]

        else:
            key_args['query'] = "matchall"

            # if tokens and len(tokens) > 1:
            #     strs = []
            #     for s in tokens:
            #         if s.endswith('*'):
            #             strs.append("(prefix '" + s[:-1] + "')")
            #         elif s.startswith('-'):
            #             strs.append("(not '" + s[1:] + "')")
            #         else:
            #             strs.append("'" + s + "'")
            #     key_args['query'] = "(and " + ' '.join(strs) + ")"
            # else:
            #     q = tokens[0]
            #     if q.endswith('*'):
            #         key_args['query'] = "(prefix '" + q[:-1] + "')"
            #     elif q.startswith('-'):
            #         key_args['query'] = "(not '" + q[1:] + "')"
            #     else:
            #         key_args['query'] = "'" + q + "'"

        ############
        # FQ-PARAM #
        ############
        filters_to_query = []
        filters_to_resolve = []
        filters_to_output = []
        negated_filters = []

        # Build filterQuery. TODO: hairy stuff that needs documentation
        for key in query_params.keys():

            # If key is negated, but not allowed to, skip it
            if key.startswith('-') and key[1:] in self.FILTERS and not self.FILTERS[key[1:]].get('negatable'):
                continue
            # remove any negation before using self.FILTERS
            stripped_key = key[1:] if key.startswith('-') else key

            if stripped_key in self.FILTERS:
                filter_type = self.FILTERS[stripped_key].get("type")

                # Go back to using the full key-label before iterating query
                for value in query_params.getlist(key):

                    if filter_type == "object":
                        filter_str = ":".join([stripped_key, "'" + value + "'"])
                        # if negation, update filter_str and add to negated[]
                        if stripped_key != key:
                            negated_filters.append((stripped_key, value))
                            filter_str = "(not " + filter_str + ")"
                        filters_to_query.append(filter_str)
                        filters_to_resolve.append((stripped_key, value))

                    elif filter_type in ["string", "integer"]:
                        filter_str = ":".join([stripped_key, "'" + value + "'"])
                        # if negation, update filter_str
                        if stripped_key != key:
                            negated_filters.append((stripped_key, value))
                            filter_str = "(not " + filter_str + ")"
                        filters_to_query.append(filter_str)
                        filters_to_output.append({"key": key, "value": value})

                    elif key == 'date_from':
                        filters_to_query.append("date_from:[" + value + ",}")
                        filters_to_output.append({"key": key, "value": value})

                    elif key == 'date_to':
                        filters_to_query.append("date_to:{," + value + "]")
                        filters_to_output.append({"key": key, "value": value})

        if filters_to_query:
            key_args['filterQuery'] = "(and "+" ".join(filters_to_query) + ")"

        ##################################
        # If Sejrs Sedler or SAM-request #
        ##################################
        if 'ids' in query_params.getlist('view'):
            key_args['returnFields'] = '_no_fields'
            key_args['size'] = query_params.get("size", 1000, int)
            if query_params.get('cursor'):
                key_args['cursor'] = query_params.get('cursor')
            else:
                key_args['cursor'] = 'initial'

            response = self.SEARCH_ENGINE.search(**key_args)

            out = {}
            out['status_code'] = 0
            out['result'] = []
            if key_args.get('size') + response['hits'].get('start') < response['hits'].get('found'):
                out['next_cursor'] = response['hits'].get('cursor')
            for hit in response['hits']['hit']:
                out['result'].append(hit['id'])
            # Debugging
            # out['total_response'] = response
            return out

        #########################
        # Else standard-request #
        #########################
        else:
            # Standard-request stuff
            key_args['facet'] = json.dumps({
                "availability": {},
                "usability": {},
                "content_types": {"size": 100},
                "subjects": {"size": 100},
            })
            key_args['returnFields'] = 'label,summary,content_types,thumbnail,portrait,collectors_label,date_from,date_to,created_at,availability,updated_at'
            key_args['start'] = query_params.get("start", 0, int)
            key_args['size'] = query_params.get("size", 20, int)

            # Request Cloudsearch
            response = self.SEARCH_ENGINE.search(**key_args)

            # Build response
            # Baseline - hits or not
            out = {}
            out['status_code'] = 0
            out['sort'] = sort
            out['direction'] = direction
            out['size'] = key_args['size']
            out['date_from'] = date_from
            out['date_to'] = date_to
            out['total'] = response['hits']['found']
            out['start'] = response['hits']['start']
            out['server_facets'] = response['facets']
            if q:
                out['query'] = q

            out['_query_string'] = key_args['query']
            # out['filterQueryString'] = key_args['filterQuery']

            # Parse hits
            records = []
            for hit in response['hits']['hit']:
                item = {}
                item['id'] = hit['id']

                label = hit['fields'].get("label")
                item['label'] = label[0] if label else None

                summary = hit['fields'].get("summary")
                item['summary'] = summary[0] if summary else None

                item['content_types'] = hit['fields'].get("content_types")

                collectors_label = hit['fields'].get("collectors_label")
                item['collectors_label'] = collectors_label[0] if collectors_label else None

                thumbnail = hit['fields'].get("thumbnail", None)
                item['thumbnail'] = thumbnail[0] if thumbnail else None

                portrait = hit['fields'].get("portrait", None)
                item['portrait'] = portrait[0] if portrait else None

                availability = hit['fields'].get("availability", None)
                item['availability'] = availability[0] if availability else None

                created_at = hit['fields'].get("created_at", None)
                item['created_at'] = created_at[0] if created_at else None

                updated_at = hit['fields'].get("updated_at", None)
                item['updated_at'] = updated_at[0] if updated_at else None

                date_from = hit['fields'].get("date_from")
                item['date_from'] = date_from[0] if date_from else None

                date_to = hit['fields'].get("date_to")
                item['date_to'] = date_to[0] if date_to else None

                records.append(item)
            out['result'] = records

            if filters_to_resolve:
                r = requests.get('/'.join([self.OAWS_BASE_URL, 'resolve_params']),
                                 params=filters_to_resolve)
                if r.ok:
                    content = json.loads(r.content)
                    for key, value in content.get('resolved_params').items():
                        for k, v in value.items():
                            negated = True if (key, k) in negated_filters else False
                            filters_to_output.append({"key": key,
                                                        "value": k,
                                                        "label": v.get('display_label'),
                                                        "negated": negated})
            out['server_filters'] = filters_to_output
            # out['negated_filters'] = negated_filters

            return out
