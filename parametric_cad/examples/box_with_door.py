from parametric_cad.primitives.box import Box
from parametric_cad.mechanisms.butthinge import ButtHinge
from parametric_cad.export.stl import STLExporter

box = Box(100, 60, 40).at(0, 0, 0)
door = Box(100, 3, 40).at(0, 63, 0)
hinge = ButtHinge(leaf_length=40, pin_diameter=3).at(50, 61.5, 20)

exporter = STLExporter(output_dir="output/box_with_door_output")
exporter.export_meshes([box,], "box")
exporter.export_meshes([door, hinge], "door_with_hinge")
