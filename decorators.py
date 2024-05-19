from flask import g, redirect, url_for
from functools import wraps

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            # If the user is logged in (g.user exists), proceed to the requested function
            # The *args is used to receive any number of positional parameters
            # The **kwargs is used to receive any number of keyword parameters
            return func(*args, **kwargs)
        else:
            # If the user is not logged in, redirect to the login page
            return redirect(url_for("auth.login"))
    return inner

    
  