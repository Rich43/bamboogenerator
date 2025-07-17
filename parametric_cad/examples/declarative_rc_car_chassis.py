# Example script to generate a simple RC car chassis declaratively
from math import pi

from parametric_cad.primitives.box import Box
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.core import combine, safe_difference
from parametric_cad.export.stl import STLExporter

# Basic chassis dimensions (all units in mm)
BASE_LENGTH = 200.0
BASE_WIDTH = 100.0
BASE_THICKNESS = 5.0

SIDE_HEIGHT = 20.0
SIDE_THICKNESS = 4.0

BRACE_WIDTH = 10.0
BRACE_HEIGHT = SIDE_HEIGHT

MOUNT_HOLE_DIAMETER = 4.0
HOLE_OFFSET_FROM_END = 20.0
HOLE_SPACING_FROM_SIDE = 15.0

# Base plate
base_plate = Box(BASE_LENGTH, BASE_WIDTH, BASE_THICKNESS).at(0, 0, 0)

# Side rails running the length of the chassis
left_rail = (
    Box(BASE_LENGTH, SIDE_THICKNESS, SIDE_HEIGHT)
    .at(0, 0, BASE_THICKNESS)
)
right_rail = (
    Box(BASE_LENGTH, SIDE_THICKNESS, SIDE_HEIGHT)
    .at(0, BASE_WIDTH - SIDE_THICKNESS, BASE_THICKNESS)
)

# Front and rear cross braces for rigidity
front_brace = (
    Box(BRACE_WIDTH, BASE_WIDTH - 2 * SIDE_THICKNESS, BRACE_HEIGHT)
    .at(0, SIDE_THICKNESS, BASE_THICKNESS)
)
rear_brace = (
    Box(BRACE_WIDTH, BASE_WIDTH - 2 * SIDE_THICKNESS, BRACE_HEIGHT)
    .at(BASE_LENGTH - BRACE_WIDTH, SIDE_THICKNESS, BASE_THICKNESS)
)

# Combine chassis components
chassis = combine([base_plate, left_rail, right_rail, front_brace, rear_brace])

# Mounting holes near the corners of the base
hole_positions = [
    (HOLE_OFFSET_FROM_END, HOLE_SPACING_FROM_SIDE),
    (HOLE_OFFSET_FROM_END, BASE_WIDTH - HOLE_SPACING_FROM_SIDE),
    (BASE_LENGTH - HOLE_OFFSET_FROM_END, HOLE_SPACING_FROM_SIDE),
    (BASE_LENGTH - HOLE_OFFSET_FROM_END, BASE_WIDTH - HOLE_SPACING_FROM_SIDE),
]
holes = [
    Cylinder(MOUNT_HOLE_DIAMETER / 2, BASE_THICKNESS + SIDE_HEIGHT + 0.2).at(x, y, 0)
    for x, y in hole_positions
]

# Subtract holes from chassis
chassis = safe_difference(chassis, [h.mesh() for h in holes])

# Export the final chassis mesh
exporter = STLExporter(output_dir="output/rc_car_chassis_output")
exporter.export_mesh(chassis, "rc_car_chassis")
