# app/presentation/main.py
import sys
from PyQt6.QtWidgets import QApplication
from app.presentation.controllers.main_controller import MainController

def start_app():
    """Inicia la aplicación"""
    # Crear la aplicación Qt
    app = QApplication(sys.argv)
    
    # Configurar algunos estilos globales si es necesario
    app.setStyle("Fusion")
    
    # Crear el controlador principal
    controller = MainController()
    
    # Mostrar la ventana principal
    controller.show()
    
    # Ejecutar el bucle de eventos
    sys.exit(app.exec())