from functools import wraps # Import 'wraps' from 'functools' to maintain metadata of decorated functions.

from flask import g, redirect, url_for # Import Flask utilities for handling user session and redirecting.


def login_required(func):
    """
    A decorator to enforce user login for certain routes.
    
    If a user is not logged in, redirects to the login page.
    """

    @wraps (func) # Preserve the metadata of the original function being decorated.
    def inner(*args,**kwargs):
        """
        The wrapper function to check user authentication before proceeding.
        
        Args:
            *args: Arbitrary positional arguments passed to the decorated function.
            **kwargs: Arbitrary keyword arguments passed to the decorated function.
        
        Returns:
            Redirect to 'auth.login' route if user is not authenticated. Otherwise,
            proceeds to call the decorated function with passed arguments.
        """

        if g.user:
            # If 'g.user' is set (indicating a logged-in user), proceed to call the original function.
            return func(*args, **kwargs)
        else:
            # If 'g.user' is not set (indicating a user is not logged in), redirect to the login page.
            return redirect(url_for("auth.login"))
    return inner
      # Example usage:
      # @login_required
      # def public_question(question_id):
      #   pass
      # This decorates 'public_question' to require a login, redirecting to login page if no user is logged in.
