# -*- coding: utf-8 -*-
from flask import session


########
# USER #
########
def get_user():
    return session.get('profile', None)

def get_user_id():
    user = session.get('profile', None)
    return user.get('user_id', None)

def get_user_roles():
    user = session.get('profile', None)
    return user.get('roles', [])


##############
# CART-ITEMS #
##############
def get_cart():
    return session.get('cart', [])


def add_to_cart(resource_id):
    cart = session.get('cart', [])
    cart.append(resource_id)
    session['cart'] = cart
    session.modified = True
    return {
        'msg': 'Materialet er lagt i kurven.',
        'id': resource_id
    }


def remove_from_cart(resource_id):
    cart = session.get('cart', [])
    if cart and resource_id in cart:
        cart.remove(resource_id)
        session['cart'] = cart
        session.modified = True
        return {
            'msg': 'Materialet fjernet fra kurven.',
            'id': resource_id
        }
    else:
        return {
            'error': True,
            'msg': 'Materialet var ikke i kurven.'
        }


#############
# BOOKMARKS #
#############
def get_bookmarks():
    return session.get('bookmarks', [])


def add_bookmark(resource_id):
    bookmarks = session.get('bookmarks', [])
    bookmarks.append(resource_id)
    session['bookmarks'] = bookmarks
    session.modified = True
    return {'msg': 'Materialet blev tilføjet i session'}


def remove_bookmark(resource_id):
    bookmarks = session.get('bookmarks', [])
    bookmarks.remove(resource_id)
    session['bookmarks'] = bookmarks
    session.modified = True
    return {'msg': 'Materialet blev fjernet fra session'}


##########
# ORDERS #
##########
def get_orders():
    return session.get('orders', [])


def add_order(resource_id):
    orders = session.get('orders', [])
    orders.append(resource_id)
    session['orders'] = orders
    session.modified = True
    return {'msg': 'Materialet blev tilføjet i session'}


def remove_order(resource_id):
    orders = session.get('orders', [])
    orders.remove(resource_id)
    session['orders'] = orders
    session.modified = True
    return {'msg': 'Materialet blev fjernet fra session'}


############
# SEARCHES #
############
def get_searches():
    return session.get('searches', [])


# Not implemented yet ?
def add_search(url):
    searches = session.get('searches', [])
    searches.append(url)
    session['searches'] = searches
    session.modified = True
    return {'msg': 'Materialet blev tilføjet i session'}


# Not implemented yet ?
def remove_search(url):
    searches = session.get('searches', [])
    searches.remove(url)
    session['searches'] = searches
    session.modified = True
    return {'msg': 'Materialet blev fjernet fra session'}


# Current_url-methods
def get_current_url():
    return session.get('current_url', '/')


def set_current_url(request):
    if request.args:
        session['current_url'] = request.full_path
    else:
        session['current_url'] = request.path
    session.modified = True
    return True


# Latest_search-methods
def get_latest_search():
    return session.get('latest_search', '/search')


def set_latest_search(request):
    if request.full_path:
        session['latest_search'] = request.full_path
        session.modified = True
    return True
