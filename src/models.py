from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Como puedo bloquear el correo para que forzosamente el campo introducido tenga que ser @gmail.com o @hotmail?
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    '''
    Como pedir que incluya al menos 1 numero e indicar restricciones en el dato guardado?
    Es obligatorio por tanto que el dato sea un string?
    '''
    subscription_date = db.Column(db.Integer, unique=False, nullable=False)
    # Como puedo hacer que la fecha sea un dato con /// o --- y sea aceptado el input en admin?
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)


    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "subscription_date": self.subscription_date,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }

class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faction_name = db.Column(db.String(120), unique=True, nullable=False)
    planets_under_control = db.Column(db.Integer, unique=False, nullable=True)
    army = db.Column(db.Integer, unique=False, nullable=True)
    leader = db.Column(db.String(120), unique=True, nullable=False)
    starships = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"<Faction {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "faction_name": self.faction_name,
            "planets_under_control": self.planets_under_control,
            "army": self.army,
            "leader": self.leader,
            "starships": self.starships
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    planet = db.Column(db.String(120), unique=False, nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey("planet.id"))
    # Añadir aquí mi user relationship
    faction = db.Column(db.String(120), unique=False, nullable=True)
    faction_id = db.Column(db.Integer, ForeignKey("faction.id"))
    # Añadir aquí mi faction relationship

    def __repr__(self):
        return f"<Character {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "planet": self.planet,
            "faction": self.faction
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(120), unique=False, nullable=False)
    planet_name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=True)
    faction = db.Column(db.String(120), unique=False, nullable=True)
    faction_id = db.Column(db.Integer, ForeignKey("faction.id"))
    # Añadir aquí mi faction relationship

    def __repr__(self):
        return f"<Planet {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "system_name": self.system_name,
            "population": self.population,
            "faction": self.faction
            # do not serialize the password, its a security breach
        }
    
# Aquí vendrían los favoritos que aun no sabemos como hacer la relacion en este modelo de plantilla