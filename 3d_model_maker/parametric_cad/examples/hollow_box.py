import trimesh
import numpy as np
from parametric_cad.primitives.box import Box
from parametric_cad.export.stl import STLExporter

def create_hollow_box(outer_length=30.0, outer_width=20.0, outer_height=15.0, wall_thickness=2.0):
    """
    Create a hollow box with specified outer dimensions and wall thickness.
    
    Args:
        outer_length (float): Outer length of the box (default: 30.0 mm)
        outer_width (float): Outer width of the box (default: 20.0 mm)
        outer_height (float): Outer height of the box (default: 15.0 mm)
        wall_thickness (float): Thickness of the walls (default: 2.0 mm)
    
    Returns:
        trimesh.Trimesh: Hollow box mesh
    """
    # Create outer box
    outer_box = Box(length=outer_length, width=outer_width, height=outer_height)
    outer_mesh = outer_box.mesh

    # Calculate inner dimensions
    inner_length = outer_length - 2 * wall_thickness
    inner_width = outer_width - 2 * wall_thickness
    inner_height = outer_height - wall_thickness  # Leave bottom solid, open top

    # Create inner box (to subtract)
    if inner_length <= 0 or inner_width <= 0 or inner_height <= 0:
        raise ValueError("Wall thickness too large for inner dimensions to be positive")

    inner_box = Box(length=inner_length, width=inner_width, height=inner_height)
    inner_mesh = inner_box.mesh
    inner_mesh.apply_translation([wall_thickness, wall_thickness, wall_thickness])  # Position inside outer box

    # Subtract inner box from outer box to create hollow structure
    hollow_box = outer_mesh.difference([inner_mesh])

    return hollow_box

if __name__ == "__main__":
    # Example usage
    mesh = create_hollow_box(outer_length=30.0, outer_width=20.0, outer_height=15.0, wall_thickness=2.0)
    exporter = STLExporter(output_dir="output/hollow_box_output")
    exporter.export_mesh(mesh, "hollow_box")
	
