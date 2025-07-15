from parametric_cad.primitives.gear import SpurGear
from parametric_cad.export.stl import export_to_stl

gear = SpurGear(module=1.0, teeth=20, width=8.0, bore_diameter=5.0, hole_count=6, hole_diameter=2.5)
export_to_stl(gear.mesh(), "spur_gear", output_folder="spur_gear_example_output")
