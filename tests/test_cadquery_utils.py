import cadquery as cq
from parametric_cad.cadquery_utils import workplane_to_mesh
from parametric_cad.core import tm


def test_workplane_to_mesh():
    wp = cq.Workplane("XY").box(1, 1, 1)
    mesh = workplane_to_mesh(wp)
    assert isinstance(mesh, tm.Trimesh)
    assert mesh.volume > 0
