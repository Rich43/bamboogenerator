import io
import cadquery as cq
from cadquery.occ_impl import exporters

from .core import tm


def workplane_to_mesh(wp: cq.Workplane) -> tm.Trimesh:
    """Convert a CadQuery Workplane to a Trimesh mesh."""
    stl = exporters.toString(wp.val(), exporters.ExportTypes.STL)
    return tm.load(io.BytesIO(stl.encode("utf-8")), file_type="stl")

__all__ = ["workplane_to_mesh"]
