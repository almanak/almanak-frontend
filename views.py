# -*- coding: utf-8 -*-

# Third party
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import jsonify
from flask import abort
from flask.views import View, MethodView

# Application
import session as ses
import db

# import mail
from auth import login_required, employee_required
import clientInterface


IP_WHITELIST = ["193.33.148.24"]


#############
# BASEVIEWS #
#############
class GUIView(View):
    def __init__(self):
        self.context = {}
        ip = request.headers.get('X-Forwarded-For')
        self.context['readingroom'] = ip in IP_WHITELIST
        self.client = clientInterface.Client()
        facet_dicts = self.client.list_facets_v2()
        self.context['active_facets'] = facet_dicts.get('active_facets')
        self.context['total_facets'] = facet_dicts.get('total_facets')
        # update current url on each gui-request
        ses.set_current_url(request)

    def error_response(self, error):
        if error.get('code') == 404:
            abort(404)
        else:
            return render_template('errorpages/error.html', **error)


class FileView(View):
    def __init__(self, root=False):
        self.root = root

    def dispatch_request(self, filename):
        folder = './static/root' if self.root else './static'
        return send_from_directory(folder, filename)


class RootfileView(View):
    def dispatch_request(self, file):
        return send_from_directory('./static/root', file)


# DERIVED VIEWS
class AppView(GUIView):
    def dispatch_request(self, page):
        self.context['subpage'] = page
        self.context['page'] = 'homepage' if page == 'index' else 'app-page'
        if page in ['searchguide', 'genealogy', 'municipality_records']:
            return render_template('guides.html', **self.context)
        elif page in ['collections', 'availability', 'usability']:
            return render_template('about.html', **self.context)
        else:
            return render_template('%s.html' % page, **self.context)
            # return jsonify(self.context)


# class AboutView(GUIView):
#     """docstring for AboutView"""
#     def dispatch_request(self, page):
#         if page in ['about', 'content', 'availability', 'usability', 'whois']:
#             self.context['page'] = 'app-page'
#             self.context['subpage'] = page
#             return render_template('about.html', **self.context)
#         else:
#             abort(404)


# class SearchView(View):
#     def dispatch_request(self):
#         self.client = clientInterface.Client()
#         self.context = self.client.list_resources(request.args)
#         ip = request.headers.get('X-Forwarded-For')
#         self.context['readingroom'] = ip in IP_WHITELIST
#         # update current url and latest search
#         ses.set_current_url(request)
#         ses.set_latest_search(request)

#         if request.args.get('view', '') == 'ids' or request.args.get('fmt') == 'json':
#             return jsonify(self.context)
#         else:
#             self.context['page'] = 'searchpage'
#             # return render_template('search.html', **self.context)
#             return jsonify(self.context)


class SearchView_v2(GUIView):
    def dispatch_request(self):
        api_response = self.client.list_resources(request.args)
        # update latest search
        ses.set_latest_search(request)

        # SAM and Sejrssedler only wants id-lists
        if 'ids' in request.args.getlist('view'):
            return jsonify(api_response)

        # This is also used by Aarhus Teater
        # Todo or enhance
        elif request.args.get('fmt', '') == 'json':
            response = {}
            response['status_code'] = api_response.get('status_code')
            response['result'] = api_response.get('result')
            response['filters'] = api_response.get('filters')
            response['next'] = api_response.get('next')
            response['previous'] = api_response.get('previous')
            return jsonify(response)

        else:
            self.context.update(api_response)
            self.context['page'] = 'searchpage'
            return render_template('search.html', **self.context)
            # return jsonify(self.context)


class CartView(GUIView):
    def dispatch_request(self):
        cart = ses.get_cart()
        self.context['cart'] = self.client.batch_records(cart)
        self.context['page'] = 'cart'
        # return jsonify(self.context)
        return render_template('cart.html', **self.context)


class ResourceView(GUIView):
    def dispatch_request(self, collection, _id):
        # _id is routed as int, just to eliminate obvious errors
        fmt = request.args.get('fmt', None)
        valid_client = request.args.get('curators', '') == '4'
        response = self.client.get_resource(collection,
                                            resource=str(_id),
                                            fmt=fmt)
        if response.get('error'):
            return self.error_response(response.get('error'))

        if fmt == 'json':
            # If request does not come from aarhusteaterarkiv-web
            # or logged in user is employee
            # then remove asset-links
            if valid_client or (ses.get_user() and 'employee' in ses.get_user_roles()):
                return jsonify(response)
            else:
                response.pop('thumbnail', None)
                response.pop('portrait', None)
                response.pop('representations', None)
                response.pop('resources', None)
                return jsonify(response)

        elif request.is_xhr:
            # If ajax-requested on the results-page it returns an html-blob
            self.context['resource'] = response
            self.context['page'] = 'searchpage'
            return render_template('components/record.html', **self.context)

        else:
            self.context['resource'] = response
            self.context['collection'] = collection
            self.context['page'] = 'resourcepage'
            return render_template('resource.html', **self.context)
            # return jsonify(self.context)


class VocabularyView(GUIView):
    def dispatch_request(self, collection, _id):
        self.context['page'] = 'vocabpage'
        if collection in ['usability', 'availability']:
            if _id not in [1, 2, 3, 4]:
                abort(404)

        self.context['resource'] = _id
        self.context['collection'] = collection

        return render_template('vocabulary.html', **self.context)
        # return jsonify(self.context)


class ProfileView(GUIView):
    decorators = [login_required]

    def dispatch_request(self, page):
        if page == 'cart':
            self.context['subpage'] = 'cart'
            # Fetch full records from remote api
            cart = self.client.batch_records(ses.get_cart())
            self.context['cart'] = cart

        elif page == 'orders':
            self.context['subpage'] = 'orders'
            # Fetch orders from db
            orders = db.list_orders(key='user_id', value=ses.get_user_id())
            # Fetch resources
            if orders:
                id_list = [i.get('resource_id') for i in orders]
                resources = self.client.batch_records(id_list)
                # Map orders and full resources
                for i, v in enumerate(orders):
                    v['resource'] = resources[i]
                self.context['orders'] = orders

        elif page == 'bookmarks':
            self.context['subpage'] = 'bookmarks'
            # Fetch full records from remote api
            full_bookmarks = self.client.batch_records(ses.get_bookmarks())
            self.context['bookmarks'] = full_bookmarks

        elif page == 'searches':
            self.context['subpage'] = 'searches'
            # Fetch searches from local database
            searches = db.list_searches(ses.get_user_id())
            self.context['searches'] = searches

        elif page == 'profile':
            self.context['subpage'] = 'profile'

        elif page == 'session':
            self.context['subpage'] = 'session'

        else:
            abort(404)

        self.context['page'] = 'userpage'
        return render_template('profile.html', **self.context)
        # return jsonify(self.context)


class AdminView(GUIView):
    decorators = [employee_required]

    def dispatch_request(self, page):
        # if page == 'orders':
        #     self.context['subpage'] = 'orders'

        # elif page == 'units':
        #     self.context['subpage'] = 'units'
        # elif page == 'default':
        #     self.context['page'] = 'default'

        # elif page == 'users':
        #     self.context['subpage'] = 'users'
        #     # Fetch users from local database
        #     self.context['users'] = db.get_users()
        render_template('admin.html', **self.context)


class OrderAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    decorators = [login_required]

    # def post(self):
    #     payload = request.get_json()
    #     unit_id = payload.get('storage_id')
    #     resource_id = payload.get('resource_id')

    #     if resource_id in ses.get_orders():
    #         resp = {'error': True,
    #                 'msg': u'Du har allerede bestilt materialet.'}

    #     elif unit_id and resource_id:
    #         # resp = db.create_order(user, resource_id, unit_id)
    #         resp = db.put_order(ses.get_user_id(), resource_id, unit_id)
    #         if not resp.get('error'):
    #             ses.add_order(resource_id)  # Add to session also

    #     else:
    #         resp = {'error': True,
    #                 'msg': u'Manglende information: unit_id eller \
    #                     resource_id.'}

    #     return jsonify(resp)

    # def delete(self, resource_id):
        # response = db.delete_order(ses.get_user_id(), resource_id)
        # key = {'user_id': ses.get_user_id(), 'resource_id': resource_id}
        # response = db.delete_order(key)

        # if not response.get('error'):
        #     ses.remove_order(resource_id)

        # m = response.get('mail')
        # if m:
        #     mail.send_mail(recipient=m.get('email'),
        #                    event='order_available',
        #                    data={'name': m.get('name'),
        #                          'resource': m.get('resource_id')})
        # return jsonify(response)


# TO IMPLEMENT
class UnitAPI(MethodView):
    def get(self):
        return jsonify({'implemented': False})


class BookmarkAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    # AND uses gui-login decorators
    decorators = [login_required]

    def post(self):
        user_id = ses.get_user_id()
        payload = request.get_json()
        resource_id = payload.get('resource_id')

        if resource_id:
            if resource_id in ses.get_bookmarks():
                return jsonify({'error': True,
                                'msg': 'Materialet var allerede bogmærket'})
            else:
                bookmark = {'user_id': user_id, 'resource_id': resource_id}
                response = db.put_bookmark(bookmark)
                if not response.get('error'):
                    ses.add_bookmark(resource_id)  # Add to session also
                return jsonify(response)
        else:
            return jsonify({'error': True,
                            'msg': 'Manglende materialeID'})

    def delete(self, resource_id):
        user_id = ses.get_user_id()
        bookmark = {'user_id': user_id, 'resource_id': resource_id}
        response = db.delete_bookmark(bookmark)
        if not response.get('error'):
            ses.remove_bookmark(resource_id)  # Remove from session also
        return jsonify(response)


class SearchesAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    decorators = [login_required]

    def post(self):
        user_id = ses.get_user_id()
        payload = request.get_json()
        url = payload.get('url')
        description = payload.get('description')
        if url:
            search = {'user_id': user_id,
                      'url': url,
                      'description': description}
            return jsonify(db.add_search(search))
        else:
            return jsonify({
                'error': True,
                'msg': 'Manglende url-parameter'
            })

    def put(self, created):
        user_id = ses.get_user_id()
        payload = request.get_json()
        description = payload.get('description')

        if description:
            response = db.update_search(user_id, created, description)
            if response.get('error'):
                return jsonify(response)
            else:
                response['msg'] = 'Søgning opdateret'
                return jsonify(response)
        else:
            return jsonify({
                'error': True,
                'msg': 'Manglende beskrivelse'
            })

    def delete(self, created):
        search = {'user_id': ses.get_user_id(), 'created': created}
        return jsonify(db.delete_search(search))


class CartAPI(MethodView):
    # Receives and returns JSON, but is dependent on a session-object
    def post(self):
        payload = request.get_json()
        resource_id = payload.get('resource_id')
        if resource_id:
            return jsonify(ses.add_to_cart(resource_id))
        else:
            return jsonify({'error': 'Missing resource_id'})

    def delete(self, resource_id):
        return jsonify(ses.remove_from_cart(resource_id))


class AutosuggestView(View):
    def dispatch_request(self):
        self.client = clientInterface.Client()
        key_args = {}
        key_args['term'] = request.args.get('q')
        key_args['limit'] = request.args.get('limit', 10)
        key_args['domain'] = request.args.get('domain')
        if key_args['term']:
            return jsonify(self.client.autocomplete(**key_args))
        else:
            return jsonify([])


class TestView(GUIView):
    def dispatch_request(self):
        # cart = ses.get_cart()
        # self.context['cart'] = self.client.batch_records(cart)
        self.context['page'] = 'test'
        # self.context['json_data'] = desktop.get_local_file()
        # return jsonify(self.context)
        return render_template('test.html', **self.context)

