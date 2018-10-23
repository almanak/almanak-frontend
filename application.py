# Standard library
import os
import json

# Third party libraries
import requests
from six.moves.urllib.parse import urlencode

# Flask
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash

# Application libraries
import views
import db

ICONS = {
    "61": {
        "icon": "far fa-image",
        "label": "Billeder"
    },
    "95": {
        "icon": "fas fa-laptop",
        "label": "Elektronisk materiale"
    },
    "10": {
        "icon": "fas fa-gavel",
        "label": "Forskrifter og vedtægter"
    },
    "1": {
        "icon": "far fa-folder-open",
        "label": "Kommunale sager og planer"
    },
    "75": {
        "icon": "far fa-map",
        "label": "Kortmateriale"
    },
    "49": {
        "icon": "far fa-file-alt",
        "label": "Manuskripter"
    },
    "87": {
        "icon": "fas fa-film",
        "label": "Medieproduktioner"
    },
    "81": {
        "icon": "fas fa-music",
        "label": "Musik og lydoptagelser"
    },
    "36": {
        "icon": "fas fa-book",
        "label": "Publikationer"
    },
    "18": {
        "icon": "fab fa-leanpub",
        "label": "Registre og protokoller"
    },
    "29": {
        "icon": "far fa-chart-bar",
        "label": "Statistisk og økonomisk materiale"
    },
    "99": {
        "icon": "far fa-file",
        "label": "Andet materiale"
    }
}


# Init app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.debug = os.environ.get('DEBUG')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', False)


# app.jinja_env.auto_reload = True
app.url_map.strict_slashes = False
# app.jinja_env.globals['ICONS'] = {
app.add_template_global(name='ICONS', f=ICONS)

@app.before_request
def before_request():
    # Copied from https://github.com/kennethreitz/flask-sslify
    criteria = [
        request.is_secure,
        app.debug,
        app.testing,
        request.headers.get('X-Forwarded-Proto', 'http') == 'https'
    ]

    if not any(criteria):
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


@app.after_request
def after_request(response):
    criteria = [
        app.debug,
        app.testing,
    ]

    if not any(criteria):
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

    return response


app_pages = ['cookies', 'tos', 'privacy']
about = ['collections', 'availability', 'usability']
guides = ['searchguide', 'genealogy', 'municipality_records']
resources = ['records', 'people', 'locations', 'organisations', 'events',
             'objects', 'collections', 'creators', 'collectors']
vocabs = ['availability', 'usability', 'content_types', 'subjects']

# Homepage
app.add_url_rule('/',
                 defaults={'page': 'index'},
                 view_func=views.AppView.as_view('index'))

# App-pages
app.add_url_rule('/<any(' + ', '.join(app_pages) + '):page>',
                 view_func=views.AppView.as_view('show_app_page'))

app.add_url_rule('/guides/<any(' + ', '.join(guides) + '):page>',
                 view_func=views.AppView.as_view('show_guide'))

app.add_url_rule('/about/<any(' + ', '.join(about) + '):page>',
                 view_func=views.AppView.as_view('show_about'))

# Static root files
app.add_url_rule('/robots.txt',
                 defaults={'file': 'robots.txt'},
                 view_func=views.RootfileView.as_view('serve_robots'))


app.add_url_rule('/BingSiteAuth.xml',
                 defaults={'file': 'BingSiteAuth.xml'},
                 view_func=views.RootfileView.as_view('serve_microsoft'))


app.add_url_rule('/google46a7bae009a5abed.html',
                 defaults={'file': 'google46a7bae009a5abed.html'},
                 view_func=views.RootfileView.as_view('serve_google'))

# Static DOM files (css, images, js, scss...)
app.add_url_rule('/static/<path:filename>',
                 view_func=views.FileView.as_view('serve_static_file'))

# Search
app.add_url_rule('/search',
                 view_func=views.SearchView_v2.as_view('search'))

# Resources
app.add_url_rule('/<any(' + ', '.join(resources) + '):collection>/<int:_id>',
                 view_func=views.ResourceView.as_view('show_resource'))

# Vocabularies (subpaged)
app.add_url_rule('/<any(' + ', '.join(vocabs) + '):collection>/<int:_id>',
                 view_func=views.VocabularyView.as_view('show_vocabulary'))

# Profile (subpaged)
app.add_url_rule('/users/me',
                 defaults={'page': 'profile'},
                 view_func=views.ProfileView.as_view('show_profile'))
app.add_url_rule('/users/me/<path:page>',
                 view_func=views.ProfileView.as_view('show_profile_subpage'))

# Autosuggest
app.add_url_rule('/autosuggest',
                 view_func=views.AutosuggestView.as_view('autosuggest'))

# CartAPI
app.add_url_rule('/cart',
                 view_func=views.CartView.as_view('show_cart'),
                 methods=['GET'])
app.add_url_rule('/cart',
                 view_func=views.CartAPI.as_view('add_to_cart'),
                 methods=['POST'])
app.add_url_rule('/cart/<resource_id>',
                 view_func=views.CartAPI.as_view('remove_from_cart'),
                 methods=['DELETE'])

# OrderAPI
app.add_url_rule('/users/me/orders',
                 view_func=views.OrderAPI.as_view('create_order'),
                 methods=['POST'])
app.add_url_rule('/users/me/orders/<resource_id>',
                 view_func=views.OrderAPI.as_view('delete_order'),
                 methods=['DELETE'])

# BookmarkAPI
app.add_url_rule('/users/me/bookmarks',
                 view_func=views.BookmarkAPI.as_view('create_bookmark'),
                 methods=['POST'])
app.add_url_rule('/users/me/bookmarks/<resource_id>',
                 view_func=views.BookmarkAPI.as_view('delete_bookmark'),
                 methods=['DELETE'])

# SearchesAPI
app.add_url_rule('/users/me/searches',
                 view_func=views.SearchesAPI.as_view('create_search'),
                 methods=['POST'])
app.add_url_rule('/users/me/searches/<created>',
                 view_func=views.SearchesAPI.as_view('delete_search'),
                 methods=['DELETE'])
app.add_url_rule('/users/me/searches/<created>',
                 view_func=views.SearchesAPI.as_view('update_search'),
                 methods=['PUT'])

# Test
app.add_url_rule('/testpage',
                 view_func=views.TestView.as_view('test'),
                 methods=['GET'])

##############
# AUTH-VIEWS #
##############
@app.route('/<any("login", "signup"):page>')
def login(page):
    # initialScreen = page if page == 'login' else 'signUp'
    if session.get('profile'):
        return redirect(url_for('show_profile'))
    else:
        params = {
            'redirect_uri': os.environ.get('AUTH0_CALLBACK_URL'),
            'response_type': 'code',
            'scope': 'openid profile email',
            'client_id': os.environ.get('AUTH0_CLIENT_ID'),
            'audience': os.environ.get('AUTH0_AUDIENCE')
        }
        url = 'https://' + os.environ.get('AUTH0_DOMAIN') + '/authorize?'
        return redirect(url + urlencode(params))


@app.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('index', _external=True),
        'client_id': os.environ.get("AUTH0_CLIENT_ID")
    }
    url = 'https://' + os.environ.get("AUTH0_DOMAIN") + '/v2/logout?'
    return redirect(url + urlencode(params))


@app.route('/callback')
def callback_handler():
    if not request.args.get('code'):
        flash('Missing "code-param". Unable to handle login/signup at the moment.')
        if session.get('current_url'):
            return redirect(session.get('current_url'))
        else:
            return redirect(url_for('index'))

    token_payload = {
        'code': request.args.get('code'),
        'client_id': os.environ.get("AUTH0_CLIENT_ID"),
        'client_secret': os.environ.get("AUTH0_CLIENT_SECRET"),
        'redirect_uri': os.environ.get("AUTH0_CALLBACK_URL"),
        'grant_type': os.environ.get("AUTH0_GRANT_TYPE")
    }

    # get token
    token_url = "https://{domain}/oauth/token".format(domain=os.environ.get("AUTH0_DOMAIN"))
    headers = {'content-type': 'application/json'}
    token_info = requests.post(token_url,
                               data=json.dumps(token_payload),
                               headers=headers).json()

    # if not token - return
    if not token_info.get('access_token'):
        flash('Missing "access_token". Unable to handle login at the moment.')
        if session.get('current_url'):
            return redirect(session.get('current_url'))
        else:
            return redirect(url_for('index'))


    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain=os.environ.get("AUTH0_DOMAIN"),
                access_token=token_info['access_token'])

    # get userinfo
    try:
        userinfo = requests.get(user_url).json()
    except ValueError as e:
        flash('Unable to fetch userdata: ' + e)
        if session.get('current_url'):
            return redirect(session.get('current_url'))
        else:
            return redirect(url_for('index'))

    # Insert or sync with db_user
    # return db_user with roles, max_units...
    db_user = db.sync_or_create_user(userinfo)

    if db_user.get('error'):
        flash('Error syncing user with local db: ' + db_user.get('msg'))
    else:
        # Populate the session
        session['profile'] = {
            'user_id': db_user.get('user_id'),
            'name': db_user.get('federated_name'),
            'email': db_user.get('email'),
            'roles': db_user.get('roles')
        }

        session['is_employee'] = 'employee' in db_user.get('roles', [])
        session['is_admin'] = 'admin' in db_user.get('roles', [])

        # Add bookmark_ids from db
        session['bookmarks'] = db.list_bookmarks(user_id=db_user.get('user_id'), ids_only=True)

        # Create session-cart, if not already created before login
        session['cart'] = session.get('cart', [])

        # Add active orders from db
        # session['orders'] = db.get_orders(user_id=user.get('user_id'), ids_only=True)
        session.modified = True

    if session.get('current_url'):
        return redirect(session.get('current_url'))
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    # Flask automatically detects if dotenv is installed, and then fetches the .env-file
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4000))
