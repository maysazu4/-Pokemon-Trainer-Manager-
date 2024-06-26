# pokemonAPI

## Project Overview:
This project involves the migration of Pokémon data from a JSON file to a relational database using SQL. Additionally, it includes the development of a Pokémon API to perform various operations related to Pokémon and trainers, including adding new Pokémon species, retrieving Pokémon by type or trainer, deleting Pokémon of a trainer, adding Pokémon to a trainer, and evolving Pokémon.

## Setup and Running the Project:

1. Clone the repository to your local machine.
2. Ensure you have Python installed, along with the required packages listed in `requirements.txt`.
3. Update the database connection details in the Python files according to your MySQL configuration.

### Running the Server:
To start the Pokémon API server using Uvicorn with auto-reloading enabled, run the following command in your terminal:
```bash
uvicorn pokemon_api.server:server --reload
```
## API Endpoints:

- `POST /pokemons?pokemon_name=<pokemon_name>`: Add new Pokémon species.
- `GET /pokemons?type=<type>`: Get Pokémon by type.
- `GET /pokemons?trainer_name=<trainer_name>`: Get Pokémon by trainer.
- `GET /trainers?pokemon=<pokemon_name>`: Get trainers of a Pokémon.
- `PATCH /pokemons/pokemon_name/trainers/trainer_name`: Delete Pokémon of a trainer.
- `POST /trainers?trainer_name=<trainer_name>&pokemon_name=<pokemon_name>`: Add Pokémon to a trainer.
- `PATCH /trainers/trainer_name/pokemons/pokemon_name`: Evolve Pokémon.

## Evolution Process:
To evolve a Pokémon:
1. Retrieve the information of the specific Pokémon.
2. Obtain the species URL from the Pokémon's general information.
3. Fetch the species information by making a request to the species URL.
4. Extract the evolution chain URL from the species information.
5. Retrieve the evolution chain information by making a request to the evolution chain URL.
6. Extract the chain item from the evolution chain information.
7. Scan the chain item to find the next form of the Pokémon.
8. Update the database accordingly to reflect the evolution.

## Additional Notes:

- Ensure that the MySQL database is running and accessible before starting the API server.
- Error handling and input validation are implemented to ensure the stability and security of the API.
- It's recommended to use appropriate authentication mechanisms to secure sensitive operations and endpoints in a production environment.

## Contributors:
- Aya Abbas 
- Maysa Zubedat
