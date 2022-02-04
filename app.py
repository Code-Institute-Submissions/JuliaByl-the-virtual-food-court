import os
from flask import (
    Flask, render_template, redirect, 
    request, session, url_for, flash
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

# global variables
mongo = PyMongo(app)
ingredients_amount = []
how_to = []


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


# search recipes
@app.route("/search_recipe", methods=["GET", "POST"])
def search_recipe():
    category_select = request.form.get("category_select")
    ingredient_search = request.form.get("ingredient_search") 
    user_id = mongo.db.users.find_one({"username": session["user"]})["_id"]
    
    # loop creating different search options depending on what has been populated
    if category_select == "all-types":
        if ingredient_search:
        # if all food types are selected and the text input is populated, search for the specific word
            recipe_search = list(mongo.db.recipes.find({"$text": {"$search": ingredient_search}}))
        else:
        #search for everything if nothing is specified in the search
            recipe_search = mongo.db.recipes.find()   
    elif category_select == "my_recipes":
        #search for user specific recipes and text search
        if ingredient_search:
            recipe_search = list(mongo.db.recipes.find(
                {"$and": [
                    {"user_id": user_id},
                    {"$text": {"$search": ingredient_search}}
                ]}
            ))
        # search only for user-specific recipes
        else:
            recipe_search = list(mongo.db.recipes.find({"user_id": user_id}))
    else:
        if ingredient_search:
        # if both dropdown and input area are populated, search for both 
            recipe_search = list(mongo.db.recipes.find(
                {"$and": [
                    {"food_category": category_select},
                    {"$text": {"$search": ingredient_search}}
                ]}
            ))
        else:
        # if only a food category is selected, search by that
            recipe_search = list(mongo.db.recipes.find({"food_category": category_select})) 

    return render_template("browse-recipes.html", recipes=recipe_search) 


# view recipe
@app.route("/view-recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view-recipe.html", recipe=recipe)


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO: change the redirect to an 403 error page 
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Name already taken!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }   
        mongo.db.users.insert_one(register)     

        session["user"] = request.form.get("username").lower() 
        flash("Successfully Registered!")

    return render_template("register.html")


# log in
@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: change the redirect to an 403 error page 
    if "user" in session:
        return redirect(url_for("home"))
        
    if request.method == "POST":
        # if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:  
            # correct passord
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("home"))
            # incorrect password
            else:
                flash("Incorrect password or username, try again!")
                return redirect(url_for("login"))
        # if username doesn't exist
        else:
            flash("Incorrect password or username, try again!")
            return redirect(url_for("login"))        

    return render_template("login.html")    


# log out
@app.route("/logout")
def logout():
    # TODO: change the redirect to an 403 error page 
    if "user" in session:

        session.pop("user")
        flash("See you later!")
        return redirect(url_for("login"))
        
    return redirect(url_for("home"))        


# delete account TODO: add an 'are you sure' popup before deleting account
@app.route("/delete_account")
def delete_account():
    # TODO: change the redirect to an 403 error page 
    if "user" in session:

        user_id = mongo.db.users.find_one({"username": session["user"]})["_id"]
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        session.pop("user")
        flash("Sad to see you go, you can regster with us again at any time!!")
        return redirect(url_for("register"))

    return redirect(url_for("home"))    


# create recipe
@app.route("/create-recipe", methods=["GET", "POST"])
def create_recipe():
    # TODO: change the redirect to an 403 error page 
    if "user" in session:
        if request.method == "POST":   
            recipes = {
                "user_id": mongo.db.users.find_one(
                    {"username": session["user"]})["_id"],
                "title": request.form.get("title"),
                "time_required": request.form.get("time_required"),
                "ingredients_amount": ingredients_amount,
                "portions_amount": request.form.get("portions_amount"),
                "food_category": request.form.get("food_category"),
                "how_to": how_to
            }
            mongo.db.recipes.insert_one(recipes)
            flash("Recipe has been created!")
        
        ingredients_amount.clear()
        how_to.clear()
        return render_template("create-recipe.html")

    return redirect(url_for("home"))


# reloads the create_recipe page without deleting potential input values
def reload_create_recipe():
    title = request.form.get("title")
    time_required = request.form.get("time_required")
    portions_amount = request.form.get("portions_amount")
    food_category = request.form.get("food_category")

    return render_template("create-recipe.html",
        ingredients_amount=ingredients_amount, how_to=how_to, title=title,
        time_required=time_required, portions_amount=portions_amount,
        food_category=food_category)


# generate ingredients inside the create recipe form and in an array
@app.route("/ingredient_input", methods=["GET", "POST"]) 
def ingredient_input():
    if request.method == "POST":
        ingredient = request.form.get("ingredients_amount")
        ingredients_amount.append(ingredient)

    return reload_create_recipe()


# delete a specific list item in the ingredients - section
@app.route("/delete_ingredient/<index>", methods=["GET", "POST"])  
def delete_ingredient(index):
    if request.method == "POST":
        ingredients_amount.pop(int(index))
    
    return reload_create_recipe()


# generate how_to sections inside the create recipe form and in an array
@app.route("/steps_input", methods=["GET", "POST"])    
def steps_input():
    if request.method == "POST":
        section = request.form.get("how_to")
        how_to.append(section)

    return reload_create_recipe()

# delete a specific list item in the how_to - section
@app.route("/delete_section/<index>", methods=["GET", "POST"]) 
def delete_section(index):
    if request.method == "POST":
        how_to.pop(int(index))
    
    return reload_create_recipe()  


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
