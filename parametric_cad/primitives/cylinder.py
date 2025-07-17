from typing import Sequence

from parametric_cad.core import tm
from .base import Primitive


class Cylinder(Primitive):
    def __init__(self, radius: float, height: float, sections: int = 32) -> None:
        super().__init__()
        self.radius = radius
        self.height = height
        self.sections = sections

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.cylinder(
            radius=self.radius,
            height=self.height,
            sections=self.sections,
        )
