# app/domain/entities/project.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProjectStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Project:
    """Entidad que representa un proyecto"""
    id: Optional[int] = None
    name: str = ""
    created_at: datetime = datetime.now()
    status: ProjectStatus = ProjectStatus.ACTIVE
    
    @property
    def is_active(self) -> bool:
        return self.status == ProjectStatus.ACTIVE
    
    def activate(self) -> None:
        self.status = ProjectStatus.ACTIVE
    
    def deactivate(self) -> None:
        self.status = ProjectStatus.INACTIVE

# app/domain/entities/flow.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class FlowStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class RecurrenceType(Enum):
    DAILY = "Diaria"
    WEEKLY = "Semanal"
    MONTHLY = "Mensual"
    CUSTOM = "Personalizada"

@dataclass
class Flow:
    """Entidad que representa un flujo dentro de un proyecto"""
    id: Optional[int] = None
    project_id: int = 0
    name: str = ""
    recurrence: RecurrenceType = RecurrenceType.DAILY
    created_at: datetime = datetime.now()
    owner: str = ""
    status: FlowStatus = FlowStatus.ACTIVE
    
    @property
    def is_active(self) -> bool:
        return self.status == FlowStatus.ACTIVE
    
    def activate(self) -> None:
        self.status = FlowStatus.ACTIVE
    
    def deactivate(self) -> None:
        self.status = FlowStatus.INACTIVE