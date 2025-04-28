# tests/domain/test_entities.py
import unittest
from datetime import datetime
from app.domain.entities.project import Project, ProjectStatus
from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType

class TestProjectEntity(unittest.TestCase):
    """Pruebas para la entidad Project"""
    
    def test_project_creation(self):
        """Prueba la creación de un proyecto"""
        project = Project(
            id=1,
            name="Test Project",
            created_at=datetime.now(),
            status=ProjectStatus.ACTIVE
        )
        
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.status, ProjectStatus.ACTIVE)
        self.assertTrue(project.is_active)
    
    def test_project_status_change(self):
        """Prueba el cambio de estado de un proyecto"""
        project = Project(
            name="Test Project",
            status=ProjectStatus.ACTIVE
        )
        
        self.assertTrue(project.is_active)
        
        # Desactivar el proyecto
        project.deactivate()
        self.assertEqual(project.status, ProjectStatus.INACTIVE)
        self.assertFalse(project.is_active)
        
        # Activar de nuevo
        project.activate()
        self.assertEqual(project.status, ProjectStatus.ACTIVE)
        self.assertTrue(project.is_active)

class TestFlowEntity(unittest.TestCase):
    """Pruebas para la entidad Flow"""
    
    def test_flow_creation(self):
        """Prueba la creación de un flujo"""
        flow = Flow(
            id=1,
            project_id=2,
            name="Test Flow",
            recurrence=RecurrenceType.DAILY,
            created_at=datetime.now(),
            owner="Test Owner",
            status=FlowStatus.ACTIVE
        )
        
        self.assertEqual(flow.id, 1)
        self.assertEqual(flow.project_id, 2)
        self.assertEqual(flow.name, "Test Flow")
        self.assertEqual(flow.recurrence, RecurrenceType.DAILY)
        self.assertEqual(flow.owner, "Test Owner")
        self.assertEqual(flow.status, FlowStatus.ACTIVE)
        self.assertTrue(flow.is_active)
    
    def test_flow_status_change(self):
        """Prueba el cambio de estado de un flujo"""
        flow = Flow(
            name="Test Flow",
            project_id=1,
            recurrence=RecurrenceType.DAILY,
            owner="Test Owner",
            status=FlowStatus.ACTIVE
        )
        
        self.assertTrue(flow.is_active)
        
        # Desactivar el flujo
        flow.deactivate()
        self.assertEqual(flow.status, FlowStatus.INACTIVE)
        self.assertFalse(flow.is_active)
        
        # Activar de nuevo
        flow.activate()
        self.assertEqual(flow.status, FlowStatus.ACTIVE)
        self.assertTrue(flow.is_active)

# tests/__init__.py
# Archivo vacío para permitir importaciones

# tests/domain/__init__.py
# Archivo vacío para permitir importaciones