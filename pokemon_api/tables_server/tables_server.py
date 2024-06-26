from fastapi import FastAPI
from pokemon_api.routes import pokemon_router, trainer_router, evolve_router

server = FastAPI()

server.include_router(pokemon_router.router)
server.include_router(trainer_router.router)
server.include_router(evolve_router.router)
