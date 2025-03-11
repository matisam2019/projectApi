import subprocess
import time
import datetime
import logging
import multiprocessing

# Configuración del logging
logging.basicConfig(
    filename='run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ejecutar_script(nombre_script):
    ahora = datetime.datetime.now()
    logging.info(f"Ejecutando {nombre_script} a las {ahora.strftime('%H:%M:%S')}")
    try:
        subprocess.run(["python", nombre_script], check=True)
        logging.info(f"{nombre_script} ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar {nombre_script}: {e}")

if __name__ == "__main__":
    # Ejecutar p1.py como un proceso independiente
    proceso_p1 = multiprocessing.Process(target=ejecutar_script, args=("p1.py",))
    proceso_p1.start()

    # Esperar 45 segundos antes de ejecutar p2.py
    time.sleep(40)

    # Ejecutar p2.py como un proceso independiente
    proceso_p2 = multiprocessing.Process(target=ejecutar_script, args=("p2.py",))
    proceso_p2.start()

    # Esperar otros 45 segundos antes de ejecutar p3.py
    time.sleep(40)

    # Ejecutar p3.py como un proceso independiente
    proceso_p3 = multiprocessing.Process(target=ejecutar_script, args=("p3.py",))
    proceso_p3.start()
    time.sleep(40)

# Ejecutar p4.py como un proceso independiente
    proceso_p4 = multiprocessing.Process(target=ejecutar_script, args=("p4.py",))
    proceso_p4.start()
    time.sleep(40)

# Ejecutar p5.py como un proceso independiente
    proceso_p5 = multiprocessing.Process(target=ejecutar_script, args=("p5.py",))
    proceso_p5.start()
    time.sleep(40)

# Ejecutar p6.py como un proceso independiente
    proceso_p6 = multiprocessing.Process(target=ejecutar_script, args=("p6.py",))
    proceso_p6.start()
    time.sleep(40)


    

    # Esperar a que todos los procesos terminen (opcional)
    proceso_p1.join()
    proceso_p2.join()
    proceso_p3.join()
    proceso_p4.join()
    proceso_p5.join()
    proceso_p6.join()

    logging.info("Todos los scripts ejecutados.")