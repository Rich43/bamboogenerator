"""Wrapper around shapely.geometry used by parametric_cad.

This indirection allows the project to avoid depending on shapely
throughout the codebase. If needed, the backend can be swapped out
by modifying this module alone.
"""

import shapely.geometry as _geometry

# Public alias so other modules can import geometry functionality
# without referencing :mod:`shapely` directly.
sg = _geometry

# Convenience factory functions wrapping ``shapely.geometry``

def Polygon(*args, **kwargs):
    """Return a :class:`shapely.geometry.Polygon` instance."""

    return sg.Polygon(*args, **kwargs)


def Point(*args, **kwargs):
    """Return a :class:`shapely.geometry.Point` instance."""

    return sg.Point(*args, **kwargs)


def box(*args, **kwargs):
    """Return a rectangular polygon as defined by :func:`shapely.geometry.box`."""

    return sg.box(*args, **kwargs)


__all__ = ["sg", "Polygon", "Point", "box"]
