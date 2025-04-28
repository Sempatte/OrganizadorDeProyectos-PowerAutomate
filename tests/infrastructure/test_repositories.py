import unittest
import os
import tempfile
from datetime import datetime

from app.domain.entities.project import Project, ProjectStatus
from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType
from app.infrastructure.database.connection import Database
from app.infrastructure.database.schema import DatabaseSchema
from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository
from app.infrastructure.repositories.sqlite_flow_repository import SQLiteFlowRepository

class TestSQLiteRepositories(unittest.TestCase):
    """Pruebas para los repositorios SQLite"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para las pruebas"""
        # Crear una base de datos temporal para las pruebas
        cls.temp_db_fd, cls.temp_db_path = tempfile.mkstemp()
        
        # Configurar la conexión a la base de datos temporal
        Database._instance = None  # Reset singleton
        cls.db = Database(cls.temp_db_path)
        
        # Crear las tablas
        DatabaseSchema.create_tables()
        
        # Inicializar repositorios
        cls.project_repository = SQLiteProjectRepository()
        cls.flow_repository = SQLiteFlowRepository()
    
    @classmethod
    def tearDownClass(cls):
        """Limpieza después de las pruebas"""
        cls.db.disconnect()
        os.close(cls.temp_db_fd)
        os.unlink(cls.temp_db_path)
    
    def setUp(self):
        """Configuración para cada prueba"""
        # Eliminar datos existentes
        self.db.execute("DELETE FROM flows")
        self.db.execute("DELETE FROM projects")
    
    def test_project_repository_create(self):
        """Prueba la creación de un proyecto en el repositorio"""
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        self.assertIsNotNone(created_project.id)
        self.assertEqual(created_project.name, "Test Project")
        self.assertEqual(created_project.status, ProjectStatus.ACTIVE)
    
    def test_project_repository_get_by_id(self):
        """Prueba obtener un proyecto por su ID"""
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        retrieved_project = self.project_repository.get_by_id(created_project.id)
        
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.id, created_project.id)
        self.assertEqual(retrieved_project.name, created_project.name)
        self.assertEqual(retrieved_project.status, created_project.status)
    
    def test_project_repository_get_all(self):
        """Prueba obtener todos los proyectos"""
        project1 = Project(name="Project 1", status=ProjectStatus.ACTIVE)
        project2 = Project(name="Project 2", status=ProjectStatus.INACTIVE)
        
        self.project_repository.create(project1)
        self.project_repository.create(project2)
        
        projects = self.project_repository.get_all()
        
        self.assertEqual(len(projects), 2)
        self.assertTrue(any(p.name == "Project 1" for p in projects))
        self.assertTrue(any(p.name == "Project 2" for p in projects))
    
    def test_project_repository_update(self):
        """Prueba actualizar un proyecto"""
        project = Project(name="Original Name", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        created_project.name = "Updated Name"
        created_project.status = ProjectStatus.INACTIVE
        
        updated_project = self.project_repository.update(created_project)
        
        self.assertEqual(updated_project.name, "Updated Name")
        self.assertEqual(updated_project.status, ProjectStatus.INACTIVE)
        
        # Verificar que los cambios se guardaron en la base de datos
        retrieved_project = self.project_repository.get_by_id(created_project.id)
        self.assertEqual(retrieved_project.name, "Updated Name")
        self.assertEqual(retrieved_project.status, ProjectStatus.INACTIVE)
    
    def test_project_repository_delete(self):
        """Prueba eliminar un proyecto"""
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        success = self.project_repository.delete(created_project.id)
        
        self.assertTrue(success)
        self.assertIsNone(self.project_repository.get_by_id(created_project.id))
    
    def test_flow_repository_create(self):
        """Prueba la creación de un flujo en el repositorio"""
        # Primero crear un proyecto
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        # Crear flujo asociado al proyecto
        flow = Flow(
            project_id=created_project.id,
            name="Test Flow",
            recurrence=RecurrenceType.DAILY,
            owner="Test Owner",
            status=FlowStatus.ACTIVE
        )
        created_flow = self.flow_repository.create(flow)
        
        self.assertIsNotNone(created_flow.id)
        self.assertEqual(created_flow.project_id, created_project.id)
        self.assertEqual(created_flow.name, "Test Flow")
        self.assertEqual(created_flow.recurrence, RecurrenceType.DAILY)
        self.assertEqual(created_flow.owner, "Test Owner")
        self.assertEqual(created_flow.status, FlowStatus.ACTIVE)
    
    def test_flow_repository_get_by_id(self):
        """Prueba obtener un flujo por su ID"""
        # Primero crear un proyecto
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        # Crear flujo
        flow = Flow(
            project_id=created_project.id,
            name="Test Flow",
            recurrence=RecurrenceType.DAILY,
            owner="Test Owner",
            status=FlowStatus.ACTIVE
        )
        created_flow = self.flow_repository.create(flow)
        
        retrieved_flow = self.flow_repository.get_by_id(created_flow.id)
        
        self.assertIsNotNone(retrieved_flow)
        self.assertEqual(retrieved_flow.id, created_flow.id)
        self.assertEqual(retrieved_flow.name, created_flow.name)
        self.assertEqual(retrieved_flow.project_id, created_flow.project_id)
        self.assertEqual(retrieved_flow.status, created_flow.status)
    
    def test_flow_repository_get_all_by_project(self):
        """Prueba obtener todos los flujos de un proyecto"""
        # Crear proyectos
        project1 = Project(name="Project 1", status=ProjectStatus.ACTIVE)
        project2 = Project(name="Project 2", status=ProjectStatus.ACTIVE)
        created_project1 = self.project_repository.create(project1)
        created_project2 = self.project_repository.create(project2)
        
        # Crear flujos para el primer proyecto
        flow1 = Flow(
            project_id=created_project1.id,
            name="Flow 1",
            recurrence=RecurrenceType.DAILY,
            owner="Owner 1",
            status=FlowStatus.ACTIVE
        )
        flow2 = Flow(
            project_id=created_project1.id,
            name="Flow 2",
            recurrence=RecurrenceType.WEEKLY,
            owner="Owner 2",
            status=FlowStatus.INACTIVE
        )
        self.flow_repository.create(flow1)
        self.flow_repository.create(flow2)
        
        # Crear flujo para el segundo proyecto
        flow3 = Flow(
            project_id=created_project2.id,
            name="Flow 3",
            recurrence=RecurrenceType.MONTHLY,
            owner="Owner 3",
            status=FlowStatus.ACTIVE
        )
        self.flow_repository.create(flow3)
        
        # Obtener flujos del primer proyecto
        flows_project1 = self.flow_repository.get_all_by_project(created_project1.id)
        
        self.assertEqual(len(flows_project1), 2)
        self.assertTrue(any(f.name == "Flow 1" for f in flows_project1))
        self.assertTrue(any(f.name == "Flow 2" for f in flows_project1))
        
        # Obtener flujos del segundo proyecto
        flows_project2 = self.flow_repository.get_all_by_project(created_project2.id)
        
        self.assertEqual(len(flows_project2), 1)
        self.assertEqual(flows_project2[0].name, "Flow 3")
    
    def test_flow_repository_update(self):
        """Prueba actualizar un flujo"""
        # Crear proyecto
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        # Crear flujo
        flow = Flow(
            project_id=created_project.id,
            name="Original Flow Name",
            recurrence=RecurrenceType.DAILY,
            owner="Original Owner",
            status=FlowStatus.ACTIVE
        )
        created_flow = self.flow_repository.create(flow)
        
        # Actualizar flujo
        created_flow.name = "Updated Flow Name"
        created_flow.recurrence = RecurrenceType.WEEKLY
        created_flow.owner = "Updated Owner"
        created_flow.status = FlowStatus.INACTIVE
        
        updated_flow = self.flow_repository.update(created_flow)
        
        self.assertEqual(updated_flow.name, "Updated Flow Name")
        self.assertEqual(updated_flow.recurrence, RecurrenceType.WEEKLY)
        self.assertEqual(updated_flow.owner, "Updated Owner")
        self.assertEqual(updated_flow.status, FlowStatus.INACTIVE)
        
        # Verificar que los cambios se guardaron en la base de datos
        retrieved_flow = self.flow_repository.get_by_id(created_flow.id)
        self.assertEqual(retrieved_flow.name, "Updated Flow Name")
        self.assertEqual(retrieved_flow.recurrence, RecurrenceType.WEEKLY)
        self.assertEqual(retrieved_flow.owner, "Updated Owner")
        self.assertEqual(retrieved_flow.status, FlowStatus.INACTIVE)
    
    def test_flow_repository_delete(self):
        """Prueba eliminar un flujo"""
        # Crear proyecto
        project = Project(name="Test Project", status=ProjectStatus.ACTIVE)
        created_project = self.project_repository.create(project)
        
        # Crear flujo
        flow = Flow(
            project_id=created_project.id,
            name="Test Flow",
            recurrence=RecurrenceType.DAILY,
            owner="Test Owner",
            status=FlowStatus.ACTIVE
        )
        created_flow = self.flow_repository.create(flow)
        
        # Eliminar flujo
        success = self.flow_repository.delete(created_flow.id)
        
        self.assertTrue(success)
        self.assertIsNone(self.flow_repository.get_by_id(created_flow.id))

# tests/infrastructure/__init__.py
# Archivo vacío para permitir importaciones