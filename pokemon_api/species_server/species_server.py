from fastapi import FastAPI, HTTPException
import requests
import base64

server = FastAPI()

TABLES_SERVICE_URL = "http://tables_service:5000"
IMAGE_SERVICE_URL = "http://image_service:8001"

@server.get("/pokemons/species/{species}")
def get_pokemon_by_species(species: str):
    # Get Pokémon details
    response = requests.get(f'{TABLES_SERVICE_URL}/pokemons/species/{species}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    pokemon_data = response.json()

    # Get Pokémon image
    image_response = requests.get(f'{IMAGE_SERVICE_URL}/images/{species}', stream=True)
    if image_response.status_code != 200:
        raise HTTPException(status_code=image_response.status_code, detail=image_response.text)
    
    # Encode image content to base64
    image_content = base64.b64encode(image_response.content).decode('utf-8')

    # Add image content to the response
    pokemon_data["image"] = image_content

    return pokemon_data
