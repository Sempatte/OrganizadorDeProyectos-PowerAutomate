# app/application/use_cases/project_use_cases.py
from typing import List, Dict, Any, Optional
from app.application.services.project_service import ProjectService
from app.domain.entities.project import Project

class ProjectUseCases:
    """Casos de uso para los proyectos"""
    
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """Listar todos los proyectos con formato para presentación"""
        projects = self.project_service.get_all_projects()
        return [self._format_project(project) for project in projects]
    
    def get_project_details(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Obtener detalles de un proyecto"""
        project = self.project_service.get_project_by_id(project_id)
        if not project:
            return None
        return self._format_project(project)
    
    def add_new_project(self, name: str) -> Dict[str, Any]:
        """Agregar un nuevo proyecto"""
        project = self.project_service.create_project(name)
        return self._format_project(project)
    
    def change_project_status(self, project_id: int) -> Dict[str, Any]:
        """Cambiar el estado de un proyecto"""
        project = self.project_service.toggle_project_status(project_id)
        return self._format_project(project)
    
    def remove_project(self, project_id: int) -> bool:
        """Eliminar un proyecto"""
        return self.project_service.delete_project(project_id)
    
    def _format_project(self, project: Project) -> Dict[str, Any]:
        """Formatear un proyecto para presentación"""
        return {
            'id': project.id,
            'name': project.name,
            'created_at': project.created_at.strftime('%d/%m/%Y'),
            'status': project.status.value,
            'is_active': project.is_active
        }

# app/application/use_cases/flow_use_cases.py
from typing import List, Dict, Any, Optional
from app.application.services.flow_service import FlowService
from app.domain.entities.flow import Flow, RecurrenceType

class FlowUseCases:
    """Casos de uso para los flujos"""
    
    def __init__(self, flow_service: FlowService):
        self.flow_service = flow_service
    
    def list_flows_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """Listar todos los flujos de un proyecto con formato para presentación"""
        flows = self.flow_service.get_flows_by_project(project_id)
        return [self._format_flow(flow) for flow in flows]
    
    def get_flow_details(self, flow_id: int) -> Optional[Dict[str, Any]]:
        """Obtener detalles de un flujo"""
        flow = self.flow_service.get_flow_by_id(flow_id)
        if not flow:
            return None
        return self._format_flow(flow)
    
    def add_new_flow(self, project_id: int, name: str, recurrence: str, owner: str) -> Dict[str, Any]:
        """Agregar un nuevo flujo"""
        recurrence_type = RecurrenceType(recurrence)
        flow = self.flow_service.create_flow(project_id, name, recurrence_type, owner)
        return self._format_flow(flow)
    
    def change_flow_status(self, flow_id: int) -> Dict[str, Any]:
        """Cambiar el estado de un flujo"""
        flow = self.flow_service.toggle_flow_status(flow_id)
        return self._format_flow(flow)
    
    def remove_flow(self, flow_id: int) -> bool:
        """Eliminar un flujo"""
        return self.flow_service.delete_flow(flow_id)
    
    def _format_flow(self, flow: Flow) -> Dict[str, Any]:
        """Formatear un flujo para presentación"""
        return {
            'id': flow.id,
            'project_id': flow.project_id,
            'name': flow.name,
            'recurrence': flow.recurrence.value,
            'created_at': flow.created_at.strftime('%d/%m/%Y'),
            'owner': flow.owner,
            'status': flow.status.value,
            'is_active': flow.is_active
        }