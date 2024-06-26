from fastapi import APIRouter, HTTPException
from Queries import trainer, pokemon

router = APIRouter()

"""
Get a list of trainers who own a specific Pokémon.
Args:
    pokemon_name (str): The name of the Pokémon.
Returns:
    List[str]: A list of trainer names.
Raises:
    HTTPException: If no trainers are found for the given Pokémon.
"""
@router.get("/trainers")
def get_trainers_by_pokemon(pokemon_name: str):
    if not pokemon.pokemon_exists(pokemon_name):
        raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")

    trainers = pokemon.get_trainers_by_pokemon(pokemon_name)
    if len(trainers) < 1:
        raise HTTPException(status_code=404, detail="No trainers found for the given Pokémon.")
    return trainers

"""
Add a Pokémon to a trainer's collection.
Args:
    trainer_name (str): The name of the trainer.
    pokemon_name (str): The name of the Pokémon.
Returns:
    dict: A confirmation message with trainer and Pokémon names.
Raises:
    HTTPException: If the insertion fails due to a database error or invalid data.
"""
@router.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):

    if not trainer.trainer_exists(trainer_name):
        raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
    result = trainer.insert_into_ownership(pokemon_name, trainer_name)
    if "Failed" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"message": result}
