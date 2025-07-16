import trimesh
import numpy as np
from parametric_cad.export.stl import STLExporter

class Box:
    def __init__(self, length=10.0, width=10.0, height=10.0):
        self.length = float(length)
        self.width = float(width)
        self.height = float(height)
        self.mesh = self._create_box()
        self.exporter = STLExporter()

    def _create_box(self):
        vertices = np.array([
            [0, 0, 0], [self.length, 0, 0], [self.length, self.width, 0],
            [0, self.width, 0], [0, 0, self.height], [self.length, 0, self.height],
            [self.length, self.width, self.height], [0, self.width, self.height]
        ])
        faces = np.array([
            [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
            [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
            [0, 3, 7], [0, 7, 4], [1, 2, 6], [1, 6, 5]
        ])
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

    def export(self, filename):
        self.exporter.export_mesh(self.mesh, filename)

if __name__ == "__main__":
    box = Box(length=20.0, width=15.0, height=10.0)
    box.export("output/box_example")
    
