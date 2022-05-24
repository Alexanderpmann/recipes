from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.recipe import Recipe
from flask_app.models.user import User

# =================================================
# Create Recipe Routes
# =================================================

@app.route("/new_recipe")
def new_recipe():
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    return render_template("new_recipe.html", user_id = session["user_id"])

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    # 1 - validate form data
    # if no hidden input on form w/user_id -> "user_id" : session["user_id"] instead
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made_on" : request.form["date_made_on"],
        "under_30_minutes" : request.form["under_30_minutes"],
        "user_id" : request.form["user_id"]
    }

    if not Recipe.validate_recipe(data):
        return redirect("/new_recipe")
    # 2 - save new recipe to database
    Recipe.create_recipe(data)

    # 3 - redirect back to the dashboard page
    return redirect("/dashboard")

# =================================================
# Show One Recipe Route
# =================================================

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    # 1 - query for recipe info w/associated info of user
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_recipe_with_user(data)

    # 2 - send info to show page

    return render_template("show_recipe.html", recipe = recipe)

# =================================================
# Edit One Recipe Route
# =================================================

@app.route("/recipe/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    # 1 - query for the recipe we want to update
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_recipe_with_user(data)
    # 2 - pass recipe info to the html
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/recipe/<int:recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id):
    # 1 - validate our form data
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made_on" : request.form["date_made_on"],
        "under_30_minutes" : request.form["under_30_minutes"],
        "recipe_id" : recipe_id
    }

    if not Recipe.validate_recipe(data):
        return redirect(f"/recipe/{recipe_id}/edit")
    # 2 - update information    
    Recipe.update_recipe_info(data)
    # 3 - redirect to dashboard

    return redirect("/dashboard")

# =================================================
# Delete One Recipe Route
# =================================================

@app.route("/recipe/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    # 1 - delete recipe
    data = {
        "recipe_id" : recipe_id
    }
    Recipe.delete_recipe(data)

    # 2 - redirect to dashboard
    return redirect("/dashboard")