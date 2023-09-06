"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#todos los miembros de la familia
@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "msg": "Estos son los miembros de la familia",
        "family": members
    }

    if members == []:
        return jsonify({"msg": "No hay miembros registrados"}), 404

    return jsonify(members), 200

#traer miembros de la familia por id
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
     #hacemos la consulta filtrando el usuario por id
    member = jackson_family.get_member(member_id)

    

    return member, 200

@app.route('/member', methods=['POST'])
def add_member():
    # this is how you can use the Family datastructure by calling its methods
    new_member = json.loads(request.data)
    jackson_family.add_member(new_member)

    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # this is how you can use the Family datastructure by calling its methods
    jackson_family.delete_member(member_id)

    return jsonify({'done':True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
