from dataclasses import dataclass

from parametric_cad.core import tm
from .base import Primitive


@dataclass
class Cylinder(Primitive):
    """Circular cylinder primitive."""

    radius: float
    height: float
    sections: int = 32

    def __post_init__(self) -> None:
        super().__init__()

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.cylinder(
            radius=self.radius,
            height=self.height,
            sections=self.sections,
        )
