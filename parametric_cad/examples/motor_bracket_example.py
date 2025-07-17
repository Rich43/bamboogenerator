from parametric_cad.mechanisms.motor_bracket import RightAngleMotorBracket
from parametric_cad.export.stl import STLExporter

bracket = RightAngleMotorBracket()

exporter = STLExporter(output_dir="output/motor_bracket_output")
exporter.export_mesh(bracket.mesh(), "motor_bracket")
