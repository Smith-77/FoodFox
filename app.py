from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
import Scraper as sc
import Query as qr
import Recipes as rp
from multiprocessing import Pool
import os
import sqlite3
from werkzeug.exceptions import abort

# globals
delimiting_string = "~*#*~"

''' Creates and returns database connection'''
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

''' Gets recipe for url from the database'''
def get_recipe(recipe_url, table_name):
    assert(table_name in ["recipes", "recipes_long"])
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM {} WHERE recipe_url = ?'.format(table_name),
                        (recipe_url,)).fetchone()
    conn.close()
    # if recipe is None:
    #     abort(404)
    return recipe

def convert_recipe(db_recipe):
    ingredients = db_recipe['ingredients'].split(delimiting_string)
    instructions = db_recipe['instructions'].split(delimiting_string)
    ingredients.pop()
    instructions.pop()
    recipe = rp.Recipe(db_recipe['title'], ingredients, instructions, db_recipe['recipe_url'])
    recipe.set_rating(db_recipe['rating'])
    recipe.set_ratings(db_recipe['ratings'])
    recipe.set_prep_time(db_recipe['time_in_minutes'])
    recipe.set_string_time(db_recipe['string_time'])
    recipe.set_author(db_recipe['author'])
    recipe.source_website = db_recipe['source_url']
    return recipe

''' Gets recipe for url from the database'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '333'

websites=["allrecipes.com"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=('GET', 'POST'))
def search_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        website = request.form['website']

        if not recipe_name:
            flash('A recipe name is required!')
        elif not website:
            flash('A website is required!')
        else:
            '''
            result = []
            with Pool(processes=os.cpu_count() - 1) as pool:
                result = pool.apply_async(__hunt_for_recipes, (website, recipe_name))
            '''
            
            #return redirect(url_for('hunting'))
            __clear_table("recipes")
            __hunt_for_recipes(website, recipe_name)
            return redirect(url_for('results'))

    return render_template('search.html', websites = websites)

def __clear_table(table_name):
    assert(table_name in ["recipes", "recipes_long"])
    conn = get_db_connection()
    conn.execute("DELETE FROM {}".format(table_name))
    conn.commit()
    conn.close()

def __hunt_for_recipes(website, recipe_name):
    print("hunting for %s recipes from %s" % (recipe_name, website))
    scraper = sc.Scraper(website, recipe_name)
    links = scraper.get_links()
    recipes = []
    for link in links:
        # Look for recipe in long-term recipe table
        recipe = None
        try:
            recipe = get_recipe(link, "recipes_long")
        except (Exception):
            pass

        # TODO: Update if it's out of date
        
        if not recipe: # Add to long-term storage if it's not there
            recipe = scraper.scrape_recipe(link)
            __add_recipe_to_table(recipe, "recipes_long")
            __add_recipe_to_table(recipe, "recipes")
        else: # Add to current recipe table
            __add_recipe_row_to_table(recipe, "recipes")

def __add_recipe_to_table(recipe, table_name):
    assert(table_name in ["recipes", "recipes_long"])
    conn = get_db_connection()
    try:
        ingredients = ""
        for ingredient in recipe.get_ingredients():
            ingredients = ingredients + ingredient + delimiting_string
        instructions = ""
        for instruction in recipe.get_instructions():
            instructions = instructions + instruction + delimiting_string
        conn.execute("INSERT INTO {} (recipe_url, source_url, title, rating, star_rating, ratings, author, ingredients, number_of_ingredients, instructions, time_in_minutes, string_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name), 
                    (recipe.url, recipe.source_website, recipe.get_name(), recipe.get_rating(), recipe.get_star_rating(), recipe.get_ratings(), recipe.get_author(), ingredients, recipe.get_number_of_ingredients(), instructions, recipe.get_prep_time(), recipe.get_string_time()))
        conn.commit()
    except (sqlite3.IntegrityError):
        pass
    conn.close()

def __add_recipe_row_to_table(recipe, table_name):
    assert(table_name in ["recipes", "recipes_long"])
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO {} (recipe_url, source_url, title, rating, star_rating, ratings, author, ingredients, number_of_ingredients, instructions, time_in_minutes, string_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name),
                    (recipe['recipe_url'], recipe['source_url'], recipe['title'], recipe['rating'], recipe['star_rating'], recipe['ratings'], recipe['author'], recipe['ingredients'], recipe['number_of_ingredients'], recipe['instructions'], recipe['time_in_minutes'], recipe['string_time']))
        conn.commit()
    except (sqlite3.IntegrityError):
        pass
    conn.close()


@app.route('/results', methods=('GET', 'POST'))
def results():
    db_recipes = []
    if request.method == 'POST':
        print("results")
        min_rating =  request.form.get('min_rating', "0")
        min_ratings =  request.form.get('min_ratings', "0")
        max_minutes =  request.form.get('max_minutes', "100000")
        max_ingredients = request.form.get('max_ingredients', "100000")

        # Fix empty values
        if len(min_rating) <= 0 or min_rating == None:
            min_rating = 0
        else:
            min_rating = float(min_rating)
        if len(min_ratings) <= 0 or min_ratings == None:
            min_ratings = 0
        else:
            min_ratings = int(min_ratings)
        print(type(min_ratings))
        if len(max_minutes) <= 0 or max_minutes == None:
            max_minutes = 100000
        else:
            max_minutes = int(max_minutes)
        if len(max_ingredients) <= 0 or max_ingredients == None:
            max_ingredients = 100000
        else:
            max_ingredients = int(max_ingredients)

        conn = get_db_connection()
        db_recipes = conn.execute("SELECT * FROM recipes WHERE rating >= ? AND ratings >= ? AND time_in_minutes <= ? AND number_of_ingredients <= ?", (min_rating/5, min_ratings, max_minutes, max_ingredients)).fetchall()
        conn.close()
    else:
        conn = get_db_connection()
        db_recipes = conn.execute("SELECT * FROM recipes").fetchall()
        conn.close()

    # Convert database rows to Recipe objects for easier manipulation of ingredients and instructions
    recipes = []
    for db_recipe in db_recipes:
        recipes.append(convert_recipe(db_recipe))
    
    return render_template('results.html', recipes=recipes)

@app.route('/hunting')
def hunting():
    return render_template('hunting.html')