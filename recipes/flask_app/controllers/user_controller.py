from flask_app import app
from flask import render_template, redirect, request, session, flash

#controllers file always has upper case model name
from flask_app.models.user import User 
from flask_app.models.recipe import Recipe


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

# =================================================
# Register / Login Routes
# =================================================

@app.route("/register", methods=["POST"])
def register():
    # 1 - validating form information
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }

    if not User.validate_register(data):
        return redirect("/")

    # 2 - bcrypt password
    data["password"] = bcrypt.generate_password_hash(request.form['password'])

    # 3 - save new user to db
    new_user_id = User.create_user(data)
    # 4 - enter user id into session and redirect to dashboard
    session["user_id"] = new_user_id
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    # 1 - validate login info
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.validate_login(data):
        return redirect("/")
    # 2 - query for user info based on email
    user = User.get_by_email(data)

    # 3 - put user id into session and redirect to dashboard
    session["user_id"] = user.id
    return redirect("/dashboard")

    # =================================================
# Render Dashboard Route - this route will reference both models
# =================================================

# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session:
#         flash("Please login or register before entering the site!")
#         return redirect("/")

#     data = {
#         "user_id" : session["user_id"]
#     }
#     user = User.get_by_id(data)
#     all_recipes = Recipe.get_all()

#     return render_template("dashboard.html", user = user, all_recipes = all_recipes)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(data)
    all_recipes = Recipe.get_all()

    return render_template("dashboard.html", user = user, all_recipes = all_recipes)


# =================================================
# Logout Route
# =================================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect("/")