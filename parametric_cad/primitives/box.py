from parametric_cad.core import tm
from .base import Primitive


class Box(Primitive):
    def __init__(self, width: float, depth: float, height: float) -> None:
        super().__init__()
        self.width = width
        self.depth = depth
        self.height = height

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.box(extents=(self.width, self.depth, self.height))
