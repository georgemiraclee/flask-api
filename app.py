from flask import Flask
from flask_restful import Api
from resources import Users, User, UserByName
from create_db import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
init_db(app)

api = Api(app)

# Tambahkan Resource ke API
api.add_resource(Users, '/api/users/', '/api/users/page/<int:page>')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(UserByName, '/api/users/name/<string:name>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
