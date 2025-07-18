from __future__ import annotations

import numpy as np

from .core import tm


def generate_scaffolding(
    mesh: tm.Trimesh,
    *,
    max_angle_deg: float = 45.0,
    support_radius: float = 0.5,
    grid_size: float = 5.0,
    sections: int = 8,
) -> tm.Trimesh:
    """Return support scaffolding for downward overhangs of ``mesh``.

    Parameters
    ----------
    mesh:
        Mesh to analyze for overhangs.
    max_angle_deg:
        Angles from vertical greater than this require support.
    support_radius:
        Radius of the cylindrical support columns.
    grid_size:
        Grid spacing for clustering support columns. ``0`` disables clustering.
    sections:
        Number of cylinder sections used to generate the columns.
    """
    normals = mesh.face_normals
    centers = mesh.triangles_center
    min_z = float(mesh.bounds[0, 2])

    angles = np.degrees(np.arccos(np.clip(normals[:, 2], -1.0, 1.0)))
    overhang = (angles > 90.0 + max_angle_deg) & (centers[:, 2] > min_z + 1e-6)
    if not np.any(overhang):
        return tm.Trimesh()

    pts = centers[overhang]
    if grid_size > 0:
        xy = np.round(pts[:, :2] / grid_size) * grid_size
        unique_xy, inverse = np.unique(xy, axis=0, return_inverse=True)
        top_z = np.zeros(len(unique_xy))
        for i in range(len(unique_xy)):
            top_z[i] = pts[inverse == i][:, 2].max()
    else:
        unique_xy = pts[:, :2]
        top_z = pts[:, 2]

    supports = []
    for (x, y), z in zip(unique_xy, top_z):
        height = z - min_z
        if height <= 0:
            continue
        cyl = tm.creation.cylinder(
            radius=support_radius, height=height, sections=sections
        )
        cyl.apply_translation([0, 0, height / 2])
        cyl.apply_translation([x, y, min_z])
        supports.append(cyl)

    if not supports:
        return tm.Trimesh()
    return tm.util.concatenate(supports)


__all__ = ["generate_scaffolding"]
