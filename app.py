import os
from flask import (
    Flask, render_template, redirect, 
    request, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# home page
@app.route("/")
def home():
    recipes = mongo.db.recipes.find()
    return render_template("home.html", recipes=recipes)


# browse recipes
@app.route("/browse-recipes")
def browse_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("browse-recipes.html", recipes=recipes)     


# view recipe
@app.route("/view-recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view-recipe.html", recipe=recipe)


# register
@app.route("/register")
def register():
    return render_template("register.html")


# log in
@app.route("/login")
def login():
    return render_template("login.html")      


# create recipe
@app.route("/create-recipe")
def create_recipe():
    return render_template("create-recipe.html")   
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            