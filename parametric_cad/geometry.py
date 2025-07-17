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

def Polygon(shell, holes=None):
    """Return a :class:`shapely.geometry.Polygon` instance."""

    return sg.Polygon(shell, holes=holes)


def Point(x, y=None, z=None):
    """Return a :class:`shapely.geometry.Point` instance."""

    if z is not None:
        return sg.Point(x, y, z)
    if y is not None:
        return sg.Point(x, y)
    return sg.Point(x)


def box(minx, miny, maxx, maxy, ccw=True):
    """Return a rectangular polygon as defined by :func:`shapely.geometry.box`."""

    return sg.box(minx, miny, maxx, maxy, ccw=ccw)


__all__ = ["sg", "Polygon", "Point", "box"]
