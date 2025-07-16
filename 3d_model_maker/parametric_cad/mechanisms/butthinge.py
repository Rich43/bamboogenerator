import trimesh
import numpy as np
from parametric_cad.export.stl import STLExporter

class ButtHinge:
    def __init__(self, leaf_length=50.0, leaf_width=25.0, leaf_thickness=2.0, knuckles=5, pin_diameter=3.0):
        """
        Initialize a parametric 3D butt hinge.
        
        Args:
            leaf_length (float): Length of each leaf (default: 50.0 mm)
            leaf_width (float): Width of each leaf (default: 25.0 mm)
            leaf_thickness (float): Thickness of each leaf (default: 2.0 mm)
            knuckles (int): Number of knuckles (cylinders) along the hinge (default: 5)
            pin_diameter (float): Diameter of the hinge pin (default: 3.0 mm)
        """
        self.leaf_length = float(leaf_length)
        self.leaf_width = float(leaf_width)
        self.leaf_thickness = float(leaf_thickness)
        self.knuckles = max(3, int(knuckles))  # Minimum 3 knuckles for stability
        self.pin_diameter = float(pin_diameter)
        self.mesh = self._create_hinge()
        self.exporter = STLExporter()

    def _create_hinge(self):
        """Create a trimesh object representing the butt hinge."""
        # Create two leaves
        leaf_vertices = np.array([
            [0, 0, 0], [self.leaf_length, 0, 0], [self.leaf_length, self.leaf_width, 0],
            [0, self.leaf_width, 0], [0, 0, self.leaf_thickness], [self.leaf_length, 0, self.leaf_thickness],
            [self.leaf_length, self.leaf_width, self.leaf_thickness], [0, self.leaf_width, self.leaf_thickness]
        ])
        leaf_faces = np.array([
            [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
            [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
            [0, 3, 7], [0, 7, 4], [1, 2, 6], [1, 6, 5]
        ])
        leaf1 = trimesh.Trimesh(vertices=leaf_vertices, faces=leaf_faces, process=False)

        # Second leaf, offset for hinge alignment
        leaf2 = leaf1.copy()
        leaf2.apply_translation([0, self.leaf_width + self.pin_diameter, 0])

        # Create knuckles (cylinders) along the hinge axis
        knuckle_meshes = []
        knuckle_spacing = self.leaf_length / (self.knuckles + 1)
        for i in range(self.knuckles):
            z_pos = knuckle_spacing * (i + 1)
            knuckle = trimesh.creation.cylinder(
                radius=self.pin_diameter / 2,
                height=self.leaf_thickness + 0.1,  # Slight overlap for union
                sections=16
            )
            knuckle.apply_translation([self.leaf_length, self.leaf_width / 2, z_pos])
            knuckle_meshes.append(knuckle)

        # Combine leaves and knuckles
        hinge = trimesh.util.concatenate([leaf1, leaf2] + knuckle_meshes)
        return hinge

    def export(self, filename):
        """Export the hinge mesh using STLExporter."""
        self.exporter.export_mesh(self.mesh, filename)

if __name__ == "__main__":
    # Example usage
    hinge = ButtHinge(leaf_length=60.0, leaf_width=30.0, leaf_thickness=3.0, knuckles=6, pin_diameter=4.0)
    hinge.export("output/butt_hinge_example")
    