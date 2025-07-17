from parametric_cad.core import tm
from typing import Sequence, Optional

class Cylinder:
    def __init__(self, radius: float, height: float, sections: int = 32):
        self.radius = radius
        self.height = height
        self.sections = sections
        self._position = (0.0, 0.0, 0.0)
        self._rotation: Optional[Sequence[float]] = None

    def at(self, x: float, y: float, z: float) -> "Cylinder":
        self._position = (x, y, z)
        return self

    def rotate(self, axis: Sequence[float], angle: float) -> "Cylinder":
        """Rotate the cylinder around ``axis`` by ``angle`` radians."""
        self._rotation = (axis, angle)
        return self

    def mesh(self) -> tm.Trimesh:
        cyl = tm.creation.cylinder(
            radius=self.radius,
            height=self.height,
            sections=self.sections,
        )
        if self._rotation is not None:
            axis, angle = self._rotation
            rot = tm.transformations.rotation_matrix(angle, axis)
            cyl.apply_transform(rot)
        cyl.apply_translation(self._position)
        return cyl
