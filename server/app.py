#!/usr/bin/env python3

#flask db init has already been run. 
#You will need to direct your Flask app to a database at app.db, create models, 
#run a migration with flask db revision --autogenerate -m'<your message>' and create the database file with flask db upgrade.

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    display = f''
    display += f'<ul>ID: {animal.id}</ul>'
    display += f'<ul>Name: {animal.name}</ul>'
    display += f'<ul>Species: {animal.species}</ul>'
    display += f'<ul>Zookeeper: {animal.zookeeper.name}</ul>'
    display += f'<ul>Enclosure: {animal.enclosure.environment}</ul>'
    return make_response(display)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    #zookeeper contains:
    # - list of animals
    display = f''
    display += f'<ul>ID: {zookeeper.id}</ul>'
    display += f'<ul>Name: {zookeeper.name}</ul>'
    display += f'<ul>Birthday: {zookeeper.birthday}</ul>'

    for animal in zookeeper.animals:
        display += f'<ul>Animal:{animal.name}</ul>'

    return make_response(display)

# id = db.Column(db.Integer, primary_key=True)
#     environment = db.Column(db.String)
#     open_to_visitors = db.Column(db.Boolean)

#     animals = db.relationship('Animal', back_populates='enclosure')
@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    display = f''
    display += f'<ul>Id: {enclosure.id}</ul>'
    display += f'<ul>Environment: {enclosure.environment}</ul>'
    display += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'
    for animal in enclosure.animals:
        display += f'<ul>Animal: {animal.name}</ul>'

    return make_response(display)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
