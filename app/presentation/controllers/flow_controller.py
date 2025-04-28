from PyQt6.QtWidgets import QMessageBox
from app.application.services.flow_service import FlowService
from app.application.use_cases.flow_use_cases import FlowUseCases
from app.infrastructure.repositories.sqlite_flow_repository import SQLiteFlowRepository
from app.domain.entities.flow import RecurrenceType, FlowStatus

class FlowController:
    """Controlador para gestionar flujos"""
    
    def __init__(self, view):
        self.view = view
        
        # Repositorios y servicios
        self.flow_repository = SQLiteFlowRepository()
        self.flow_service = FlowService(self.flow_repository)
        self.flow_use_cases = FlowUseCases(self.flow_service)
        
        # Conectar eventos
        self._connect_events()
    
    def _connect_events(self):
        """Conecta los eventos de la vista"""
        # Se implementará según la vista específica que se use
        pass
    
    def load_flows(self, project_id):
        """Carga la lista de flujos de un proyecto"""
        try:
            flows = self.flow_use_cases.list_flows_by_project(project_id)
            return flows
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudieron cargar los flujos: {str(e)}"
            )
            return []
    
    def get_flow(self, flow_id):
        """Obtiene un flujo por su ID"""
        try:
            flow = self.flow_use_cases.get_flow_details(flow_id)
            return flow
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo cargar el flujo: {str(e)}"
            )
            return None
    
    def add_flow(self, project_id, name, recurrence, owner):
        """Agrega un nuevo flujo"""
        try:
            if not name.strip():
                raise ValueError("El nombre del flujo no puede estar vacío")
                
            if not owner.strip():
                raise ValueError("El propietario del flujo no puede estar vacío")
                
            # Validar que la recurrencia sea un valor válido
            try:
                RecurrenceType(recurrence)
            except ValueError:
                raise ValueError("Tipo de recurrencia no válido")
                
            flow = self.flow_use_cases.add_new_flow(
                project_id, name, recurrence, owner
            )
            return flow
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo agregar el flujo: {str(e)}"
            )
            return None
    
    def update_flow(self, flow_id, name, recurrence, owner, is_active):
        """Actualiza un flujo existente"""
        try:
            if not name.strip():
                raise ValueError("El nombre del flujo no puede estar vacío")
                
            if not owner.strip():
                raise ValueError("El propietario del flujo no puede estar vacío")
                
            # Validar que la recurrencia sea un valor válido
            try:
                RecurrenceType(recurrence)
            except ValueError:
                raise ValueError("Tipo de recurrencia no válido")
            
            # Obtener el flujo actual
            flow = self.flow_service.get_flow_by_id(flow_id)
            if not flow:
                raise ValueError(f"No se encontró el flujo con ID {flow_id}")
            
            # Actualizar los datos
            flow.name = name
            flow.recurrence = RecurrenceType(recurrence)
            flow.owner = owner
            flow.status = FlowStatus.ACTIVE if is_active else FlowStatus.INACTIVE
            
            # Guardar los cambios
            updated_flow = self.flow_service.update_flow(flow)
            
            # Formatear el resultado para la vista
            return self.flow_use_cases._format_flow(updated_flow)
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo actualizar el flujo: {str(e)}"
            )
            return None
    
    def toggle_flow_status(self, flow_id):
        """Cambia el estado de un flujo"""
        try:
            flow = self.flow_use_cases.change_flow_status(flow_id)
            return flow
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo cambiar el estado del flujo: {str(e)}"
            )
            return None
    
    def delete_flow(self, flow_id):
        """Elimina un flujo"""
        try:
            confirmation = QMessageBox.question(
                self.view,
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este flujo? Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirmation == QMessageBox.StandardButton.Yes:
                success = self.flow_use_cases.remove_flow(flow_id)
                if success:
                    return True
                else:
                    raise ValueError("No se pudo eliminar el flujo")
            return False
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"No se pudo eliminar el flujo: {str(e)}"
            )
            return False