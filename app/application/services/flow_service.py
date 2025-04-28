from typing import List, Optional
from app.domain.entities.flow import Flow, FlowStatus, RecurrenceType
from app.domain.repositories.flow_repository import FlowRepository

class FlowService:
    """Servicio para gestionar flujos"""
    
    def __init__(self, flow_repository: FlowRepository):
        self.flow_repository = flow_repository
    
    def get_flows_by_project(self, project_id: int) -> List[Flow]:
        """Obtiene todos los flujos de un proyecto"""
        return self.flow_repository.get_all_by_project(project_id)
    
    def get_flow_by_id(self, flow_id: int) -> Optional[Flow]:
        """Obtiene un flujo por su ID"""
        return self.flow_repository.get_by_id(flow_id)
    
    def create_flow(self, project_id: int, name: str, recurrence: RecurrenceType, owner: str) -> Flow:
        """Crea un nuevo flujo"""
        flow = Flow(
            project_id=project_id,
            name=name,
            recurrence=recurrence,
            owner=owner,
            status=FlowStatus.ACTIVE
        )
        return self.flow_repository.create(flow)
    
    def update_flow(self, flow: Flow) -> Flow:
        """Actualiza un flujo existente"""
        return self.flow_repository.update(flow)
    
    def delete_flow(self, flow_id: int) -> bool:
        """Elimina un flujo por su ID"""
        return self.flow_repository.delete(flow_id)
    
    def toggle_flow_status(self, flow_id: int) -> Flow:
        """Cambia el estado de un flujo (activo/inactivo)"""
        flow = self.get_flow_by_id(flow_id)
        if not flow:
            raise ValueError(f"No se encontró el flujo con ID {flow_id}")
            
        if flow.is_active:
            flow.deactivate()
        else:
            flow.activate()
            
        return self.flow_repository.update(flow)