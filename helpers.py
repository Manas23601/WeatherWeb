import os
import requests

from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(city_name):
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=76bd0de5ad7b82db506c1caf3e131d5e")
        quote = response.json()
    except Exception:
        return None
    try:
        if quote['cod'] == '404':
            return 1
        return quote
    except Exception:
        return None

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

