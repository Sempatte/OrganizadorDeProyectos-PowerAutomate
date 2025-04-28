# app/config.py
import os
from pathlib import Path

# Directorio base de la aplicación
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio de datos
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Archivo de base de datos
DB_FILE = os.path.join(DATA_DIR, 'power_automate.db')

# Configuración de la base de datos
DATABASE = {
    'path': DB_FILE,
}

# Configuración de la interfaz de usuario
UI = {
    'app_name': "Flujos de Power Automate Yapé",
    'min_width': 900,
    'min_height': 600,
}

# Asegurarse de que exista el directorio de datos
os.makedirs(DATA_DIR, exist_ok=True)