from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QGroupBox, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from app.presentation.controllers.project_controller import ProjectController

class EditProjectView(QWidget):
    """Vista para editar un proyecto existente"""
    
    back_requested = pyqtSignal()
    project_updated = pyqtSignal(int)  # project_id
    
    def __init__(self):
        super().__init__()
        
        # Controlador
        self.controller = ProjectController(self)
        
        # ID del proyecto actual
        self.current_project_id = None
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con título y botón de volver
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("Regresar")
        back_button.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_button)
        
        self.title = QLabel("Editar Proyecto")
        self.title.setObjectName("titleLabel")
        header_layout.addWidget(self.title, 1)
        
        self.layout.addLayout(header_layout)
        
        # Formulario
        form_group = QGroupBox("Información del Proyecto")
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
        
        save_button = QPushButton("Guardar Cambios")
        save_button.setObjectName("secondaryButton")
        save_button.clicked.connect(self._on_save)
        buttons_layout.addWidget(save_button)
        
        self.layout.addLayout(buttons_layout)
        
        # Espacio adicional
        self.layout.addStretch()
    
    def set_project(self, project_id, project_name):
        """Establece el proyecto a editar"""
        self.current_project_id = project_id
        self.title.setText(f"Editar Proyecto: {project_name}")
        
        # Obtener datos actuales del proyecto
        project_data = self.controller.get_project(project_id)
        if project_data:
            self.name_input.setText(project_data['name'])
    
    def _on_save(self):
        """Manejador para guardar los cambios"""
        if not self.current_project_id:
            QMessageBox.warning(
                self, 
                "Error", 
                "No se ha seleccionado un proyecto para editar."
            )
            return
            
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(
                self, 
                "Campos Incompletos", 
                "Por favor, complete todos los campos requeridos."
            )
            return
        
        try:
            # Llamar al método de actualización del controlador
            self.controller.update_project(self.current_project_id, name)
            
            QMessageBox.information(
                self,
                "Éxito",
                "El proyecto ha sido actualizado correctamente."
            )
            self.project_updated.emit(self.current_project_id)
            self.back_requested.emit()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error al Guardar", 
                f"No se pudo actualizar el proyecto: {str(e)}"
            )