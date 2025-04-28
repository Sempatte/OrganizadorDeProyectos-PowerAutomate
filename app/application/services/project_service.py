# app/application/services/project_service.py
from typing import List, Optional
from app.domain.entities.project import Project, ProjectStatus
from app.domain.repositories.project_repository import ProjectRepository

class ProjectService:
    """Servicio para gestionar proyectos"""
    
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    def get_all_projects(self) -> List[Project]:
        """Obtiene todos los proyectos"""
        return self.project_repository.get_all()
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Obtiene un proyecto por su ID"""
        return self.project_repository.get_by_id(project_id)
    
    def create_project(self, name: str) -> Project:
        """Crea un nuevo proyecto"""
        project = Project(name=name, status=ProjectStatus.ACTIVE)
        return self.project_repository.create(project)
    
    def update_project(self, project: Project) -> Project:
        """Actualiza un proyecto existente"""
        return self.project_repository.update(project)
    
    def delete_project(self, project_id: int) -> bool:
        """Elimina un proyecto por su ID"""
        return self.project_repository.delete(project_id)
    
    def toggle_project_status(self, project_id: int) -> Project:
        """Cambia el estado de un proyecto"""
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ValueError("El proyecto no existe.")
        
        # Alternar el estado del proyecto
        if project.status == ProjectStatus.ACTIVE:
            project.status = ProjectStatus.INACTIVE
        else:
            project.status = ProjectStatus.ACTIVE
        
        # Actualizar el proyecto en el repositorio
        return self.project_repository.update(project)

