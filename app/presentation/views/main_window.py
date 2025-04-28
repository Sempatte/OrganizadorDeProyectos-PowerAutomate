import os
from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QVBoxLayout, 
    QWidget, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFontDatabase, QFont

from app.presentation.views.project_list_view import ProjectListView
from app.presentation.views.project_detail_view import ProjectDetailView
from app.presentation.views.add_project_view import AddProjectView
from app.presentation.views.add_flow_view import AddFlowView
from app.presentation.views.edit_flow_view import EditFlowView
from app.presentation.views.edit_project_view import EditProjectView

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    edit_project_requested = pyqtSignal(int, str)  # project_id, project_name
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("Flujos de Power Automate Yape")
        self.setMinimumSize(900, 600)
        
        # Cargar estilos
        self._load_styles()
        
        # Crear widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear header
        self._create_header()
        
        # Crear el stacked widget para las diferentes vistas
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Inicializar vistas
        self.project_list_view = None
        self.project_detail_view = None
        self.add_project_view = None
        self.add_flow_view = None
        self.edit_flow_view = None
        self.edit_project_view = None  # Agregar esta línea
        
        # Iniciar con la vista de lista de proyectos
        self._initialize_views()
    
    def _load_styles(self):
        """Carga los estilos CSS de la aplicación"""
        style_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'assets', 
            'styles.qss'
        )
        
        try:
            with open(style_path, 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error al cargar los estilos: {e}")
    
    def _create_header(self):
        """Crea el header de la aplicación"""
        header = QWidget()
        header.setObjectName("appHeader")
        header.setFixedHeight(60)
        
        header_layout = QHBoxLayout(header)
        
        # Título de la aplicación
        title = QLabel("Flujos de Power Automate Yape")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        # Agregar el header al layout principal
        self.main_layout.addWidget(header)
    
    def _initialize_views(self):
        """Inicializa las vistas de la aplicación"""
        # Vista de lista de proyectos
        self.project_list_view = ProjectListView()
        self.stacked_widget.addWidget(self.project_list_view)
        
        # Conectar señales de la vista de lista de proyectos
        self.project_list_view.project_selected.connect(self.show_project_detail)
        self.project_list_view.add_project_requested.connect(self.show_add_project)
        
        # Mostrar la vista de lista de proyectos
        self.stacked_widget.setCurrentWidget(self.project_list_view)
    
    def show_project_detail(self, project_id, project_name):
        """Muestra la vista de detalle de un proyecto"""
        if not self.project_detail_view:
            self.project_detail_view = ProjectDetailView()
            self.stacked_widget.addWidget(self.project_detail_view)
            
            # Conectar señales
            self.project_detail_view.back_requested.connect(
                lambda: self.stacked_widget.setCurrentWidget(self.project_list_view)
            )
            self.project_detail_view.add_flow_requested.connect(self.show_add_flow)
            self.project_detail_view.edit_flow_requested.connect(self.show_edit_flow)
            self.project_detail_view.project_updated.connect(self._refresh_project_list)
            self.project_detail_view.edit_project_requested.connect(self.show_edit_project)
        
        self.project_detail_view.set_project(project_id, project_name)
        self.stacked_widget.setCurrentWidget(self.project_detail_view)
    
    def show_add_project(self):
        """Muestra la vista de agregar proyecto"""
        if not self.add_project_view:
            self.add_project_view = AddProjectView()
            self.stacked_widget.addWidget(self.add_project_view)
            
            # Conectar señales
            self.add_project_view.back_requested.connect(
                lambda: self.stacked_widget.setCurrentWidget(self.project_list_view)
            )
            self.add_project_view.project_added.connect(self.on_project_added)
        
        self.stacked_widget.setCurrentWidget(self.add_project_view)
    
    def show_add_flow(self, project_id, project_name):
        """Muestra la vista de agregar flujo"""
        if not self.add_flow_view:
            self.add_flow_view = AddFlowView()
            self.stacked_widget.addWidget(self.add_flow_view)
            
            # Conectar señales
            self.add_flow_view.back_requested.connect(
                lambda: self.project_detail_view and 
                self.stacked_widget.setCurrentWidget(self.project_detail_view)
            )
            self.add_flow_view.flow_added.connect(self.on_flow_added)
        
        self.add_flow_view.set_project(project_id, project_name)
        self.stacked_widget.setCurrentWidget(self.add_flow_view)
    
    def show_edit_flow(self, flow_id, project_id):
        """Muestra la vista de edición de flujo"""
        if not self.edit_flow_view:
            self.edit_flow_view = EditFlowView()
            self.stacked_widget.addWidget(self.edit_flow_view)
            
            # Conectar señales
            self.edit_flow_view.back_requested.connect(
                lambda: self.project_detail_view and 
                self.stacked_widget.setCurrentWidget(self.project_detail_view)
            )
            self.edit_flow_view.flow_updated.connect(self.on_flow_updated)
        
        self.edit_flow_view.set_flow(flow_id, project_id)
        self.stacked_widget.setCurrentWidget(self.edit_flow_view)
    
    def show_edit_project(self, project_id, project_name):
        """Muestra la vista de edición de proyecto"""
        if not self.edit_project_view:
            self.edit_project_view = EditProjectView()
            self.stacked_widget.addWidget(self.edit_project_view)
            
            # Conectar señales
            self.edit_project_view.back_requested.connect(
                lambda: self.stacked_widget.setCurrentWidget(self.project_detail_view)
            )
            self.edit_project_view.project_updated.connect(self._refresh_project_list)
        
        self.edit_project_view.set_project(project_id, project_name)
        self.stacked_widget.setCurrentWidget(self.edit_project_view)
    
    def on_project_added(self):
        """Manejador para cuando se agrega un proyecto"""
        self.project_list_view.refresh_projects()
        self.stacked_widget.setCurrentWidget(self.project_list_view)
    
    def on_flow_added(self, project_id):
        """Manejador para cuando se agrega un flujo"""
        if self.project_detail_view:
            self.project_detail_view.refresh_flows()
            self.stacked_widget.setCurrentWidget(self.project_detail_view)
    
    def on_flow_updated(self, project_id):
        """Manejador para cuando se actualiza un flujo"""
        if self.project_detail_view:
            self.project_detail_view.refresh_flows()
            self.stacked_widget.setCurrentWidget(self.project_detail_view)
    
    def _refresh_project_list(self, project_id=None):
        """Actualiza la lista de proyectos"""
        if self.project_list_view:
            self.project_list_view.refresh_projects()