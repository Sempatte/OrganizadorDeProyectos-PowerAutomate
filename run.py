#!/usr/bin/env python
# run.py - Punto de entrada de la aplicación

import sys
import os

# Agregar el directorio actual al path para importar módulos correctamente
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importar la función principal de la aplicación
from app.presentation.main import start_app

if __name__ == "__main__":
    # Iniciar la aplicación
    start_app()