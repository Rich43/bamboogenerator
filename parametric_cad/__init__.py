"""Consolidated parametric_cad package."""

from .core import tm, safe_difference, combine
from .geometry import sg, Polygon, Point, box
from .primitives.base import Primitive
from .primitives.box import Box
from .primitives.cylinder import Cylinder
from .primitives.gear import SpurGear
from .primitives.sprocket import ChainSprocket
from .primitives.sphere import Sphere
from .mechanisms.butthinge import ButtHinge
from .export.stl import STLExporter
from .printability import PrintabilityValidator
from .scaffolding import generate_scaffolding, generate_scaffolding_from_workplane
from .cadquery_utils import workplane_to_mesh

__all__ = [
    "tm",
    "sg",
    "safe_difference",
    "combine",
    "Primitive",
    "Box",
    "Cylinder",
    "Sphere",
    "SpurGear",
    "ChainSprocket",
    "ButtHinge",
    "STLExporter",
    "PrintabilityValidator",
    "generate_scaffolding",
    "generate_scaffolding_from_workplane",
    "workplane_to_mesh",
    "Polygon",
    "Point",
    "box",
]
