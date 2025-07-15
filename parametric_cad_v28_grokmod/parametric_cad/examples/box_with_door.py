from parametric_cad.primitives.box import Box
from parametric_cad.mechanisms.hinge import ButtHinge
from parametric_cad.export.stl import export_to_stl

box = Box(100, 60, 40).at(0, 0, 0)
door = Box(100, 3, 40).at(0, 63, 0)
hinge = ButtHinge(leaf_length=40, pin_diameter=3).at(50, 61.5, 20)

export_to_stl([box], "box", output_folder="box_with_door_output")
export_to_stl([door, hinge], "door_with_hinge", output_folder="box_with_door_output")
