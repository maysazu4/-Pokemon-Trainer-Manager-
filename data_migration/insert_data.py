import sys
import os

import requests
from pymongo import MongoClient
from gridfs import GridFS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from Queries import database




def insert_image_from_pokeapi(fs, pokemon):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon['id']}")
    if response.status_code == 200:
        data = response.json()
        image_url = data['sprites']['front_default']
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_id = fs.put(image_response.content, filename=pokemon["name"], _id=pokemon["id"])
                return image_id
    return None


'''
Inserts a single type to the types table
'''
def insert_single_type(connection, type_name):
    database.execute_query(connection,
        "INSERT INTO Type (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name",
                           (type_name,)
                           )
    return connection.cursor().lastrowid
'''
Inserts single pokemon to the pokemen table and its type to the pokemenType table 
'''
def insert_pokemon(connection, pokemon, type_name):
    database.execute_query(connection,
        "INSERT IGNORE INTO Pokemon (id, name, height, weight) VALUES (%s, %s, %s, %s)",
                           (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
                           )
    database.execute_query(connection,
        "INSERT IGNORE INTO PokemonType (pokemon_id, type_name) VALUES (%s, %s)",
                           (pokemon["id"], type_name)
                           )
'''
Insert data into the pokemon table and save images to MongoDB
'''
def insert_into_pokemons_and_types(data, connection, fs):
    for pokemon in data:
        # Insert image into MongoDB
        image_id = insert_image_from_pokeapi(fs, pokemon)
        if not image_id:
            print(f"Failed to retrieve image for Pokemon ID {pokemon['id']}")
        # Insert pokemon data into MySQL
        if isinstance(pokemon["type"], str):
            insert_single_type(connection, pokemon["type"])
            insert_pokemon(connection, pokemon, pokemon["type"])
        elif isinstance(pokemon["type"], list):
            for type_name in pokemon["type"]:
                insert_single_type(connection, type_name)
                insert_pokemon(connection, pokemon, type_name)
'''
Insert data into the trainer table
'''
def insert_into_trainer(data, connection):
    trainers = set()
    for pokemon in data:
        for trainer in pokemon["ownedBy"]:
            trainers.add((trainer["name"], trainer["town"]))

    for trainer in trainers:
        database.execute_query(connection,
            "INSERT IGNORE INTO Trainer (name, town) VALUES (%s, %s)",
                               trainer
                               )
'''
Insert data into the ownership table
'''
def insert_into_ownership(data, connection):
    for pokemon in data:
        for trainer in pokemon["ownedBy"]:
            database.execute_query(connection,
                "INSERT IGNORE INTO Ownership (trainer_name, pokemon_id) VALUES (%s, %s)",
                                   (trainer["name"], pokemon["id"])
                                   )
'''
Inserts all the data in the json files to MySql database
'''
def insert_data():
    # Load JSON data
    with open('POKEMONS/pokemons_data.json') as file:
        data = json.load(file)

    # Connect to MySQL database
    connection = database.connect_to_database()

    fs = database.connect_to_mongodb()

    insert_into_pokemons_and_types(data, connection, fs)

    insert_into_trainer(data,connection)
    insert_into_ownership(data, connection)

    # Commit changes and close connection
    database.close_connection(connection)

insert_data()