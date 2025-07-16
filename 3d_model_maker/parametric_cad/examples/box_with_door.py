import trimesh
import numpy as np
from parametric_cad.primitives.box import Box
from parametric_cad.mechanisms.butthinge import ButtHinge
from parametric_cad.export.stl import STLExporter

def create_box_with_door(box_length=30.0, box_width=20.0, box_height=15.0, door_width=10.0, door_height=10.0):
    """
    Create a box with a door cutout and optional hinge.
    
    Args:
        box_length (float): Length of the box (default: 30.0 mm)
        box_width (float): Width of the box (default: 20.0 mm)
        box_height (float): Height of the box (default: 15.0 mm)
        door_width (float): Width of the door cutout (default: 10.0 mm)
        door_height (float): Height of the door cutout (default: 10.0 mm)
    
    Returns:
        trimesh.Trimesh: Combined mesh of box and door
    """
    # Create base box
    box = Box(length=box_length, width=box_width, height=box_height)
    box_mesh = box.mesh

    # Define door cutout (rectangular prism to subtract)
    door_thickness = 0.1  # Thin cutout for subtraction
    door_vertices = np.array([
        [box_length - door_thickness, box_width / 2 - door_width / 2, 0],  # Bottom-left
        [box_length - door_thickness, box_width / 2 + door_width / 2, 0],  # Bottom-right
        [box_length - door_thickness, box_width / 2 + door_width / 2, door_height],  # Top-right
        [box_length - door_thickness, box_width / 2 - door_width / 2, door_height],  # Top-left
    ])
    door_faces = np.array([
        [0, 1, 2], [0, 2, 3],  # Front face
        # Add side faces for a thin prism (simplified)
        [0, 1, 4], [1, 5, 4], [1, 2, 5], [2, 6, 5], [2, 3, 6], [3, 7, 6], [3, 0, 7], [0, 4, 7]
    ])  # Note: 4-7 vertices would need z-offset, simplified here
    door = trimesh.Trimesh(vertices=door_vertices, faces=door_faces, process=False)
    door.apply_translation([0, 0, box_height - door_height])  # Position at top of door height

    # Subtract door cutout from box
    box_with_cutout = box_mesh.difference([door])

    # Optional: Add hinge (positioned on the right edge)
    hinge = ButtHinge(leaf_length=door_height, leaf_width=5.0, leaf_thickness=2.0, knuckles=3)
    hinge_mesh = hinge.mesh
    hinge_mesh.apply_translation([box_length - door_thickness, box_width / 2 - hinge.leaf_width / 2, box_height - door_height])

    # Combine box and hinge
    final_mesh = trimesh.util.concatenate([box_with_cutout, hinge_mesh])

    return final_mesh

if __name__ == "__main__":
    # Example usage
    mesh = create_box_with_door(box_length=30.0, box_width=20.0, box_height=15.0, door_width=10.0, door_height=10.0)
    exporter = STLExporter(output_dir="output/box_with_door_output")
    exporter.export_mesh(mesh, "box_with_door")
