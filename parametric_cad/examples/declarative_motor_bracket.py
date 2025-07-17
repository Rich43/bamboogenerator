from math import pi

from parametric_cad.primitives.box import Box
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.core import combine, safe_difference
from parametric_cad.export.stl import STLExporter

# Basic dimensions for a 540/550 motor bracket
BASE_LENGTH = 50.0
BASE_WIDTH = 40.0
PLATE_HEIGHT = 40.0
THICKNESS = 3.0
MOTOR_HOLE_SPACING = 25.0
MOTOR_HOLE_DIAMETER = 3.2
SHAFT_CLEARANCE_DIAMETER = 10.0
MOTOR_MOUNT_HEIGHT = 20.0

# Create the two plates of the bracket
base = Box(BASE_LENGTH, BASE_WIDTH, THICKNESS).at(0, 0, 0)
plate = Box(BASE_LENGTH, THICKNESS, PLATE_HEIGHT).at(
    0, BASE_WIDTH - THICKNESS, THICKNESS
)

# Union the plates into a single mesh
bracket = combine([base, plate])

# Define mounting and shaft clearance holes
hole_y = BASE_WIDTH - THICKNESS / 2
hole_z = THICKNESS + MOTOR_MOUNT_HEIGHT
holes = [
    Cylinder(MOTOR_HOLE_DIAMETER / 2, THICKNESS + 0.2)
    .rotate([1, 0, 0], pi / 2)
    .at(BASE_LENGTH / 2 - MOTOR_HOLE_SPACING / 2, hole_y, hole_z),
    Cylinder(MOTOR_HOLE_DIAMETER / 2, THICKNESS + 0.2)
    .rotate([1, 0, 0], pi / 2)
    .at(BASE_LENGTH / 2 + MOTOR_HOLE_SPACING / 2, hole_y, hole_z),
    Cylinder(SHAFT_CLEARANCE_DIAMETER / 2, THICKNESS + 0.2)
    .rotate([1, 0, 0], pi / 2)
    .at(BASE_LENGTH / 2, hole_y, hole_z),
]

# Subtract holes from the bracket body
bracket = safe_difference(bracket, [h.mesh() for h in holes])

# Export result
exporter = STLExporter(output_dir="output/declarative_motor_bracket_output")
exporter.export_mesh(bracket, "declarative_motor_bracket")
