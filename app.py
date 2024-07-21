from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, primary_key=True)
    description = db.Column(db.String(120))


@app.route('/')
def index():
    return 'hello'

@app.route('/drinks')
def get_drinks():
    return {'drinks': 'drink_data'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
    # db.create_all()
    ...
