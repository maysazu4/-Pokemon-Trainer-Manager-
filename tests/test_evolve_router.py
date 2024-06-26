from fastapi.testclient import TestClient
from Queries import pokemon
from pokemon_api.tables_server.tables_server import server

client = TestClient(server)


def test_evolve_pokemon_does_not_evolve():
    response = client.patch("/trainers/Misty/pokemons/pinsir")
    # Check response status code
    assert response.status_code == 400

    assert response.json() == {"detail": "pinsir does not evolve"}


def test_evolve_pokemon_trainer_do_not_have_pokemon():
    response = client.patch("/trainers/Archie/pokemons/spearow")
    # Check response status code
    assert response.status_code == 404
    assert response.json() == {"detail": "Archie does not have spearow pokemon"}


def test_evolve_pokemon_success():
    response = client.patch("/trainers/Whitney/pokemons/oddish")
    # Check response status code
    assert response.status_code == 200
    assert response.json() == {"message": "Evolved oddish to gloom for trainer Whitney"}
    response = client.patch("/trainers/Whitney/pokemons/oddish")
    assert response.status_code == 404
    assert response.json() == {"detail": "Whitney does not have oddish pokemon"}
    assert 'gloom' in pokemon.get_pokemons_by_trainer('Whitney')

def test_evolve_pokemon_already_have_evolved_pokemon():
    assert 'pikachu' and 'raichu' in pokemon.get_pokemons_by_trainer('Whitney')
    response = client.patch("/trainers/Whitney/pokemons/pikachu")
    assert response.status_code == 409
    assert response.json() == {"detail": "Whitney already has raichu pokemon"}
