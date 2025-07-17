from parametric_cad.primitives.box import Box
from parametric_cad.export.stl import STLExporter

outer = Box(100, 60, 40).at(0, 0, 0)
inner = Box(90, 50, 30).at(5, 5, 5)

# Create hollow box by subtracting inner from outer
outer_mesh = outer.mesh()
inner_mesh = inner.mesh()
try:
    hollow_box = outer_mesh.difference(inner_mesh, engine='scad')
except Exception:
    try:
        hollow_box = outer_mesh.difference(inner_mesh)
    except Exception:
        hollow_box = outer_mesh

exporter = STLExporter(output_dir="output/hollow_box_output")
exporter.export_mesh(hollow_box, "hollow_box")
