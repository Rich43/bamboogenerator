# Example script to generate a simple RC car chassis declaratively
"""Generate a parametric RC car chassis with rounded features."""

from math import pi

from parametric_cad.geometry import box, Point

from parametric_cad.primitives.box import Box
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.core import combine, safe_difference, tm
from parametric_cad.export.stl import STLExporter
from parametric_cad.logging_config import setup_logging

setup_logging()

# Basic chassis dimensions (all units in mm)
BASE_LENGTH = 200.0
BASE_WIDTH = 100.0
BASE_THICKNESS = 5.0

# Rounded corner radius for the base
CORNER_RADIUS = 15.0

# Large central cutout
CENTER_HOLE_RADIUS = 20.0

# Mounting hole spacing for a centre differential
CENTER_DIFF_SPACING_X = 20.0
CENTER_DIFF_SPACING_Y = 15.0

SIDE_HEIGHT = 20.0
SIDE_THICKNESS = 4.0

BRACE_WIDTH = 10.0
BRACE_HEIGHT = SIDE_HEIGHT

MOUNT_HOLE_DIAMETER = 4.0
HOLE_OFFSET_FROM_END = 20.0
HOLE_SPACING_FROM_SIDE = 15.0

# Base plate with rounded corners and a large centre cutout
outer = box(0, 0, BASE_LENGTH, BASE_WIDTH)
rounded = outer.buffer(CORNER_RADIUS).buffer(-CORNER_RADIUS)
# Curved cutouts on the sides for style and weight reduction
SIDE_CUTOUT_RADIUS = 12.0
rounded = rounded.difference(Point(BASE_LENGTH / 2, 0).buffer(SIDE_CUTOUT_RADIUS))
rounded = rounded.difference(Point(BASE_LENGTH / 2, BASE_WIDTH).buffer(SIDE_CUTOUT_RADIUS))
# Large centre hole for driveshaft access
rounded = rounded.difference(Point(BASE_LENGTH / 2, BASE_WIDTH / 2).buffer(CENTER_HOLE_RADIUS))
base_plate = tm.creation.extrude_polygon(rounded, BASE_THICKNESS, engine="triangle")

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

# Additional mounting holes for a centre differential
center_x = BASE_LENGTH / 2
center_y = BASE_WIDTH / 2
diff_positions = [
    (center_x - CENTER_DIFF_SPACING_X / 2, center_y - CENTER_DIFF_SPACING_Y / 2),
    (center_x - CENTER_DIFF_SPACING_X / 2, center_y + CENTER_DIFF_SPACING_Y / 2),
    (center_x + CENTER_DIFF_SPACING_X / 2, center_y - CENTER_DIFF_SPACING_Y / 2),
    (center_x + CENTER_DIFF_SPACING_X / 2, center_y + CENTER_DIFF_SPACING_Y / 2),
]
holes.extend(
    Cylinder(MOUNT_HOLE_DIAMETER / 2, BASE_THICKNESS + SIDE_HEIGHT + 0.2).at(x, y, 0)
    for x, y in diff_positions
)

# Subtract holes from chassis
chassis = safe_difference(chassis, [h.mesh() for h in holes])

# Export the final chassis mesh
exporter = STLExporter(output_dir="output/rc_car_chassis_output")
exporter.export_mesh(chassis, "rc_car_chassis")
