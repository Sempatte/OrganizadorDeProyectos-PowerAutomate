# app/infrastructure/repositories/sqlite_project_repository.py
from typing import List, Optional
from datetime import datetime
from app.domain.entities.project import Project, ProjectStatus
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.database.connection import Database

class SQLiteProjectRepository(ProjectRepository):
    """Implementación SQLite del repositorio de proyectos"""
    
    def __init__(self):
        self.db = Database()
    
    def _map_to_entity(self, data: dict) -> Project:
        """Convierte un diccionario de datos a una entidad Project"""
        if not data:
            return None
            
        return Project(
            id=data['id'],
            name=data['name'],
            created_at=datetime.fromisoformat(data['created_at']),
            status=ProjectStatus(data['status'])
        )
    
    def get_all(self) -> List[Project]:
        """Obtiene todos los proyectos"""
        query = "SELECT * FROM projects ORDER BY created_at DESC"
        results = self.db.fetch_all(query)
        return [self._map_to_entity(data) for data in results]
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Obtiene un proyecto por su ID"""
        query = "SELECT * FROM projects WHERE id = ?"
        result = self.db.fetch_one(query, (project_id,))
        return self._map_to_entity(result) if result else None
    
    def create(self, project: Project) -> Project:
        """Crea un nuevo proyecto"""
        query = """
            INSERT INTO projects (name, created_at, status)
            VALUES (?, ?, ?)
        """
        cursor = self.db.execute(
            query, 
            (
                project.name, 
                project.created_at.isoformat(), 
                project.status.value
            )
        )
        project.id = cursor.lastrowid
        return project
    
    def update(self, project: Project) -> Project:
        """Actualiza un proyecto existente"""
        if not project.id:
            raise ValueError("No se puede actualizar un proyecto sin ID")
            
        query = """
            UPDATE projects
            SET name = ?, status = ?
            WHERE id = ?
        """
        self.db.execute(
            query, 
            (
                project.name,
                project.status.value,
                project.id
            )
        )
        return project
    
    def delete(self, project_id: int) -> bool:
        """Elimina un proyecto por su ID"""
        query = "DELETE FROM projects WHERE id = ?"
        cursor = self.db.execute(query, (project_id,))
        return cursor.rowcount > 0

# app/infrastructure/repositories/sqlite_flow_repository.py
from typing import List, Optional
from datetime import datetime
from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType
from app.domain.repositories.flow_repository import FlowRepository
from app.infrastructure.database.connection import Database

class SQLiteFlowRepository(FlowRepository):
    """Implementación SQLite del repositorio de flujos"""
    
    def __init__(self):
        self.db = Database()
    
    def _map_to_entity(self, data: dict) -> Flow:
        """Convierte un diccionario de datos a una entidad Flow"""
        if not data:
            return None
            
        return Flow(
            id=data['id'],
            project_id=data['project_id'],
            name=data['name'],
            recurrence=RecurrenceType(data['recurrence']),
            created_at=datetime.fromisoformat(data['created_at']),
            owner=data['owner'],
            status=FlowStatus(data['status'])
        )
    
    def get_all_by_project(self, project_id: int) -> List[Flow]:
        """Obtiene todos los flujos de un proyecto"""
        query = "SELECT * FROM flows WHERE project_id = ? ORDER BY created_at DESC"
        results = self.db.fetch_all(query, (project_id,))
        return [self._map_to_entity(data) for data in results]
    
    def get_by_id(self, flow_id: int) -> Optional[Flow]:
        """Obtiene un flujo por su ID"""
        query = "SELECT * FROM flows WHERE id = ?"
        result = self.db.fetch_one(query, (flow_id,))
        return self._map_to_entity(result) if result else None
    
    def create(self, flow: Flow) -> Flow:
        """Crea un nuevo flujo"""
        query = """
            INSERT INTO flows (project_id, name, recurrence, created_at, owner, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.db.execute(
            query, 
            (
                flow.project_id,
                flow.name, 
                flow.recurrence.value,
                flow.created_at.isoformat(),
                flow.owner,
                flow.status.value
            )
        )
        flow.id = cursor.lastrowid
        return flow
    
    def update(self, flow: Flow) -> Flow:
        """Actualiza un flujo existente"""
        if not flow.id:
            raise ValueError("No se puede actualizar un flujo sin ID")
            
        query = """
            UPDATE flows
            SET name = ?, recurrence = ?, owner = ?, status = ?
            WHERE id = ?
        """
        self.db.execute(
            query, 
            (
                flow.name,
                flow.recurrence.value,
                flow.owner,
                flow.status.value,
                flow.id
            )
        )
        return flow
    
    def delete(self, flow_id: int) -> bool:
        """Elimina un flujo por su ID"""
        query = "DELETE FROM flows WHERE id = ?"
        cursor = self.db.execute(query, (flow_id,))
        return cursor.rowcount > 0