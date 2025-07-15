import trimesh
import os
from pathlib import Path
import numpy as np
import logging

logging.basicConfig(filename='stl_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def export_to_stl(objects, filename, output_folder="output"):
    if not isinstance(objects, list):
        objects = [objects]

    out_dir = os.path.join("output", output_folder)
    os.makedirs(out_dir, exist_ok=True)

    meshes = []
    for obj in objects:
        if isinstance(obj, trimesh.Trimesh):
            meshes.append(obj)
        elif hasattr(obj, "mesh"):
            meshes.append(obj.mesh())
        else:
            raise TypeError(f"Object {obj} has no .mesh() method and is not a Trimesh object.")

    combined = trimesh.util.concatenate(meshes)
    logging.debug(f"Combined mesh has {len(combined.vertices)} vertices")

    if not combined.is_watertight or combined.vertices.shape[0] == 0:
        logging.warning("Mesh is invalid or empty, attempting repair...")
        repaired = combined.fill_holes()
        if repaired is False:
            logging.warning("fill_holes() failed, using convex_hull as fallback")
            combined = combined.convex_hull
        else:
            combined = repaired

    output_path = os.path.join(out_dir, f"{filename}.stl")
    combined.export(output_path)
    logging.info(f"Exported to {output_path}")

    try:
        _render_preview_multiangle(combined, Path(out_dir), filename)
    except Exception as e:
        logging.error(f"Could not generate multi-angle OpenGL previews for {filename}: {e}")

def _render_preview_multiangle(mesh, output_dir, base_name):
    if not mesh.is_watertight or mesh.vertices.shape[0] == 0:
        logging.warning(f"Invalid or empty mesh for {base_name}, skipping preview.")
        return

    scene = mesh.scene()
    centroid = mesh.centroid
    radius = max(mesh.extents) * 1.5

    angles = [
        [1, 0, 1],
        [-1, 0, 1],
        [0, 1, 1],
        [0, -1, 1],
        [1, 1, 1],
        [-1, -1, 1],
        [0, 0, 1],
        [0, 0, -1],
    ]

    for i, direction in enumerate(angles, start=1):
        eye = centroid + np.array(direction) * radius
        try:
            scene.camera_transform = _look_at(eye, centroid, up=[0, 0, 1])
            img = scene.save_image(resolution=(600, 600), visible=False, background=[255, 255, 255, 255])
            if img:
                preview_path = output_dir / f"{base_name}_view{i}.png"
                with open(preview_path, 'wb') as f:
                    f.write(img)
            else:
                logging.warning(f"No image data returned for view {i} of {base_name}")
        except Exception as render_error:
            logging.error(f"Failed to render view {i} for {base_name}: {render_error}")

def _look_at(eye, target, up):
    eye = np.array(eye)
    target = np.array(target)
    up = np.array(up)

    forward = (target - eye)
    forward /= np.linalg.norm(forward)

    right = np.cross(forward, up)
    norm = np.linalg.norm(right)
    right = right / norm if norm > 1e-6 else np.array([1, 0, 0])

    true_up = np.cross(right, forward)
    rot = np.eye(4)
    rot[:3, :3] = np.stack([right, true_up, -forward], axis=1)
    rot[:3, 3] = eye
    return rot