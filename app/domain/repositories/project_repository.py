# app/domain/repositories/project_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.project import Project

class ProjectRepository(ABC):
    """Interfaz para el repositorio de proyectos"""
    
    @abstractmethod
    def get_all(self) -> List[Project]:
        """Obtiene todos los proyectos"""
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Obtiene un proyecto por su ID"""
        pass
    
    @abstractmethod
    def create(self, project: Project) -> Project:
        """Crea un nuevo proyecto"""
        pass
    
    @abstractmethod
    def update(self, project: Project) -> Project:
        """Actualiza un proyecto existente"""
        pass
    
    @abstractmethod
    def delete(self, project_id: int) -> bool:
        """Elimina un proyecto por su ID"""
        pass

# app/domain/repositories/flow_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.flow import Flow

class FlowRepository(ABC):
    """Interfaz para el repositorio de flujos"""
    
    @abstractmethod
    def get_all_by_project(self, project_id: int) -> List[Flow]:
        """Obtiene todos los flujos de un proyecto"""
        pass
    
    @abstractmethod
    def get_by_id(self, flow_id: int) -> Optional[Flow]:
        """Obtiene un flujo por su ID"""
        pass
    
    @abstractmethod
    def create(self, flow: Flow) -> Flow:
        """Crea un nuevo flujo"""
        pass
    
    @abstractmethod
    def update(self, flow: Flow) -> Flow:
        """Actualiza un flujo existente"""
        pass
    
    @abstractmethod
    def delete(self, flow_id: int) -> bool:
        """Elimina un flujo por su ID"""
        pass