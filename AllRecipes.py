import requests as rq
import Recipes as rp
import Query as q
from bs4 import BeautifulSoup

def get_links(url):
    page = rq.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    link_tags = soup.find_all('a', class_='card__titleLink')
    links = []
    for link in link_tags:
        try:
            if not link.get('href') in links:
                links.append(link.get('href'))
        except (Exception):
            pass
    return links

def scrape_recipe(link):
    page = rq.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Extract Recipe Title
    title = soup.find('h1', class_="headline").get_text()

    # Extract Recipe Ingredients
    ingredients_section = soup.find('ul', class_="ingredients-section")
    ingredient_tags = ingredients_section.find_all('span', class_="ingredients-item-name")
    ingredients = []
    for tag in ingredient_tags:
        ingredients.append(tag.get_text())
    
    # Extract Recipe Instructions
    instructions_section = soup.find('ul', class_="instructions-section")
    instruction_tags = instructions_section.find_all('div', class_="paragraph")
    instructions = []
    for tag in instruction_tags:
        instructions.append(tag.get_text())

    # Create the recipe
    recipe = rp.Recipe(title, ingredients, instructions, link)
        
    # Extract Recipe Time and Servings - neither required
    string_time = "N/A"
    total_time = -1
    servings = -1
    try:
        info_section = soup.find('section', class_="recipe-meta-container")
        tags = info_section.find_all('div', class_="two-subcol-content-wrapper")

        time_tag = tags[0]
        servings_tag = tags[1]
        
        try:
            tags = zip(time_tag.find_all('div', class_="recipe-meta-item-header"), time_tag.find_all('div', class_="recipe-meta-item-body"))
            for tag in tags:
                if tag[0].get_text().lower() == 'total:':
                    string_time = tag[1].get_text()
                    time = string_time.split()
                    total_time = 0
                    for i in range(len(time)):
                        if time[i] == 'hrs' or time[i] == 'hr':
                            total_time = total_time + int(time[i - 1]) * 60
                        elif time[i] == 'mins' or time[i] == 'min':
                            total_time = total_time + int(time[i - 1])
            recipe.set_prep_time(total_time)
            if string_time == "":
                string_time = "N/A"
            recipe.set_string_time(string_time)
        except (Exception):
            pass
        
        try:
            tags = zip(servings_tag.find_all('div', class_="recipe-meta-item-header"), servings_tag.find_all('div', class_="recipe-meta-item-body"))
            for tag in tags:
                if tag[0].get_text().lower() == 'servings:':
                    servings = int(tag[1].get_text())
            recipe.set_servings(servings)
        except (Exception):
            pass
        
    except (Exception):
        pass
    
    # Extract Recipe Rating - not required
    rating = -1
    ratings = -1
    try:
        review_tag = soup.find('div', class_="recipe-review-container")
        
        try:
            star_text = review_tag.find('span', class_="review-star-text").get_text()
            star_text = star_text.split()
            for i in range(len(star_text)):
                if star_text[i].lower() == 'rating:':
                    rating = float(star_text[i + 1]) / 5.0
            recipe.set_rating(rating)
        except (Exception):
            pass
            
        try:
            ratings = review_tag.find('span', class_="ugc-ratings-item").get_text()
            ratings = int(ratings.replace(',','').split()[0])
            recipe.set_ratings(ratings)
        except (Exception):
            pass
        
    except (Exception):
        pass

    # Extract Recipe Author - Not Necessary
    try:
        author = soup.find('span', class_="author-name").get_text()
        recipe.set_author(author)
    except (Exception):
        pass

    recipe.source_website = "allrecipes.com"

    return recipe
    