from app.infrastructure.database.connection import Database

class DatabaseSchema:
    """Clase para gestionar el esquema de la base de datos"""
    
    @staticmethod
    def create_tables():
        """Crea las tablas necesarias en la base de datos"""
        db = Database()
        
        # Tabla de proyectos
        db.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        
        # Tabla de flujos
        db.execute('''
            CREATE TABLE IF NOT EXISTS flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                recurrence TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        db.disconnect()
        
    @staticmethod
    def drop_tables():
        """Elimina las tablas de la base de datos"""
        db = Database()
        db.execute('DROP TABLE IF EXISTS flows')
        db.execute('DROP TABLE IF EXISTS projects')
        db.disconnect()
        
    @staticmethod
    def init_demo_data():
        """Inicializa datos de demostración"""
        from datetime import datetime
        from app.domain.entities.project import Project, ProjectStatus
        from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType
        from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository
        from app.infrastructure.repositories.sqlite_flow_repository import SQLiteFlowRepository
        
        project_repo = SQLiteProjectRepository()
        flow_repo = SQLiteFlowRepository()
        
        # Crear un proyecto de ejemplo
        project = Project(
            name="Proyecto XYZ",
            created_at=datetime.now(),
            status=ProjectStatus.ACTIVE
        )
        project = project_repo.create(project)
        
        # Crear flujos de ejemplo
        flow1 = Flow(
            project_id=project.id,
            name="Mandar Forms TC Share Point",
            recurrence=RecurrenceType.DAILY,
            created_at=datetime.now(),
            owner="Sebastián De la Torre",
            status=FlowStatus.ACTIVE
        )
        flow_repo.create(flow1)
        
        flow2 = Flow(
            project_id=project.id,
            name="Reminder Teams",
            recurrence=RecurrenceType.DAILY,
            created_at=datetime.now(),
            owner="Sebastián De la Torre",
            status=FlowStatus.ACTIVE
        )
        flow_repo.create(flow2)
        
        # Crear un segundo proyecto
        project2 = Project(
            name="Proyecto ABC",
            created_at=datetime.now(),
            status=ProjectStatus.INACTIVE
        )
        project_repo.create(project2)