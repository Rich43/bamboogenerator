"""Consolidated parametric_cad package."""

from .core import tm, safe_difference
from .primitives.box import Box
from .primitives.gear import SpurGear
from .primitives.sprocket import ChainSprocket
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter

__all__ = [
    "tm",
    "safe_difference",
    "Box",
    "SpurGear",
    "ChainSprocket",
    "ButtHinge",
    "STLExporter",
]
