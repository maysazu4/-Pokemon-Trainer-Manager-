from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pymongo import MongoClient
from gridfs import GridFS
from io import BytesIO
import requests
from Queries import database

server = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://mongo:27017/")
db = client.pokemon_db
fs = GridFS(db)

@server.post("/images/{pokemon_name}")
async def save_image(pokemon_name: str):
    
   
        # Fetch image from PokeAPI
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Pokemon not found on PokeAPI")
    
        data = response.json()
        pokemon_id = data['id']
         # Connect to MongoDB
        fs = database.connect_to_mongodb()
        if fs.exists({"_id": pokemon_id}):
            raise HTTPException(status_code=400, detail="Pokemon image already exists in MongoDB")
        image_url = data['sprites']['front_default']
        if not image_url:
            raise HTTPException(status_code=404, detail="Pokemon image not found")

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch Pokemon image")

        fs.put(image_response.content, filename=data['name'], _id=pokemon_id)
        return {"detail": "Pokemon image saved successfully"}


# Read image from DB
@server.get("/images/{pokemon_name}")
async def get_pokemon_image(pokemon_name: str):
    image = fs.find_one({"filename": pokemon_name})
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return StreamingResponse(BytesIO(image.read()), media_type="image/png")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8001)
