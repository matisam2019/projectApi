from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pytesseract
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime
#import datetime
import sys


# Configura las opciones de Chrome
options = Options()

# Define las columnas que tendrá tu DataFrame
columnas = [
    'id_ciclo', 'nombre', 'ubicacion', 'coordenadas', 'nivel_combustible',
    'km_hasta vacio', 'nivel_adblue', 'odometro', 'horas_motor',
    'peso_camion', 'peso_remolque', 'actualizacion', 'conductor', 'velocidad','alarma'
]

# Crea un DataFrame vacío con las columnas definidas
df = pd.DataFrame(columns=columnas)
# Conexión a base de datos
conn = sqlite3.connect('volvo.db')
cursor = conn.cursor()
# Inicializa el navegador
driver = webdriver.Chrome(options=options)
print("Ejecutando p1.py  abriendo web")
# Navega a la URL deseada
driver.get("https://volvoconnect.com/login/")
#time.sleep(10)
# Maximiza la pantalla
driver.maximize_window()

# Espera a que la página cargue
time.sleep(3)

# Tiempo de espera en segundos
tiempo_espera_pyautogui = 5

# Función para escribir texto usando copy_paste
def escribir_texto(x, y, texto):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyperclip.copy(texto)
    pyautogui.hotkey('ctrl', 'v')  # Windows
    # pyautogui.hotkey('command', 'v')  # macOS

# Función para simular la pulsación de Enter
def dar_enter(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.press('enter')

# Espera inicial
print(f"Esperando {tiempo_espera_pyautogui} segundos...")
time.sleep(tiempo_espera_pyautogui)

print("Ejecutando acciones de escritura...")

# Escribir texto
escribir_texto(22, 567, 'sparra@jcabrera.cl')
escribir_texto(20, 648, "M@ti2711")
dar_enter(229, 712)

print("segundos para dar Enter...")

# Espera a que el botón "Abrir mapa" esté presente
print("Esperando botón 'Abrir mapa'...")
try:
    boton_mapa = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//a[span[text()='Abrir mapa']]"))
    )
    print("Botón 'Abrir mapa' encontrado. Continuando con la rutina.")
except Exception as e:
    print(f"Error: El botón 'Abrir mapa' no se encontró después de 60 segundos. {e}")
    driver.quit()
    sys.exit(1)
    
print("Continuando con el flujo...")

def generar_id_ciclo():
    #"""Genera un ID de ciclo único combinando un número secuencial y la hora actual."""
    try:
        with open('id_ciclo.txt', 'r') as f:
            num_ciclo = int(f.read()) + 1
    except FileNotFoundError:
        num_ciclo = 1
    hora_actual = datetime.now()
    fecha_hora_formateada = hora_actual.strftime("%Y-%m-%d %H:%M:%S")  # Formato: AAAA-MM-DD HH:MM:SS
    #hora_actual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    id_ciclo = f"{num_ciclo}-{hora_actual}"

    with open('id_ciclo.txt', 'w') as f:
        f.write(str(num_ciclo))
    return id_ciclo


time.sleep(3)
print("Simulando Enter para seleccionar Mapa...")
dar_enter(1133, 673)  # Selecciona Mapa

try:
    # Esperar hasta 15 segundos para que el elemento esté presente
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-list-category-primary="true"]'))
    )
    print("La categoría 'Vehículos' está presente.")
except Exception as e:
    print(f"Error: El elemento categoría no está presente o no se cargó a tiempo. {e}")
    driver.quit()
    sys.exit(1)

#time.sleep(3) 
#dar_enter(408, 409)
#time.sleep(3) 
#dar_enter(411, 464)

###
time.sleep(1) 
try:
    # Primer enter
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="kb-list-category"][data-test-id="assetMenuItem-vehicle"]'))
    )

    # Haz clic en el elemento <a>
    element.click()
    print("Clic simulado con éxito en el elemento <a>.")

except Exception as e:
    print(f"Error al simular el clic en el elemento <a>: {e}")
time.sleep(1) 
try:
    # Segundo enter
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="kb-list-group-header-item"]'))
    )

    # Haz clic en el elemento div
    element.click()
    print("Clic simulado con éxito en el elemento div.")

except Exception as e:
    print(f"Error al simular el clic en el elemento div: {e}")
# Lista de vehículos a procesar
lista_vehiculos =['452 Tracto 6x4 EA 460', '398 Tracto 6x4 EA 460', '443 Tracto 6x4 EA 460', '448 Tracto 6x4 EA 460', '379 Tracto 6x4 EA 460', '385 Tracto 6x4 EA 460', '455 Tracto 6x4 EA 460', '411 Tracto 6x4 EA 460', '387 Tracto 6x4 EA 460', '402 Tracto 6x4 EA 460', '381 Tracto 6x4 EA 460', '466 Tracto 6x4 EA 460', '445 Tracto 6x4 EA 460', '454 Tracto 6x4 EA 460', '451 Tracto 6x4 EA 460', '473 Tracto 6x4 EA 460', '414 Tracto 6x4 EA 460']
#lista_vehiculos = ['452 Tracto 6x4 EA 460', '398 Tracto 6x4 EA 460', '443 Tracto 6x4 EA 460', '448 Tracto 6x4 EA 460', '379 Tracto 6x4 EA 460', '385 Tracto 6x4 EA 460', '455 Tracto 6x4 EA 460', '411 Tracto 6x4 EA 460', '387 Tracto 6x4 EA 460', '402 Tracto 6x4 EA 460', '381 Tracto 6x4 EA 460', '466 Tracto 6x4 EA 460', '445 Tracto 6x4 EA 460', '454 Tracto 6x4 EA 460', '451 Tracto 6x4 EA 460', '473 Tracto 6x4 EA 460', '414 Tracto 6x4 EA 460', '389 Tracto 6x4 EA 460', '434 Tracto 6x4 EA 460', '462 Tracto 6x4 EA 460', '471 Tracto 6x4 EA 460', '453 Tracto 6x4 EA 460', '433 Tracto 6x4 EA 460', '449 Tracto 6x4 EA 460', '403 Tracto 6x4 EA 460', '461 Tracto 6x4 EA 460', '446 Tracto 6x4 EA 460', '370 Tracto 6x4 EA 460', '442 Tracto 6x4 EA 460', '377 Tracto 6x4 EA 460', '380 Tracto 6x4 EA 460', '373 Tracto 6x4 EA 460', '357 EA', '365 EA'] 
# Minimiza la ventana
#driver.minimize_window()
time.sleep(1) 
driver.minimize_window()
vehiculos_data = []
id_ciclo = generar_id_ciclo()  # Genera un único ID de ciclo para toda la sesión

for vehiculo_id in lista_vehiculos:
    print(f"Procesando vehículo-Inicio Flujo: {vehiculo_id}")
    max_reintentos = 3
    reintentos = 0
    vehiculos_data = []
    
    while reintentos < max_reintentos:
        # Inicializar diccionario con valores por defecto para todos los campos
        vehiculo_info = {
            'id_ciclo': id_ciclo,
            'nombre': "Sin Nombre",
            'ubicacion': "Sin Ubicación",
            'coordenadas': "0.0, 0.0",
            'nivel_combustible': "0",
            'km_hasta_vacio': "0",
            'nivel_adblue': "0",
            'odometro': "0",
            'horas_motor': "0",
            'peso_camion': "0",
            'peso_remolque': "0",
            'actualizacion': "Sin Datos",
            'conductor': "Sin Conductor",
            'velocidad': 0
        }
        
        try:
            #escribir_texto(61, 390, str(vehiculo_id))
            #time.sleep(3)
            #dar_enter(406, 560)
            #time.sleep(5)  # Dar tiempo para que cargue la información
            
            try:
                # Escribo texto id vehiculo
                input_element = WebDriverWait(driver, 20).until(
                     EC.presence_of_element_located((By.ID, "positioningSearch"))
                )
            
                # Limpia el contenido anterior del input (si lo hay)
                input_element.clear()
            
                 # Escribe el vehiculo_id en el elemento input
                input_element.send_keys(vehiculo_id)
            
                print(f"Escribo en caja texto '{vehiculo_id}'")
                print(vehiculo_id)
                 # Aquí puedes agregar otras acciones que necesites realizar con cada vehículo
                 # Por ejemplo, hacer clic en un botón de búsqueda, esperar resultados, etc.
            
                 # Espera un breve momento antes de continuar con el siguiente vehículo
                #time.sleep(2)  # Espera 2 segundos (ajusta según sea necesario)
            
            except Exception as e:
                print(f"Error durante el bucle: {e}")    
                
            time.sleep(2)
            ##
            try:
                boton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//button[@data-testid='asset-locator' and @nature='primary']"
                    ))
                )
                boton.click()
                print("Boton para ir a detallles")
               # print("Elemento de vehículo clickeado.")
            
            except TimeoutException:
                print("Tiempo de espera excedido al buscar el elemento del vehículo.")
            except NoSuchElementException:
                print("No se encontró el elemento del vehículo.")
            except Exception as e:
                print(f"Error general: {e}")
            ##
            #try:
                # Hacemos enter
              #  element = WebDriverWait(driver, 20).until(
              #      EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="asset-row-vehicle-467B3698ADC12F9887C5D6CB7C059951"]'))
              #  )
            
                # Haz clic en el elemento div
               # element.click()
               # print("Boton para ir a detallles")
            
            #except Exception as e:
             #   print(f"Error al simular el clic en el elemento div: {e}")
            time.sleep(4)
            # Obtener HTML y crear objeto BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            print(f"leemos el DOM")
            elementos = soup.find_all('li')
            datos_validos = False
            
            for elemento in elementos:
                data_testid = elemento.get('data-testid')
                
                try:
                    if data_testid == 'vehicle-name':
                        nombre = elemento.find('span', {'data-testid': 'mui-primary-text'})
                        if nombre:
                            vehiculo_info['nombre'] = nombre.text.strip()
                            datos_validos = True
                            #if vehiculo_info['nombre'] == vehiculo_id:
                               # datos_validos = True
                            #else:
                                #print(f"Error: El nombre del vehículo extraído '{vehiculo_info['nombre']}' no coincide con el ID '{vehiculo_id}'. Reintentando...")
                               # print(vehiculo_info['nombre'])
                              #  print(vehiculo_id)
                              #  break
                    
                    elif data_testid == 'mui-list-item' and elemento.find('span', {'data-testid': 'address-loaded-successful'}):
                        ubicacion = elemento.find('span', {'data-testid': 'address-loaded-successful'})
                        if ubicacion:
                            vehiculo_info['ubicacion'] = ubicacion.text
                        
                        coordenadas_element = elemento.find('a', {'data-testid': 'clickable-text-copy-latlng'})
                        if coordenadas_element:
                            vehiculo_info['coordenadas'] = coordenadas_element.text
                    
                    elif data_testid == 'fuel-level':
                        combustible_span = elemento.find('span', {'data-list-item-value': 'true'})
                        if combustible_span:
                            combustible_str = combustible_span.text.strip()
                            try:
                                porcentaje_combustible = combustible_str.split('%')[0].strip()
                                vehiculo_info['nivel_combustible'] = porcentaje_combustible
                                
                                if '(' in combustible_str and ')' in combustible_str:
                                    km_hasta_vacio = combustible_str.split('(')[1].split(')')[0].split('km')[0].strip()
                                    vehiculo_info['km_hasta_vacio'] = km_hasta_vacio
                            except IndexError:
                                pass  # Usa el valor predeterminado
                    
                    elif data_testid == 'ad-blue':
                        adblue_span = elemento.find('span', {'data-testid': 'mui-primary-text'})
                        if adblue_span:
                            adblue_str = adblue_span.text.strip()
                            try:
                                porcentaje_adblue = adblue_str.split('%')[0].strip()
                                vehiculo_info['nivel_adblue'] = porcentaje_adblue
                            except IndexError:
                                pass
                    
                    elif data_testid == 'lov-vehicle-distance':
                        distancia_span = elemento.find('span', {'data-testid': 'mui-primary-text'})
                        if distancia_span:
                            distancia_str = distancia_span.text.strip()
                            try:
                                distancia = distancia_str.split('km')[0].strip()
                                vehiculo_info['odometro'] = distancia
                            except IndexError:
                                pass
                    
                    elif data_testid == 'data-test-engine-hours-enricher':
                        horas_motor_span = elemento.find('span', {'data-list-item-value': 'true'})
                        if horas_motor_span:
                            horas_motor_str = horas_motor_span.text.strip()
                            try:
                                horas_motor = horas_motor_str.split('h')[0].strip()
                                vehiculo_info['horas_motor'] = horas_motor
                            except IndexError:
                                pass
                    
                    elif data_testid == 'vehicle-weight':
                        peso_camion_element = elemento.find('span', {'data-testid': 'truck-total-weight'})
                        if peso_camion_element:
                            peso_span = peso_camion_element.find('span', {'data-list-item-value': 'true'})
                            if peso_span:
                                peso_camion_str = peso_span.text.strip()
                                try:
                                    peso_camion = peso_camion_str.split('t')[0].strip()
                                    vehiculo_info['peso_camion'] = peso_camion
                                except IndexError:
                                    pass
                    
                    elif data_testid == 'trailer-weight':
                        peso_remolque_element = elemento.find('span', {'data-testid': 'trailer-total-weight'})
                        if peso_remolque_element:
                            peso_span = peso_remolque_element.find('span', {'data-list-item-value': 'true'})
                            if peso_span:
                                peso_remolque_str = peso_span.text.strip()
                                try:
                                    peso_remolque = peso_remolque_str.split('t')[0].strip()
                                    vehiculo_info['peso_remolque'] = peso_remolque
                                except IndexError:
                                    pass
                    
                    elif data_testid == 'mui-list-item' and elemento.find('span', {'data-testid': 'update-time'}):
                        actualizacion = elemento.find('span', {'data-testid': 'update-time'})
                        if actualizacion:
                            vehiculo_info['actualizacion'] = actualizacion.text
                    
                    # Extraer conductor
                    conductor_link = elemento.find('a', href=lambda href: href and "/positioning/driver/" in href)
                    if conductor_link:
                        vehiculo_info['conductor'] = conductor_link.text
                    id_ciclo = generar_id_ciclo() 
                    # Extraer velocidad
                    if data_testid == 'vehicle-speed':
                        velocidad_span = elemento.find('span', {'data-testid': 'mui-primary-text'})
                        if velocidad_span:
                            velocidad_str = velocidad_span.text.strip()
                            try:
                                vehiculo_info['velocidad'] = int(velocidad_str.split('km/h')[0].strip())
                            except (ValueError, IndexError):
                                pass  # Usa el valor predeterminado


                    # Buscar elementos con la clase ccgui-icon-alertfilled
                    elementos_alerta = soup.find_all(class_='ccgui-icon-alertfilled')       
                    alarma = 1 if elementos_alerta else 0  # 1 si hay alertas, 0 si no
                    vehiculo_info['alarma'] = alarma
                    
                    # Ahora puedes usar vehiculo_info['alarma']
                    #print(f"Información del vehículo: {vehiculo_info}")
                except (AttributeError, Exception) as e:
                    print(f"Error al extraer datos de {data_testid}: {e}")
                    # Continúa con el siguiente elemento


            
            # Si los datos son válidos, añadir a la lista y salir del bucle de reintentos
            if datos_validos:
                
                print(f"p1.py Información del vehículo: {vehiculo_info}")
                print(f"p1.py Datos válidos para vehículo: {vehiculo_id}")
                vehiculos_data.append(vehiculo_info)
                #Insert bd
                # Crear DataFrame con los datos recopilados
                df = pd.DataFrame(vehiculos_data)
                # Limpiar caracteres no deseados
                #df['actualizacion'] = df['actualizacion'].str.replace('\xa0', ' ')
                print("revisar df")
                print(df.columns)
                df['odometro'] = df['odometro'].str.replace('.', '', regex=False).astype(int)
                df['horas_motor'] = df['horas_motor'].str.replace('.', '', regex=False).astype(int)
                df['peso_camion'] = df['peso_camion'].str.replace(',', '.', regex=False).astype(float)
                df['peso_remolque'] = df['peso_remolque'].str.replace(',', '.', regex=False).astype(float)


                def procesar_actualizacion(actualizacion_str):
                    actualizacion_str = actualizacion_str.replace('\xa0', ' ')
                    partes = actualizacion_str.split(' ')
                    if 'hoy' in actualizacion_str:
                        hora = partes[1]
                        try:
                            fecha_hora = datetime.strptime(f"{datetime.now().strftime('%Y-%m-%d')} {hora}", "%Y-%m-%d %H:%M")
                            fecha_hora = fecha_hora.replace(second=0)
                            return fecha_hora.strftime("%Y-%m-%d %H:%M:%S")  # Formato sin la 'T'
                        except ValueError:
                            return None
                    else:
                        try:
                            fecha_str = f"{partes[1]} {partes[2]}"
                            fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
                            fecha_hora = fecha_hora.replace(second=0)
                            return fecha_hora.strftime("%Y-%m-%d %H:%M:%S")  # Formato sin la 'T'
                        except ValueError:
                            return None

                df['fecha'] = df['actualizacion'].apply(procesar_actualizacion)

                
                # Guardar en CSV para debug/respaldo
                #df.to_csv('datos_vehiculos.csv', index=False, encoding='utf-8')
                
                # Insertar los datos en la base de datos
                try:
                    for index, row in df.iterrows():
                        cursor.execute('''
                            INSERT INTO aquiEstoy (
                                id_ciclo, nombre, ubicacion, coordenadas, nivel_combustible,
                                km_hasta_vacio, nivel_adblue, odometro, horas_motor,
                                peso_camion, peso_remolque, actualizacion, fecha, conductor, velocidad, alarma
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row['id_ciclo'], row['nombre'], row['ubicacion'], row['coordenadas'],
                            row['nivel_combustible'], row['km_hasta_vacio'], row['nivel_adblue'],
                            row['odometro'], row['horas_motor'], row['peso_camion'],
                            row['peso_remolque'], row['actualizacion'], row['fecha'],row['conductor'], row['velocidad'], row['alarma']
                        ))
                    conn.commit()
                    print("p1.py Datos guardados correctamente en la base de datos.")
                    #
                except Exception as e:
                    print(f"Error al guardar en la base de datos: {e}")
                finally:
                    #conn.close()
                    #driver.quit()
                    #print("Proceso completado")
                    break
            else:
                reintentos += 1
                print(f"Datos no válidos. Reintento {reintentos}/{max_reintentos}")
                time.sleep(2)
        
        except Exception as e:
            print(f"Error procesando vehículo {vehiculo_id}: {e}")
            reintentos += 1
            time.sleep(2)
        
        finally:
            # Cerrar la ficha del vehículo actual
            try:

                ##
                # Localizar el botón CORRECTO (versión 1)
                clear_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@class, 'css-wzqarj') and .//*[@data-test-icon-type='close']]")
                    )
                )
               
                # Click en el botón correcto
                clear_button.click()
                
                ####
                
                
            except Exception as e:
                print(f"Error al cerrar la ficha del vehículo: {e}")
                # Intentar volver atrás de forma alternativa
                driver.back()
                time.sleep(3)
    
conn.close()
driver.quit()
print("Proceso completado") 