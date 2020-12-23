API_BASE_URL = 'http://www.thecocktaildb.com/api/json/v1'
API_KEY = None


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

    def query(self, cid: str, name: str, filters: list[str]) -> None:
        """
        Query manager, calls desired query from argument given
        :param cid: str - cocktail ID
        :param name: str - cocktail name
        :param filters: List[str] - List of filters (ingredients/alcoholic/category/glass) strings
        :return: None
        """
        pass

    def queryId(self, cid: str) -> None:
        """
        Fetch cocktail with cocktail ID from API
        :param cid: str - cocktail ID
        :return: None
        """
        pass

    def queryName(self, name: str) -> None:
        """
        Fetch list of cocktails with cocktail name from API
        :param name: str - cocktail name
        :return: None
        """
        pass

    def queryFilters(self, filters: list[str]) -> None:
        """
        Fetch list of cocktails with cocktail filters from API
        :param filters: List[str] - List of filters (ingredients/alcoholic/category/glass) strings
        :return: None
        """
        pass


class Cocktail:
    def __init__(self, cocktailDict: dict) -> None:
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
