from PyQt6.QtWidgets import QMessageBox
from app.application.services.project_service import ProjectService
from app.application.use_cases.project_use_cases import ProjectUseCases
from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository

class ProjectController:
    """Controlador para gestionar proyectos"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Inicializar el repositorio y el servicio
        self.project_repository = SQLiteProjectRepository()
        self.project_service = ProjectService(self.project_repository)
        
        # Inicializar los casos de uso con el servicio y el repositorio
        self.use_cases = ProjectUseCases(self.project_service, self.project_repository)
        
        # Conectar eventos
        self._connect_events()
    
    def _connect_events(self):
        """Conecta los eventos de la vista"""
        # Implementar según sea necesario
        pass
    
    def load_projects(self):
        """Carga la lista de proyectos"""
        try:
            projects = self.use_cases.list_projects()
            return projects
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Error",
                f"No se pudieron cargar los proyectos: {str(e)}"
            )
            return []
    
    def get_project(self, project_id):
        """Obtiene un proyecto por su ID"""
        try:
            project = self.use_cases.get_project_details(project_id)
            return project
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Error",
                f"No se pudo cargar el proyecto: {str(e)}"
            )
            return None
    
    def add_project(self, name):
        """Agrega un nuevo proyecto"""
        try:
            if not name.strip():
                raise ValueError("El nombre del proyecto no puede estar vacío")
                
            project = self.use_cases.add_new_project(name)
            return project
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Error",
                f"No se pudo agregar el proyecto: {str(e)}"
            )
            return None
    
    def toggle_project_status(self, project_id: int):
        """Cambia el estado de un proyecto"""
        try:
            return self.use_cases.toggle_project_status(project_id)
        except ValueError as e:
            QMessageBox.warning(
                self.parent,
                "Error",
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Error",
                f"Ocurrió un error inesperado: {str(e)}"
            )
    
    def delete_project(self, project_id):
        """Elimina un proyecto"""
        try:
            confirmation = QMessageBox.question(
                self.parent,
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este proyecto? Se eliminarán también todos los flujos asociados. Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirmation == QMessageBox.StandardButton.Yes:
                success = self.use_cases.remove_project(project_id)
                if success:
                    return True
                else:
                    raise ValueError("No se pudo eliminar el proyecto")
            return False
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Error",
                f"No se pudo eliminar el proyecto: {str(e)}"
            )
            return False
    
    def update_project(self, project_id, name):
        """Actualiza un proyecto existente"""
        self.use_cases.update_project(project_id, name)