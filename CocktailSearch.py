import datetime
import json

from resources.thecocktaildb import Cocktail, Api


def outputJSON(drinkDict):
    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d-%H%M%S")
    with open('output/output-'+date+ '.json', 'w') as f:
        json.dump(drinkDict, f, indent=4)
    return


def removeNone(drink):
    for key, val in list(drink.items()):
        if val is None:
            del drink[key]


def cocktailDictFormat(cocktails):
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
                 'thumbnail': drink.thumb,
                 'recipe': drink.getRecipes(),
                 'imageAttribution': drink.imgAttr,
                 'video': drink.video,
                 'imageSource': drink.imgSrc,
                 'creativeCommonsConfirmed': drink.getIsCreativeCC(),
                 'dateModified': drink.getDate()
                 }
        removeNone(entry)
        drinks.append(entry)
    output['drinks'] = drinks
    print(json.dumps(output, indent=4))
    return output


def search(drink: dict, key: str):
    cocktail = Cocktail(drink)
    api = Api(key)
    cocktailQueries = api.query(cocktail.getHint())
    cocktailList = [Cocktail(c) for c in cocktailQueries]
    drinks = cocktailDictFormat(cocktailList)
    outputJSON(drinks)
