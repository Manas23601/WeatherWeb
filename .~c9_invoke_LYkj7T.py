import os
import math
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import  login_required, lookup, apology
import requests
# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///data.db")



@app.route("/register", methods=["GET", "POST"])
def register():
    # directed from an another page
    if request.method == "GET":
        return render_template("register.html")

    else:
        # get username from form
        username = request.form.get("username")

        # get password from form
        password = request.form.get("password")

        # get password from form again
        re_password = request.form.get("re_password")

        #if no username is input
        if not username:
           return apology("You should enter a name", 403)

        #if no password is input
        elif not password:
            return apology("You should enter a password", 403)

        #if no password is input again
        elif not re_password:
            return apology("You should enter the password again", 403)

        # if input passwords dont match
        if password != re_password:
            return apology("Passwords don't match", 403)

        #generate hash for the password
        password_hash = generate_password_hash(password)

        #store hash_value of the password
        db.execute("INSERT INTO users (id,hash) VALUES (:id, :hash)",id=username,hash=password_hash)
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/" , methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("lol.html",message="Welcome")

    else:
        city_name = request.form.get("city")
        if city_name == "":
            return render_template("lol.html",message="No such City exists")
        details = lookup(city_name)
        if details == 1:
            return render_template("lol.html",message="No such City exists")
        latitude = details["coord"]["lat"]
        longitude =details["coord"]["lon"]
        icon_id=details["weather"][0]["icon"]
        temp=math.floor(details["main"]["temp"]-273.16)
        temp_min = math.floor(details["main"]["temp_min"]-273.16)
        temp_max=math.floor(details["main"]["temp_max"]-273.16)
        pressure=details["main"]["pressure"]
        humidity=details["main"]["humidity"]
        speed=details["wind"]["speed"]
        deg=details["wind"]["deg"]
        description=details["weather"][0]["description"]
        country=details["sys"]["country"]
        name=details["name"]
        return render_template("forecast.html",latitude=latitude,longitude=longitude,icon_id=icon_id,temp=temp,temp_min=temp_min,temp_max=temp_max,pressure=pressure,humidity=humidity,speed=speed,deg=deg,description=description,country=country,name=name)

@app.route("/change_password" , methods=["GET", "POST"])
@login_required
def change_password():

    #redirected from an another page
    if request.method=="GET":
        return render_template("change_password.html")

    else:
        #get old password of the user from users table
        orginal_password_hash=db.execute("SELECT hash FROM users WHERE id=:user_id",user_id=session["user_id"])

        #get old_password entered by user
        old_password = request.form.get("old_password")

        #get new_password entered by user
        new_password = request.form.get("new_password")

        #get new_password_again entered by user
        new_re_password = request.form.get("new_re_password")

        #check if new password and new_password_re match
        if new_re_password != new_password:
            return apology("passwords should match", 403)

        #check if old_password is not empty
        elif not old_password:
            return apology("you must enter your old password", 403)

        #check if new_password is not empty
        elif not new_password:
            return apology("you must enter your new password", 403)

        #check new_re_password is not empty
        elif not new_re_password:
            return apology("you must enter your new password(again)", 403)

        #verify if user has input the right old_password
        elif not  check_password_hash(orginal_password_hash[0]["hash"],old_password):
            return apology("old password does not match", 403)

        #update hash value of the user
        else:
            db.execute("UPDATE users SET hash=:hash WHERE id=:user_id",hash=generate_password_hash(new_password),user_id=session["user_id"])
            return redirect("/")

