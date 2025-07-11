from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Get MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/") #should change after I will dockarize the mongodb and app.py
# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['poke_db']
pokemon_collection = db['pokemons']

# POST /pokemon → Save Pokémon to MongoDB
@app.route('/pokemon', methods=['POST'])
def save_pokemon():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing Pokémon name"}), 400

    # Insert document
    pokemon_collection.insert_one(data)

    return jsonify({"message": f"Pokémon {data['name']} saved!"}), 201

# GET /pokemon/<name> → Retrieve Pokémon by name
@app.route('/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    result = pokemon_collection.find_one({"name": name})

    if result:
        result.pop('_id')  # Remove Mongo’s internal ID for clean JSON
        return jsonify(result), 200

    return jsonify({"error": "Pokémon not found"}), 404

if __name__ == '__main__':
    # Run on all interfaces inside container
    app.run(host="0.0.0.0", port=5000, debug=True)
