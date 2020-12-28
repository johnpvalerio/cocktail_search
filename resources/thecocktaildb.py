import datetime
from typing import List, Dict, Optional

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

    def query(self, hints: Dict[str, str] = None) -> List[Dict[str, list]]:
        """
        Query manager, calls desired query from argument given
        :param hints: Dict[str, str] - cocktail hints
        :return: None
        """
        output = []
        if 'id' in hints:
            output = [self.queryId(hints['id'])]
        else:
            name = hints['name'] if 'name' in hints else None

            ing = hints['ing'] if 'ing' in hints else None
            alc = hints['alc'] if 'alc' in hints else None
            cat = hints['cat'] if 'cat' in hints else None
            gla = hints['gla'] if 'gla' in hints else None
            temp = self.queryFilters(name=name, ingredients=ing, alcoholic=alc, category=cat, glass=gla)
            keys = self.intersectKeys(*temp)
            print(keys)
            output = [self.queryId(x) for x in keys]
        if not output:
            return None
        print(output)
        return output

    @staticmethod
    def queryId(cid: str) -> Dict[str, list]:
        """
        Fetch at most 1 cocktail with cocktail ID from API
        :param cid: str - cocktail ID
        :return: None
        """
        url = API_BASE_URL + API_KEY + '/lookup.php'
        data = requests.get(url, params={'i': cid})
        if data.text == '':
            return None
        data = data.json()
        return data['drinks'][0]

    @staticmethod
    def intersectKeys(*cocktails: List[Dict[str, str]]) -> List[str]:
        """
        From given cocktail dicts, finds common idDrink strings
        :param cocktails: List(Dict) - Lists of cocktail dicts
        :return: List(str) - List of idDrink strings
        """
        keys = []
        for _c in cocktails:
            keys1 = set(x['idDrink'] for x in _c)
            keys.append(keys1)
        if not keys:
            return []
        return list(set.intersection(*keys))

    @staticmethod
    def queryFilters(name: str = None, ingredients: List[str] = None, alcoholic: str = None, category: str = None,
                     glass: str = None) -> List[List[Dict[str, str]]]:
        """
        Fetch list of cocktails with cocktail filters from API
        :param name:
        :param alcoholic: str - Alcoholic, Non Alcoholic, or Optional alcohol
        :param category: str - drink category: Ordinary Drink, Cocktail, Cocoa, etc
        :param glass: str - glass type: Highball glass, Cocktail glass, etc
        :param ingredients: List[str] - List of filters (ingredients/alcoholic/category/glass) strings
        :return: None
        """

        cocktails = []

        def qFilter(payload, _type):
            """
            Inner function to query API database, queries ingredients, categories, glass, alcoholic
            :param payload: string - item filtered (ingredients, categories, glass, alcoholic)
            :param _type: string - API query filter param (i, a, c, g)
            :return:
            """
            url = API_BASE_URL + API_KEY + '/filter.php'
            data = requests.get(url, params={_type: payload})
            # if input not in db
            if data.text == '':
                return None
            data = data.json()
            return data['drinks']

        def qName(name: str = None) -> Optional[List[Dict[str, str]]]:
            """
            Fetch list of cocktails with cocktail name from API
            :param name: str - cocktail name
            :return:
            """
            url = API_BASE_URL + API_KEY + '/search.php'
            data = requests.get(url, params={'s': name})
            if data.text == '':
                return None
            data = data.json()
            return data['drinks']

        if name:
            f0 = qName(name)
            if f0:
                print('name', len(f0), f0)
                cocktails.append(f0)
        if ingredients:
            # todo: if premium key, use batched ingredients function
            for ingr in ingredients:
                f1 = qFilter(ingr, 'i')
                if f1:
                    print(ingr, len(f1), f1)
                    cocktails.append(f1)
        if alcoholic:
            f2 = qFilter(alcoholic, 'a')
            if f2:
                cocktails.append(f2)
                print('alc', len(f2), f2)
        if category:
            f3 = qFilter(category, 'c')
            if f3:
                cocktails.append(f3)
                print('cat', len(f3), f3)
        if glass:
            f4 = qFilter(glass, 'g')
            if f4:
                cocktails.append(f4)
                print('glass', len(f4), f4)

        return cocktails


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
        self.instructions = cocktailDict["strInstructions"] if "strInstructions" in cocktailDict else None
        self.instructionsES = cocktailDict["strInstructionsES"] if "strInstructionsES" in cocktailDict else None
        self.instructionsDE = cocktailDict["strInstructionsDE"] if "strInstructionsDE" in cocktailDict else None
        self.instructionsFR = cocktailDict["strInstructionsFR"] if "strInstructionsFR" in cocktailDict else None
        self.instructionsZHHANS = cocktailDict["strInstructionsZH-HANS"] if "strInstructionsZH-HANS" in cocktailDict else None
        self.instructionsZHHANT = cocktailDict["strInstructionsZH-HANT"] if "strInstructionsZH-HANT" in cocktailDict else None
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

    def getRecipes(self):
        output = []
        for i in range(1, 15 + 1):
            # todo: maybe allow ingredient/drink to be none (just remove) and not stop complete entry
            try:
                if getattr(self, 'ingredient' + str(i)) is None:
                    continue
                elif getattr(self, 'measure' + str(i)) is None:
                    continue
                recipe = {'ingredient': getattr(self, 'ingredient' + str(i)),
                          'measure:': getattr(self, 'measure' + str(i))}
                output.append(recipe)
            except AttributeError:
                continue
        return output

    def getGroupLanguage(self, attribute):
        output = {}
        languages = ['', 'ES', 'DE', 'FR', 'ZHHANS', 'ZHHANT']
        for _l in languages:
            if getattr(self, attribute + _l) is None:
                continue
            if _l == '':
                output['en'] = getattr(self, attribute + _l)
            elif _l[:2] == 'ZH':
                output[_l[:2] + '-' + _l[2:]] = getattr(self, attribute + _l)
            else:
                output[_l.lower()] = getattr(self, attribute + _l)
        return output

    def getInstructions(self):
        return self.getGroupLanguage('instructions')

    def getNames(self):
        return self.getGroupLanguage('name')

    def getDate(self):
        if not self.dateMod:
            return
        date = datetime.datetime.strptime(self.dateMod, '%Y-%m-%d %H:%M:%S')
        return date.isoformat()

    def getIsAlcoholic(self):
        if not self.alcoholic:
            return
        return True if self.alcoholic in ['Alcoholic', 'Optional alcohol'] else False

    def getIsCreativeCC(self):
        if not self.creativeCC:
            return
        return True if self.creativeCC == 'Yes' else False
