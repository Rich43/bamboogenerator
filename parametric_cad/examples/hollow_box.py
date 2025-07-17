from parametric_cad.primitives.box import Box
from parametric_cad.export.stl import STLExporter
from parametric_cad.core import safe_difference
from parametric_cad.logging_config import setup_logging

setup_logging()

outer = Box(100, 60, 40).at(0, 0, 0)
inner = Box(90, 50, 30).at(5, 5, 5)

# Create hollow box by subtracting inner from outer
outer_mesh = outer.mesh()
inner_mesh = inner.mesh()
hollow_box = safe_difference(outer_mesh, inner_mesh)

exporter = STLExporter(output_dir="output/hollow_box_output")
exporter.export_mesh(hollow_box, "hollow_box")
