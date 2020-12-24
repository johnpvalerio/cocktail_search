from typing import List, Dict

import requests

API_BASE_URL = 'http://www.thecocktaildb.com/api/json/v1/'
API_KEY = ''


class Api:
    """
    API methods:
    name -> list of cocktails
        first letter -> list of cocktails
    ingredient name -> ingredient info
    cocktail id -> full cocktail info
        <random> -> full cocktail info
    ingredient name -> cocktail
    alcoholic yes/no -> cocktail list
    category -> cocktail list
    glass -> cocktail list
    list categories/glasses/ingredients/alcoholic -> list
    """

    def __init__(self, key: str = '1') -> None:
        """
        API constructor
        :param key: str - API key, default 1 (test API key)
        """
        global API_KEY
        API_KEY = key

    def query(self, hints: Dict[str, str] = None) -> Dict[str, list]:
        """
        Query manager, calls desired query from argument given
        :param hints: Dict[str, str] - cocktail hints
        :return: None
        """
        if 'id' in hints:
            output = self.queryId(hints['id'])
            print('id', output)
        else:
            name = hints['name'] if 'name' in hints else None
            temp1 = self.queryName(name)
            print('temp1', temp1)

            ing = hints['ing'] if 'ing' in hints else None
            alc = hints['alc'] if 'alc' in hints else None
            cat = hints['cat'] if 'cat' in hints else None
            gla = hints['gla'] if 'gla' in hints else None
            temp2 = self.queryFilters(ing, alc, cat, gla)
            print('temp2', temp2)
            output = temp1
            # todo: find intersection of temp1 & temp 2 keys
        print(output)
        return output

    def queryId(self, cid: str) -> Dict[str, list]:
        """
        Fetch cocktail with cocktail ID from API
        :param cid: str - cocktail ID
        :return: None
        """
        url = API_BASE_URL + API_KEY + '/lookup.php'
        data = requests.get(url, params={'i': cid})
        data = data.json()
        return data

    def queryName(self, name: str = None) -> Dict[str, list]:
        """
        Fetch list of cocktails with cocktail name from API
        :param name: str - cocktail name
        :return: None
        """
        if not name:
            return {'drinks': []}
        url = API_BASE_URL + API_KEY + '/search.php'
        data = requests.get(url, params={'s': name})
        data = data.json()
        return data

    def queryFilters(self, ingredients: List[str] = None, alcoholic: str = None, category: str = None,
                     glass: str = None) -> Dict[str, list]:
        """
        Fetch list of cocktails with cocktail filters from API
        :param alcoholic: str - Alcoholic, Non Alcoholic, or Optional alcohol
        :param category: str - drink category: Ordinary Drink, Cocktail, Cocoa, etc
        :param glass: str - glass type: Highball glass, Cocktail glass, etc
        :param ingredients: List[str] - List of filters (ingredients/alcoholic/category/glass) strings
        :return: None
        """
        url = API_BASE_URL + API_KEY + '/filter.php'
        payload = {}
        if ingredients:
            payload['i'] = ingredients
        if alcoholic:
            payload['a'] = alcoholic
        if category:
            payload['c'] = category
        if glass:
            payload['g'] = glass

        if not payload:
            return {'drinks': []}
        data = requests.get(url, params=payload)
        data = data.json()
        return data


class Cocktail:
    def __init__(self, cocktailDict: Dict[str, str]) -> None:
        """
        Cocktail constructor
        If not in dict, set to None
        :param cocktailDict: dict - attribute inputs
        """
        self.id = cocktailDict["idDrink"] if "idDrink" in cocktailDict else None
        self.name = cocktailDict["strDrink"] if "strDrink" in cocktailDict else None
        self.nameAlt = cocktailDict["strDrinkAlternate"] if "strDrinkAlternate" in cocktailDict else None
        self.nameES = cocktailDict["strDrinkES"] if "strDrinkES" in cocktailDict else None
        self.nameDE = cocktailDict["strDrinkDE"] if "strDrinkDE" in cocktailDict else None
        self.nameFR = cocktailDict["strDrinkFR"] if "strDrinkFR" in cocktailDict else None
        self.nameZHHANS = cocktailDict["strDrinkZH-HANS"] if "strDrinkZH-HANS" in cocktailDict else None
        self.nameZHHANT = cocktailDict["strDrinkZH-HANT"] if "strDrinkZH-HANT" in cocktailDict else None
        self.tags = cocktailDict["strTags"] if "strTags" in cocktailDict else None
        self.video = cocktailDict["strVideo"] if "strVideo" in cocktailDict else None
        self.category = cocktailDict["strCategory"] if "strCategory" in cocktailDict else None
        self.iba = cocktailDict["strIBA"] if "strIBA" in cocktailDict else None
        self.alcoholic = cocktailDict["strAlcoholic"] if "strAlcoholic" in cocktailDict else None
        self.glass = cocktailDict["strGlass"] if "strGlass" in cocktailDict else None
        self.recipe = cocktailDict["strInstructions"] if "strInstructions" in cocktailDict else None
        self.recipeES = cocktailDict["strInstructionsES"] if "strInstructionsES" in cocktailDict else None
        self.recipeDE = cocktailDict["strInstructionsDE"] if "strInstructionsDE" in cocktailDict else None
        self.recipeFR = cocktailDict["strInstructionsFR"] if "strInstructionsFR" in cocktailDict else None
        self.recipeZHHANS = cocktailDict["strInstructionsZH-HANS"] if "strInstructionsZH-HANS" in cocktailDict else None
        self.recipeZHHANT = cocktailDict["strInstructionsZH-HANT"] if "strInstructionsZH-HANT" in cocktailDict else None
        self.thumb = cocktailDict["strDrinkThumb"] if "strDrinkThumb" in cocktailDict else None
        self.imgSrc = cocktailDict["strImageSource"] if "strImageSource" in cocktailDict else None
        self.imgAttr = cocktailDict["strImageAttribution"] if "strImageAttribution" in cocktailDict else None
        self.creativeCC = cocktailDict["strCreativeCommonsConfirmed"] if "strCreativeCommonsConfirmed" in cocktailDict else None
        self.dateMod = cocktailDict["dateModified"] if "dateModified" in cocktailDict else None

        self.ingredient1 = cocktailDict["strIngredient1"] if "strIngredient1" in cocktailDict else None
        self.ingredient2 = cocktailDict["strIngredient2"] if "strIngredient2" in cocktailDict else None
        self.ingredient3 = cocktailDict["strIngredient3"] if "strIngredient3" in cocktailDict else None
        self.ingredient4 = cocktailDict["strIngredient4"] if "strIngredient4" in cocktailDict else None
        self.ingredient5 = cocktailDict["strIngredient5"] if "strIngredient5" in cocktailDict else None
        self.ingredient6 = cocktailDict["strIngredient6"] if "strIngredient6" in cocktailDict else None
        self.ingredient7 = cocktailDict["strIngredient7"] if "strIngredient7" in cocktailDict else None
        self.ingredient8 = cocktailDict["strIngredient8"] if "strIngredient8" in cocktailDict else None
        self.ingredient9 = cocktailDict["strIngredient9"] if "strIngredient9" in cocktailDict else None
        self.ingredient10 = cocktailDict["strIngredient10"] if "strIngredient10" in cocktailDict else None
        self.ingredient11 = cocktailDict["strIngredient11"] if "strIngredient11" in cocktailDict else None
        self.ingredient12 = cocktailDict["strIngredient12"] if "strIngredient12" in cocktailDict else None
        self.ingredient13 = cocktailDict["strIngredient13"] if "strIngredient13" in cocktailDict else None
        self.ingredient14 = cocktailDict["strIngredient14"] if "strIngredient14" in cocktailDict else None
        self.ingredient15 = cocktailDict["strIngredient15"] if "strIngredient15" in cocktailDict else None

        self.measure1 = cocktailDict["strMeasure1"] if "strMeasure1" in cocktailDict else None
        self.measure2 = cocktailDict["strMeasure2"] if "strMeasure2" in cocktailDict else None
        self.measure3 = cocktailDict["strMeasure3"] if "strMeasure3" in cocktailDict else None
        self.measure4 = cocktailDict["strMeasure4"] if "strMeasure4" in cocktailDict else None
        self.measure5 = cocktailDict["strMeasure5"] if "strMeasure5" in cocktailDict else None
        self.measure6 = cocktailDict["strMeasure6"] if "strMeasure6" in cocktailDict else None
        self.measure7 = cocktailDict["strMeasure7"] if "strMeasure7" in cocktailDict else None
        self.measure8 = cocktailDict["strMeasure8"] if "strMeasure8" in cocktailDict else None
        self.measure9 = cocktailDict["strMeasure9"] if "strMeasure9" in cocktailDict else None
        self.measure10 = cocktailDict["strMeasure10"] if "strMeasure10" in cocktailDict else None
        self.measure11 = cocktailDict["strMeasure11"] if "strMeasure11" in cocktailDict else None
        self.measure12 = cocktailDict["strMeasure12"] if "strMeasure12" in cocktailDict else None
        self.measure13 = cocktailDict["strMeasure13"] if "strMeasure13" in cocktailDict else None
        self.measure14 = cocktailDict["strMeasure14"] if "strMeasure14" in cocktailDict else None
        self.measure15 = cocktailDict["strMeasure15"] if "strMeasure15" in cocktailDict else None

    def getHint(self) -> Dict[str, str]:
        """
        Gets most relevant attributes to find cocktail
        if id given, return id
        else give dict of filters (name/ingredients/alcoholic/category/glass)
        :return: Dict[str, str] - param key, value
        """
        output = {}
        if self.id:
            output['id'] = self.id
        else:
            if self.name is not None:
                output['name'] = self.name
            ingrList = []
            for i in range(1, 15 + 1):
                ingr = getattr(self, 'ingredient' + str(i))
                if ingr:
                    ingrList.append(ingr)
            if ingrList:
                output['ing'] = ingrList
            if self.alcoholic is not None:
                output['alc'] = self.alcoholic
            if self.category is not None:
                output['cat'] = self.category
            if self.glass is not None:
                output['gla'] = self.glass
        print('hint', output)
        return output