from functools import wraps

from flask import g, redirect, url_for


def login_required(func):
    @wraps (func)
    def inner(*args,**kwargs):
        if g.user:
            #The first is used to receive any number of positional parameters
            #and the second is used to receive any number of keyword parameters.
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner
        # @login_required
        # def public_question(quesiton_id):
        #   pass
        # login_required(public_question)(question_id)f
  