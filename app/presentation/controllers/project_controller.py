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
    
    def get_project(self, project_id):
        """Obtiene un proyecto por su ID"""
        try:
            project = self.project_use_cases.get_project_details(project_id)
            return project
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo cargar el proyecto: {str(e)}"
            )
            return None
    
    def add_project(self, name):
        """Agrega un nuevo proyecto"""
        try:
            if not name.strip():
                raise ValueError("El nombre del proyecto no puede estar vacío")
                
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
    
    def delete_project(self, project_id):
        """Elimina un proyecto"""
        try:
            confirmation = QMessageBox.question(
                self.view,
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este proyecto? Se eliminarán también todos los flujos asociados. Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirmation == QMessageBox.StandardButton.Yes:
                success = self.project_use_cases.remove_project(project_id)
                if success:
                    return True
                else:
                    raise ValueError("No se pudo eliminar el proyecto")
            return False
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo eliminar el proyecto: {str(e)}"
            )
            return False