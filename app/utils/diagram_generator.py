from graphviz import Digraph
from app.infrastructure.repositories.sqlite_project_repository import SQLiteProjectRepository
from app.infrastructure.repositories.sqlite_flow_repository import SQLiteFlowRepository

def generate_project_diagram(project_id: int) -> str:
    """Genera un diagrama de flujo para un proyecto y lo guarda como archivo SVG."""
    project_repo = SQLiteProjectRepository()
    flow_repo = SQLiteFlowRepository()

    # Obtener el proyecto
    project = project_repo.get_by_id(project_id)
    if not project:
        raise ValueError(f"El proyecto con ID {project_id} no existe.")

    # Obtener los flujos del proyecto
    flows = flow_repo.get_all_by_project(project_id)
    if not flows:
        raise ValueError(f"No hay flujos asociados al proyecto '{project.name}'.")

    # Crear el diagrama
    dot = Digraph(format="svg")
    dot.attr(rankdir="LR", size="10,7")  # Dirección de izquierda a derecha, tamaño ajustado
    dot.attr("node", fontname="Arial", fontsize="12")  # Fuente y tamaño de texto

    # Agregar el nombre del proyecto en la parte superior izquierda
    dot.node(
        "project_label",
        f"<<b>{project.name}</b>>",  # Texto en negrita
        shape="plaintext",  # Nodo invisible
        fontsize="16",
        fontcolor="black"
    )
    dot.attr(labeljust="l")  # Alinear la etiqueta a la izquierda
    dot.attr(labelloc="t")  # Colocar la etiqueta en la parte superior

    # Nodo del proyecto (rectángulo redondeado)
    dot.node(
        f"project_{project.id}",
        project.name,
        shape="box",
        style="rounded,filled",
        color="#FF6F91",
        fontcolor="white",
        fontsize="14",
        penwidth="2"
    )

    # Nodos y conexiones de los flujos
    for flow in flows:
        flow_node_id = f"flow_{flow.id}"
        # Nodo del flujo (todos serán procesos con forma de elipse)
        dot.node(
            flow_node_id,
            flow.name,
            shape="ellipse",  # Forma de elipse para todos los flujos
            style="filled",
            color="#D65DB1",  # Color uniforme para los procesos
            fontcolor="black",
            fontsize="12",
            penwidth="2"
        )
        # Conexión entre el proyecto y el flujo
        dot.edge(
            f"project_{project.id}",
            flow_node_id,
            label=flow.recurrence.value,
            color="#845EC2",
            fontcolor="#4B4453",
            fontsize="10",
            penwidth="2"
        )

    # Guardar el diagrama
    output_path = f"diagrams/project_{project_id}_diagram.svg"
    dot.render(output_path, cleanup=True)
    return output_path