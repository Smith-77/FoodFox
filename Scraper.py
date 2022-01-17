import AllRecipes
import Query as q
import requests as rq
from bs4 import BeautifulSoup as bsp

class Scraper:

    def __init__(self, website, search):
        self.__query = q.Query(website, search)
        self.__links = self.get_links()
        self.__recipes = []
        
    def get_answer(self):
        return self.__answer

    def get_links(self):
        source_website = self.__query.get_source_website()
        if source_website.lower() == "allrecipes.com":
            search_url = "https://www.allrecipes.com/search/results/?search=" + self.__query.get_search()
            return AllRecipes.get_links(search_url)
        else:
            print("Unable to search query for source website: %s" % (source_website))

    def scrape_recipe(self, link):
        source_website = self.__query.get_source_website()
        if source_website.lower() == "allrecipes.com":
            return AllRecipes.scrape_recipe(link)
        else:
            print("Unable to search query for source website: %s" % (source_website))
        
'''
query1 = q.Query("allrecipes.com", "cool banana bread")
scraper1 = Scraper(query1)
answer1 = scraper1.get_answer()
for answer in answer1:
    print(answer)
'''
    
    