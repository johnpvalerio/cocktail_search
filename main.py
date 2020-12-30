import sys

import requests

import CocktailSearch
import json


def main() -> None:
    """
    Main driver function, reads input files and searches for cocktail output
    If given CLI args, use given paths
    else use default example
    :return: None
    """
    # get API key from file
    with open('resources/config.json') as f:
        key = json.load(f)['API_KEY']
    paths = sys.argv[1:] if len(sys.argv) > 1 else ['example/input.json']
    # loop through paths
    for fpath in paths:
        try:
            with open(fpath) as f:
                # load json as dict
                cInput = json.load(f)['drinks']
                # loop through drinks in dict
                for drink in cInput:
                    try:
                        CocktailSearch.search(drink, key)
                    # no results found, try next drink if available
                    except TypeError as e:
                        print(e)
                        continue
        # File error, try next if available
        except FileNotFoundError:
            continue
        # HTTP error, bad key, stop
        except requests.exceptions.HTTPError as e_:
            print(e_, 'with API key:', key)
            sys.exit(1)


if __name__ == '__main__':
    main()
