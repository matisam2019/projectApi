from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar las opciones de Chrome
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Iniciar el navegador
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)