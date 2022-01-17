class Recipe:

    def __init__():
        self.__rating = 0
        self.__ingredients = []
        self.__instructions = []
        self.__time_to_prepare = 0
        self.__serving_size = 0
        self.__servings = []
        self.url = ""
        self.sourceWebsite = ""

    def get_rating(self):
        return self.__rating

    def set_rating(self, rating):
        self.__rating = rating

    def add_ingredient(self, new_ingredient):
        self.__ingredients.append(new_ingredient)
        return True

    def remove_ingredient(self, ingredient):
        try:
            self.__ingredients.remove(ingredient)
            return True
        except:
            return False

    def get_prep_time(self):
        return self.__prep_time

    def set_prep_time(self, time):
        self.__prep_time = time

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
        self._servings = servings

class Ingredient:

    def __init__():
        self.__name = ""
        self.__quantity = 0
        self.__unit = ""

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

    def __init__():
        self.__query = []
        self.__recipes = []

    def fill_recipe_book(self, query):
        x = 1

    def sort_recipes(self):
        x = 1

    def filter_recipes(self):
        x = 1

    
        