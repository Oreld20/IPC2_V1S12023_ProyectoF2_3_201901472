from flask import Flask, jsonify
from flask import request 
import json
import xmltodict



app = Flask(__name__)

@app.route('/json_usuarios', methods=['GET'])
def json_usuarios():
            archivo_xml = r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\usuario.XML'
            with open(archivo_xml, 'r') as file:
                xml_data = file.read()
            xml_dict = xmltodict.parse(xml_data)
            json_data = json.dumps(xml_dict, indent=4)
            return jsonify(json_data)


@app.route('/json_salas', methods=['GET'])
def json_salas():
            archivo_xml2 = r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\salas.XML'
            with open(archivo_xml2, 'r') as file:
                xml_data2 = file.read()
            xml_dict2 = xmltodict.parse(xml_data2)
            json_data2 = json.dumps(xml_dict2, indent=4)
            print(json_data2)
            return jsonify(json_data2)


@app.route('/categorias_peliculas', methods=['GET'])
def categorias_peliculas():
            archivo_xml3 = r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\categorias_peliculas.XML'
            with open(archivo_xml3, 'r') as file:
                xml_data3 = file.read()
            xml_dict3 = xmltodict.parse(xml_data3)
            json_data3 = json.dumps(xml_dict3, indent=4)
            print(json_data3)
            return jsonify(json_data3)



@app.route('/json_tarjetas', methods=['GET'])
def json_tarjetas():
            archivo_xml4 = r'C:\Users\eliot\OneDrive\Documentos\MyEspacio_De_Trabajo\proyecto-ipc2\aplicacion_web\tarjetas.XML'
            with open(archivo_xml4, 'r') as file:
                xml_data4 = file.read()
            xml_dict4 = xmltodict.parse(xml_data4)
            json_data4 = json.dumps(xml_dict4, indent=4)
            print(json_data4)
            return jsonify(json_data4)  



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700, debug=True)

    






    
