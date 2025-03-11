# gunicorn_config.py
import multiprocessing

# Número de workers: normalmente (2 x núcleos) + 1
workers = multiprocessing.cpu_count() * 2 + 1
# Usar workers threads para manejar múltiples solicitudes
threads = 2
# Puerto en el que escuchará
bind = "0.0.0.0:5000"
# Tiempo máximo de respuesta
timeout = 120
# Nivel de log
loglevel = "info"
# Archivo para registrar accesos
accesslog = "-"  # Stdout para CloudWatch
# Archivo para registrar errores
errorlog = "-"   # Stdout para CloudWatch
# Clase de worker
worker_class = "sync"
# Limitar el número de solicitudes por worker
max_requests = 1000
max_requests_jitter = 50