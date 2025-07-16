import numpy as np
import pytest
import trimesh

from parametric_cad.mechanisms.butthinge import ButtHinge


def test_butthinge_mesh_and_translation():
    hinge = ButtHinge()
    mesh = hinge.mesh()
    assert isinstance(mesh, trimesh.Trimesh)
    original_centroid = mesh.centroid.copy()
    hinge.at(1.0, 2.0, 3.0)
    translated_centroid = hinge.mesh().centroid
    assert np.allclose(translated_centroid, original_centroid + [1.0, 2.0, 3.0])
