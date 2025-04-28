import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

from app.domain.entities.project import Project, ProjectStatus
from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType
from app.presentation.controllers.project_controller import ProjectController
from app.presentation.controllers.flow_controller import FlowController

# Mocks para los QMessageBox
@patch('app.presentation.controllers.project_controller.QMessageBox')
class TestProjectController(unittest.TestCase):
    """Pruebas para el controlador de proyectos"""
    
    def setUp(self):
        """Configuración para cada prueba"""
        # Mock de la vista
        self.view_mock = MagicMock()
        
        # Mock del repositorio de proyectos
        self.repository_patch = patch('app.presentation.controllers.project_controller.SQLiteProjectRepository')
        self.repository_mock = self.repository_patch.start()
        
        # Mock del servicio de proyectos
        self.service_patch = patch('app.presentation.controllers.project_controller.ProjectService')
        self.service_mock = self.service_patch.start()
        
        # Mock de los casos de uso de proyectos
        self.use_cases_patch = patch('app.presentation.controllers.project_controller.ProjectUseCases')
        self.use_cases_mock = self.use_cases_patch.start()
        
        # Crear controlador con los mocks
        self.controller = ProjectController(self.view_mock)
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.repository_patch.stop()
        self.service_patch.stop()
        self.use_cases_patch.stop()
    
    def test_load_projects(self, mock_messagebox):
        """Prueba la carga de proyectos"""
        # Configurar mock de casos de uso
        projects_data = [
            {
                'id': 1,
                'name': 'Project 1',
                'created_at': '01/01/2023',
                'status': 'active',
                'is_active': True
            },
            {
                'id': 2,
                'name': 'Project 2',
                'created_at': '02/01/2023',
                'status': 'inactive',
                'is_active': False
            }
        ]
        self.controller.project_use_cases.list_projects.return_value = projects_data
        
        # Llamar al método a probar
        result = self.controller.load_projects()
        
        # Verificar que se llamó al caso de uso correcto
        self.controller.project_use_cases.list_projects.assert_called_once()
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, projects_data)
    
    def test_load_projects_error(self, mock_messagebox):
        """Prueba la carga de proyectos con error"""
        # Configurar mock para lanzar una excepción
        self.controller.project_use_cases.list_projects.side_effect = Exception("Test error")
        
        # Llamar al método a probar
        result = self.controller.load_projects()
        
        # Verificar que se llamó al caso de uso correcto
        self.controller.project_use_cases.list_projects.assert_called_once()
        
        # Verificar que se mostró un mensaje de error
        mock_messagebox.critical.assert_called_once()
        
        # Verificar que se devuelve una lista vacía en caso de error
        self.assertEqual(result, [])
    
    def test_add_project(self, mock_messagebox):
        """Prueba la adición de un proyecto"""
        # Configurar mock de casos de uso
        project_data = {
            'id': 1,
            'name': 'New Project',
            'created_at': '01/01/2023',
            'status': 'active',
            'is_active': True
        }
        self.controller.project_use_cases.add_new_project.return_value = project_data
        
        # Llamar al método a probar
        result = self.controller.add_project("New Project")
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.project_use_cases.add_new_project.assert_called_once_with("New Project")
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, project_data)
    
    def test_add_project_empty_name(self, mock_messagebox):
        """Prueba la adición de un proyecto con nombre vacío"""
        # Llamar al método a probar con nombre vacío
        result = self.controller.add_project("")
        
        # Verificar que no se llamó al caso de uso
        self.controller.project_use_cases.add_new_project.assert_not_called()
        
        # Verificar que se mostró un mensaje de error
        mock_messagebox.critical.assert_called_once()
        
        # Verificar que se devuelve None en caso de error
        self.assertIsNone(result)
    
    def test_toggle_project_status(self, mock_messagebox):
        """Prueba el cambio de estado de un proyecto"""
        # Configurar mock de casos de uso
        project_data = {
            'id': 1,
            'name': 'Test Project',
            'created_at': '01/01/2023',
            'status': 'inactive',
            'is_active': False
        }
        self.controller.project_use_cases.change_project_status.return_value = project_data
        
        # Llamar al método a probar
        result = self.controller.toggle_project_status(1)
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.project_use_cases.change_project_status.assert_called_once_with(1)
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, project_data)
    
    """def test_delete_project_confirmed(self, mock_messagebox):
        #Prueba la eliminación de un proyecto confirmada
        # Configurar mock para la confirmación
        mock_messagebox.question.return_value = QMessageBox.StandardButton.Yes
        
        # Configurar mock de casos de uso
        self.controller.project_use_cases.remove_project.return_value = True
        
        # Llamar al método a probar
        result = self.controller.delete_project(1)
        
        # Verificar que se mostró el diálogo de confirmación
        mock_messagebox.question.assert_called_once()
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.project_use_cases.remove_project.assert_called_once_with(1)
        
        # Verificar que el resultado es el esperado
        self.assertTrue(result)
    """

@patch('app.presentation.controllers.flow_controller.QMessageBox')
class TestFlowController(unittest.TestCase):
    """Pruebas para el controlador de flujos"""
    
    def setUp(self):
        """Configuración para cada prueba"""
        # Mock de la vista
        self.view_mock = MagicMock()
        
        # Mock del repositorio de flujos
        self.repository_patch = patch('app.presentation.controllers.flow_controller.SQLiteFlowRepository')
        self.repository_mock = self.repository_patch.start()
        
        # Mock del servicio de flujos
        self.service_patch = patch('app.presentation.controllers.flow_controller.FlowService')
        self.service_mock = self.service_patch.start()
        
        # Mock de los casos de uso de flujos
        self.use_cases_patch = patch('app.presentation.controllers.flow_controller.FlowUseCases')
        self.use_cases_mock = self.use_cases_patch.start()
        
        # Crear controlador con los mocks
        self.controller = FlowController(self.view_mock)
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.repository_patch.stop()
        self.service_patch.stop()
        self.use_cases_patch.stop()
    
    def test_load_flows(self, mock_messagebox):
        """Prueba la carga de flujos de un proyecto"""
        # Configurar mock de casos de uso
        flows_data = [
            {
                'id': 1,
                'project_id': 1,
                'name': 'Flow 1',
                'recurrence': 'Diaria',
                'created_at': '01/01/2023',
                'owner': 'Owner 1',
                'status': 'active',
                'is_active': True
            },
            {
                'id': 2,
                'project_id': 1,
                'name': 'Flow 2',
                'recurrence': 'Semanal',
                'created_at': '02/01/2023',
                'owner': 'Owner 2',
                'status': 'inactive',
                'is_active': False
            }
        ]
        self.controller.flow_use_cases.list_flows_by_project.return_value = flows_data
        
        # Llamar al método a probar
        result = self.controller.load_flows(1)
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.flow_use_cases.list_flows_by_project.assert_called_once_with(1)
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, flows_data)
    
    def test_load_flows_error(self, mock_messagebox):
        """Prueba la carga de flujos con error"""
        # Configurar mock para lanzar una excepción
        self.controller.flow_use_cases.list_flows_by_project.side_effect = Exception("Test error")
        
        # Llamar al método a probar
        result = self.controller.load_flows(1)
        
        # Verificar que se llamó al caso de uso correcto
        self.controller.flow_use_cases.list_flows_by_project.assert_called_once_with(1)
        
        # Verificar que se mostró un mensaje de error
        mock_messagebox.critical.assert_called_once()
        
        # Verificar que se devuelve una lista vacía en caso de error
        self.assertEqual(result, [])
    
    def test_add_flow(self, mock_messagebox):
        """Prueba la adición de un flujo"""
        # Configurar mock de casos de uso
        flow_data = {
            'id': 1,
            'project_id': 1,
            'name': 'New Flow',
            'recurrence': 'Diaria',
            'created_at': '01/01/2023',
            'owner': 'Test Owner',
            'status': 'active',
            'is_active': True
        }
        self.controller.flow_use_cases.add_new_flow.return_value = flow_data
        
        # Llamar al método a probar
        result = self.controller.add_flow(1, "New Flow", "Diaria", "Test Owner")
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.flow_use_cases.add_new_flow.assert_called_once_with(1, "New Flow", "Diaria", "Test Owner")
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, flow_data)
    
    def test_add_flow_empty_name(self, mock_messagebox):
        """Prueba la adición de un flujo con nombre vacío"""
        # Llamar al método a probar con nombre vacío
        result = self.controller.add_flow(1, "", "Diaria", "Test Owner")
        
        # Verificar que no se llamó al caso de uso
        self.controller.flow_use_cases.add_new_flow.assert_not_called()
        
        # Verificar que se mostró un mensaje de error
        mock_messagebox.critical.assert_called_once()
        
        # Verificar que se devuelve None en caso de error
        self.assertIsNone(result)
    
    def test_toggle_flow_status(self, mock_messagebox):
        """Prueba el cambio de estado de un flujo"""
        # Configurar mock de casos de uso
        flow_data = {
            'id': 1,
            'project_id': 1,
            'name': 'Test Flow',
            'recurrence': 'Diaria',
            'created_at': '01/01/2023',
            'owner': 'Test Owner',
            'status': 'inactive',
            'is_active': False
        }
        self.controller.flow_use_cases.change_flow_status.return_value = flow_data
        
        # Llamar al método a probar
        result = self.controller.toggle_flow_status(1)
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.flow_use_cases.change_flow_status.assert_called_once_with(1)
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, flow_data)
    
    """def test_delete_flow_confirmed(self, mock_messagebox):
        #Prueba la eliminación de un flujo confirmada
        # Configurar mock para la confirmación
        mock_messagebox.question.return_value = QMessageBox.StandardButton.Yes
        
        # Configurar mock de casos de uso
        self.controller.flow_use_cases.remove_flow.return_value = True
        
        # Llamar al método a probar
        result = self.controller.delete_flow(1)
        
        # Verificar que se mostró el diálogo de confirmación
        mock_messagebox.question.assert_called_once()
        
        # Verificar que se llamó al caso de uso correcto con los parámetros adecuados
        self.controller.flow_use_cases.remove_flow.assert_called_once_with(1)
        
        # Verificar que el resultado es el esperado
        self.assertTrue(result)
    """
# tests/presentation/__init__.py
# Archivo vacío para permitir importaciones