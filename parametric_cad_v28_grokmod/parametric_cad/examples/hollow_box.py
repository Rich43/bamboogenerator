from parametric_cad.primitives.box import Box
from parametric_cad.export.stl import export_to_stl
import trimesh

outer = Box(100, 60, 40).at(0, 0, 0)
inner = Box(90, 50, 30).at(5, 5, 5)

# Create hollow box by subtracting inner from outer
outer_mesh = outer.mesh()
inner_mesh = inner.mesh()
hollow_box = outer_mesh.difference(inner_mesh)

export_to_stl(hollow_box, "hollow_box", output_folder="hollow_box_output")
