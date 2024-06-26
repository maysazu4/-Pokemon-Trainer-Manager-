from Queries import database


def get_pokemons_of_type(type_name):
    connection = database.connect_to_database()
    query = """
    SELECT p.name FROM Pokemon p
    JOIN PokemonType pt ON pt.pokemon_id=p.id WHERE pt.type_name=%s;
    """
    result = database.execute_and_fetch_query(connection, query, (type_name,))
    return result

def delete_pokemon_of_trainer(trainer_name, pokemon_name):
    connection = database.connect_to_database()
    query = """
    DELETE FROM Ownership 
    WHERE pokemon_id = (SELECT id FROM Pokemon WHERE name = %s )
    AND trainer_name = %s ;
    """
    database.execute_query(connection, query, (pokemon_name, trainer_name,))

def get_trainers_by_pokemon(name):
    connection = database.connect_to_database()

    query = """
    SELECT o.trainer_name
    FROM Ownership o
    JOIN Pokemon p ON p.id = o.pokemon_id
    WHERE p.name = %s;
    """
    result = database.execute_and_fetch_query(connection, query, (name,))
    
    return result

   
def get_pokemon_by_species(name):
    connection = database.connect_to_database()

    query = """
    SELECT id, name, height, weight 
    FROM Pokemon 
    WHERE name = %s;
    """
    result = database.execute_and_fetch_query(connection, query, (name,))
    return result

    
def get_pokemons_by_trainer(name):
    connection = database.connect_to_database()

    query = """
    SELECT p.name
    FROM Pokemon p
    JOIN Ownership o ON p.id = o.pokemon_id
    WHERE o.trainer_name = %s;
    """
    result = database.execute_and_fetch_query(connection, query, (name,))
    return result

def type_exists(type):
    connection = database.connect_to_database()
    query = """
    SELECT name 
    FROM Type 
    WHERE name=%s;
    """
    result = database.execute_and_fetch_query(connection, query, (type,))
    return len(result) != 0

def pokemon_exists(pokemon_name):
    connection = database.connect_to_database()
    query = """
    SELECT id 
    FROM Pokemon 
    WHERE name=%s;
    """

    result = database.execute_and_fetch_query(connection, query, (pokemon_name,))

    return len(result) != 0

def insert_pokemon(pokemon_info):
    connection = database.connect_to_database()
    try:
        # Start a transaction
        cursor = connection.cursor()

        # Insert into pokemon table
        cursor.execute(
            "INSERT IGNORE INTO Pokemon (id, name, height, weight) VALUES (%s, %s, %s, %s)",
            (pokemon_info[0], pokemon_info[1], pokemon_info[2], pokemon_info[3])
        )

        # Insert into pokemonType table
        types = pokemon_info[4]
        for type_ in types:
            cursor.execute(
                "INSERT IGNORE INTO PokemonType (pokemon_id, type_name) VALUES (%s, %s)",
                (pokemon_info[0], type_)
            )

        # Commit the transaction
        connection.commit()
        return f"Successfully inserted Pokémon '{pokemon_info[1]}' with ID '{pokemon_info[0]}'."
    except Exception as e:
        connection.rollback()
        return f"Failed to insert Pokémon '{pokemon_info[1]}' with ID '{pokemon_info[0]}': {str(e)}"
    finally:
        connection.close()
