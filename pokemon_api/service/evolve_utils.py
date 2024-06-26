import json

from fastapi import HTTPException
import httpx


def find_evolution(chain, target_name):
    if chain["species"]["name"] == target_name:
        if chain["evolves_to"]:
            return chain["evolves_to"][0]["species"]["name"]
        else:
            return None
    for evolves_to in chain["evolves_to"]:
        result = find_evolution(evolves_to, target_name)
        if result:
            return result
        return None


async def get_evolved_pokemon(pokemon_name: str):
    async with httpx.AsyncClient() as client:
        with open('pokemon_api/tables_server/constants.json') as f:
            constants = json.load(f)
        print(constants)
        pokemon_response = await client.get(f"{constants['pokapi_url']}/pokemon/{pokemon_name.lower()}")
        if pokemon_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Pokémon not found")

        pokemon_data = pokemon_response.json()
        species_url = pokemon_data["species"]["url"]

        # Fetch the species data
        species_response = await client.get(species_url)
        if species_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Species data not found")

        species_data = species_response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]

        # Fetch the evolution chain data
        evolution_chain_response = await client.get(evolution_chain_url)
        if evolution_chain_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Evolution chain data not found")

        evolution_chain_data = evolution_chain_response.json()

        # Traverse the evolution chain to find the evolution details
        chain = evolution_chain_data["chain"]
        return find_evolution(chain, pokemon_name.lower())
