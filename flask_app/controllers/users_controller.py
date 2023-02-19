from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.users_model import User

# index page with login and registration
@app.route("/")
def index():
    return render_template("index.html")


# form submission to register a new user
@app.route("/register", methods=["POST"])
def register_user():

    # run validation for a new user and if it fails
    # then redirect to "/"
    if not User.validate_new(request.form):
        return redirect("/")
    
    session["user_id"] = User.create(request.form)
    return redirect("/dashboard")


# form submission to login a user
@app.route("/login", methods=["POST"])
def login():

    # validate the login request and save the result
    logged_in_user = User.validate_login(request.form)

    # if the user is not logged in redirect to "/"
    if not logged_in_user:
        return redirect("/")

    # if the user is logged in then save their id in session
    session["user_id"] = logged_in_user.id
    return redirect("/dashboard")

# route to show to dashboard if a user is logged in
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    user = User.get_one({"id": session["user_id"]})
    return render_template("dashboard.html", user = user)

# route to log out and clear session
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")