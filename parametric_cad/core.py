"""Backend access for parametric_cad.

This module centralizes interaction with the mesh backend so other
parts of the package do not need to import the backend directly.
Currently :mod:`trimesh` provides all geometry functionality, but this
wrapper allows the backend to be swapped or mocked easily.
"""

import trimesh as _trimesh


def safe_difference(mesh, other, *, engine="scad"):
    """Perform a boolean difference with graceful fallback.

    Parameters
    ----------
    mesh : _trimesh.Trimesh
        Base mesh to subtract from.
    other : _trimesh.Trimesh or list
        Mesh or list of meshes to subtract.
    engine : str or None, optional
        Preferred boolean engine. ``"scad"`` is tried by default.

    Returns
    -------
    _trimesh.Trimesh
        Resulting mesh if the operation succeeds, otherwise the original
        ``mesh`` if all boolean attempts fail.
    """

    try:
        if engine:
            return mesh.difference(other, engine=engine)
        return mesh.difference(other)
    except Exception:
        try:
            return mesh.difference(other)
        except Exception:
            return mesh

# Public alias so that other modules can use the backend without
# importing ``trimesh`` themselves.
tm = _trimesh

__all__ = ["tm", "safe_difference"]
