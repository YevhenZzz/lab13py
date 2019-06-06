from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'dbsqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
# Init ma
marshmallow = Marshmallow(app)


class Dress(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    size = database.Column(database.Integer)
    material_types = database.Column(database.Integer)

    def __init__(self, size, material_types):
        self.size = size
        self.material_types = material_types


class DressSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'size', 'material_types')


dress_schema = DressSchema(strict=True)
dresses_schema = DressSchema(many=True, strict=True)


@app.route('/dress', methods=['POST'])
def add_dress():
    size = request.json['size']
    material_types = request.json['material_types']

    new_dress = Dress(size, material_types)

    database.session.add(new_dress)
    database.session.commit()

    return dress_schema.jsonify(new_dress)


@app.route('/dress', methods=['GET'])
def get_all_dresses():
    all_dresses = Dress.query.all()
    result = dresses_schema.dump(all_dresses)
    return jsonify(result.data)


@app.route('/dress/<id>', methods=['GET'])
def get_dress(id):
    dress = Dress.query.get(id)
    return dress_schema.jsonify(dress)


@app.route('/dress/<id>', methods=['PUT'])
def update_dress(id):
    dress = Dress.query.get(id)

    size = request.json["size"]
    material_types = request.json["material_types"]

    dress.size = size
    dress.material_types = material_types

    database.session.commit()

    return  dress_schema.jsonify(dress)


@app.route('/dress/<id>', methods=['DELETE'])
def delete_dress(id):
    dress = Dress.query.get(id)
    database.session.delete(dress)
    database.session.commit()
    return dress_schema.jsonify(dress)


database.create_all()


if __name__ == '__main__':
    app.run(debug=True)
