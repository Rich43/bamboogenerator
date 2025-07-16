import subprocess
import sys
import logging

logging.basicConfig(filename='install_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def install_openscad():
    logging.debug("Starting OpenSCAD installation process")
    print("Installing OpenSCAD dependency...")
    try:
        subprocess.run([sys.executable, "install_openscad.py"], check=True)
        logging.info("OpenSCAD installation completed successfully")
        print("OpenSCAD installation completed.")
    except subprocess.CalledProcessError:
        logging.error("OpenSCAD installation failed")
        print("Failed to install OpenSCAD. Continuing with Python packages...")
        return False
    return True

def install_python_packages():
    logging.debug("Starting Python package installation process")
    print("Installing all required Python packages including triangulation engines...")
    packages = ["trimesh", "numpy", "matplotlib", "pyglet<2", "networkx", "scipy", "shapely", 
                "triangle", "mapbox_earcut", "manifold3d", "pillow", "requests", "beautifulsoup4"]
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + packages, check=True)
        logging.info("Python packages installed successfully")
        print("Python packages installed successfully.")
    except subprocess.CalledProcessError:
        logging.error("Python package installation failed")
        print("Failed to install Python packages!")
        sys.exit(1)

def configure_trimesh_scad():
    logging.debug("Starting trimesh configuration process")
    print("Configuring trimesh for OpenSCAD...")
    try:
        subprocess.run([sys.executable, "configure_trimesh_scad.py"], check=True)
        logging.info("trimesh configuration completed")
    except subprocess.CalledProcessError:
        logging.error("trimesh configuration failed")
        print("Failed to configure trimesh for OpenSCAD. You may need to run configure_trimesh_scad.py manually.")
        return False
    return True

if __name__ == "__main__":
    logging.debug("Starting install_requirements.py execution")
    install_openscad()
    install_python_packages()
    configure_trimesh_scad()
    logging.info("All installation processes completed")
    print("\n✅ All dependencies and OpenSCAD configured (manual trimesh configuration may be required).")
    input("Press Enter to continue...")
