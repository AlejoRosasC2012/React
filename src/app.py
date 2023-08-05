from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
from pymongo import MongoClient 

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonreactdb'
mongo = PyMongo(app)

CORS(app)


db = mongo.db.users

#Crear un Usuario
@app.route('/users', methods=['POST'])
def createUser():


    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })

    result = str(id.inserted_id)

    return result

#Consultar Usuarios
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password'],
        })
    return jsonify(users)

#Consultar un solo Usuario
@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password'],
    })

#Eliminar un Usuario
@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({"msg": 'User deleted'})

#Actualizar un Usuario
@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    print(id)
    print(request.json)

    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password'],
    }})
    return jsonify({"msg": 'User updated'})

if __name__ == "__main__":
    app.run(debug=True)