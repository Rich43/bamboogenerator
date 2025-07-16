import os
import pytest
import trimesh
from parametric_cad.primitives.box import Box
from parametric_cad.export.stl import STLExporter


def test_stl_exporter(tmp_path):
    exporter = STLExporter(output_dir=tmp_path)
    box = Box(1.0, 1.0, 1.0)
    path = exporter.export_mesh(box, "test_box", preview=False)
    assert os.path.isfile(path)
    assert path == str(tmp_path / "test_box.stl")
