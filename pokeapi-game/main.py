import requests
import random
import os


# Public PokeAPI
API_BASE_URL = "https://pokeapi.co/api/v2"
POKEMON_LIST_URL = f"{API_BASE_URL}/pokemon?limit=10000&offset=0"

# Backend API
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5000")


def save_pokemon_to_backend(pokemon):
    response = requests.post(f"{BACKEND_API_URL}/pokemon", json=pokemon)
    if response.status_code == 201:
        print(f"Pokémon {pokemon['name']} saved to backend.")
    else:
        print(f"Error saving Pokémon: {response.text}")

def get_pokemon_from_backend(name):
    response = requests.get(f"{BACKEND_API_URL}/pokemon/{name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_pokemon_data(name_or_id):
    if str(name_or_id).isdigit():
        # Always fetch by ID from public PokeAPI
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

        existing = get_pokemon_from_backend(pokemon_info['name'])
        if not existing:
            save_pokemon_to_backend(pokemon_info)

        return pokemon_info

    else:
        # Look up by name in backend first
        found = get_pokemon_from_backend(name_or_id)
        if found:
            return found

        # If not found, get from public PokeAPI
        url = f"{POKEAPI_BASE_URL}/pokemon/{name_or_id}"
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

        save_pokemon_to_backend(pokemon_info)
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
