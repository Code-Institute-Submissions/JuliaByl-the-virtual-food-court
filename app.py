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


# home page
@app.route("/")
def home():
    return render_template("home.html")


# browse recipes
@app.route("/browse-recipes")
def browse_recipes():
    return render_template("browse-recipes.html")    


# view recipe
@app.route("/view-recipe")
def view_recipe():
    return render_template("view-recipe.html")


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
            