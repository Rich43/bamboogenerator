"""Consolidated parametric_cad package."""

from .core import tm
from .primitives.box import Box
from .primitives.gear import SpurGear
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter

__all__ = ["tm", "Box", "SpurGear", "ButtHinge", "STLExporter"]
