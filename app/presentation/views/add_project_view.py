from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QGroupBox, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from app.presentation.controllers.project_controller import ProjectController

class AddProjectView(QWidget):
    """Vista para agregar un nuevo proyecto"""
    
    back_requested = pyqtSignal()
    project_added = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Controlador
        self.controller = ProjectController(self)
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con título y botón de volver
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("Regresar")
        back_button.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_button)
        
        title = QLabel("Agregar Proyecto")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title, 1)
        
        self.layout.addLayout(header_layout)
        
        # Formulario
        form_group = QGroupBox("Formulario para agregar proyecto con todos los campos necesarios")
        form_layout = QFormLayout(form_group)
        
        # Campo de nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del proyecto")
        form_layout.addRow("Nombre:", self.name_input)
        
        self.layout.addWidget(form_group)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.back_requested.emit)
        buttons_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Guardar Proyecto")
        save_button.setObjectName("secondaryButton")
        save_button.clicked.connect(self._on_save)
        buttons_layout.addWidget(save_button)
        
        self.layout.addLayout(buttons_layout)
        
        # Espacio adicional
        self.layout.addStretch()
    
    def _on_save(self):
        """Manejador para guardar un nuevo proyecto"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(
                self, 
                "Campos Incompletos", 
                "Por favor, ingrese el nombre del proyecto."
            )
            return
        
        try:
            project = self.controller.add_project(name)
            if project:
                self.project_added.emit()
                self.name_input.clear()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error al Guardar", 
                f"No se pudo guardar el proyecto: {str(e)}"
            )