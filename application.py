import re
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def as_dict(self):
        names = 'name description'.split()
        return {k: v for k, v in vars(self).items() if k in names}
        return {'name': self.name, 'description': self.description}

    def __repr__(self) -> str:
        return f'{self.name} - {self.description}'

@app.route('/')
def index():
    return 'hello'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    result = {'drinks': [drink.as_dict() for drink in drinks]}
    print(result)
    return result

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return drink.as_dict()

@app.route('/drinks', methods=['POST'])
def add_drink():
    print(request.json)
    drink = Drink(**request.json)
    try:
        db.session.add(drink)
        db.session.commit()
        return {'id': drink.id}
    except exc.IntegrityError:
        return {'error':f'drink {drink.name!r} already exists'}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if not drink:
        return {'error': 'not found'}
    
    db.session.delete(drink)
    db.session.commit()
    return {'message': 'deleted'}


if __name__ == '__main__':
    with app.app_context():
        # reset instance/data.db
        db.drop_all()
        # create instance/data.db
        db.create_all()
        # unnecessary because of drop_all()
        if not len(Drink.query.all()):
            for drink in [{'name':'Grapes', 'description': 'grapes juice'}, {'name':'Cherry', 'description': 'cherry juice'}]:
                drink = Drink(**drink)
                db.session.add(drink)
                db.session.commit()
        print(Drink.query.all())
    
    app.run(debug=True)
