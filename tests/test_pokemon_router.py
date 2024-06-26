import pytest
from fastapi.testclient import TestClient
from pokemon_api.tables_server.tables_server import server

# Create a TestClient
client = TestClient(server)


# Define test cases
def test_get_pokemons_type():
    response = client.get("/pokemons?type=fire")
    assert response.status_code == 200
    assert response.json() == ["charmander", "charmeleon", "charizard", "vulpix", "ninetales", "growlithe", "arcanine",
                               "ponyta", "rapidash", "magmar", "flareon", "moltres"]


def test_get_pokemons_trainer_name():
    response = client.get("/pokemons?trainer_name=Drasna")
    assert response.status_code == 200
    assert response.json() == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian",
                               "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]


def test_get_pokemons_both_params():
    response = client.get("/pokemons?type=Electric&trainer_name=Ash")
    assert response.status_code == 400
    assert response.json() == {"detail": "Specify either type or trainer_name, not both."}


def test_get_pokemons_no_params():
    response = client.get("/pokemons")
    assert response.status_code == 400
    assert response.json() == {"detail": "Specify at least one query parameter: type or trainer_name."}


def test_add_pokemon_success():
    response = client.post("/pokemons?pokemon_name=yanma")
    assert response.status_code == 200
    assert response.json() == {"message": "Pokemon added successfully"}
    response = client.get(("/pokemons?type=bug"))
    result = response.json()
    assert "yanma" in result
    response = client.get(("/pokemons?type=flying"))
    result = response.json()
    assert "yanma" in result

