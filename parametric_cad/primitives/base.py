from typing import Optional, Sequence

from parametric_cad.core import tm


class Primitive:
    """Base class for simple parametric primitives."""

    def __init__(self) -> None:
        self._position = (0.0, 0.0, 0.0)
        self._rotation: Optional[tuple[Sequence[float], float]] = None

    def at(self, x: float, y: float, z: float):
        """Translate the primitive to ``(x, y, z)``."""
        self._position = (x, y, z)
        return self

    def rotate(self, axis: Sequence[float], angle: float):
        """Rotate the primitive around ``axis`` by ``angle`` radians."""
        self._rotation = (axis, angle)
        return self

    def _create_mesh(self) -> tm.Trimesh:
        """Return the untransformed mesh for this primitive."""
        raise NotImplementedError

    def mesh(self) -> tm.Trimesh:
        mesh = self._create_mesh()
        if self._rotation is not None:
            axis, angle = self._rotation
            rot = tm.transformations.rotation_matrix(angle, axis)
            mesh.apply_transform(rot)
        mesh.apply_translation(self._position)
        return mesh
