import numpy as np
from math import pi
from parametric_cad.core import tm, safe_difference

class RightAngleMotorBracket:
    """Simple right angle bracket for a 540/550 size motor."""

    def __init__(
        self,
        base_length: float = 50.0,
        base_width: float = 40.0,
        plate_height: float = 40.0,
        thickness: float = 3.0,
        motor_hole_spacing: float = 25.0,
        motor_hole_diameter: float = 3.2,
        shaft_clearance_diameter: float = 10.0,
        motor_mount_height: float = 20.0,
    ) -> None:
        self.base_length = base_length
        self.base_width = base_width
        self.plate_height = plate_height
        self.thickness = thickness
        self.motor_hole_spacing = motor_hole_spacing
        self.motor_hole_diameter = motor_hole_diameter
        self.shaft_clearance_diameter = shaft_clearance_diameter
        self.motor_mount_height = motor_mount_height
        self._mesh = self._create_bracket()

    def _create_bracket(self) -> tm.Trimesh:
        # Base plate
        base = tm.creation.box(
            extents=(self.base_length, self.base_width, self.thickness)
        )
        base.apply_translation(
            [self.base_length / 2, self.base_width / 2, self.thickness / 2]
        )

        # Vertical plate
        plate = tm.creation.box(
            extents=(self.base_length, self.thickness, self.plate_height)
        )
        plate.apply_translation(
            [
                self.base_length / 2,
                self.base_width - self.thickness / 2,
                self.thickness + self.plate_height / 2,
            ]
        )

        bracket = tm.util.concatenate([base, plate])

        # Create mounting holes
        holes = []
        hole_y = self.base_width - self.thickness / 2
        hole_z = self.thickness + self.motor_mount_height
        for x_off in [
            self.base_length / 2 - self.motor_hole_spacing / 2,
            self.base_length / 2 + self.motor_hole_spacing / 2,
        ]:
            cyl = tm.creation.cylinder(
                radius=self.motor_hole_diameter / 2,
                height=self.thickness + 0.2,
                sections=32,
            )
            rot = tm.transformations.rotation_matrix(pi / 2, [1, 0, 0])
            cyl.apply_transform(rot)
            cyl.apply_translation([x_off, hole_y, hole_z])
            holes.append(cyl)

        # Motor shaft clearance
        shaft = tm.creation.cylinder(
            radius=self.shaft_clearance_diameter / 2,
            height=self.thickness + 0.2,
            sections=32,
        )
        shaft.apply_transform(tm.transformations.rotation_matrix(pi / 2, [1, 0, 0]))
        shaft.apply_translation([self.base_length / 2, hole_y, hole_z])
        holes.append(shaft)

        bracket = safe_difference(bracket, holes)
        return bracket

    def mesh(self) -> tm.Trimesh:
        return self._mesh.copy()

    def at(self, x: float, y: float, z: float) -> "RightAngleMotorBracket":
        self._mesh.apply_translation([x, y, z])
        return self
