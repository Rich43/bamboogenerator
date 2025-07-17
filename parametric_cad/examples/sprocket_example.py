from parametric_cad.primitives.sprocket import ChainSprocket
from parametric_cad.export.stl import STLExporter
from parametric_cad.logging_config import setup_logging

setup_logging()

# Example sprocket for #420 chain (pitch 12.7 mm, roller dia ~7.75 mm)

sprocket = ChainSprocket(pitch=12.7, roller_diameter=7.75, teeth=14,
                         thickness=6.0, bore_diameter=25.0)

exporter = STLExporter(output_dir="output/sprocket_example_output")
exporter.export_mesh(sprocket.mesh(), "sprocket")
