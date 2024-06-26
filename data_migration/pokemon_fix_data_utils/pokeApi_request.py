import json

import requests



def get_pokemon_types(pokemon_name):
    """
    Get the types of a specified Pokémon from the PokéAPI.

    Parameters:
    pokemon_name (str): The name of the Pokémon.

    Returns:
    list: A list of types for the specified Pokémon. If the request fails, an exception is raised.
    """
    with open('pokemon_api/service/constants.json') as f:
        constants = json.load(f)

    response = requests.get(f"{constants["pokapi_url"]}/pokemon/{pokemon_name.lower()}")

    # Raise an HTTPError if the request returned an unsuccessful status code
    response.raise_for_status()

    data = response.json()
    types = [type_info["type"]["name"] for type_info in data["types"]]
    return types
