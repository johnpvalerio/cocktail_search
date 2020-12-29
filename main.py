import sys

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
                    CocktailSearch.search(drink, key)
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    main()
