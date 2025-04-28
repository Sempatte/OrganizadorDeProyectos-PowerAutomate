from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QScrollArea, QGridLayout, QSizePolicy,
    QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QIcon, QFont

from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository
from app.application.services.project_service import ProjectService
from app.application.use_cases.project_use_cases import ProjectUseCases

class ProjectCard(QFrame):
    """Tarjeta para mostrar un proyecto"""
    
    clicked = pyqtSignal(int, str)  # ID del proyecto, nombre del proyecto
    
    def __init__(self, project_data):
        super().__init__()
        self.project_data = project_data
        self.setObjectName("projectCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Aplicar efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
        
        # Establecer tamaño mínimo para la tarjeta
        self.setMinimumSize(300, 200)
        self.setMaximumSize(400, 250)
        
        # Hacer que la tarjeta sea clicable
        self.mousePressEvent = self._on_click
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Contenedor superior para título y estado
        top_container = QVBoxLayout()
        top_container.setSpacing(5)
        
        # Nombre del proyecto
        name_label = QLabel(project_data['name'])
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333333;")
        name_label.setWordWrap(True)
        top_container.addWidget(name_label)
        
        # Línea divisoria
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #e0e0e0;")
        top_container.addWidget(line)
        
        main_layout.addLayout(top_container)
        
        # Contenedor de información
        info_container = QVBoxLayout()
        info_container.setSpacing(10)
        
        # Estado del proyecto
        status_layout = QHBoxLayout()
        status_text = "Activo" if project_data['is_active'] else "Inactivo"
        status_obj_name = "activeStatus" if project_data['is_active'] else "inactiveStatus"
        
        status_label = QLabel("Estado:")
        status_label.setStyleSheet("font-weight: bold; color: #555555;")
        
        status_value = QLabel(status_text)
        status_value.setObjectName(status_obj_name)
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(status_value)
        status_layout.addStretch()
        
        info_container.addLayout(status_layout)
        
        # Fecha de creación
        date_layout = QHBoxLayout()
        
        date_label = QLabel("Creado:")
        date_label.setStyleSheet("font-weight: bold; color: #555555;")
        
        date_value = QLabel(project_data['created_at'])
        date_value.setStyleSheet("color: #555555;")
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_value)
        date_layout.addStretch()
        
        info_container.addLayout(date_layout)
        
        main_layout.addLayout(info_container)
        main_layout.addStretch()
    
    def _on_click(self, event):
        """Manejador del evento de clic"""
        self.clicked.emit(self.project_data['id'], self.project_data['name'])


class ProjectListView(QWidget):
    """Vista de lista de proyectos"""
    
    project_selected = pyqtSignal(int, str)  # ID del proyecto, nombre del proyecto
    add_project_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Repositorio y casos de uso
        self.project_repository = SQLiteProjectRepository()
        self.project_service = ProjectService(self.project_repository)
        self.project_use_cases = ProjectUseCases(self.project_service, self.project_repository)
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header con título y botón de agregar
        header_layout = QHBoxLayout()
        
        # Título con estilo mejorado
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        
        title = QLabel("Proyectos")
        title.setObjectName("titleLabel")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        title_container.addWidget(title)
        
        subtitle = QLabel("Gestione sus proyectos de automatización")
        subtitle.setStyleSheet("font-size: 14px; color: #666666;")
        title_container.addWidget(subtitle)
        
        header_layout.addLayout(title_container)
        
        header_layout.addStretch()
        
        # Botón de agregar mejorado
        add_button = QPushButton("Agregar Proyecto")
        add_button.setObjectName("secondaryButton")
        add_button.setMinimumSize(150, 40)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #9c27b0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e24aa;
            }
            QPushButton:pressed {
                background-color: #7b1fa2;
            }
        """)
        add_button.clicked.connect(self.add_project_requested.emit)
        header_layout.addWidget(add_button)
        
        self.layout.addLayout(header_layout)
        
        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0;")
        self.layout.addWidget(separator)
        
        # Área desplazable para las tarjetas de proyectos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #f5f5f5;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #cccccc;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #bbbbbb;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.projects_container = QWidget()
        self.projects_container.setStyleSheet("background-color: #f5f5f5;")
        self.projects_layout = QGridLayout(self.projects_container)
        self.projects_layout.setContentsMargins(10, 10, 10, 10)
        self.projects_layout.setSpacing(20)
        
        scroll_area.setWidget(self.projects_container)
        self.layout.addWidget(scroll_area)
        
        # Cargar proyectos
        self.refresh_projects()
    
    def refresh_projects(self):
        """Actualiza la lista de proyectos"""
        # Limpiar proyectos existentes
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtener proyectos
        projects = self.project_use_cases.list_projects()
        
        # Si no hay proyectos, mostrar mensaje
        if not projects:
            no_projects_container = QWidget()
            no_projects_layout = QVBoxLayout(no_projects_container)
            no_projects_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            no_projects_icon = QLabel("📁")
            no_projects_icon.setStyleSheet("font-size: 48px; color: #999999;")
            no_projects_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_projects_layout.addWidget(no_projects_icon)
            
            no_projects_label = QLabel("No hay proyectos disponibles")
            no_projects_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #666666;")
            no_projects_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_projects_layout.addWidget(no_projects_label)
            
            no_projects_sublabel = QLabel("Haga clic en 'Agregar Proyecto' para comenzar")
            no_projects_sublabel.setStyleSheet("font-size: 14px; color: #999999;")
            no_projects_sublabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_projects_layout.addWidget(no_projects_sublabel)
            
            self.projects_layout.addWidget(no_projects_container, 0, 0, 1, 3)
            return
        
        # Crear tarjetas de proyectos (3 columnas)
        row, col = 0, 0
        max_cols = 3
        
        for project in projects:
            card = ProjectCard(project)
            card.clicked.connect(self.project_selected.emit)
            
            self.projects_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1