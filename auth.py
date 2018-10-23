# -*- coding: utf-8 -*-

# Standard library
from functools import wraps

# Third party libraries
from flask import session
from flask import redirect

# Session-key-name which stores the third-oarty user-info
SESSION_KEY = 'profile'


# Base-authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if SESSION_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


def employee_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if SESSION_KEY not in session:
            return redirect('/login')
        elif 'employee' not in session[SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated


# Use only with all three of my logins
def tester_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if SESSION_KEY not in session:
            return redirect('/login')
        elif 'tester' not in session[SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated


# Admin-authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if SESSION_KEY not in session:
            return redirect('/login')
        elif 'admin' not in session[SESSION_KEY].get('roles', ['user']):
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return decorated
