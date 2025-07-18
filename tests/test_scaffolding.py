import pytest
from parametric_cad import Box, combine, generate_scaffolding


def test_scaffolding_generation():
    base = Box(2.0, 2.0, 1.0)
    overhang = Box(1.0, 1.0, 0.5).at(1.5, 0.5, 1.0)
    mesh = combine([base, overhang])
    scaff = generate_scaffolding(mesh)
    assert isinstance(scaff, type(mesh))
    # Should extend from model base upwards
    assert scaff.bounds[0, 2] == pytest.approx(mesh.bounds[0, 2])
    assert scaff.bounds[1, 2] <= mesh.bounds[1, 2]
    assert scaff.vertices.shape[0] > 0
