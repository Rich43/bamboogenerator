from parametric_cad.mechanisms.motor_bracket import RightAngleMotorBracket
from parametric_cad.export.stl import STLExporter
from parametric_cad.logging_config import setup_logging

setup_logging()

bracket = RightAngleMotorBracket()

exporter = STLExporter(output_dir="output/motor_bracket_output")
exporter.export_mesh(bracket.mesh(), "motor_bracket")
