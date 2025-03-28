import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///list.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show to-do list"""
    user_id = session["user_id"]
    tday = datetime.date.today()
    lists_db = db.execute("SELECT tasks, date FROM lists WHERE( user_id = ? AND date >= ?)", user_id, tday)
    for row in lists_db:
        row['remaining_days'] = (datetime.date.fromisoformat(row['date']) - tday).days
    return render_template("index.html", database=lists_db, len=len(lists_db))


@app.route("/append", methods=["GET", "POST"])
@login_required
def append():
    """Buy shares of stock"""

    if request.method == "POST":
        task = request.form.get("append")
        try:
            date = datetime.date.fromisoformat(request.form.get("date"))
        except ValueError:
            return apology("Must type date")
        tdate = datetime.date.today()
        #validation
        if not task:
            return apology("Must Give task")
        elif not date:
            return apology("Must type date")
        elif (date < tdate):
            return apology("must be future")
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM lists WHERE (user_id = ? AND tasks = ?)", user_id, task)
        if len(rows) != 0:
            return apology("The task is repeated")
        db.execute("INSERT INTO lists (user_id, tasks, date) VALUES (?, ?, ?)",user_id, task, date)


        flash("Appended!")

        return redirect("/")

    else:
        date_string = datetime.date.today().strftime("%Y-%m-%d")
        return render_template("append.html", date=date_string)


@app.route("/destroy", methods=["GET", "POST"])
@login_required
def destroy():
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid password", 403)
        db.execute("DELETE FROM lists WHERE user_id = ?", user_id)
        flash("Your TO-DO List is destroyed")
        return redirect("/")
    else:
        return render_template("destroy.html")



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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Logged In!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        task = request.form.get("change")
        date = datetime.date.fromisoformat(request.form.get("ndate"))
        tdate = datetime.date.today()
        #validation
        if not task:
            return apology("Must provide task")
        elif not date:
            return apology("Must type date")
        elif (date < tdate):
            return apology("must be future")
        user_id = session["user_id"]

        rows = db.execute("SELECT * FROM lists WHERE (user_id = ? AND tasks = ?)", user_id, task)
        if len(rows) != 1:
            return apology("The task doesn't exist.")
        db.execute("UPDATE lists SET date = ? WHERE (user_id = ? AND tasks = ?)", date, user_id, task)



        flash(f"the date of {task} is changed!")
        return redirect("/")

    else:
        date_string = datetime.date.today().strftime("%Y-%m-%d")
        return render_template("change.html", date=date_string)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        # check the submition
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match!", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("username is taken.", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/erase", methods=["GET", "POST"])
@login_required
def erase():
    if request.method == "POST":
        task = request.form.get("erase")
        #validation
        if not task:
            return apology("Must provide task")
        user_id = session["user_id"]

        rows = db.execute("SELECT * FROM lists WHERE (user_id = ? AND tasks = ?)", user_id, task)
        if len(rows) != 1:
            return apology("The task doesn't exist.")
        db.execute("DELETE FROM lists WHERE (user_id = ? AND tasks = ?)", user_id, task)
        flash(f"{task} is erased!")
        return redirect("/")

    else:
        return render_template("erase.html")
