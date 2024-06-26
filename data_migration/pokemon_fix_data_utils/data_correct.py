from pokeApi_request import get_pokemon_types
from file_handler import read_data_json, write_data_json
import requests


def fix_all_pokemons_type(file_path):
    """
    Fix the types of all Pokemon in the given JSON file by fetching the correct types from the PokeAPI.

    Parameters:
    file_path (str): The path to the JSON file containing Pokemon data.
    """
    pokemons = read_data_json(file_path)

    for pokemon in pokemons:

        try:
            types = get_pokemon_types(pokemon["name"])
            if types != pokemon["type"]:
                pokemon["type"] = types
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while retrieving data for Pokemon {pokemon['name']}: {http_err}")
        except Exception as err:
            print(f"An error occurred while retrieving data for Pokemon {pokemon['name']}: {err}")
    write_data_json(file_path, pokemons)


if __name__ == "__main__":
    fix_all_pokemons_type("POKEMONS/pokemons_data.json")
