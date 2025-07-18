from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .core import tm
import numpy as np


def _default_rules_path() -> Path:
    return Path(__file__).resolve().parent.parent / "bambu_printability_rules.json"


class PrintabilityValidator:
    """Validate meshes against Bambu Labs printability guidelines."""

    def __init__(self, rules_file: str | Path | None = None) -> None:
        path = Path(rules_file) if rules_file else _default_rules_path()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.rules = data.get("rules", {})
        self.rules_file = path

    def validate_mesh(self, mesh: tm.Trimesh) -> List[str]:
        r = self.rules
        errors: List[str] = []

        if r.get("manifold_geometry_required") and not mesh.is_watertight:
            errors.append("Mesh is not watertight")

        if r.get("no_open_edges") and mesh.euler_number < 2:
            errors.append("Mesh has open edges")

        if r.get("no_intersecting_geometry"):
            try:
                if mesh.is_self_intersecting:
                    errors.append("Mesh has self intersections")
            except Exception:
                pass

        max_tris = r.get("maximum_file_triangle_count")
        if max_tris and mesh.faces.shape[0] > max_tris:
            errors.append(
                f"Triangle count {mesh.faces.shape[0]} exceeds maximum of {max_tris}"
            )

        max_size = r.get("max_model_size_mm", {})
        extents = mesh.extents
        for axis, idx in zip(["X", "Y", "Z"], range(3)):
            max_dim = max_size.get(axis)
            if max_dim and extents[idx] > max_dim:
                errors.append(
                    f"{axis} dimension {extents[idx]:.2f}mm exceeds max of {max_dim}mm"
                )

        min_feat = r.get("minimum_feature_size_mm")
        if min_feat:
            try:
                min_len = float(min(mesh.edges_unique_length))
                if min_len < min_feat:
                    errors.append(
                        f"Minimum feature size {min_len:.2f}mm below {min_feat}mm"
                    )
            except Exception:
                pass

        max_angle = r.get("overhang_max_angle_deg")
        if max_angle is not None:
            normals = mesh.face_normals
            min_z = mesh.bounds[0, 2]
            downward = (normals[:, 2] < 0) & (
                mesh.triangles_center[:, 2] > min_z + 1e-6
            )
            if np.any(downward):
                angles = np.degrees(
                    np.arccos(np.clip(normals[downward, 2], -1.0, 1.0))
                )
                if angles.size > 0 and angles.max() > max_angle:
                    errors.append("Overhang angle exceeds maximum")

        return errors

    def validate_file(self, file_path: str | Path) -> List[str]:
        mesh = tm.load(file_path)
        return self.validate_mesh(mesh)


__all__ = ["PrintabilityValidator"]
