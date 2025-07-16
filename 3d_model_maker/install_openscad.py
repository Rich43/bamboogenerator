import os
import subprocess
import sys
import logging

logging.basicConfig(filename='install_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def download_openscad():
    try:
        with open('openscad_download_url.txt', 'r') as f:
            url = f.read().strip()
    except FileNotFoundError:
        logging.error("openscad_download_url.txt not found! Please run scrape_openscad_download.py first.")
        print("openscad_download_url.txt not found! Please run scrape_openscad_download.py first to get the latest URL.")
        sys.exit(1)
    
    installer = os.path.basename(url)
    logging.debug(f"Attempting to download OpenSCAD from {url}")
    print("Downloading OpenSCAD installer...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        logging.info(f"Download started for {url}")
        with open(installer, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Download completed, saved as {installer}")
        print("Download completed.")
        return True
    except requests.RequestException as e:
        logging.error(f"Download failed: {e}")
        print(f"Failed to download OpenSCAD installer: {e}")
        return False

def install_openscad():
    installer = os.path.basename(url)  # Use the same name as downloaded
    logging.debug(f"Checking if installer exists at {installer}")
    if not os.path.exists(installer):
        logging.warning("Installer not found after download attempt")
        print("Installer not found! Download failed.")
        return False
    
    logging.info(f"Starting installation of {installer}")
    print("Installing OpenSCAD...")
    try:
        subprocess.run([installer, "/S"], check=True, shell=True)
        logging.info("OpenSCAD installation completed")
        print("OpenSCAD installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Installation failed: {e}")
        print(f"Installation failed: {e}")
        return False

def cleanup():
    installer = os.path.basename(url)
    logging.debug(f"Checking for cleanup of {installer}")
    if os.path.exists(installer):
        os.remove(installer)
        logging.info(f"Cleaned up installer file {installer}")
        print("Cleaned up installer file.")

if __name__ == "__main__":
    import requests  # Import here to avoid circular dependency issues
    logging.debug("Starting install_openscad.py execution")
    if not download_openscad():
        sys.exit(1)
    if not install_openscad():
        cleanup()
        sys.exit(1)
    cleanup()
    logging.info("OpenSCAD installation process completed")
    print("Please ensure OpenSCAD is added to your system PATH.")
    print("You may need to restart your command prompt or system for changes to take effect.")
    input("Press Enter to continue...")
