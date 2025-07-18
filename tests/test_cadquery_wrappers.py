import cadquery as cq
from parametric_cad import (
    generate_scaffolding_from_workplane,
    PrintabilityValidator,
    tm,
)


def test_scaffolding_from_workplane():
    base = cq.Workplane("XY").box(2, 2, 1)
    overhang = cq.Workplane("XY").box(1, 1, 0.5).translate((1.5, 0.5, 1))
    wp = base.union(overhang)
    scaff = generate_scaffolding_from_workplane(wp)
    assert isinstance(scaff, tm.Trimesh)
    assert scaff.vertices.shape[0] > 0


def test_validate_workplane():
    wp = cq.Workplane("XY").box(10, 10, 10)
    validator = PrintabilityValidator()
    errors = validator.validate_workplane(wp)
    assert errors == []
