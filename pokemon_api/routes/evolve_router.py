from fastapi import APIRouter, HTTPException
from Queries import trainer, pokemon
from pokemon_api.service.evolve_utils import get_evolved_pokemon
from pokemon_api.service.get_pokemon_info_utils import get_pokemon_info

router = APIRouter()


"""
 Evolve a Pokémon for a specific trainer.
 This endpoint checks if the given trainer and Pokémon exist, and if the trainer owns the Pokémon.
 If the Pokémon can evolve, it will be evolved and updated in the trainer's list.
 Parameters:
 - trainer_name: str - The name of the trainer.
 - pokemon_name: str - The name of the Pokémon to be evolved.
 Raises:
 - HTTPException: 404 if the trainer does not exist.
 - HTTPException: 404 if the Pokémon does not exist.
 - HTTPException: 404 if the trainer does not own the specified Pokémon.
 - HTTPException: 400 if the Pokémon cannot evolve.
 - HTTPException: 409 if the trainer already owns the evolved Pokémon.
 Returns:
 - dict: A message indicating the successful evolution of the Pokémon.
 """

@router.patch("/trainers/{trainer_name}/pokemons/{pokemon_name}")
async def evolve_pokemon(trainer_name: str, pokemon_name: str):

    if not trainer.trainer_exists(trainer_name):
        raise HTTPException(status_code=404, detail=f"{trainer_name} trainer not found.")
    if not pokemon.pokemon_exists(pokemon_name):
        raise HTTPException(status_code=404, detail=f"{pokemon_name} pokemon not found.")
    if not trainer.trainer_has_pokemon(trainer_name, pokemon_name):
        raise HTTPException(status_code=404, detail=f"{trainer_name} does not have {pokemon_name} pokemon")
    evolved_pokemon_name = await get_evolved_pokemon(pokemon_name)
    if not evolved_pokemon_name:
        raise HTTPException(status_code=400, detail=f"{pokemon_name} does not evolve")
    if trainer.trainer_has_pokemon(trainer_name, evolved_pokemon_name):
        raise HTTPException(status_code=409, detail=f"{trainer_name} already has {evolved_pokemon_name} pokemon")
    pokemon.delete_pokemon_of_trainer(trainer_name, pokemon_name)
    if not pokemon.pokemon_exists(evolved_pokemon_name):
        pokemon_info = get_pokemon_info(evolved_pokemon_name)
        pokemon.insert_pokemon(pokemon_info)
    trainer.insert_into_ownership(evolved_pokemon_name, trainer_name)
    return {"message": f"Evolved {pokemon_name} to {evolved_pokemon_name} for trainer {trainer_name}", "evolved_pokemon_name": evolved_pokemon_name}