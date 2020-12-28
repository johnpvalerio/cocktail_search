import datetime
import json

from resources.thecocktaildb import Cocktail, Api


def removeNone(drink):
    for key, val in list(drink.items()):
        if val is None:
            del drink[key]


def getIsCreativeCC(drink):
    creativeCC = drink['strCreativeCommonsConfirmed']
    if not creativeCC:
        return
    return True if creativeCC == 'Yes' else False


def getIsAlcoholic(drink):
    alc = drink['strAlcoholic']
    if not alc:
        return
    return True if alc in ['Alcoholic', 'Optional alcohol'] else False


def getDate(drink):
    # todo: might be match good output, check conversion
    date = drink['dateModified']
    print(date)
    if not date:
        return
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    print(date.isoformat())
    print(date)
    return date.isoformat()


def getNames(drink):
    output = {}
    languages = ['', 'ES', 'DE', 'FR', 'ZH-HANS', 'ZH-HANT']
    for _l in languages:
        if drink['strDrink' + _l] is None:
            continue
        if _l == '':
            output['en'] = drink['strDrink' + _l]
        else:
            output[_l.lower()] = drink['strDrink' + _l]
    return output


def getInstructions(drink):
    output = {}
    languages = ['', 'ES', 'DE', 'FR', 'ZH-HANS', 'ZH-HANT']
    for _l in languages:
        if drink['strInstructions' + _l] is None:
            continue
        if _l == '':
            output['en'] = drink['strInstructions' + _l]
        else:
            output[_l.lower()] = drink['strInstructions' + _l]
    return output


def getRecipes(drink):
    output = []
    for i in range(1, 15 + 1):
        # todo: maybe allow ingredient/drink to be none (just remove) and not stop complete entry
        if drink['strIngredient' + str(i)] is None:
            continue
        elif drink['strMeasure' + str(i)] is None:
            continue
        recipe = {'ingredient': drink['strIngredient' + str(i)],
                  'measure:': drink['strMeasure' + str(i)]}
        output.append(recipe)
    return output


def display(cocktails):
    output = {}
    drinks = []
    for drink in cocktails:
        entry = {'id': drink["idDrink"] if "idDrink" in drink else None,
                 'name': getNames(drink),
                 'nameAlt': drink["strDrinkAlternate"] if "strDrinkAlternate" in drink else None,
                 'category': drink["strCategory"] if "strCategory" in drink else None,
                 'iba': drink["strIBA"] if "strIBA" in drink else None,
                 'tags': drink["strTags"] if "strTags" in drink else None,
                 'alcoholic': getIsAlcoholic(drink),
                 'glass': drink["strGlass"] if "strGlass" in drink else None,
                 'instructions': getInstructions(drink),
                 'thumb': drink["strDrinkThumb"] if "strDrinkThumb" in drink else None,
                 'recipe': getRecipes(drink),
                 'imgAttr': drink["strImageAttribution"] if "strImageAttribution" in drink else None,
                 'video': drink["strVideo"] if "strVideo" in drink else None,
                 'imgSrc': drink["strImageSource"] if "strImageSource" in drink else None,
                 'creativeCC': getIsCreativeCC(drink), 'dateModified': getDate(drink)
                 }

        print(drink)
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
    # todo: maybe create cocktail objects to send instead of dict
    display(x)
