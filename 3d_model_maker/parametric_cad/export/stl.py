import trimesh
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='export_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class STLExporter:
    def __init__(self, output_dir="output", binary=True):
        """
        Initialize the STLExporter with output directory and format settings.
        
        Args:
            output_dir (str): Directory for exported files (default: "output")
            binary (bool): Use binary STL format (default: True)
        """
        self.output_dir = output_dir
        self.binary = binary
        os.makedirs(self.output_dir, exist_ok=True)
        logging.debug(f"Initialized STLExporter with output_dir={self.output_dir}, binary={self.binary}")

    def export_mesh(self, mesh, base_filename, timestamp=False):
        """
        Export a trimesh object to an STL file.
        
        Args:
            mesh (trimesh.Trimesh): The mesh to export
            base_filename (str): Base name for the output file (e.g., "box")
            timestamp (bool): Append timestamp to filename (default: False)
        
        Returns:
            str: Full path of the exported file
        """
        if not isinstance(mesh, trimesh.Trimesh):
            logging.error("Input must be a trimesh.Trimesh object")
            raise ValueError("Input must be a trimesh.Trimesh object")

        # Generate filename with optional timestamp
        if timestamp:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_filename}_{timestamp_str}.stl"
        else:
            filename = f"{base_filename}.stl"

        full_path = os.path.join(self.output_dir, filename)
        logging.info(f"Exporting mesh to {full_path} with binary={self.binary}")

        try:
            mesh.export(full_path, file_type="stl", include_texture=False, binary=self.binary)
            logging.info(f"Successfully exported to {full_path}")
            print(f"Exported to {full_path}")
            return full_path
        except Exception as e:
            logging.error(f"Failed to export to {full_path}: {e}")
            print(f"Failed to export to {full_path}: {e}")
            raise

    def export_meshes(self, meshes, base_filename, timestamp=False):
        """
        Export multiple meshes to separate STL files with a common base name.
        
        Args:
            meshes (list): List of trimesh.Trimesh objects
            base_filename (str): Base name for the output files
            timestamp (bool): Append timestamp to filenames (default: False)
        
        Returns:
            list: List of full paths of exported files
        """
        if not isinstance(meshes, (list, tuple)) or not all(isinstance(m, trimesh.Trimesh) for m in meshes):
            logging.error("meshes must be a list of trimesh.Trimesh objects")
            raise ValueError("meshes must be a list of trimesh.Trimesh objects")

        paths = []
        for i, mesh in enumerate(meshes):
            suffix = f"_{i}" if len(meshes) > 1 else ""
            path = self.export_mesh(mesh, f"{base_filename}{suffix}", timestamp)
            paths.append(path)
        return paths

if __name__ == "__main__":
    # Example usage
    box_mesh = trimesh.creation.box([10, 10, 10])
    exporter = STLExporter(output_dir="output", binary=True)
    exporter.export_mesh(box_mesh, "test_box", timestamp=True)
	