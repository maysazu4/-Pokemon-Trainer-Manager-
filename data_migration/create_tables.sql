-- SQL script to create the necessary tables

-- Create the Pokemon table
CREATE TABLE IF NOT EXISTS Pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

-- Create the Type table
CREATE TABLE IF NOT EXISTS Type (
    name VARCHAR(255) PRIMARY KEY
);

-- Create the PokemonType table
CREATE TABLE IF NOT EXISTS PokemonType (
    pokemon_id INT,
    type_name VARCHAR(255),
    PRIMARY KEY (pokemon_id, type_name),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
    FOREIGN KEY (type_name) REFERENCES Type(name)
);

-- Create the Trainer table
CREATE TABLE IF NOT EXISTS Trainer (
    name VARCHAR(255) PRIMARY KEY,
    town VARCHAR(255) NOT NULL
);

-- Create the Ownership table
CREATE TABLE IF NOT EXISTS Ownership (
    trainer_name VARCHAR(255),
    pokemon_id INT,
    PRIMARY KEY (trainer_name, pokemon_id),
    FOREIGN KEY (trainer_name) REFERENCES Trainer(name),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id)
);
