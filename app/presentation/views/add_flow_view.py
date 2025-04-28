from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QGroupBox, QFormLayout, QMessageBox,
    QComboBox, QDateEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime

from app.domain.entities.flow import RecurrenceType
from app.presentation.controllers.flow_controller import FlowController

class AddFlowView(QWidget):
    """Vista para agregar un nuevo flujo"""
    
    back_requested = pyqtSignal()
    flow_added = pyqtSignal(int)  # project_id
    
    def __init__(self):
        super().__init__()
        
        # Controlador
        self.controller = FlowController(self)
        
        # ID y nombre del proyecto actual
        self.current_project_id = None
        self.current_project_name = None
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con título y botón de volver
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("Regresar")
        back_button.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_button)
        
        self.title = QLabel("Agregar Flujo")
        self.title.setObjectName("titleLabel")
        header_layout.addWidget(self.title, 1)
        
        self.layout.addLayout(header_layout)
        
        # Formulario
        form_group = QGroupBox("Formulario para agregar flujo con todos los campos necesarios")
        form_layout = QFormLayout(form_group)
        
        # Campo de nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del flujo")
        form_layout.addRow("Nombre:", self.name_input)
        
        # Campo de recurrencia
        self.recurrence_combo = QComboBox()
        for recurrence_type in RecurrenceType:
            self.recurrence_combo.addItem(recurrence_type.value, recurrence_type.value)
        form_layout.addRow("Recurrencia:", self.recurrence_combo)
        
        # Campo de propietario
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Ingrese el nombre del propietario")
        form_layout.addRow("Propietario:", self.owner_input)
        
        for i in range(form_layout.rowCount()):
            item = form_layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            if item and item.widget():
                item.widget().setStyleSheet("color: #333333;")
        
        self.layout.addWidget(form_group)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.back_requested.emit)
        buttons_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Guardar Flujo")
        save_button.setObjectName("secondaryButton")
        save_button.clicked.connect(self._on_save)
        buttons_layout.addWidget(save_button)
        
        self.layout.addLayout(buttons_layout)
        
        # Espacio adicional
        self.layout.addStretch()
    
    def set_project(self, project_id, project_name):
        """Establece el proyecto actual"""
        self.current_project_id = project_id
        self.current_project_name = project_name
        self.title.setText(f"Agregar Flujo al Proyecto {project_name}")
    
    def _on_save(self):
        """Manejador para guardar un nuevo flujo"""
        if not self.current_project_id:
            QMessageBox.warning(
                self, 
                "Error", 
                "No se ha seleccionado un proyecto."
            )
            return
            
        name = self.name_input.text().strip()
        recurrence = self.recurrence_combo.currentData()
        owner = self.owner_input.text().strip()
        
        if not name or not owner:
            QMessageBox.warning(
                self, 
                "Campos Incompletos", 
                "Por favor, complete todos los campos requeridos."
            )
            return
        
        try:
            flow = self.controller.add_flow(
                self.current_project_id,
                name,
                recurrence,
                owner
            )
            if flow:
                self.flow_added.emit(self.current_project_id)
                self._clear_form()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error al Guardar", 
                f"No se pudo guardar el flujo: {str(e)}"
            )
    
    def _clear_form(self):
        """Limpia el formulario"""
        self.name_input.clear()
        self.recurrence_combo.setCurrentIndex(0)
        self.owner_input.clear()