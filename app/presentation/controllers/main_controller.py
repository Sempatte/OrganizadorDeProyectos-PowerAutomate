# app/presentation/controllers/main_controller.py
from app.presentation.views.main_window import MainWindow
from app.infrastructure.database.schema import DatabaseSchema

class MainController:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        # Inicializar la base de datos
        self._init_database()
        
        # Crear la ventana principal
        self.main_window = MainWindow()
    
    def _init_database(self):
        """Inicializa la base de datos"""
        DatabaseSchema.create_tables()
    
    def show(self):
        """Muestra la ventana principal"""
        self.main_window.show()

# app/presentation/controllers/project_controller.py
from PyQt6.QtWidgets import QMessageBox
from app.application.services.project_service import ProjectService
from app.application.use_cases.project_use_cases import ProjectUseCases
from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository

class ProjectController:
    """Controlador para gestionar proyectos"""
    
    def __init__(self, view):
        self.view = view
        
        # Repositorios y servicios
        self.project_repository = SQLiteProjectRepository()
        self.project_service = ProjectService(self.project_repository)
        self.project_use_cases = ProjectUseCases(self.project_service)
        
        # Conectar eventos
        self._connect_events()
    
    def _connect_events(self):
        """Conecta los eventos de la vista"""
        # Implementar según sea necesario
        pass
    
    def load_projects(self):
        """Carga la lista de proyectos"""
        try:
            projects = self.project_use_cases.list_projects()
            return projects
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudieron cargar los proyectos: {str(e)}"
            )
            return []
    
    def add_project(self, name):
        """Agrega un nuevo proyecto"""
        try:
            project = self.project_use_cases.add_new_project(name)
            return project
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo agregar el proyecto: {str(e)}"
            )
            return None
    
    def toggle_project_status(self, project_id):
        """Cambia el estado de un proyecto"""
        try:
            project = self.project_use_cases.change_project_status(project_id)
            return project
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo cambiar el estado del proyecto: {str(e)}"
            )
            return None

# app/presentation/controllers/flow_controller.py
from PyQt6.QtWidgets import QMessageBox
from app.application.services.flow_service import FlowService
from app.application.use_cases.flow_use_cases import FlowUseCases
from app.infrastructure.repositories.sqlite_flow_repository import SQLiteFlowRepository

class FlowController:
    """Controlador para gestionar flujos"""
    
    def __init__(self, view):
        self.view = view
        
        # Repositorios y servicios
        self.flow_repository = SQLiteFlowRepository()
        self.flow_service = FlowService(self.flow_repository)
        self.flow_use_cases = FlowUseCases(self.flow_service)
        
        # Conectar eventos
        self._connect_events()
    
    def _connect_events(self):
        """Conecta los eventos de la vista"""
        # Implementar según sea necesario
        pass
    
    def load_flows(self, project_id):
        """Carga la lista de flujos de un proyecto"""
        try:
            flows = self.flow_use_cases.list_flows_by_project(project_id)
            return flows
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudieron cargar los flujos: {str(e)}"
            )
            return []
    
    def add_flow(self, project_id, name, recurrence, owner):
        """Agrega un nuevo flujo"""
        try:
            flow = self.flow_use_cases.add_new_flow(
                project_id, name, recurrence, owner
            )
            return flow
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo agregar el flujo: {str(e)}"
            )
            return None
    
    def toggle_flow_status(self, flow_id):
        """Cambia el estado de un flujo"""
        try:
            flow = self.flow_use_cases.change_flow_status(flow_id)
            return flow
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo cambiar el estado del flujo: {str(e)}"
            )
            return None