# Explanations
Explanation of the code, further details can be found in docstrings.

## Code

### Flow
1. Loop through drink entries
2. Search API with a drink entry
   1. Create `Cocktail` object with drink entry information to get hints.
   2. Use hints in `Api` to find drink results.
3. Format the results.
4. Write to file.

### Main
`main.py` is the driver for the code operations and any error is handled here. \
Starts by reading the API key from `resources/config.json` and the input files given to be processed. 
If no input files given, it will use the example file `example/input.json` as input.
From a file, it will loop through each drink entry to be processed.

#### Error handling
- `FileNotFoundError` - Given file is not found, skip to next file.
- `json.decoder.JSONDecodeError` - Given file is incorrect.
- `requests.exceptions.HTTPError` - HTTP GET request error, did not return a `[200 response]` status code. API key may be incorrect. Skip to next drink input.
- `TypeError` - Queried input did not yield results, skip to next drink input. \
  Possible cause: 
  - No valid hints given - combination of drink information have no drink in common
  - No entry found with given requirements - input file drink entry key or values are in incorrect format
  - No info found - queried may be in database but not shown (maybe caused by using public test API key)\
    Either not all information on an item is given or query results are limited.
    - ex: searching for drinks with ingredient `cherry` will bring no value even though it is a valid ingredient.
    - ex: `"Long Island Iced Tea"` is a valid entry with the category `"Ordinary Drink"` but searching for drinks with 
      category `"Ordinary Drinks"` does not include `"Long Island Iced Tea"`.
  - Info not found in database - queried input not in database
    
### cocktailsearch
`cocktailsearch.py` initiates the search and output of the queries in a formatted result.\
It initiates `Api` and `Cocktail` with corresponding key and dict. Query the API with the determining hints from the cocktail object.
Gather all queried results then process it to be formatted and in a dict. \
Format:
- ingredients/measure - List of dicts 
- translated value(name/instruction) - dicts by language
- alcoholic/creativeCommonsConfirmed - bool
- date - ISO 8601 EST timezone
- string - if none of the above and not None
- None - removed entries

Output results in a JSON file. Files are made in the `/output` folder and named as `output-YYYMMDD-HHMMSSFFFFFF.json`.

### thecocktaildb
`thecocktaildb.py` contains 2 classes `Api` for querying the API and `Cocktail` for managing the drink objects.

#### Cocktail
With given file input as a dict, create a `Cocktail` object with information given as attributes.
Creating hints uses the most relevant attributes in order to best query a cocktail. \
Hint output:
- id - the drink ID is enough to isolate the query to 1 drink, or
- name, ingredients, alcohol, category, glass - use these information to find common drink between all requirements.

For the final output, we need to provide drink information in a specific format. `Cocktail` provides getters to access them.
- `getNames()`/`getInstructions()` both uses `getGroupLanguage()` in order to group attributes by languages (EN/ES/DE/FR/ZH-HANS/ZH-HANT) as a dict.
  - ex: 
  ```json
  {
   "en": "Shake brandy, juice of lemon, and powdered sugar with ice and strain into a whiskey sour glass. Decorate with the lemon slice, top with the cherry, and serve.",
   "de": "Brandy, Zitronensaft und Puderzucker mit Eis sch\u00fctteln und in ein Whiskey Sour Glas abseihen. Mit der Zitronenscheibe dekorieren, mit der Kirsche garnieren und servieren."  
  }
  ```
- `getRecipes()` groups the ingredient and its measurement together as a list of dicts
  - ex:
  ```json
  [
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
  ]
  ```
  
- `getIsAlcoholic()` Converts attribute `self.alcoholic` string value "alcoholic" or "optional alcohol" to True, else False.

- `getIsCreativeCC()` Converts attribute `self.creativeCC` string value "Yes" to True, else False 

- `getDate()` Converts attribute `self.dateMod` string to ISO 8601 EST timezone (-4:00)

#### Api
With given string as API key in the constructor, queries the API database. API key value defaults to the public test key `"1"`.

When calling `query()`, it acts as a function manager to best find the drink.

- If given drink's `id`, calling `queryApi()` to directly call the API to yield 1 result, or
- attempt to find best matching drink with given requirements (hints) with `queryFilters()`:
  name, ingredients, alcohol, category, glass.\
Call the API to get drinks with each of these requirements (if given), then compare each queried drinks results and select
  only the ones common in all queries with `intersectKeys()`.\
  Call the API with those common results to get their full information details.