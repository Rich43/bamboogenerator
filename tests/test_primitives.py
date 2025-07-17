import pytest
import numpy as np
from parametric_cad.core import tm, safe_difference
from math import cos, pi

from parametric_cad.primitives.box import Box
from parametric_cad.primitives.gear import SpurGear
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.primitives.sphere import Sphere


def test_box_mesh_extents_and_position():
    box = Box(1.0, 2.0, 3.0).at(1.0, 1.0, 1.0)
    mesh = box.mesh()
    assert np.allclose(mesh.centroid, [1.0, 1.0, 1.0])
    assert mesh.extents[0] == pytest.approx(1.0)
    assert mesh.extents[1] == pytest.approx(2.0)
    assert mesh.extents[2] == pytest.approx(3.0)


def test_spur_gear_diameters():
    gear = SpurGear(module=2.0, teeth=10)
    assert gear.pitch_diameter == pytest.approx(20.0)
    expected_base = gear.pitch_diameter * cos(20 * pi / 180)
    assert gear.base_diameter == pytest.approx(expected_base)


def test_cylinder_and_sphere_meshes():
    cyl = Cylinder(radius=1.0, height=2.0).at(0.5, 0.5, 0)
    sph = Sphere(radius=1.0).at(-0.5, -0.5, 0)
    cyl_mesh = cyl.mesh()
    sph_mesh = sph.mesh()
    assert isinstance(cyl_mesh, tm.Trimesh)
    assert isinstance(sph_mesh, tm.Trimesh)
    assert cyl_mesh.is_watertight
    assert sph_mesh.is_watertight


def test_safe_difference_returns_mesh():
    outer = Box(1.0, 1.0, 1.0)
    inner = Box(0.5, 0.5, 0.5).at(0.25, 0.25, 0.25)
    result = safe_difference(outer.mesh(), inner.mesh(), engine="invalid")
    assert isinstance(result, tm.Trimesh)
