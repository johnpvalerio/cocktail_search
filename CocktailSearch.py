import datetime
import json
from typing import Dict, Union, List, Optional

from resources.thecocktaildb import Cocktail, Api


def outputJSON(drinkDict: Dict[str, List[Dict[str, Union[str, bool, Dict[str, str], List[Dict[str, str]]]]]]) -> None:
    """
    Creates JSON file from dict given
    :param drinkDict: dict - drink entries
    :return:
    """
    # use date timestamp as unique identifier for file name
    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d-%H%M%S%f")
    fpath = 'output/output-' + date + '.json'
    with open(fpath, 'w') as f:
        json.dump(drinkDict, f, indent=4)
    return


def removeNone(drinkDict: Dict[str, Optional[Union[str, bool, Dict[str, str], List[Dict[str, str]]]]]) -> None:
    """
    Iterates through dict and removes entries with None values in-place
    :param drinkDict: dict - drink entry
    :return: None
    """
    for key, val in list(drinkDict.items()):
        if val is None:
            del drinkDict[key]
    return


def cocktailDictFormat(cocktails: List[Cocktail]) -> Dict[str, List[Dict[str, Union[str, bool, Dict[str, str], List[Dict[str, str]]]]]]:
    """
    Create dict output from cocktail info with proper format
    format:
        ingredients/measure - List of dicts
        translated value(name/instruction) - dicts by language
        alcoholic/creativeCommonsConfirmed - bool
        date - ISO 8601 EST timezone
        string - if none of the above and not None
    :param cocktails: List[Cocktail] - List of cocktail objects
    :return: Dict[str, dict] - dict of drink
    """
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


def search(drinkDict: Dict[str, Optional[Union[str, bool, Dict[str, str], List[Dict[str, str]]]]], keyStr: str = '1') -> None:
    """
    Starts search query then creates final output
    :param drinkDict: dict - drink entry
    :param keyStr: API key, default "1"
    :return: None
    """
    api = Api(keyStr)
    cocktail = Cocktail(drinkDict)
    # query API with cocktail object hints (ID/name/ingredients/alcoholic/category/glass)
    cocktailQueries = api.query(cocktail.getHint())
    cocktailList = [Cocktail(c) for c in cocktailQueries]
    # create cocktail in proper format
    drinks = cocktailDictFormat(cocktailList)
    # write to file
    outputJSON(drinks)
    return None
