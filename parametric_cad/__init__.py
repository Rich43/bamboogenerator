"""Consolidated parametric_cad package."""

from .primitives.box import Box
from .primitives.gear import SpurGear
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter

__all__ = ["Box", "SpurGear", "ButtHinge", "STLExporter"]
