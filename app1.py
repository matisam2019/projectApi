import os
from flask import Flask, render_template
import googlemaps
import folium
import polyline

app = Flask(__name__)

# Asegurarse de que la carpeta templates exista
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Configuración de la API de Google Maps
API_KEY = 'AIzaSyDtDvUXCJ-25dL7OQBipL_QtoKYNjUtT6o'
gmaps = googlemaps.Client(key=API_KEY)

def seleccionar_punto_mas_cercano_matriz(puntos, destino):
    """
    Selecciona el punto más cercano al destino usando la matriz de distancias de Google.
    
    :param puntos: Diccionario de puntos con sus coordenadas
    :param destino: Coordenadas del punto de destino
    :return: Nombre del punto más cercano y diccionario de distancias/duraciones
    """
    # Preparar lista de orígenes
    origenes = list(puntos.values()) + [destino]
    
    try:
        # Obtener matriz de distancias
        matriz_distancias = gmaps.distance_matrix(
            origenes[:-1],  # Puntos A, B, C
            [origenes[-1]],  # Destino
            mode='driving'
        )
        
        # Procesar resultados
        distancias = {}
        duraciones = {}
        
        for i, (nombre, _) in enumerate(puntos.items()):
            elemento = matriz_distancias['rows'][i]['elements'][0]
            
            # Verificar si la ruta es válida
            if elemento['status'] == 'OK':
                distancia = elemento['distance']['text']
                duracion = elemento['duration']['text']
                
                distancias[nombre] = float(distancia.split()[0])
                duraciones[nombre] = duracion
        
        # Encontrar el punto más cercano
        punto_cercano = min(distancias, key=distancias.get)
        
        return punto_cercano, {
            'distancias': distancias, 
            'duraciones': duraciones
        }
    
    except Exception as e:
        print(f'Error en matriz de distancias: {e}')
        return None, None

def generar_mapa_ruta(inicio, punto_cercano, destino):
    """
    Genera un mapa con la ruta entre inicio, punto cercano y destino.
    
    :param inicio: Coordenadas de inicio
    :param punto_cercano: Coordenadas del punto más cercano
    :param destino: Coordenadas de destino
    :return: Detalles de la ruta
    """
    try:
        # Obtener direcciones para toda la ruta
        direcciones = gmaps.directions(inicio, destino, 
                                       waypoints=[punto_cercano],
                                       optimize_waypoints=True,
                                       mode='driving')
        
        if direcciones:
            # Decodificar la ruta en puntos geográficos
            ruta_encoded = direcciones[0]['overview_polyline']['points']
            ruta_puntos = polyline.decode(ruta_encoded)
            
            # Crear un mapa centrado en el punto medio
            punto_medio = [
                sum(p[0] for p in [inicio, punto_cercano, destino]) / 3,
                sum(p[1] for p in [inicio, punto_cercano, destino]) / 3
            ]
            mapa = folium.Map(location=punto_medio, zoom_start=12)
            
            # Añadir marcadores
            folium.Marker(
                inicio, 
                popup='Punto de Inicio', 
                icon=folium.Icon(color='green', icon='play')
            ).add_to(mapa)
            
            folium.Marker(
                punto_cercano, 
                popup=f'Punto Intermedio ({punto_cercano})', 
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
            
            folium.Marker(
                destino, 
                popup='Punto de Destino', 
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(mapa)
            
            # Añadir la ruta al mapa
            folium.PolyLine(
                ruta_puntos, 
                color='blue', 
                weight=5, 
                opacity=0.8
            ).add_to(mapa)
            
            # Guardar el mapa
            ruta_mapa = os.path.join(TEMPLATES_DIR, 'ruta_generada.html')
            mapa.save(ruta_mapa)
            
            # Obtener detalles de la ruta
            ruta = direcciones[0]['legs'][0]
            return {
                'distancia': ruta['distance']['text'],
                'duracion': ruta['duration']['text'],
                'pasos': [paso['html_instructions'] for paso in ruta['steps']]
            }
        
        return None
    
    except Exception as e:
        print(f'Error al generar mapa: {e}')
        return None

@app.route('/')
def index():
    """Página principal con análisis de ruta."""
    # Puntos y destino definidos
    puntos = {
        'A': (-36.820173756479875, -73.05053032725317),
        'B': (-36.82252319981827, -73.04106613087734),
        'C': (-36.8341152, -73.0513574)
    }
    destino = (-36.8179996, -73.0546743)
    inicio = (-36.8341152, -73.0513574)
    
    # Seleccionar punto más cercano usando matriz de Google
    punto_cercano, detalles_matriz = seleccionar_punto_mas_cercano_matriz(puntos, destino)
    
    # Generar mapa de ruta
    detalles_ruta = generar_mapa_ruta(inicio, puntos[punto_cercano], destino)
    
    return render_template('index.html', 
                           detalles_ruta=detalles_ruta,
                           punto_cercano=punto_cercano,
                           detalles_matriz=detalles_matriz)

@app.route('/ruta')
def mapa_ruta():
    """Renderiza el mapa generado."""
    return render_template('ruta_generada.html')

if __name__ == '__main__':
    # Crear archivo index.html si no existe
    index_template = os.path.join(TEMPLATES_DIR, 'index.html')
    if not os.path.exists(index_template):
        with open(index_template, 'w', encoding='utf-8') as f:
            f.write('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Selector de Ruta Óptima</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding-top: 50px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Selector de Ruta Óptima</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card mb-4">
                    <div class="card-header">
                        Análisis de Distancias y Tiempos
                    </div>
                    <div class="card-body">
                        <h5>Distancias a Destino:</h5>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Punto</th>
                                    <th>Distancia</th>
                                    <th>Tiempo</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% if detalles_matriz %}
                                {% for punto, distancia in detalles_matriz.distancias.items() %}
                                <tr {% if punto == punto_cercano %}class="table-success"{% endif %}>
                                    <td>{{ punto }}</td>
                                    <td>{{ distancia }} km</td>
                                    <td>{{ detalles_matriz.duraciones[punto] }}</td>
                                </tr>
                                {% endfor %}
                                {% endif %}
                            </tbody>
                        </table>
                        <p class="alert alert-info">
                            Punto más cercano: <strong>{{ punto_cercano }}</strong>
                        </p>
                    </div>
                </div>
                
                {% if detalles_ruta %}
                <div class="card">
                    <div class="card-header">
                        Detalles de la Ruta
                    </div>
                    <div class="card-body">
                        <p><strong>Distancia:</strong> {{ detalles_ruta.distancia }}</p>
                        <p><strong>Duración:</strong> {{ detalles_ruta.duracion }}</p>
                        
                        <h5>Pasos de la Ruta:</h5>
                        <ul>
                            {% for paso in detalles_ruta.pasos %}
                                <li>{{ paso | safe }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-6">
                <iframe src="/ruta" width="100%" height="600" frameborder="0"></iframe>
            </div>
        </div>
    </div>
</body>
</html>
''')
    
    app.run(debug=True)