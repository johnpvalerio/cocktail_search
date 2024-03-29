import datetime
from typing import List, Dict, Optional, Union

import requests

API_BASE_URL = 'http://www.thecocktaildb.com/api/json/v1/'  # API URL
DEFAULT_API_KEY = '1'  # API key

# typing reference
DrinkQueried = Dict[str, Optional[str]]
Hints = Dict[str, Union[str, List[str]]]


class Api:
    """
    Class for querying thecocktaildb API.
    """

    def __init__(self, key: str = DEFAULT_API_KEY) -> None:
        """
        API constructor
        :param key: str - API key, default 1 (test API key)
        """
        self._keyApi = key

    def query(self, hints: Hints = None) -> List[DrinkQueried]:
        """
        Query manager, calls desired query from argument given
        :param hints: Dict[str, Union[str, List[str]]] - cocktail hints
        :return: List[Dict[str, Optional[str]]] - List of drink dictionary
        """
        id_ = hints['id'] if 'id' in hints else None
        name = hints['name'] if 'name' in hints else None
        ing = hints['ing'] if 'ing' in hints else None
        alc = hints['alc'] if 'alc' in hints else None
        cat = hints['cat'] if 'cat' in hints else None
        gla = hints['gla'] if 'gla' in hints else None
        # Check if any hints given
        if not hints:
            raise TypeError("Query results 0 - No hints given")
        # Check if hints are ""
        if not all(hints.values()):
            raise TypeError("Query results 0 - Hints given \"\"")
        if 'ing' in hints and not all(hints['ing']):
            raise TypeError("Query results 0 - Hints given \"\"")

        # make ID the main query to cross reference
        if id_:
            mainQuery = self.queryApi('lookup', 'i', id_)
            del hints['id']
            output = self.filterDrink(mainQuery, hints)
        # make name the main query to cross reference
        elif name:
            mainQuery = self.queryApi('search', 's', name)
            del hints['name']
            output = self.filterDrink(mainQuery, hints)
        # query filters then find common entries: ingredients/alcohol/category/glass
        else:
            qResults = self.queryFilters(ingredients=ing, alcoholic=alc, category=cat, glass=gla)
            commonKeys = self.intersectKeys(*qResults)
            # get cocktail detail for each entry
            output = [self.queryApi('lookup', 'i', x) for x in commonKeys]
            output = [x[0] for x in output]
        # no ID or no hint, raise error and skip this drink query input
        if not output:
            raise TypeError("Query results 0 - No entry found with given requirements")

        return output

    @staticmethod
    def filterDrink(mainDrinks: List[DrinkQueried], filterChecks: Hints) -> List[DrinkQueried]:
        """
        Finds drinks from mainDrinks with common details as given filterCheck
        :param mainDrinks: List[Dict[str, Optional[str]]] - List of drinks to iterate through, remove drink entry if not needed.
        :param filterChecks: Dict[str, Optional[str, List[str]]] - Dict of hints to find in common
        :return:
        """
        output = []
        # iterate through drinks (when querying name, multiple drinks are given possibly)
        for drink in mainDrinks:
            toSkip = False
            # go through filter hints
            # if hint not found but available, mark to skip drink entry for output
            for checkKey, checkVal in filterChecks.items():
                # check name match
                if checkKey == 'name':
                    if drink['strDrink'].upper() != checkVal.upper():
                        toSkip = True
                        break
                # check alcohol match
                if checkKey == 'alc':
                    if drink['strAlcoholic'].upper() != checkVal.upper():
                        toSkip = True
                        break
                # check glass match
                if checkKey == 'gla':
                    if drink['strGlass'].upper() != checkVal.upper():
                        toSkip = True
                        break
                # check category match
                if checkKey == 'cat':
                    if drink['strCategory'].upper() != checkVal.upper():
                        toSkip = True
                        break
                # check ingredient match
                if checkKey == 'ing':
                    # checkVal is a list of str ingredients
                    # iterate through ingredients
                    for ingredientEntry in checkVal:
                        ingList = []
                        # check ingredient list of drink [1-15]
                        for i in range(1, 15 + 1):
                            if not drink["strIngredient" + str(i)]:
                                break
                            ingList.append(drink["strIngredient" + str(i)].upper())
                        # check if an ingredient is missing
                        if ingredientEntry.upper() not in ingList:
                            toSkip = True
                            break
                    if toSkip:
                        break
            # if all match, add to output
            if not toSkip:
                output.append(drink)
        return output

    @staticmethod
    def intersectKeys(*cocktails: List[DrinkQueried]) -> List[str]:
        """
        From given cocktail dicts, finds common idDrink strings
        :param cocktails: List[Dict[str, Optional[str]]] - Lists of cocktail dicts
        :return: List[str] - List of idDrink strings
        """
        keysList = []
        for drink in cocktails:
            keys = set(x['idDrink'] for x in drink)
            keysList.append(keys)
        return list(set.intersection(*keysList))

    def queryApi(self, searchType: str, key: str, payload: Union[str, List[str]]) -> List[DrinkQueried]:
        """
        Queries the API with given args
        :param searchType: str - lookup/filter
        :param key: str - s/i/a/c/g
        :param payload: str - param payload (public test key call)
                        list - param payload (premium key & ingredients call)
        :return: List[Dict[str, Optional[str]]] - list of drink entry
        """
        try:
            url = API_BASE_URL + self._keyApi + '/' + searchType + '.php'
            data = requests.get(url, params={key: payload})
            data.raise_for_status()
        # Response code not 200
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError("Bad API key") from e
        # Response empty/not found, may be triggered when using public API key
        if data.text == '':
            raise TypeError('Query results 0 - Cannot retrieve information.')
        data = data.json()
        # check if theres contents in drinks
        try:
            data['drinks']
            data['drinks'][0]
        # Response gave None
        except TypeError:
            raise TypeError('Query results 0 - Information does not exist in database.')
        return data['drinks']

    def queryFilters(self, ingredients: List[str] = None, alcoholic: str = None, category: str = None,
                     glass: str = None) -> List[List[DrinkQueried]]:
        """
        Fetch list of cocktails with cocktail filters from API
        :param alcoholic: str - Alcoholic, Non Alcoholic, or Optional alcohol
        :param category: str - drink category: Ordinary Drink, Cocktail, Cocoa, etc
        :param glass: str - glass type: Highball glass, Cocktail glass, etc
        :param ingredients: List[str] - List of filters (ingredients/alcoholic/category/glass) strings
        :return: List[List[Dict[str, Optional[str]]]] - List containing the List of drinks Dict queried from the filter hints
        """
        # holds all drink query responses
        cocktails = []
        # get drinks from ingredients
        if ingredients:
            # if premium key, use multi-ingredient filter
            if self._keyApi == DEFAULT_API_KEY:
                f1 = self.queryApi('filter', 'i', ingredients)
                if f1:
                    cocktails.append(f1)
            # iterate through ingredients
            else:
                for ingr in ingredients:
                    f1 = self.queryApi('filter', 'i', ingr)
                    if f1:
                        cocktails.append(f1)
        # get drinks from alcohol
        if alcoholic:
            f2 = self.queryApi('filter', 'a', alcoholic)
            if f2:
                cocktails.append(f2)
        # get drinks from category
        if category:
            f3 = self.queryApi('filter', 'c', category)
            if f3:
                cocktails.append(f3)
        # get drinks from class
        if glass:
            f4 = self.queryApi('filter', 'g', glass)
            if f4:
                cocktails.append(f4)

        return cocktails


class Cocktail:
    """
    Cocktail class for accessing cocktail information attributes
    """

    def __init__(self, cocktailDict: Dict[str, str]) -> None:
        """
        Cocktail constructor
        If not in dict, set to None
        :param cocktailDict: Dict[str, str] - attribute inputs
        """
        self.id = cocktailDict["idDrink"] if "idDrink" in cocktailDict else None
        self.nameEN = cocktailDict["strDrink"] if "strDrink" in cocktailDict else None
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
        self.instructionsEN = cocktailDict["strInstructions"] if "strInstructions" in cocktailDict else None
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
        else give dict of filters (nameEN/ingredients/alcoholic/category/glass)
        :return: Dict[str, str] - param key (name, ing, alc, cat, gla), corresponding attribute value
        """
        output = {}
        # give ID, name, ingredients, alcoholic, category, glass as hints
        # only include not None values
        if self.id is not None:
            output['id'] = self.id
        if self.nameEN is not None:
            output['name'] = self.nameEN
        ingrList = []
        for i in range(1, 15 + 1):
            ingr = getattr(self, 'ingredient' + str(i))
            if ingr is not None:
                ingrList.append(ingr)
        if ingrList:
            output['ing'] = ingrList
        if self.alcoholic is not None:
            output['alc'] = self.alcoholic
        if self.category is not None:
            output['cat'] = self.category
        if self.glass is not None:
            output['gla'] = self.glass
        return output

    def getRecipes(self) -> List[Dict[str, str]]:
        """
        Groups ingredients and measurement together, returns as dict of dicts
        :return: List[Dict[str, str]] - List of Dict of ingredient and measurement
                                    ex: [{"ingredient": "Vodka",
                                          "measure": "1 oz "}, {...}]
        """
        output = []
        for i in range(1, 15 + 1):
            recipe = {}
            if getattr(self, 'ingredient' + str(i)) is not None:
                recipe['ingredient'] = getattr(self, 'ingredient' + str(i))
            if getattr(self, 'measure' + str(i)) is not None:
                recipe['measure'] = getattr(self, 'measure' + str(i))
            # if no ingredient/measurement, skip
            if not recipe:
                continue
            output.append(recipe)
        return output

    def getGroupLanguage(self, attribute: str) -> Dict[str, str]:
        """
        Groups given attribute (name/instructions) by language
        :param attribute: str - "instructions" or "name"
        :return: Dict[str, str] - dict of language string code and translated string
                                    ex: {"en": "Long Island Iced Tea"}
        """
        output = {}
        languages = ['EN', 'ES', 'DE', 'FR', 'ZHHANS', 'ZHHANT']
        for _l in languages:
            # skip if entry in language is missing
            if getattr(self, attribute + _l) is None:
                continue
            # for ZH-HANS and ZH-HANT
            if _l[:2] == 'ZH':
                output[_l[:2] + '-' + _l[2:]] = getattr(self, attribute + _l)
            # all other
            else:
                output[_l.lower()] = getattr(self, attribute + _l)
        return output

    def getInstructions(self) -> Dict[str, str]:
        """
        Helper function
        Calls getGroupLanguage with "instructions" param
        :return: Dict[str, str] - dict of language string code and translated string
        """
        return self.getGroupLanguage('instructions')

    def getNames(self) -> Dict[str, str]:
        """
        Helper function
        Calls getGroupLanguage with "name" param
        :return: Dict[str, str] - dict of language string code and translated string
        """
        return self.getGroupLanguage('name')

    def getDate(self) -> Optional[str]:
        """
        Converts dateMod attribute to ISO 8601 EST timezone
        :return: datetime - string date in EST timezone
                            None if no self.dateMod attribute given
        """
        if not self.dateMod:
            return
        date = datetime.datetime.strptime(self.dateMod, '%Y-%m-%d %H:%M:%S')
        # EST: -4:00
        date = date.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
        return date.isoformat()

    def getIsAlcoholic(self) -> Optional[bool]:
        """
        Returns bool of alcoholic attribute
        alcoholic -> true
        optional alcohol -> true
        non alcoholic -> false
        :return: bool - if attribute given, else return None
        """
        if not self.alcoholic:
            return
        return True if self.alcoholic.lower() in ['alcoholic', 'optional alcohol'] else False

    def getIsCreativeCC(self) -> Optional[bool]:
        """
        Returns bool of creativeCC attribute
        yes -> true
        no -> false
        :return: bool - if attribute given, else return None
        """
        if not self.creativeCC:
            return
        return True if self.creativeCC.lower() == 'yes' else False
