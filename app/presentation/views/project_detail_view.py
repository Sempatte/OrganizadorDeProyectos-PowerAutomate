from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QMenu, QMessageBox, QFrame, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QWidgetAction
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QColor, QIcon, QFont, QAction

from app.presentation.controllers.project_controller import ProjectController
from app.presentation.controllers.flow_controller import FlowController

class ProjectDetailView(QWidget):
    """Vista de detalle de un proyecto"""
    
    back_requested = pyqtSignal()
    add_flow_requested = pyqtSignal(int, str)  # project_id, project_name
    edit_flow_requested = pyqtSignal(int, int)  # flow_id, project_id
    project_updated = pyqtSignal(int)  # project_id
    edit_project_requested = pyqtSignal(int, str)  # project_id, project_name
    
    def __init__(self):
        super().__init__()
        
        # Controladores
        self.project_controller = ProjectController(self)
        self.flow_controller = FlowController(self)
        
        # ID y nombre del proyecto actual
        self.current_project_id = None
        self.current_project_name = None
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header con título y botones
        header_container = QHBoxLayout()
        
        # Botón Regresar
        self.back_button = QPushButton("Regresar")
        self.back_button.setMinimumWidth(120)
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.back_requested.emit)
        header_container.addWidget(self.back_button)
        
        # Título
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        
        self.project_title = QLabel("Flujos del proyecto")
        self.project_title.setObjectName("titleLabel")
        self.project_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; margin-left: 15px;")
        title_container.addWidget(self.project_title)
        
        self.project_subtitle = QLabel("Gestione los flujos de automatización para este proyecto")
        self.project_subtitle.setStyleSheet("font-size: 14px; color: #666666; margin-left: 15px;")
        title_container.addWidget(self.project_subtitle)
        
        header_container.addLayout(title_container, 1)
        
        # Botón Agregar Flujo
        self.add_flow_button = QPushButton("Agregar Flujo")
        self.add_flow_button.setMinimumWidth(150)
        self.add_flow_button.setStyleSheet("""
            QPushButton {
                background-color: #9c27b0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
            QPushButton:pressed {
                background-color: #7b1fa2;
            }
        """)
        self.add_flow_button.clicked.connect(self._on_add_flow)
        header_container.addWidget(self.add_flow_button)
        
        self.layout.addLayout(header_container)
        
        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        self.layout.addWidget(separator)
        
        # Panel de información del proyecto
        info_panel = QFrame()
        info_panel.setFrameShape(QFrame.Shape.StyledPanel)
        info_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        # Aplicar sombra al panel
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        info_panel.setGraphicsEffect(shadow)
        
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(20, 15, 20, 15)
        
        # Estado del proyecto
        status_container = QHBoxLayout()
        status_container.setSpacing(10)
        
        self.project_status_label = QLabel("Estado:")
        self.project_status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #555555;")
        status_container.addWidget(self.project_status_label)
        
        self.project_status_value = QLabel("Activo")
        self.project_status_value.setObjectName("activeStatus")
        self.project_status_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #4caf50;")
        status_container.addWidget(self.project_status_value)
        
        self.toggle_status_button = QPushButton("Cambiar Estado")
        self.toggle_status_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #555555;
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
                border: 1px solid #cccccc;
            }
        """)
        self.toggle_status_button.clicked.connect(self._on_toggle_project_status)
        status_container.addWidget(self.toggle_status_button)
        
        status_container.addStretch(1)
        
        info_layout.addLayout(status_container, 3)
        
        # Separador vertical
        vseparator = QFrame()
        vseparator.setFrameShape(QFrame.Shape.VLine)
        vseparator.setFrameShadow(QFrame.Shadow.Sunken)
        vseparator.setStyleSheet("background-color: #e0e0e0;")
        info_layout.addWidget(vseparator)
        
        # Botón de eliminar proyecto
        delete_container = QHBoxLayout()
        delete_container.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.delete_project_button = QPushButton("Eliminar Proyecto")
        self.delete_project_button.setObjectName("dangerButton")
        self.delete_project_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.delete_project_button.clicked.connect(self._on_delete_project)
        delete_container.addWidget(self.delete_project_button)

        self.edit_project_button = QPushButton("Editar Proyecto")
        self.edit_project_button.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b78e7;
            }
            QPushButton:pressed {
                background-color: #3367d6;
            }
        """)
        self.edit_project_button.clicked.connect(self._on_edit_project)
        delete_container.addWidget(self.edit_project_button)
        
        info_layout.addLayout(delete_container, 1)
        
        self.layout.addWidget(info_panel)
        
        # Título de la tabla
        table_header = QHBoxLayout()
        
        table_title = QLabel("Flujos de Trabajo")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333; margin-top: 10px;")
        table_header.addWidget(table_title)
        
        table_subtitle = QLabel("Haga clic derecho sobre un flujo para ver más opciones")
        table_subtitle.setStyleSheet("font-size: 13px; color: #666666; margin-top: 10px;")
        table_header.addStretch(1)
        table_header.addWidget(table_subtitle)
        
        self.layout.addLayout(table_header)
        
        # Tabla de flujos mejorada
        self.flows_table = QTableWidget()
        self.flows_table.setColumnCount(6)  # Añadimos una columna más para el número
        self.flows_table.setHorizontalHeaderLabels(["#", "Nombre", "Recurrencia", "Creado", "Owner", "Estado"])
        
        # Estilo de la tabla
        self.flows_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #eeeeee;
                selection-background-color: #e3f2fd;
                selection-color: #2196f3;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QTableCornerButton::section {
                background-color: #f5f5f5;
                border: none;
            }
        """)
        
        # Aplicar sombra a la tabla
        table_shadow = QGraphicsDropShadowEffect()
        table_shadow.setBlurRadius(15)
        table_shadow.setColor(QColor(0, 0, 0, 30))
        table_shadow.setOffset(0, 3)
        self.flows_table.setGraphicsEffect(table_shadow)
        
        # Configurar ancho de las columnas
        self.flows_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.flows_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        # Altura de las filas
        self.flows_table.verticalHeader().setDefaultSectionSize(40)
        self.flows_table.verticalHeader().setVisible(False)
        
        # Menú contextual
        self.flows_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.flows_table.customContextMenuRequested.connect(self._show_context_menu)
        
        # Permitir doble clic para editar
        self.flows_table.cellDoubleClicked.connect(self._on_flow_double_clicked)
        
        self.layout.addWidget(self.flows_table)
        
        # Placeholder para tabla vacía
        self.empty_message = QLabel("No hay flujos para este proyecto. Haga clic en 'Agregar Flujo' para comenzar.")
        self.empty_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_message.setStyleSheet("font-size: 14px; color: #666666; margin: 40px 0;")
        self.empty_message.setVisible(False)
        self.layout.addWidget(self.empty_message)
    
    def set_project(self, project_id, project_name):
        """Establece el proyecto actual y actualiza la vista"""
        self.current_project_id = project_id
        self.current_project_name = project_name
        self.project_title.setText(f"Flujos del proyecto {project_name}")
        
        # Obtener detalles del proyecto
        project = self.project_controller.get_project(project_id)
        if project:
            # Actualizar estado del proyecto
            is_active = project.get('is_active', True)
            status_text = "Activo" if is_active else "Inactivo"
            status_color = "#4caf50" if is_active else "#f44336"
            self.project_status_value.setText(status_text)
            self.project_status_value.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {status_color};")
        
        self.refresh_flows()
    
    def refresh_flows(self):
        """Actualiza la lista de flujos del proyecto"""
        if not self.current_project_id:
            return
            
        # Limpiar tabla
        self.flows_table.setRowCount(0)
        
        # Obtener flujos
        flows = self.flow_controller.load_flows(self.current_project_id)
        
        # Mostrar mensaje si no hay flujos
        if not flows:
            self.flows_table.setVisible(False)
            self.empty_message.setVisible(True)
            return
        else:
            self.flows_table.setVisible(True)
            self.empty_message.setVisible(False)
        
        # Añadir filas a la tabla
        for i, flow in enumerate(flows):
            self.flows_table.insertRow(i)
            
            # Número de fila
            item_num = QTableWidgetItem(str(i + 1))
            item_num.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_num.setData(Qt.ItemDataRole.UserRole, flow['id'])  # Guardar ID del flujo
            self.flows_table.setItem(i, 0, item_num)
            
            # Nombre
            item_name = QTableWidgetItem(flow['name'])
            self.flows_table.setItem(i, 1, item_name)
            
            # Recurrencia
            item_recurrence = QTableWidgetItem(flow['recurrence'])
            item_recurrence.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.flows_table.setItem(i, 2, item_recurrence)
            
            # Fecha de creación
            item_date = QTableWidgetItem(flow['created_at'])
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.flows_table.setItem(i, 3, item_date)
            
            # Owner
            item_owner = QTableWidgetItem(flow['owner'])
            self.flows_table.setItem(i, 4, item_owner)
            
            # Estado
            status_text = "Activo" if flow['is_active'] else "Inactivo"
            item_status = QTableWidgetItem(status_text)
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color según estado
            if flow['is_active']:
                item_status.setForeground(QColor("#4caf50"))  # Verde para activo
            else:
                item_status.setForeground(QColor("#f44336"))  # Rojo para inactivo
                
            self.flows_table.setItem(i, 5, item_status)
    
    def _on_add_flow(self):
        """Manejador para agregar un nuevo flujo"""
        if self.current_project_id and self.current_project_name:
            self.add_flow_requested.emit(self.current_project_id, self.current_project_name)
    
    def _on_toggle_project_status(self):
        """Manejador para cambiar el estado del proyecto"""
        if not self.current_project_id:
            return
            
        project = self.project_controller.toggle_project_status(self.current_project_id)
        if project:
            # Actualizar estado del proyecto en la interfaz
            is_active = project.get('is_active', True)
            status_text = "Activo" if is_active else "Inactivo"
            status_color = "#4caf50" if is_active else "#f44336"
            self.project_status_value.setText(status_text)
            self.project_status_value.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {status_color};")
            
            # Emitir señal de actualización
            self.project_updated.emit(self.current_project_id)
    
    def _on_delete_project(self):
        """Manejador para eliminar el proyecto"""
        if not self.current_project_id:
            return
            
        success = self.project_controller.delete_project(self.current_project_id)
        if success:
            self.back_requested.emit()
    
    def _on_edit_project(self):
        """Manejador para editar el proyecto"""
        if self.current_project_id and self.current_project_name:
            self.edit_project_requested.emit(self.current_project_id, self.current_project_name)
    
    def _on_flow_double_clicked(self, row, column):
        """Manejador para el evento de doble clic en un flujo"""
        flow_id = self.flows_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.edit_flow_requested.emit(flow_id, self.current_project_id)
    
    def _show_context_menu(self, position):
        """Muestra el menú contextual al hacer clic derecho en un flujo"""
        # Obtener el item seleccionado
        item = self.flows_table.itemAt(position)
        if not item:
            return
            
        row = item.row()
        flow_id = self.flows_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Estilo del menú contextual
        menu_style = """
            QMenu {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 25px 5px 25px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #2196f3;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e0e0;
                margin: 3px 10px;
            }
        """
        
        # Crear menú contextual
        context_menu = QMenu(self)
        context_menu.setStyleSheet(menu_style)
        
        flow_name = self.flows_table.item(row, 1).text()
        title_widget = QLabel(f"  {flow_name}  ")
        title_widget.setStyleSheet("font-weight: bold; color: #333333; padding: 3px;")
        
        # Crear acciones para el menú
        title_action = QWidgetAction(context_menu)
        title_action.setDefaultWidget(title_widget)
        
        context_menu.addAction(title_action)
        context_menu.addSeparator()
        
        # Opción para editar
        edit_action = context_menu.addAction("Editar Flujo")
        edit_action.triggered.connect(lambda: self._edit_flow(flow_id))
        
        # Opción para cambiar estado
        toggle_status_action = context_menu.addAction("Cambiar Estado")
        toggle_status_action.triggered.connect(lambda: self._toggle_flow_status(flow_id, row))
        
        # Opción para eliminar
        context_menu.addSeparator()
        delete_action = context_menu.addAction("Eliminar Flujo")
        delete_action.triggered.connect(lambda: self._delete_flow(flow_id))
        
        # Mostrar menú contextual
        context_menu.exec(QCursor.pos())
    
    def _edit_flow(self, flow_id):
        """Editar un flujo"""
        if self.current_project_id:
            self.edit_flow_requested.emit(flow_id, self.current_project_id)
    
    def _toggle_flow_status(self, flow_id, row):
        """Cambia el estado de un flujo"""
        flow = self.flow_controller.toggle_flow_status(flow_id)
        if flow:
            # Actualizar estado en la tabla
            is_active = flow.get('is_active', True)
            status_text = "Activo" if is_active else "Inactivo"
            status_color = "#4caf50" if is_active else "#f44336"
            
            item_status = self.flows_table.item(row, 5)
            item_status.setText(status_text)
            item_status.setForeground(QColor(status_color))
    
    def _delete_flow(self, flow_id):
        """Elimina un flujo"""
        success = self.flow_controller.delete_flow(flow_id)
        if success:
            self.refresh_flows()