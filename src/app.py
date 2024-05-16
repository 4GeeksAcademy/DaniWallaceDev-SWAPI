"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Faction
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = map(lambda user: user.serialize(),all_users)

    return jsonify(list(results)), 200

@app.route('/character', methods=['GET'])
def get_character():
    all_characters = Character.query.all()
    results = map(lambda character: character.serialize(),all_characters)

    return jsonify (list(results)), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planets = Planet.query.all()
    results = map(lambda planet: planet.serialize(),all_planets)

    return jsonify (list(results)), 200

@app.route('/faction', methods=['GET'])
def get_faction():
    all_factions = Faction.query.all()
    results = map(lambda faction: faction.serialize(),all_factions)

    return jsonify (list(results)), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    user_to_create = User(**user_data)

    db.session.add(user_to_create)
    db.session.commit()

    return jsonify(user_to_create.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"Deleted": f"The user was deleted"}), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    character_fav = Favorite_character.query.filter_by(user_id=user_id).all()
    planet_fav = Favorite_planet.query.filter_by(user_id=user_id).all()
    favorites = character_fav + planet_fav
    show_favorites = list(map(lambda fav: fav.serialize(), favorites))

    return jsonify(show_favorites), 200

@app.route('/users/<int:user_id>/favorites/characters', methods=['POST'])
def add_favorites_characters(user_id):
    character_data = request.json
    character_id = character_data["character_id"]

    new_favorite_character = Favorite_character(character_id=character_id, user_id=user_id)
    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify(new_favorite_character.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
