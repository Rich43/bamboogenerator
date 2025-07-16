import os
import pytest
import trimesh
from parametric_cad.primitives.box import Box
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.primitives.sphere import Sphere
from parametric_cad.export.stl import STLExporter


def test_stl_exporter(tmp_path):
    exporter = STLExporter(output_dir=tmp_path)
    box = Box(1.0, 1.0, 1.0)
    path = exporter.export_mesh(box, "test_box", preview=False)
    assert os.path.isfile(path)
    assert path == str(tmp_path / "test_box.stl")


def test_ascii_stl_multiple_objects(tmp_path):
    exporter = STLExporter(output_dir=tmp_path, binary=False)
    box = Box(1.0, 2.0, 1.0)
    cyl = Cylinder(radius=0.5, height=1.0)
    sph = Sphere(radius=0.25)
    path = exporter.export_meshes([box, cyl, sph], "combo", preview=False)
    assert os.path.isfile(path)
    assert path == str(tmp_path / "combo.stl")
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    assert first_line.startswith("solid")
