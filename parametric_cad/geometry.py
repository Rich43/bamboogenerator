"""Wrapper around shapely.geometry used by parametric_cad.

This indirection allows the project to avoid depending on shapely
throughout the codebase. If needed, the backend can be swapped out
by modifying this module alone.
"""

import shapely.geometry as _geometry

# Public alias so other modules can import geometry functionality
# without referencing :mod:`shapely` directly.
sg = _geometry

# Commonly used geometry primitives
Polygon = sg.Polygon
Point = sg.Point
box = sg.box

__all__ = ["sg", "Polygon", "Point", "box"]
