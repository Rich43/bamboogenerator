import pytest
import numpy as np
from parametric_cad.core import tm, safe_difference, combine
from math import cos, sin, pi

from parametric_cad.primitives.base import Primitive
from parametric_cad.primitives.box import Box
from parametric_cad.primitives.gear import SpurGear
from parametric_cad.primitives.cylinder import Cylinder
from parametric_cad.primitives.sphere import Sphere
from parametric_cad.primitives.sprocket import ChainSprocket


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


def test_combine_and_rotation():
    box = Box(1.0, 1.0, 1.0)
    cyl = Cylinder(radius=0.5, height=2.0).rotate([1, 0, 0], pi / 2)
    combined = combine([box, cyl])
    assert isinstance(combined, tm.Trimesh)
    # Cylinder rotated around X should extend its height along Y axis
    assert combined.extents[1] >= 2.0


def test_chain_sprocket_properties_and_mesh():
    sprocket = ChainSprocket(pitch=12.7, roller_diameter=7.75, teeth=10)
    expected_pitch_dia = 2 * sprocket.pitch / (2 * sin(pi / sprocket.teeth))
    assert sprocket.pitch_diameter == pytest.approx(expected_pitch_dia)
    mesh = sprocket.mesh()
    assert isinstance(mesh, tm.Trimesh)
    assert mesh.is_watertight


def test_primitive_inheritance():
    assert isinstance(Box(1, 1, 1), Primitive)
    assert isinstance(Cylinder(1, 1), Primitive)
    assert isinstance(Sphere(1), Primitive)
    assert isinstance(SpurGear(module=1.0, teeth=8), Primitive)
    assert isinstance(ChainSprocket(), Primitive)
