from flask import Flask, flash, jsonify, request, Blueprint, Response
from flask_pymongo import PyMongo, ObjectId
from flask_pymongo import pymongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from routes.files import routes_files
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import numpy as np
import base64
import cv2
#from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__, static_url_path='', static_folder='backend/static')
# app = Flask(__name__)
# app.config['MONGO_URI']='mongodb://127.0.0.1/Plantas_medicinalesDB'
# mongo = PyMongo(app)
CONNECTION = 'mongodb+srv://yoselin:123@cluster0.sfj6m.mongodb.net/test'

client = pymongo.MongoClient(CONNECTION)
mongo = client.get_database('Plantas_MedicinalesDB')
db = mongo.Administrador

cors = CORS(app)
# BASE DE DATOS
# db = mongo.db.Administrador
app.register_blueprint(routes_files)

@app.route('/Administrador-login', methods=['POST'])
def validateUser():
    print(request.json)
    # if key doesn't exist, returns None
    email = request.json['email']
    contrasena = request.json['contrasena']
    #nombre = request.json['nombre']

    result = db.find_one({"email": email})
    if result is None:
        return jsonify({"Error": "no autorizado"}), 401

    if not check_password_hash(result['contrasena'], contrasena):
        return jsonify({"error": "contrasena incorrecta"}), 401

    response = jsonify({'email': email, 'constrasenaaaa': contrasena})
    response.headers.add('Access-Control-Allow-Origin', '*')
    # if key doesn't exist, returns a 400, bad request error
    return response
    # return jsonify(contrasena)

# Vamos a tener una ruta para poder crear usuarios


@app.route('/Administrador', methods=['POST'])
def createUsers():
    # print(json.loads(request.data))
    print(request.json)

    encriptado = generate_password_hash(request.json['contrasena'])

    id = db.insert_one(
        {'nombre': request.json['nombre'], 'email': request.json['email'], 'contrasena': encriptado})

    return jsonify(str(id.inserted_id))  # muestra el id de un usuario


# Vamos a tener una ruta para obtener usuarios
@app.route('/Administrador', methods=['GET'])
def getUsers():
    Administrador = []
    for doc in db.find():  # vamos ir anadiendo por cada documento e la lista
        Administrador.append({
            '_id': str(ObjectId(doc['_id'])),  # nos va a mostrar el id en str
            'nombre': doc['nombre'],
            'email': doc['email'],
            'contrasena': doc['contrasena']
        })

    return jsonify(Administrador)

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrado/<id>', methods=['GET'])
def getUser(id):
    # va a retorar un administrador
    Administrado = db.find_one({'_id': ObjectId(id)})
    # print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Administrado['_id'])),
        'nombre': Administrado['nombre'],
        'email': Administrado['email'],
        'contrasena': Administrado['contrasena']
    })

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrador/<id>', methods=['DELETE'])
def deleteUsers(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'usuario eliminado'})

# Vamos a tener una ruta para crear usuarios


@app.route('/Administrador/<id>', methods=['PUT'])
def updateUsers(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre': request.json['nombre'],
        'email': request.json['email'],
        'contrasena': request.json['contrasena']
    }})
    return jsonify({'msg': 'usuario actualizado'})


################################################################################################################
# PLANTAS

# db1 = mongo.db.Plantas_medicinales
db1 = mongo.Plantas_medicinales


# Vamos a tener una ruta para poder crear usuarios
@app.route('/Plantas_medicinales', methods=['POST'])
def createPlantas_medicinales():
    print(request.json)
    id = db1.insert_one({
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    })

    return jsonify(str(id.inserted_id))  # muestra el id de un usuario


# Vamos a tener una ruta para obtener usuarios
@app.route('/Plantas_medicinales', methods=['GET'])
def getPlantas_medicinales():
    Plantas_medicinales = []
    for doc in db1.find():  # vamos ir anadiendo por cada documento e la lista
        Plantas_medicinales.append({
            '_id': str(ObjectId(doc['_id'])),  # nos va a mostrar el id en str
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


# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinale/<id>', methods=['GET'])
def getPlantas_medicinale(id):
    # va a retorar un administrador
    Plantas_medicinale = db1.find_one({'_id': ObjectId(id)})
    # print(Administrado)
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

# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinales/<id>', methods=['DELETE'])
def deletePlantas_medicinales(id):
    db1.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'dato eliminado'})

# Vamos a tener una ruta para crear usuarios
@app.route('/Plantas_medicinales/<id>', methods=['PUT'])
def updatePlantas_medicinales(id):
    db1.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre_cientifico': request.json['nombre_cientifico'],
        'nombre_planta': request.json['nombre_planta'],
        'propiedades': request.json['propiedades'],
        'descripcion': request.json['descripcion'],
        'conocimiento_ancestral': request.json['conocimiento_ancestral'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    }})
    # return jsonify({'msg': 'dato actualizado'})
    response = jsonify({'hola': 'hola'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


##########################################################################################################
#LOCALIZACION

db2 = mongo.Geolocalizacion


# Vamos a tener una ruta para poder crear usuarios
@app.route('/Localizacion', methods=['POST'])
def createLocalizacion():
    print(request.json)
    id = db2.insert_one({
        'nombre_planta': request.json['nombre_planta'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    })

    return jsonify(str(id.inserted_id))  # muestra el id de un usuario


@app.route('/savePredict', methods=['POST'])
def create():
    print(request.json)

    id = db2.insert_one({
        'nombre_planta': request.json['nombre_planta'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    })

    return jsonify('ok')

# Vamos a tener una ruta para obtener usuarios
@app.route('/Localizacion', methods=['GET'])
def getLocalizacion():
    Localizacion = []
    for doc in db2.find():  # vamos ir anadiendo por cada documento e la lista
        Localizacion.append({
            '_id': str(ObjectId(doc['_id'])),  # nos va a mostrar el id en str
            'nombre_planta': doc['nombre_planta'],
            'imagen': doc['imagen'],
            'latitud': doc['latitud'],
            'longitud': doc['longitud']
        })

    return jsonify(Localizacion)


# Vamos a tener una ruta para crear usuarios
@app.route('/Localizacio/<id>', methods=['GET'])
def getLocalizacio(id):
    # va a retorar un administrador
    Localizacio = db2.find_one({'_id': ObjectId(id)})
    # print(Administrado)
    return jsonify({
        '_id': str(ObjectId(Localizacio['_id'])),
        'nombre_planta': Localizacio['nombre_planta'],
        'imagen': Localizacio['imagen'],
        'latitud': Localizacio['latitud'],
        'longitud': Localizacio['longitud']
    })

# Vamos a tener una ruta para crear usuarios
@app.route('/Localizacion/<id>', methods=['DELETE'])
def deleteLocalizacion(id):
    db2.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'dato eliminado'})

# Vamos a tener una ruta para crear usuarios
@app.route('/Localizacion/<id>', methods=['PUT'])
def updateLocalizacion(id):
    db2.update_one({'_id': ObjectId(id)}, {'$set': {
        'nombre_planta': request.json['nombre_planta'],
        'imagen': request.json['imagen'],
        'latitud': request.json['latitud'],
        'longitud': request.json['longitud']
    }})
    # return jsonify({'msg': 'dato actualizado'})
    response = jsonify({'hola': 'hola'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getinfoplant', methods=['POST'])
def getIDplant():
    # print(json.loads(request.data))
    print(request.json['nombre']) 
    nombre = request.json['nombre']
    result = db1.find_one({"nombre_planta": nombre})

    print(result['_id'])

    return jsonify({'result': str(result['_id'])})  # muestra el id de un usuario


##########################################################################################################
################# RECONOCIMIENTO PLANTAS ###################

width_shape = 320
height_shape = 320



@app.route('/prediccion img save', methods=['POST'])
def test():
    print('CREO QUE YA NO HAY ERROR')
    request.json['nombre']
    # NO SE TOCAAAAA
    img_data = b'',request.json
    img = img_data[1]['json']
    joselito = img.encode()
    fh = open(""+  request.json['nombre'], "wb")
    fh.write(base64.decodebytes(joselito))
    fh.close()
    
    return "OK"

names = ['ARRAYAN', 'EUCALIPTO', 'HINOJO', 'LLANTEN', 'MALVA', 'MANZANILLA', 'QUECHUARA', 'RUDA_BLANCA', 'RUDA_VERDE', 'WIRA_WIRA', 'DESCONOCIDO']
MODEL_PATH = './models/ptangente.h5'
model = load_model(MODEL_PATH)

def model_predict(img_path):

    imaget=cv2.resize(cv2.imread(img_path), (width_shape, height_shape), interpolation = cv2.INTER_AREA)

    xt = np.asarray(imaget)
    xt=preprocess_input(xt)
    xt = np.expand_dims(xt,axis=0)
    preds = model.predict(xt)
    return preds



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Obtiene el archivo del request
        # f = request.files['file']

        # # Graba el archivo en ./uploads
        # basepath = os.path.dirname(__file__)
        # file_path = os.path.join(
        #     basepath, 'uploads', secure_filename(f.filename))
        # f.save(file_path)

        # Predicción
        preds = model_predict(request.json['photo'])
        prediccion_hecha = names[np.argmax(preds)]

        print('PREDICCIÓN', prediccion_hecha)
        
        # Enviamos el resultado de la predicción
        # result = str(names[np.argmax(preds)])              
        # return result
        return prediccion_hecha

@app.route("/")
def index():
    return "HELLO YOOOS"

# if __name__ == "__main__":
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443)



