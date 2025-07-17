from dataclasses import dataclass

from parametric_cad.core import tm
from .base import Primitive


@dataclass
class Box(Primitive):
    """Axis-aligned rectangular prism primitive."""

    width: float
    depth: float
    height: float

    def __post_init__(self) -> None:
        super().__init__()

    def _create_mesh(self) -> tm.Trimesh:
        return tm.creation.box(extents=(self.width, self.depth, self.height))
