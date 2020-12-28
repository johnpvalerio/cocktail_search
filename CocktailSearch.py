import datetime
import json

from resources.thecocktaildb import Cocktail, Api


def removeNone(drink):
    for key, val in list(drink.items()):
        if val is None:
            del drink[key]


def display(cocktails):
    output = {}
    drinks = []
    for drink in cocktails:
        entry = {'id': drink.id,
                 'name': drink.getNames(),
                 'nameAlt': drink.nameAlt,
                 'category': drink.category,
                 'iba': drink.iba,
                 'tags': drink.tags,
                 'alcoholic': drink.getIsAlcoholic(),
                 'glass': drink.glass,
                 'instructions': drink.getInstructions(),
                 'thumb': drink.thumb,
                 'recipe': drink.getRecipes(),
                 'imgAttr': drink.imgAttr,
                 'video': drink.video,
                 'imgSrc': drink.imgSrc,
                 'creativeCommonsConfirmed': drink.getIsCreativeCC(),
                 'dateModified': drink.getDate()
                 }

        removeNone(entry)
        drinks.append(entry)
    print(entry)
    output['drinks'] = drinks
    print(json.dumps(output, indent=4))
    pass


def search(drink: dict):
    cocktail = Cocktail(drink)
    api = Api('1')
    x = api.query(cocktail.getHint())
    x = [Cocktail(c) for c in x]
    print(x)
    display(x)
