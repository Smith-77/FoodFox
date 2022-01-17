class Recipe:

    def __init__(self, name, ingredients, instructions, url):
        self.__name = name
        self.__author = "N/A"
        self.__rating = -1
        self.__ratings = -1
        self.__ingredients = []
        self.__instructions = []
        self.__time_to_prepare = -1
        self.__serving_size = 0
        self.__servings = -1
        self.url = url
        self.sourceWebsite = ""

    def __str__(self):
        rep = "%s   |  By %s\n\tRating: %f\tRatings: %d\n\tTotal Time: %d min\tServings: %d\n\turl: %s\n" % (self.__name, self.__author, self.__rating, self.__ratings, self.__time_to_prepare, self.__servings, self.url)
        return rep

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_author(self):
        return self.__author
        
    def set_author(self, author):
        self.__author = author

    def get_rating(self):
        return self.__rating

    def set_rating(self, rating):
        self.__rating = rating

    def get_ratings(self):
        return self.__ratings

    def set_ratings(self, ratings):
        self.__ratings = ratings

    def __add_ingredient(self, new_ingredient):
        if new_ingredient in self.__ingredients:
            return False
        self.__ingredients.append(new_ingredient)
        return True

    def add_ingredients(self, *args):
        added = 0
        for arg in args:
            print(arg)
            if self.__add_ingredient(arg):
                added = added + 1
        return added

    def __remove_ingredient(self, ingredient):
        try:
            self.__ingredients.remove(ingredient)
            return True
        except:
            return False

    def remove_ingredients(self, *args):
        removed = 0
        for arg in args:
            if self.__remove_ingredient(arg):
                removed = removed + 1
        return removed

    def clear_ingredients(self):
        self.__ingredients = []

    def get_ingredients(self):
        return self.__ingredients

    def get_prep_time(self):
        return self.__prep_time

    def set_prep_time(self, time):
        self.__time_to_prepare = time

    def get_serving_size(self):
        return self.__serving_size

    def set_serving_size(self, serving_size):
        if self.__serving_size == serving_size:
            return False
        self.__serving_size = serving_size
        return True

    def get_servings(self):
        return self.__servings

    def set_servings(self, servings):
        self.__servings = servings

class Ingredient:

    def __init__(self, name="no_name", quantity=0, unit=""):
        self.__name = name
        self.__quantity = quantity
        self.__unit = unit

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quanityt = quantity

    def get_unit(self):
        return self.__unit

    def set_unit(self, unit):
        self.__unit = unit

class RecipeBook:

    def __init__(self):
        self.__query = []
        self.__recipes = []

    def fill_recipe_book(self, query):
        x = 1

    def sort_recipes(self):
        x = 1

    def filter_recipes(self):
        x = 1
    
        