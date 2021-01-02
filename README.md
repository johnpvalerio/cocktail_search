# Cocktail search
A simple program function that fetches cocktails and outputs a JSON file. Uses TheCocktailDB API to fetch and retrieve
cocktail information.
## Installation
```
python -m pip install 'git+https://github.com/johnpvalerio/cocktail_search.git'
```
### Requirements
- Python 3
- [Requests >= 2.25.1](https://requests.readthedocs.io/en/master/user/install/#install) - HTTP library
## Setup
In order to get the full access to [TheCocktailDB's databse](https://www.thecocktaildb.com/api.php) you will need
to be a paid Patreon supporter for API production key. 
You can always use the default test API key "1" for some queries.

In order to set your API key go to `resources/config.json` and set your key there.
```json
{
  "API_KEY": "SECRET_API_KEY"
}
```
By default, the value of the key `API_KEY` is set to `"1"`.

## Usage
```
> main.py [file path 1] [file path 2] [...]
```

### Input
The input JSON file given needs to be in a specific format in order to properly function and query.
If not in the proper format, the program will skip that entry and attempt to read the next one.

format:
```json
{
  "drinks": [
    {
      "idDrink": "11170",
      "strDrink": "Brandy Sour",
      "strCategory": "Ordinary Drink",
      "strAlcoholic": "Alcoholic",
      "strGlass": "Whiskey sour glass",
      "strIngredient1": "Brandy",
      "strIngredient2": "Lemon",
      "strIngredient3": "Powdered sugar",
      "strIngredient4": "Lemon",
      "strIngredient5": "Cherry"
    },
    {
      "idDrink": "11170"
    },
    {
      "strDrink": "Brandy Sour",
      "strCategory": "Ordinary Drink",
      "strAlcoholic": "Alcoholic"
    }
  ]
}
```
With this file input, it will make 3 queries of the same drink. The program can directly query the API with only the `idDrink` key and value.
If no `idDrink` is given, it will attempt to find the drink with matching attributes `strDrink`, `strCategory`, `strAlcoholic`, `strGlass`, and
`strIngredient[1,2,3,...,15]`
### Output
The output result will be a JSON file of similar format of the drink query results. 
- `ingredients`/`measure`: List of dicts 
- translated value(`name`/`instruction`): Dicts by language (English, Spanish, Deutsch, French, Chinese simplified, Chinese traditional)
- `alcoholic`/`creativeCommonsConfirmed`: Boolean
- `date` : ISO 8601 EST timezone (-4:00)
- Any queried results with no value (`null`/`None`) returned will not be included.

format:
```json
{
    "drinks": [
        {
            "id": "11170",
            "name": {
                "en": "Brandy Sour"
            },
            "category": "Ordinary Drink",
            "alcoholic": true,
            "glass": "Whiskey sour glass",
            "instructions": {
                "en": "Shake brandy, juice of lemon, and powdered sugar with ice and strain into a whiskey sour glass. Decorate with the lemon slice, top with the cherry, and serve.",
                "de": "Brandy, Zitronensaft und Puderzucker mit Eis sch\u00fctteln und in ein Whiskey Sour Glas abseihen. Mit der Zitronenscheibe dekorieren, mit der Kirsche garnieren und servieren."
            },
            "thumbnail": "https://www.thecocktaildb.com/images/media/drink/b1bxgq1582484872.jpg",
            "recipe": [
                {
                    "ingredient": "Brandy",
                    "measure": "2 oz "
                },
                {
                    "ingredient": "Lemon",
                    "measure": "Juice of 1/2 "
                },
                {
                    "ingredient": "Powdered sugar",
                    "measure": "1/2 tsp "
                },
                {
                    "ingredient": "Lemon",
                    "measure": "1/2 slice "
                },
                {
                    "ingredient": "Cherry",
                    "measure": "1 "
                }
            ],
            "creativeCommonsConfirmed": true,
            "dateModified": "2017-09-02T16:35:40-04:00"
        }
    ]
}
```
The input file will produce a file with this formatted output. You can find the output in the `/output` folder.
All JSON files produced will be named in the format `output-YYYYMMDD-HHMMSSffffff.json`.


