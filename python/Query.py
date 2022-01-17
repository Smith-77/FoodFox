class Query:

    def __init__(self, source, search):
        self.__source_website = source.lower()
        search = search.replace(" ", "+")
        self.__search = search

    def get_source_website(self):
        return self.__source_website

    def get_search(self):
        return self.__search
