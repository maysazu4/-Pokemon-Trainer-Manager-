from fastapi import FastAPI, HTTPException, UploadFile,Query ,File,Response ,Request
from fastapi.responses import StreamingResponse
import requests
from fastapi.templating import Jinja2Templates


server = FastAPI()

TABLES_SERVICE_URL = 'http://tables_service:5000'
IMAGE_SERVICE_URL = 'http://image_service:8001'
SPECIES_SERVICE_URL = "http://species_service:8002"

templates = Jinja2Templates(directory="pokemon_api/gateway_server/templates")

@server.get("/pokemons/species/{species}")
async def get_pokemon_by_species(species: str):
    response = requests.get(f'{SPECIES_SERVICE_URL}/pokemons/species/{species}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@server.get("/pokemons/species/{species}/view")
async def view_pokemon_image(request: Request, species: str):
    response = requests.get(f'{SPECIES_SERVICE_URL}/pokemons/species/{species}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    pokemon_data = response.json()
    return templates.TemplateResponse("pokemon_image.html", {
        "request": request,
        "name": pokemon_data['name'],
        "image": pokemon_data['image']
    })

@server.get("/pokemons")
def get_pokemons(type: str = Query(None), trainer_name: str = Query(None)):
    params = {}
    if type:
        params['type'] = type
    if trainer_name:
        params['trainer_name'] = trainer_name

    response = requests.get(f'{TABLES_SERVICE_URL}/pokemons', params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()



@server.patch("/pokemons/{pokemon_name}/trainers/{trainer_name}")
def delete_pokemon_of_trainer(trainer_name: str, pokemon_name: str):
    response = requests.patch(f'{TABLES_SERVICE_URL}/pokemons/{pokemon_name}/trainers/{trainer_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@server.post("/pokemons")
def add_pokemon(pokemon_name: str):
    params = {}
    if pokemon_name:
        params['pokemon_name'] = pokemon_name
    
    response = requests.post(f'{TABLES_SERVICE_URL}/pokemons', params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    response = requests.post(f'{IMAGE_SERVICE_URL}/images/{pokemon_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()



@server.get("/trainers")
def get_trainers_by_pokemon(pokemon_name: str):
    params = {}
    if pokemon_name:
        params['pokemon_name'] = pokemon_name
    
    response = requests.get(f'{TABLES_SERVICE_URL}/trainers', params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@server.post("/trainers")
def add_pokemon_to_trainer(trainer_name: str, pokemon_name: str):
    params = {}
    if trainer_name:
        params['trainer_name'] = trainer_name
    if pokemon_name:
        params['pokemon_name'] = pokemon_name
    
    response = requests.post(f'{TABLES_SERVICE_URL}/trainers', params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()



@server.patch("/trainers/{trainer_name}/pokemons/{pokemon_name}")
async def evolve_pokemon(trainer_name: str, pokemon_name: str):
    response = requests.patch(f'{TABLES_SERVICE_URL}/trainers/{trainer_name}/pokemons/{pokemon_name}')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    # if we get here the pokemon was added, so add its image to the database
    evolved_data = response.json()  # Assuming this contains evolved Pokémon data
    evolved_pokemon_name = evolved_data.get("evolved_pokemon_name")
    response1 = requests.post(f'{IMAGE_SERVICE_URL}/images/{evolved_pokemon_name}')
    if response1.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()


@server.post("/images/")
async def save_image(file: UploadFile = File(...)):
    files = {"file": (file.filename, await file.read(), file.content_type)}
    response = requests.post(f'{IMAGE_SERVICE_URL}/images/', files=files)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@server.get("/images/{file_id}")
async def read_image(file_id: str):
    response = requests.get(f'{IMAGE_SERVICE_URL}/images/{file_id}', stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return StreamingResponse(response.raw, media_type=response.headers['Content-Type'])