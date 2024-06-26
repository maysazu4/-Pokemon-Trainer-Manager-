from fastapi.testclient import TestClient
from pokemon_api.tables_server.tables_server import server

client = TestClient(server)


def test_get_trainers_by_pokemon_success():
    response = client.get("/trainers?pokemon_name=charmander")

    # Check response status code
    assert response.status_code == 200

    # Check response JSON content
    assert response.json() == ["Giovanni", "Jasmine", "Whitney"]


def test_get_trainers_by_pokemon_not_found():
    response = client.get("/trainers?pokemon_name=MyPokemon")
    assert response.status_code == 404
    assert response.json() == {"detail": "MyPokemon pokemon not found."}

