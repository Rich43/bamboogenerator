"""Consolidated parametric_cad package."""

from .core import tm, safe_difference, combine
from .geometry import sg, Polygon, Point, box
from .primitives.box import Box
from .primitives.cylinder import Cylinder
from .primitives.gear import SpurGear
from .primitives.sprocket import ChainSprocket
from .primitives.sphere import Sphere
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter

__all__ = [
    "tm",
    "sg",
    "safe_difference",
    "combine",
    "Box",
    "Cylinder",
    "Sphere",
    "SpurGear",
    "ChainSprocket",
    "ButtHinge",
    "STLExporter",
    "Polygon",
    "Point",
    "box",
]
