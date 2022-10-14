from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS


app = Flask(__name__)
app.config['MONGO_URI']='mongodb://127.0.0.1/Plantas_medicinalesDB'
mongo = PyMongo(app)

CORS(app)
#BADE DE DATOS
db = mongo.db.Plantas_medicinales

@app.route('/Plantas_medicinales', methods=['POST']) #Vamos a tener una ruta para poder crear usuarios
def createPlantas_medicinales():
    print(request.json)
    id = db.insert_one({
            'nombre_cientifico': request.json['nombre_cientifico'],
            'nombre_planta': request.json['nombre_planta'],
            'propiedades': request.json['propiedades'],
            'descripcion': request.json['descripcion'],
            'conocimiento_ancestral': request.json['conocimiento_ancestral'],
            'imagen': request.files['imagen'],
            'latitud': request.json['latitud'],
            'longitud': request.json['longitud']
        })
    return jsonify(str(id.inserted_id)) #muestra el id de un usuario

@app.route('/Plantas_medicinales', methods=['GET']) #Vamos a tener una ruta para obtener usuarios
def getPlantas_medicinales():
    Plantas_medicinales = []
    for doc in db.find():#vamos ir anadiendo por cada documento e la lista
        Plantas_medicinales.append({
            '_id': str(ObjectId(doc['_id'])), #nos va a mostrar el id en str
            'nombre_cientifico': doc['nombre_cientifico'],
            'nombre_planta': doc['nombre_planta'],
            'propiedades': doc['propiedades'],
            'descripcion': doc['descripcion'],
            'conocimiento_ancestral': doc['conocimiento_ancestral'],
            'imagen': doc['imagen'],
            'latitud': doc['latitud'],
            'longitud': doc['longitud']
        })

    return jsonify(Plantas_medicinales)


@app.route('/Plantas_medicinale/<id>', methods=['GET']) #Vamos a tener una ruta para crear usuarios
def getPlantas_medicinale(id):
    Plantas_medicinale = db.find_one({'_id': ObjectId(id)})#va a retorar un administrador
    #print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Plantas_medicinale['_id'])),
        'nombre_cientifico': Plantas_medicinale['nombre_cientifico'],
        'nombre_planta': Plantas_medicinale['nombre_planta'],
        'propiedades': Plantas_medicinale['propiedades'],
        'descripcion': Plantas_medicinale['descripcion'],
        'conocimiento_ancestral': Plantas_medicinale['conocimiento_ancestral'],
        'imagen': Plantas_medicinale['imagen'],
        'latitud': Plantas_medicinale['latitud'],
        'longitud': Plantas_medicinale['longitud']


    })

@app.route('/Plantas_medicinales/<id>', methods=['DELETE']) #Vamos a tener una ruta para crear usuarios
def deletePlantas_medicinales(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'dato eliminado'})

@app.route('/Plantas_medicinales/<id>', methods=['PUT']) #Vamos a tener una ruta para crear usuarios
def updatePlantas_medicinales(id):
    db.update_one({'_id': ObjectId(id)}, {'$set':{
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.files['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']

    }})
    return jsonify({'msg': 'dato actualizado'})


#if __name__ == "__main__":
    #app.run(debug=True)


###############################################################################################################
# USUARIOS


