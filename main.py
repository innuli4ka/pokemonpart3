import requests
import random
from db import get_pokemon_from_db, save_pokemon_to_db, create_table_if_not_exists

API_BASE_URL = "https://pokeapi.co/api/v2"
POKEMON_LIST_URL = f"{API_BASE_URL}/pokemon?limit=10000&offset=0"

create_table_if_not_exists()


def get_pokemon_data(name_or_id):
    # Check if name_or_id is numeric (ID case)
    if str(name_or_id).isdigit():
        # Always fetch from API by ID
        url = f"{API_BASE_URL}/pokemon/{name_or_id}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error: Pokémon not found.")
            return None

        data = response.json()
        pokemon_info = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]]
        }

        existing = get_pokemon_from_db(pokemon_info['name'])
        if not existing:
            save_pokemon_to_db(pokemon_info)

        return pokemon_info
    else:
        # Search by name → check Dynamo first
        found = get_pokemon_from_db(name_or_id)
        if found:
            return found

        # Not in DB → fetch from API
        url = f"{API_BASE_URL}/pokemon/{name_or_id}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error: Pokémon not found.")
            return None

        data = response.json()
        pokemon_info = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]]
        }

        save_pokemon_to_db(pokemon_info)
        return pokemon_info

def print_pokemon_info(pokemon):
    print(f"ID: {pokemon['id']}")
    print(f"Name: {pokemon['name']}")
    print(f"Height: {pokemon['height']}")
    print(f"Weight: {pokemon['weight']}")
    print(f"Types: {', '.join(pokemon['types'])}")

def get_random_pokemon_data():
    response_random = requests.get(POKEMON_LIST_URL)
    data_random = response_random.json()
    results = data_random["results"]

    random_pokemon = random.choice(results)
    random_name = random_pokemon["name"]

    return get_pokemon_data(random_name)