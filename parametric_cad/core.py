"""Backend access for parametric_cad.

This module centralizes interaction with the mesh backend so other
parts of the package do not need to import the backend directly.
Currently :mod:`trimesh` provides all geometry functionality, but this
wrapper allows the backend to be swapped or mocked easily.
"""

import trimesh as _trimesh

# Public alias so that other modules can use the backend without
# importing ``trimesh`` themselves.
tm = _trimesh

__all__ = ["tm"]
