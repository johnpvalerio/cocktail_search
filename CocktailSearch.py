from resources.thecocktaildb import Cocktail, Api


def query(cocktail: Cocktail):
    pass


def search(cocktailDict: dict):
    cocktail = Cocktail(cocktailDict)
    api = Api('1')
    api.query(cocktail.getHint())
