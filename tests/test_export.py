import os
from pathlib import Path
import pytest
from parametric_cad.primitives.box import Box
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.export.stl import STLExporter

EXPECTED_DIR = Path(__file__).parent / "expected_stl"


def test_stl_exporter(tmp_path):
    exporter = STLExporter(output_dir=tmp_path)
    box = Box(1.0, 1.0, 1.0)
    path = exporter.export_mesh(box, "test_box", preview=False)
    assert os.path.isfile(path)
    assert path == str(tmp_path / "test_box.stl")
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
    with open(EXPECTED_DIR / "test_box.stl", "r", encoding="utf-8") as f:
        expected = f.read()
    assert contents == expected


def test_ascii_stl_multiple_objects(tmp_path):
    exporter = STLExporter(output_dir=tmp_path)
    box = Box(1.0, 2.0, 1.0).at(0, 0, 0.5)
    cyl = Cylinder(radius=2.0, height=1.0, sections=8).at(3, 0, 0.5)
    box2 = Box(0.5, 0.5, 0.5).at(0, 3, 0.25)
    path = exporter.export_meshes([box, cyl, box2], "combo", preview=False)
    assert os.path.isfile(path)
    assert path == str(tmp_path / "combo.stl")
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
    with open(EXPECTED_DIR / "combo.stl", "r", encoding="utf-8") as f:
        expected = f.read()
    assert contents == expected


def test_exporter_printability_failure(tmp_path):
    exporter = STLExporter(output_dir=tmp_path)
    big_box = Box(300.0, 10.0, 10.0)
    with pytest.raises(ValueError):
        exporter.export_mesh(big_box, "bad_box", preview=False)
