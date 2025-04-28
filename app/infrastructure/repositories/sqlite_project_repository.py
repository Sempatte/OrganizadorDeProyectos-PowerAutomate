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
        """Actualiza un proyecto en la base de datos"""
        query = """
        UPDATE projects
        SET name = ?, status = ?
        WHERE id = ?
        """
        with self.db.connection as conn:
            conn.execute(query, (project.name, project.status.value, project.id))
        return project
    
    def delete(self, project_id: int) -> bool:
        """Elimina un proyecto por su ID"""
        query = "DELETE FROM projects WHERE id = ?"
        cursor = self.db.execute(query, (project_id,))
        return cursor.rowcount > 0
