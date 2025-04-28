from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QGroupBox, QFormLayout, QMessageBox,
    QComboBox, QDateEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime

from app.domain.entities.flow import RecurrenceType
from app.presentation.controllers.flow_controller import FlowController

class EditFlowView(QWidget):
    """Vista para editar un flujo existente"""
    
    back_requested = pyqtSignal()
    flow_updated = pyqtSignal(int)  # project_id
    
    def __init__(self):
        super().__init__()
        
        # Controlador
        self.controller = FlowController(self)
        
        # ID del flujo y proyecto actual
        self.current_flow_id = None
        self.current_project_id = None
        self.current_flow_data = None
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header con título y botón de volver
        header_layout = QHBoxLayout()
        
        back_button = QPushButton("Regresar")
        back_button.setMinimumWidth(120)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3b78e7;
            }
            QPushButton:pressed {
                background-color: #3367d6;
            }
        """)
        back_button.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_button)
        
        self.title = QLabel("Editar Flujo")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; margin-left: 15px;")
        header_layout.addWidget(self.title, 1)
        
        self.layout.addLayout(header_layout)
        
        # Línea separadora
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        separator.setStyleSheet("background-color: #e0e0e0;")
        self.layout.addWidget(separator)
        
        # Formulario
        form_group = QGroupBox("Información del flujo")
        form_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 20px;
                padding: 15px;
                background-color: white;
                color: #333333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: white;
                font-weight: bold;
                color: #333333;
            }
        """)
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 30, 20, 20)
        
        # Campo de nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del flujo")
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #2196f3;
            }
        """)
        form_layout.addRow("Nombre:", self.name_input)
        
        # Campo de recurrencia
        self.recurrence_combo = QComboBox()
        self.recurrence_combo.setMinimumHeight(40)
        self.recurrence_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                color: #333333;
            }
            QComboBox:focus {
                border: 1px solid #2196f3;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 20px;
                border-left-width: 0px;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
        for recurrence_type in RecurrenceType:
            self.recurrence_combo.addItem(recurrence_type.value, recurrence_type.value)
        form_layout.addRow("Recurrencia:", self.recurrence_combo)
        
        # Campo de propietario
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Ingrese el nombre del propietario")
        self.owner_input.setMinimumHeight(40)
        self.owner_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 1px solid #2196f3;
            }
        """)
        form_layout.addRow("Propietario:", self.owner_input)
        
        # Estado
        self.status_combo = QComboBox()
        self.status_combo.setMinimumHeight(40)
        self.status_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                color: #333333;
            }
            QComboBox:focus {
                border: 1px solid #2196f3;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 20px;
                border-left-width: 0px;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
        """)
        self.status_combo.addItem("Activo", "active")
        self.status_combo.addItem("Inactivo", "inactive")
        form_layout.addRow("Estado:", self.status_combo)
        
        self.layout.addWidget(form_group)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setMinimumSize(120, 40)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #555555;
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
                border: 1px solid #cccccc;
            }
        """)
        cancel_button.clicked.connect(self.back_requested.emit)
        buttons_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Guardar Cambios")
        save_button.setMinimumSize(150, 40)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        save_button.clicked.connect(self._on_save)
        buttons_layout.addWidget(save_button)
        
        self.layout.addLayout(buttons_layout)
        
        # Espacio adicional
        self.layout.addStretch()
    
    def set_flow(self, flow_id, project_id):
        """Establece el flujo a editar"""
        self.current_flow_id = flow_id
        self.current_project_id = project_id
        
        # Obtener datos actuales del flujo
        flow_data = self.controller.get_flow(flow_id)
        if flow_data:
            self.current_flow_data = flow_data
            self.title.setText(f"Editar Flujo: {flow_data['name']}")
            
            # Llenar el formulario con los datos actuales
            self.name_input.setText(flow_data['name'])
            
            # Establecer la recurrencia
            recurrence_index = 0
            for i in range(self.recurrence_combo.count()):
                if self.recurrence_combo.itemData(i) == flow_data['recurrence']:
                    recurrence_index = i
                    break
            self.recurrence_combo.setCurrentIndex(recurrence_index)
            
            # Establecer el propietario
            self.owner_input.setText(flow_data['owner'])
            
            # Establecer el estado
            status_index = 0 if flow_data['is_active'] else 1
            self.status_combo.setCurrentIndex(status_index)
    
    def _on_save(self):
        """Manejador para guardar los cambios"""
        if not self.current_flow_id or not self.current_project_id:
            QMessageBox.warning(
                self, 
                "Error", 
                "No se ha seleccionado un flujo para editar."
            )
            return
            
        name = self.name_input.text().strip()
        recurrence = self.recurrence_combo.currentData()
        owner = self.owner_input.text().strip()
        status = self.status_combo.currentData()
        
        if not name or not owner:
            QMessageBox.warning(
                self, 
                "Campos Incompletos", 
                "Por favor, complete todos los campos requeridos."
            )
            return
        
        try:
            flow = self.controller.update_flow(
                self.current_flow_id,
                name,
                recurrence,
                owner,
                status == "active"
            )
            if flow:
                QMessageBox.information(
                    self,
                    "Éxito",
                    "El flujo ha sido actualizado correctamente."
                )
                self.flow_updated.emit(self.current_project_id)
                self.back_requested.emit()
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error al Guardar", 
                f"No se pudo actualizar el flujo: {str(e)}"
            )