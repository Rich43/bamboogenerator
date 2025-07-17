"""Consolidated parametric_cad package."""

from .core import tm, safe_difference, combine
from .primitives.box import Box
from .primitives.cylinder import Cylinder
from .primitives.gear import SpurGear
from .primitives.sprocket import ChainSprocket
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter

__all__ = [
    "tm",
    "safe_difference",
    "combine",
    "Box",
    "Cylinder",
    "SpurGear",
    "ChainSprocket",
    "ButtHinge",
    "STLExporter",
]
