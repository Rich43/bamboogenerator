import pytest
import numpy as np
import trimesh
from math import cos, pi

from parametric_cad.primitives.box import Box
from parametric_cad.primitives.gear import SpurGear


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
