from flask import Flask, jsonify
from flask import request 
import json
import xmltodict



app = Flask(__name__)

@app.route('/json_usuarios', methods=['GET'])
def json_usuarios():
            
            json_data = {
    "usuarios": {
        "usuario": [
            {
                "rol": "cliente",
                "nombre": "John",
                "apellido": "Doe",
                "telefono": "123456789",
                "correo": "john.doe@example.com",
                "contrasena": "mipassword123"
            },
            {
                "rol": "cliente",
                "nombre": "holy",
                "apellido": "flags",
                "telefono": "54125632",
                "correo": "holi21@gmail.com",
                "contrasena": "holi21"
            },
            {
                "rol": "administrador",
                "nombre": "Oreld",
                "apellido": "Ardon",
                "telefono": "41445281",
                "correo": "eliotorel10@gmail.com",
                "contrasena": "201901472"
            },
            {
                "rol": "cliente",
                "nombre": "Enner",
                "apellido": "Ardon",
                "telefono": "41147886",
                "correo": "Enner49@gmail.com",
                "contrasena": "enner4949"
            }
        ]
    }
}

            print(json_data)
            
            return jsonify(json_data)


@app.route('/json_salas', methods=['GET'])
def json_salas():
           
            json_data2 = {
    "cines": {
        "cine": {
            "nombre": "Cine ABC",
            "salas": {
                "sala": [
                    {
                        "numero": "#USACIPC2_202212333_1",
                        "asientos": "100"
                    },
                    {
                        "numero": "#USACIPC2_202212333_2",
                        "asientos": "90"
                    }
                ]
            }
        }
    }
}
            print(json_data2)
            return jsonify(json_data2)


@app.route('/categorias_peliculas', methods=['GET'])
def categorias_peliculas():
            
            json_data3 = {
    "categorias": {
        "categoria": [
            {
                "nombre": "Accion",
                "peliculas": {
                    "pelicula": [
                        {
                            "titulo": "Avengers: Endgame",
                            "director": "Anthony Russo, Joe Russo",
                            "anio": "2019",
                            "fecha": "2023-06-02",
                            "hora": "18:30",
                            "imagen": "https://prod-ripcut-delivery.disney-plus.net/v1/variant/disney/DB176BD1488D7E4822256EF1778C124FC17388FC1E7F0F6D89B38AFF5FB001F6/scale?width=1200&aspectRatio=1.78&format=jpeg",
                            "precio": "40"
                        },
                        {
                            "titulo": "John Wick",
                            "director": "Chad Stahelski",
                            "anio": "2014",
                            "fecha": "2023-06-06",
                            "hora": "20:00",
                            "imagen": "https://images3.alphacoders.com/103/thumb-1920-1033561.jpg",
                            "precio": "45"
                        },
                        {
                            "titulo": "Mision Imposible: Fallout",
                            "director": "Christopher McQuarrie",
                            "anio": "2018",
                            "fecha": "2023-06-07",
                            "hora": "19:15",
                            "imagen": "https://garutplus.co.id/wp-content/uploads/2021/02/1_vkKPtzPYAysiyW2PQ_5zmQ-696x392.jpeg",
                            "precio": "55"
                        }
                    ]
                }
            },
            {
                "nombre": "Comedia",
                "peliculas": {
                    "pelicula": [
                        {
                            "titulo": "Deadpool",
                            "director": "Tim Miller",
                            "anio": "2016",
                            "fecha": "2023-06-05",
                            "hora": "20:30",
                            "imagen": "https://wallpapercave.com/wp/wp5116401.jpg",
                            "precio": "65"
                        },
                        {
                            "titulo": "Superbad",
                            "director": "Greg Mottola",
                            "anio": "2007",
                            "fecha": "2023-06-06",
                            "hora": "21:00",
                            "imagen": "https://images7.alphacoders.com/118/1180548.jpg",
                            "precio": "45"
                        },
                        {
                            "titulo": "Bridesmaids",
                            "director": "Paul Feig",
                            "anio": "2011",
                            "fecha": "2023-06-07",
                            "hora": "20:15",
                            "imagen": "https://c4.wallpaperflare.com/wallpaper/61/848/843/movie-bridesmaids-wallpaper-preview.jpg",
                            "precio": "42"
                        }
                    ]
                }
            }
        ]
    }
}
            print(json_data3)
            return jsonify(json_data3)



@app.route('/json_tarjetas', methods=['GET'])
def json_tarjetas():
            
            json_data4 = {
    "tarjetas": {
        "tarjeta": [
            {
                "tipo": "Debito",
                "numero": "1234567890123456",
                "titular": "John",
                "fecha_expiracion": "12/2024"
            },
            {
                "tipo": "Credito",
                "numero": "9876543210987654",
                "titular": "Jane",
                "fecha_expiracion": "08/2023"
            }
        ]
    }
}
            print(json_data4)
            return jsonify(json_data4)  



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5700, debug=True)

    






    
