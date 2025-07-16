import trimesh
import numpy as np
import math
from parametric_cad.export.stl import STLExporter

class SpurGear:
    def __init__(self, teeth=20, module=1.0, thickness=5.0, pressure_angle=20.0):
        """
        Initialize a parametric 3D spur gear.
        
        Args:
            teeth (int): Number of teeth (default: 20)
            module (float): Module (pitch diameter / number of teeth, default: 1.0 mm)
            thickness (float): Thickness of the gear along the z-axis (default: 5.0 mm)
            pressure_angle (float): Pressure angle in degrees (default: 20.0)
        """
        self.teeth = max(5, int(teeth))  # Minimum 5 teeth for stability
        self.module = float(module)
        self.thickness = float(thickness)
        self.pressure_angle = math.radians(float(pressure_angle))
        self.pitch_diameter = self.module * self.teeth
        self.mesh = self._create_gear()
        self.exporter = STLExporter()

    def _create_gear(self):
        """Create a trimesh object representing the spur gear."""
        # Calculate key dimensions
        addendum = self.module
        dedendum = 1.25 * self.module
        outer_diameter = self.pitch_diameter + 2 * addendum
        root_diameter = self.pitch_diameter - 2 * dedendum

        # Generate points for the involute tooth profile
        points = []
        for i in range(self.teeth):
            angle = 2 * math.pi * i / self.teeth
            base_radius = self.pitch_diameter / 2 * math.cos(self.pressure_angle)
            involute_angle = math.sqrt(self.pitch_diameter / (2 * base_radius)) * (angle / 2)
            tooth_radius = base_radius * (math.cos(involute_angle) + involute_angle * math.sin(involute_angle))
            x = tooth_radius * math.cos(angle)
            y = tooth_radius * math.sin(angle)
            points.append([x, y, 0])
            points.append([x, y, self.thickness])

        # Create a simple circular base and extrude
        base = trimesh.creation.annulus(
            outer_radius=outer_diameter / 2,
            inner_radius=root_diameter / 2,
            height=self.thickness,
            sections=self.teeth * 2
        )
        return base

    def export(self, filename):
        """Export the gear mesh using STLExporter."""
        self.exporter.export_mesh(self.mesh, filename)

if __name__ == "__main__":
    # Example usage
    gear = SpurGear(teeth=20, module=2.0, thickness=10.0)
    gear.export("output/spur_gear_example")
    
