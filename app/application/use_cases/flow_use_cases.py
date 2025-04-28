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