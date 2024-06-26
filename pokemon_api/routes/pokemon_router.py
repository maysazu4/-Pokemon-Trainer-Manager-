from fastapi import APIRouter, Query, HTTPException
from Queries import pokemon,trainer,database
from pokemon_api.service.get_pokemon_info_utils import get_pokemon_info


router = APIRouter()


@router.get("/pokemons/species/{species}")
def get_pokemon_by_sepecies(species: str):
    # pokemon_data = pokemon.get_pokemon_by_species(species)
    # if not pokemon_data:
    #     raise HTTPException(status_code=404, detail=f"Pokémon with species {species} not found.")
    # return pokemon_data
    connection = database.connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Get Pokémon details
    cursor.execute(
        "SELECT id, name, height, weight FROM Pokemon WHERE name = %s", (species,)
    )
    pokemon = cursor.fetchone()
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokémon with species {species} not found.")

    # Get Pokémon types
    cursor.execute(
        "SELECT type_name FROM PokemonType WHERE pokemon_id = %s", (pokemon['id'],)
    )
    types = cursor.fetchall()
    pokemon['types'] = [t['type_name'] for t in types]

    cursor.close()
    connection.close()
    return pokemon



"""
 Get a list of Pokémon based on type or trainer.
 This endpoint retrieves a list of Pokémon either by their type or by the trainer who owns them.
 The query parameters `type` and `trainer_name` are mutually exclusive.
 Parameters:
 - type: str (optional) - The type of Pokémon to filter by.
 - trainer_name: str (optional) - The name of the trainer to filter by.
 Raises:
 - HTTPException: 400 if both `type` and `trainer_name` are specified.
 - HTTPException: 400 if neither `type` nor `trainer_name` is specified.
 - HTTPException: 404 if the specified type does not exist.
 - HTTPException: 404 if no Pokémon of the specified type are found.
 - HTTPException: 404 if the specified trainer does not exist.
 - HTTPException: 404 if the trainer does not own any Pokémon.
 Returns:
 - list: A list of Pokémon that match the specified criteria.
 """

@router.get("/pokemons")
def get_pokemons(type: str = Query(None), trainer_name: str = Query(None)):
    if type and trainer_name:
        raise HTTPException(status_code=400, detail="Specify either type or trainer_name, not both.")
    elif type:
        if not pokemon.type_exists(type):
            raise HTTPException(status_code=404, detail=f"{type} type not found.")
        pokemons = pokemon.get_pokemons_of_type(type)
        if not pokemons:
            raise HTTPException(status_code=404, detail=f"No pokemons found of type {type}.")
        return pokemons
    elif trainer_name:
        if not trainer.trainer_exists(trainer_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
        pokemons = pokemon.get_pokemons_by_trainer(trainer_name)
        if not pokemons:
            raise HTTPException(status_code=404, detail=f"No pokemons found for trainer {trainer_name}.")
        return pokemons
    else:
        raise HTTPException(status_code=400, detail="Specify at least one query parameter: type or trainer_name.")


"""
Delete a specific Pokémon from a trainer's collection.
This endpoint removes a Pokémon from a trainer's list of owned Pokémon. It checks
if the Pokémon and trainer exist, and if the trainer owns the specified Pokémon.
Parameters:
- trainer_name: str - The name of the trainer.
- pokemon_name: str - The name of the Pokémon to be deleted.
Raises:
- HTTPException: 404 if the Pokémon does not exist.
- HTTPException: 404 if the trainer does not exist.
- HTTPException: 404 if the trainer does not own the specified Pokémon.
Returns:
- dict: A message indicating the successful deletion of the Pokémon.
"""

@router.patch("/pokemons/{pokemon_name}/trainers/{trainer_name}")
def delete_pokemon_of_trainer(trainer_name: str, pokemon_name: str):
        if not pokemon.pokemon_exists(pokemon_name):
            raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")
        if not trainer.trainer_exists(trainer_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
        if not trainer.trainer_has_pokemon(trainer_name, pokemon_name):
            raise HTTPException(status_code=404, detail=f"{trainer_name} does not have {pokemon_name} pokemon")
        pokemon.delete_pokemon_of_trainer(trainer_name, pokemon_name)
        return {"message": "Pokemon deleted successfully"}


"""
 Add a new Pokémon to the database.
 This endpoint adds a new Pokémon to the database if it does not already exist.
 It fetches the Pokémon information from an external source and inserts it into the database.
 Parameters:
 - pokemon_name: str - The name of the Pokémon to be added.
 Raises:
 - HTTPException: 409 if the Pokémon already exists in the database.
 - HTTPException: 404 if the Pokémon information cannot be found.
 Returns:
 - dict: A message indicating the successful addition of the Pokémon.
 """
@router.post("/pokemons")
def add_pokemon(pokemon_name: str):
    if pokemon.pokemon_exists(pokemon_name):
        raise HTTPException(status_code=409, detail=f"{pokemon_name} pokemon is already in the database.")
    pokemon_info = get_pokemon_info(pokemon_name)
    if not pokemon_info:
        raise HTTPException(status_code=404, detail=f"{pokemon_name} not found.")
    pokemon.insert_pokemon(pokemon_info)
    return {"message": "Pokemon added successfully"}
