# Amigo progrmador , si le va hacer mantenimineto a este codigo , le deseo suerte.
# Cuando este codigo fue creado solo dios y yo sabiamos como funcionaba , hoy en dia solo dios sabe
from flask import Flask, make_response, request
from microservices.scholar import main
from resources.ProcesarArchivoDocente import leerArchivoDocentes,Mensaje
from resources.ModificarFecha import CambiarFechaTope
from resources.ConsultarUltmimafecha import UltimaFecha,ActualizacionApi
#from resources.EnviarCorreo import enviar
from flask_cors import CORS
from flask_restful import Api
import os
from werkzeug.utils import secure_filename
from flask_restful import reqparse, abort, Api, Resource
import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.Teachers import TeachersInsertInitial, TeacherstUpdate
import requests
#UPLOAD_FOLDER = 'C:/Users/wilke/Desktop/Mari 10112018/test-backend-apis-master'
UPLOAD_FOLDER = os.getcwd() 
ALLOWED_EXTENSIONS = set(['csv'])
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class File(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
   
    def post(self,user):
        file = request.files['file']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            NombreArchivo=file.filename
            User=user
            data = {}
            data['Erros'] = []
            Error= leerArchivoDocentes(NombreArchivo,User,data)
            
            os.remove(NombreArchivo) 
            if(Error=="El Archivo csv ha sido procesado con exito!!!"):
                #data1={"username":user,"action": "Carga de archivo", "module": "Docentes"}
                #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))
                pass
            data['Erros'].append({'exitosa': Error})
            return json.dumps(data, 201, { 'Access-Control-Allow-Origin': '*' })
        else:
            # return error
            return json.dumps({'exitosa':'Error !!!. El formato del archivo ingresado no es csv'}), 201, { 'Access-Control-Allow-Origin': '*' }


class fecha(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    def post(self,faces,facyt,face,odontologia,fcjp,ingieneria,derecho):
        CambiarFechaTope(faces,facyt,face,odontologia,fcjp,ingieneria,derecho)
        Error="Las fechas topes han sido modificadas con exito !!!"
        return json.dumps({'exitosa':Error}), 201, { 'Access-Control-Allow-Origin': '*' }
    
class ultima(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    print("hola")
    def post(self):
        print(str(UltimaFecha("Facyt")))
        
        return json.dumps({'APi':str(ActualizacionApi()),'Facyt':str(UltimaFecha("Facyt")),'Face':str(UltimaFecha("Face")),'Faces':str(UltimaFecha("Faces")),'Fcs':str(UltimaFecha("Fcs")),'Fcjp':str(UltimaFecha("Fcjp")),'Odontologia':str(UltimaFecha("Odontologia")),'Ingieneria':str(UltimaFecha("Ingieneria"))}), 201, { 'Access-Control-Allow-Origin': '*' }
            
# docentes route
api.add_resource(TeachersInsertInitial, '/docentes')
api.add_resource(TeacherstUpdate, '/docentes/<date_update>')
#api.add_resource(File, '/upload')
api.add_resource(File, '/upload/<user>')
api.add_resource(ultima, '/ultimaFecha')
api.add_resource(fecha, '/fechas/<string:faces>/<string:facyt>/<string:face>/<string:odontologia>/<string:fcjp>/<string:ingieneria>/<string:derecho>')
#api.add_resource(fecha, '/fechas')


if __name__ == '__main__':
   
    app.run(debug=True, port=int('8083'))



