from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# if in models folder, no need to add .name_of_model before import 
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data["id"]

        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made_on = data["date_made_on"]
        self.under_30_minutes = data["under_30_minutes"]
        self.user_id = data["user_id"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# placeholder of empty user for get all_recipes query
        self.user = {}

# user_id is not needed to be validated as it should be in session already
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if data["name"] == "":
            flash("Please enter the name of your recipe!")
            is_valid = False    
        elif len(data["name"]) < 3:
            flash("Recipe name must be at least 3 characters long!")
            is_valid = False
        if data["description"] == "":
            flash("Please enter the description of your recipe!")
            is_valid = False    
        elif len(data["description"]) < 3:
            flash("Recipe description must be at least 3 characters long!")
            is_valid = False
        if data["instructions"] == "":
            flash("Please enter the instructions for your recipe!")
            is_valid = False    
        elif len(data["instructions"]) < 3:
            flash("Recipe instructions must be at least 3 characters long!")
            is_valid = False
        if data['date_made_on'] == '':
            flash("Please provide date")
            is_valid = False

        return is_valid
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_30_minutes, user_id, created_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_30_minutes)s, %(user_id)s, NOW());"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return results

# left join on the line that connects the 1 to many relationship in the erd
# recipe tables -> user_id + users table -> id = recipes.user_id = users.id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL("recipes_schema").query_db(query)

        # time to parse
        # any overlapping fields with the 2nd model needs to be specified via ____.created_at, etc
        all_recipes = []
        for row in results: 
            recipe = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
# if in models folder - must reference the model name then class name
# if in controllers folder - can reference just the class name
            recipe.user = user.User(user_data)
            all_recipes.append(recipe)

        return all_recipes
    
    @classmethod
    def get_recipe_with_user(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)

        recipe = cls(results[0])

        user_data = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }
        recipe.user = user.User(user_data)
        return recipe

    @classmethod
    def update_recipe_info(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s, under_30_minutes = %(under_30_minutes)s, updated_at = NOW() WHERE id = %(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return
        # update queries return nothing unless updated in site. no need to include a return here

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return