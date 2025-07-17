from parametric_cad.core import tm
import os
import logging
import numpy as np
from pathlib import Path
from datetime import datetime

logging.basicConfig(filename='stl_export.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class STLExporter:
    """Export trimesh objects to STL with optional previews."""

    def __init__(self, output_dir="output", binary=False):
        self.output_dir = output_dir
        self.binary = binary
        os.makedirs(self.output_dir, exist_ok=True)

    def _ensure_mesh(self, obj):
        if isinstance(obj, tm.Trimesh):
            return obj
        if hasattr(obj, "mesh"):
            m = obj.mesh
            return m() if callable(m) else m
        raise TypeError(f"Object {obj} has no mesh data")

    def export_mesh(self, obj, base_filename, timestamp=False, preview=True):
        return self.export_meshes([obj], base_filename, timestamp=timestamp,
                                  preview=preview)

    def export_meshes(self, objs, base_filename, timestamp=False, preview=True):
        meshes = [self._ensure_mesh(o) for o in objs]
        combined = tm.util.concatenate(meshes)
        if not combined.is_watertight or combined.vertices.shape[0] == 0:
            repaired = combined.fill_holes()
            if repaired is not False:
                combined = repaired
            else:
                combined = combined.convex_hull

        filename = f"{base_filename}.stl"
        if timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_filename}_{ts}.stl"
        path = os.path.join(self.output_dir, filename)
        if self.binary:
            combined.export(path, file_type="stl")
        else:
            text = tm.exchange.stl.export_stl_ascii(combined)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        logging.info(f"Exported STL to {path}")

        if preview:
            try:
                self._render_preview_multiangle(combined, Path(self.output_dir), base_filename)
            except Exception as e:
                logging.error(f"Could not generate preview for {base_filename}: {e}")
        return path

    def _render_preview_multiangle(self, mesh, output_dir: Path, base_name: str):
        if not mesh.is_watertight or mesh.vertices.shape[0] == 0:
            logging.warning(f"Invalid mesh for preview: {base_name}")
            return

        scene = mesh.scene()
        centroid = mesh.centroid
        radius = max(mesh.extents) * 1.5
        angles = [
            [1, 0, 1], [-1, 0, 1], [0, 1, 1], [0, -1, 1],
            [1, 1, 1], [-1, -1, 1], [0, 0, 1], [0, 0, -1]
        ]
        for i, direction in enumerate(angles, start=1):
            eye = centroid + np.array(direction) * radius
            scene.camera_transform = self._look_at(eye, centroid, up=[0, 0, 1])
            img = scene.save_image(resolution=(600, 600), visible=False,
                                   background=[255, 255, 255, 255])
            if img:
                preview_path = output_dir / f"{base_name}_view{i}.png"
                with open(preview_path, "wb") as f:
                    f.write(img)

    def _look_at(self, eye, target, up):
        eye = np.array(eye)
        target = np.array(target)
        up = np.array(up)
        forward = target - eye
        forward /= np.linalg.norm(forward)
        right = np.cross(forward, up)
        norm = np.linalg.norm(right)
        right = right / norm if norm > 1e-6 else np.array([1, 0, 0])
        true_up = np.cross(right, forward)
        rot = np.eye(4)
        rot[:3, :3] = np.stack([right, true_up, -forward], axis=1)
        rot[:3, 3] = eye
        return rot
