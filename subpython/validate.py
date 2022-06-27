from functools import wraps
from flask import request, redirect, url_for
from flask import redirect, render_template, request, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def validate_field(string):
    """take a field ad validate it"""
    if not string:
        return False
    for i in string:
        if i == "_" or i.isdigit() or i.isalpha():
            continue
        else:
            return False
    return True

def validate_passwords(password1,password2):
    """validate multi input"""
    if not validate_field(password1):
        return False
    if not validate_field(password2):
        return False
    if password1 != password2:
        return False

    return True
