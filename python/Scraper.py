import AllRecipes
import Query as q
import requests as rq
from bs4 import BeautifulSoup as bsp

class Scraper:

    def __init__(self, website, recipe_name):
        self.__query = q.Query(website, recipe_name)
        self.__answer = self.__search(self.__query)
        
    def get_answer(self):
        return self.__answer

    def __search(self, query):
        source_website = query.get_source_website()
        if source_website.lower() == "allrecipes.com":
            return AllRecipes.search_all_recipes(query)
        else:
            print("Unable to search query for source website: %s" % (source_website))

    def __search_all_recipes(self, query):
        search_url = "https://www.allrecipes.com/search/results/?search=" + query.get_search()
        search_page = rq.get(search_url)
        
query1 = q.Query("allrecipes.com", "cool banana bread")
scraper1 = Scraper(query1)
answer1 = scraper1.get_answer()
for answer in answer1:
    print(answer)
    
    