from parametric_cad.core import tm
from .base import Primitive


class Sphere(Primitive):
    def __init__(self, radius: float, subdivisions: int = 3) -> None:
        super().__init__()
        self.radius = radius
        self.subdivisions = subdivisions

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.icosphere(
            subdivisions=self.subdivisions,
            radius=self.radius,
        )
