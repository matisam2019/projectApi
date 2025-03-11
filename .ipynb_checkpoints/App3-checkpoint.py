import tkinter as tk
from tkinter import ttk, messagebox
import googlemaps
import folium
import webbrowser
import os
from math import radians, sin, cos, sqrt, atan2

class AsignadorRutas:
    def __init__(self, root):
        self.root = root
        self.root.title("Asignador de Rutas por Proximidad")
        self.root.geometry("800x600")
        
        # Configuración de la API de Google Maps
        self.api_key = "AIzaSyDtDvUXCJ-25dL7OQBipL_QtoKYNjUtT6o"  # Reemplaza con tu clave de API
        try:
            self.gmaps = googlemaps.Client(key=self.api_key)
        except Exception as e:
            messagebox.showerror("Error de API", f"No se pudo conectar a la API de Google Maps: {e}")
            self.gmaps = None
        
        # Inicializar variables
        self.puntos = {
            'A': {'lat': -36.832167414590664, 'lng': -73.05216204784001, 'nombre': 'Punto A'},
            'B': {'lat': -36.8251732056805, 'lng': -73.05059306754286, 'nombre': 'Punto B'},
            'C': {'lat': -36.82350923465638, 'lng': -73.04037317766043, 'nombre': 'Punto C'}
        }
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para los puntos fijos
        puntos_frame = ttk.LabelFrame(main_frame, text="Puntos Disponibles", padding="10")
        puntos_frame.pack(fill=tk.X, pady=10)
        
        # Mostrar los puntos fijos
        for i, (id_punto, punto) in enumerate(self.puntos.items()):
            ttk.Label(puntos_frame, text=f"{punto['nombre']}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            ttk.Label(puntos_frame, text=f"Lat: {punto['lat']}, Lng: {punto['lng']}").grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Frame para ingresar la ruta
        ruta_frame = ttk.LabelFrame(main_frame, text="Detalles de la Ruta", padding="10")
        ruta_frame.pack(fill=tk.X, pady=10)
        
        # Entrada para el origen
        ttk.Label(ruta_frame, text="Origen:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.origen_var = tk.StringVar(value="Rengo 1306, Concepción, Chile")
        ttk.Entry(ruta_frame, textvariable=self.origen_var, width=50).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(ruta_frame, text="Latitud:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.origen_lat_var = tk.StringVar(value="-36.8252")
        ttk.Entry(ruta_frame, textvariable=self.origen_lat_var, width=20).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(ruta_frame, text="Longitud:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.origen_lng_var = tk.StringVar(value="-73.0501")
        ttk.Entry(ruta_frame, textvariable=self.origen_lng_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Entrada para el destino
        ttk.Label(ruta_frame, text="Destino:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.destino_var = tk.StringVar(value="Manuel Bulnes 1115, Concepción, Chile")
        ttk.Entry(ruta_frame, textvariable=self.destino_var, width=50).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(ruta_frame, text="Latitud:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.destino_lat_var = tk.StringVar(value="-36.8180")
        ttk.Entry(ruta_frame, textvariable=self.destino_lat_var, width=20).grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(ruta_frame, text="Longitud:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.destino_lng_var = tk.StringVar(value="-73.0547")
        ttk.Entry(ruta_frame, textvariable=self.destino_lng_var, width=20).grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(botones_frame, text="Asignar Ruta", command=self.asignar_ruta).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Visualizar Mapa", command=self.visualizar_mapa).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_frame, text="Salir", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Frame para resultados
        self.resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabla para mostrar resultados
        self.tabla = ttk.Treeview(self.resultados_frame, columns=("punto", "distancia", "estado"), show="headings")
        self.tabla.heading("punto", text="Punto")
        self.tabla.heading("distancia", text="Distancia al Origen (km)")
        self.tabla.heading("estado", text="Estado")
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
    def calcular_distancia_haversine(self, lat1, lon1, lat2, lon2):
        # Calcula la distancia entre dos puntos usando la fórmula de Haversine
        # Útil como respaldo si la API de Google Maps no está disponible
        R = 6371.0  # Radio de la Tierra en km
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distancia = R * c
        return distancia
    
    def calcular_distancia_gmaps(self, lat1, lon1, lat2, lon2):
        try:
            origen = (lat1, lon1)
            destino = (lat2, lon2)
            
            # Obtener la distancia usando la API de Distance Matrix
            matriz_distancia = self.gmaps.distance_matrix(origen, destino, mode="driving")
            
            # Extraer la distancia en kilómetros
            distancia_km = matriz_distancia['rows'][0]['elements'][0]['distance']['value'] / 1000
            return distancia_km
        except Exception as e:
            messagebox.showwarning("Error API", f"Error al calcular distancia con Google Maps: {e}\nUsando método alternativo.")
            return self.calcular_distancia_haversine(lat1, lon1, lat2, lon2)
    
    def asignar_ruta(self):
        # Limpiar tabla de resultados
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        try:
            # Obtener las coordenadas del origen
            origen_lat = float(self.origen_lat_var.get())
            origen_lng = float(self.origen_lng_var.get())
            
            # Calcular distancia desde cada punto al origen
            distancias = {}
            
            for id_punto, punto in self.puntos.items():
                if self.gmaps:
                    distancia = self.calcular_distancia_gmaps(
                        punto['lat'], punto['lng'], origen_lat, origen_lng
                    )
                else:
                    distancia = self.calcular_distancia_haversine(
                        punto['lat'], punto['lng'], origen_lat, origen_lng
                    )
                
                distancias[id_punto] = distancia
                
                # Añadir a la tabla
                self.tabla.insert("", "end", values=(
                    punto['nombre'],
                    f"{distancia:.2f}",
                    "Pendiente"
                ))
            
            # Encontrar el punto más cercano
            punto_cercano = min(distancias, key=distancias.get)
            mensaje = f"La ruta ha sido asignada al {self.puntos[punto_cercano]['nombre']} (distancia: {distancias[punto_cercano]:.2f} km)"
            
            # Actualizar el estado en la tabla
            for item in self.tabla.get_children():
                valores = self.tabla.item(item, "values")
                if valores[0] == self.puntos[punto_cercano]['nombre']:
                    self.tabla.item(item, values=(valores[0], valores[1], "ASIGNADO"))
                else:
                    self.tabla.item(item, values=(valores[0], valores[1], "No asignado"))
            
            messagebox.showinfo("Asignación Completada", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al asignar la ruta: {e}")
    
    def visualizar_mapa(self):
        try:
            # Obtener coordenadas
            origen_lat = float(self.origen_lat_var.get())
            origen_lng = float(self.origen_lng_var.get())
            destino_lat = float(self.destino_lat_var.get())
            destino_lng = float(self.destino_lng_var.get())
            
            # Crear mapa
            mapa = folium.Map(location=[(origen_lat + destino_lat) / 2, 
                                        (origen_lng + destino_lng) / 2], 
                             zoom_start=14)
            
            # Añadir marcadores para los puntos A, B y C
            for id_punto, punto in self.puntos.items():
                folium.Marker(
                    [punto['lat'], punto['lng']],
                    popup=punto['nombre'],
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(mapa)
            
            # Añadir marcadores para origen y destino
            folium.Marker(
                [origen_lat, origen_lng],
                popup='Origen',
                icon=folium.Icon(color='green', icon='play')
            ).add_to(mapa)
            
            folium.Marker(
                [destino_lat, destino_lng],
                popup='Destino',
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(mapa)
            
            # Intentar dibujar la ruta si la API está disponible
            if self.gmaps:
                try:
                    # Obtener direcciones
                    direcciones = self.gmaps.directions(
                        (origen_lat, origen_lng),
                        (destino_lat, destino_lng),
                        mode='driving'
                    )
                    
                    if direcciones:
                        # Decodificar la ruta en puntos geográficos
                        ruta_encoded = direcciones[0]['overview_polyline']['points']
                        import polyline
                        ruta_puntos = polyline.decode(ruta_encoded)
                        
                        # Añadir la ruta al mapa
                        folium.PolyLine(
                            ruta_puntos,
                            color='blue',
                            weight=5,
                            opacity=0.8
                        ).add_to(mapa)
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo dibujar la ruta: {e}")
            
            # Guardar y abrir el mapa
            mapa_path = os.path.join(os.path.expanduser("~"), "ruta_mapa.html")
            mapa.save(mapa_path)
            webbrowser.open('file://' + mapa_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al visualizar el mapa: {e}")

if __name__ == "__main__":
    try:
        import sys
        import platform
        
        # Configurar la apariencia según el sistema operativo
        if platform.system() == "Windows":
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
            
        root = tk.Tk()
        app = AsignadorRutas(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        if 'root' in locals():
            messagebox.showerror("Error Fatal", f"Error al iniciar la aplicación: {e}")