from resources.thecocktaildb import Cocktail
import json

fpath = 'example/input.json'
with open(fpath) as f:
    cInput = json.load(f)['drinks'][0]
print(cInput)
c = Cocktail(cInput)

print(c.__dict__)
