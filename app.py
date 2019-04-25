import os
import pymongo
from flask import Flask,redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipies_test'
app.config["MONGO_URI"] = 'mongodb+srv://first:27AshleySwords@cluster0-hkaqa.mongodb.net/recipes?retryWrites=true'
mongo = PyMongo(app)
mongo = PyMongo(app)


# ********************************************************************** Homepage route
@app.route('/')
def home_page():
    return render_template("home.html", categries = mongo.db.category.find())
#**********************************************************************    Recipes 


# ***********************************************************************  Get all recipes
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html",
                           recipes=mongo.db.recipe.find())
# ***********************************************************************  Home page                        

    

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', cuisines=mongo.db.cuisine.find(), alergens = mongo.db.alergen.find(),
    meal_types=mongo.db.meal_type.find(), categries = mongo.db.category.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipe
    
    recipe_form={
        "category_name": request.form['category_name'],
        "title": request.form['title'],
        "description": request.form['description'],
        "method": request.form['method'],
        "ingredients": request.form.getlist('ingredients'),
        "meal_type": request.form.getlist('meal_type'),
        "serves":   request.form['serves'],
        "cooking_time": request.form['cooking_time'],
        "preparation_time": request.form['preparation_time'],
        "cuisine_name": request.form['cuisine_name'],
        "alergen_name": request.form.getlist('alergen_name'),
    }
    
    if request.form['picture']:
        recipe_form['picture'] = request.form['picture']
    elif request.form['category_name'] == 'Breakfast':
        recipe_form['picture'] = '/static/img/breakfast.jpg'
    elif request.form['category_name'] == 'Lunch':
        recipe_form['picture'] = '/static/img/lunch.jpg'
    elif request.form['category_name'] == 'Brunch':
        recipe_form['picture'] = '/static/img/brunch.jpg'
    elif request.form['category_name'] == 'Dinner':
        recipe_form['picture'] = '/static/img/dinner.jpg'
    elif request.form['category_name'] == 'Dessert':
        recipe_form['picture'] = '/static/img/dessert.jpg'
    elif request.form['category_name'] == 'Snack':
        recipe_form['picture'] = '/static/img/snack.jpg'
    
    recipes.insert_one(recipe_form)
    return redirect(url_for('get_recipes'))


@app.route('/recipe_single/<recipe_id>')
def recipe_single(recipe_id):
    recipe = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe_page.html", recipe=recipe)
    
                           
#********************************************************************** Cuisine                          
@app.route('/get_cuisine')
def get_cuisine():
    return render_template("cuisine.html",
                           cuisine=mongo.db.cuisine.find())
                           
@app.route('/cuisine_single/<cuisine_name>')
def cuisine_single(cuisine_name):
    recipes= mongo.db.recipe.find({'cuisine_name': cuisine_name})
    return render_template("cuisine_single.html", recipes=recipes)   
    
#********************************************************************** Category        
@app.route('/category_single/<category_name>')
def category_single(category_name):
    recipes= mongo.db.recipe.find({'category_name': category_name})
    
    return render_template("category_single.html", recipes=recipes)  
    
    
#********************************************************************** Alergen                          
@app.route('/get_alergen')
def get_alergen():
    return render_template("alergen.html",
                           alergen=mongo.db.alergen.find())
                           
@app.route('/alergen_single/<alergen_name>')
def alergen_single(alergen_name):
    recipes= mongo.db.recipe.find({'alergen_name':{"$not": { "$regex": alergen_name}}})
    return render_template("alergen_single.html", recipes=recipes)   
    
#********************************************************************** Restrictions                       
@app.route('/get_meal_type')
def get_meal_type():
    return render_template("restrictions.html",
                           meal_type=mongo.db.meal_type.find())
                           
@app.route('/meal_type_single/<meal_type_name>')
def meal_type_single(meal_type_name):
    recipes= mongo.db.recipe.find({'meal_type_name': meal_type_name})
    return render_template("restrictions_single.html", recipes=recipes)   
    
    
#********************************************************************** Update


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editrecipe.html', cuisines=mongo.db.cuisine.find(), alergens = mongo.db.alergen.find(),
    meal_types=mongo.db.meal_type.find(), categries = mongo.db.category.find(), recipe=recipe) 
                           

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipe
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "title": request.form.get('title'),
        "description": request.form.get('description'),
        "method": request.form.get('method'),
        "ingredients": request.form.getlist('ingredients'),
        "meal_type": request.form.getlist('meal_type'),
        "serves":   request.form.get('serves'),
        "cooking_time": request.form.get('cooking_time'),
        "preparation_time": request.form.get('preparation_time'),
        "cuisine_name": request.form.get('cuisine_name'),
        "alergen_name": request.form.getlist('alergen_name'),
    })
    return redirect(url_for('get_recipes'))

#********************************************************************** Delete
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True )
    
