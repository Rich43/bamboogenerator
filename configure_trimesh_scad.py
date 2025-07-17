import os
import sys
from parametric_cad.core import tm
import logging

logging.basicConfig(filename='install_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_trimesh_scad():
    logging.debug("Starting trimesh configuration process")
    # Default OpenSCAD path
    default_path = r"C:\Program Files\OpenSCAD\openscad.exe"
    openscad_path = os.environ.get("OPENSCAD_PATH", default_path)
    logging.debug(f"Initial OpenSCAD path set to {openscad_path}")

    print("Configuring trimesh to use OpenSCAD engine...")
    logging.info("Checking trimesh module availability")

    # Check if trimesh (the mesh backend) is available
    try:
        _ = tm.__version__
        logging.info("trimesh module found")
        print("trimesh module found.")
    except Exception:
        logging.error("trimesh module not found")
        print("trimesh module not found! Please ensure it is installed via 'pip install trimesh'.")
        sys.exit(1)

    # Check if OpenSCAD executable exists
    logging.debug(f"Verifying OpenSCAD existence at {openscad_path}")
    if not os.path.exists(openscad_path):
        logging.warning(f"OpenSCAD not found at {openscad_path}")
        print(f"OpenSCAD not found at {openscad_path}! Please install OpenSCAD or specify the correct path.")
        openscad_path = input("Enter the full path to openscad.exe: ")
        logging.debug(f"User provided OpenSCAD path: {openscad_path}")
        if not os.path.exists(openscad_path):
            logging.error("User provided invalid OpenSCAD path")
            print("Invalid path! Aborting.")
            sys.exit(1)

    # Note: set_engine_options is not available in trimesh 4.7.0
    logging.warning("trimesh.boolean.set_engine_options not available in trimesh 4.7.0")
    print("Warning: trimesh.boolean.set_engine_options is not available in this version of trimesh (4.7.0).")
    print("To use the OpenSCAD engine, set the OPENSCADPATH environment variable manually or use an older version of trimesh.")
    print(f"Manually set OPENSCADPATH to {openscad_path} in your environment variables or trimesh configuration.")
    logging.info(f"Recommended OPENSCADPATH: {openscad_path}")

    print("Restart your Python environment or IDE for changes to take effect.")
    logging.debug("Configuration process completed, awaiting user input")
    input("Press Enter to continue...")

if __name__ == "__main__":
    configure_trimesh_scad()
