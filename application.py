from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
