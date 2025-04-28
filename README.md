# Flujos de Power Automate Yape

Aplicación para gestionar flujos de trabajo y proyectos, desarrollada con Python, PyQt6 y SQLite.

## Características

- Gestión de proyectos con estados (activo/inactivo)
- Organización de flujos por proyecto
- Interfaz gráfica de usuario intuitiva
- Almacenamiento persistente con SQLite
- Arquitectura limpia y organizada

## Requisitos

- Python 3.8 o superior
- Windows 11
- PyQt6
- SQLite

## Instalación

1. Clonar este repositorio:
```
git clone https://github.com/tu-usuario/power-automate-app.git
cd power-automate-app
```

2. Crear y activar un entorno virtual:
```
python -m venv venv
venv\Scripts\activate
```

3. Instalar las dependencias:
```
pip install -r requirements.txt
```

## Ejecución

Para iniciar la aplicación, ejecute:
```
python run.py
```

## Estructura del Proyecto

El proyecto sigue los principios de arquitectura limpia, con una clara separación entre:

- **Domain**: Contiene las entidades del negocio y las interfaces de repositorios
- **Infrastructure**: Implementa el acceso a datos
- **Application**: Contiene la lógica de negocio y los casos de uso
- **Presentation**: Gestiona la interfaz de usuario y la interacción

```
power_automate_app/
├── README.md
├── requirements.txt
├── run.py  # Punto de entrada de la aplicación
├── app/
│   ├── config.py  # Configuraciones globales
│   ├── domain/  # Capa de dominio
│   ├── infrastructure/  # Capa de infraestructura
│   ├── application/  # Capa de aplicación
│   └── presentation/  # Capa de presentación
└── tests/  # Pruebas unitarias
```

## Capturas de Pantalla

[Incluir capturas de pantalla de la aplicación]

## Licencia

[Incluir información de licencia]