from dataclasses import dataclass

from parametric_cad.core import tm
from .base import Primitive


@dataclass
class Sphere(Primitive):
    """Icosphere primitive."""

    radius: float
    subdivisions: int = 3

    def __post_init__(self) -> None:
        super().__init__()

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.icosphere(
            subdivisions=self.subdivisions,
            radius=self.radius,
        )
