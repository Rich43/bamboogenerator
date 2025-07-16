import requests
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='scrape_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_openscad_download():
    url = "https://www.openscad.org/downloads.html"
    logging.debug(f"Attempting to scrape {url}")
    print(f"Scraping {url} for the latest OpenSCAD Windows 64-bit installer...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully fetched {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for links containing ".exe" and "Win64" in the text
        latest_link = None
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and '.exe' in href.lower() and 'win64' in href.lower():
                latest_link = href
                logging.info(f"Found potential download link: {latest_link}")
                break
        
        if not latest_link:
            logging.error("No Windows 64-bit .exe link found on the page")
            print("No Windows 64-bit .exe link found! Please check the website manually.")
            return None
        
        # Ensure the link is absolute
        if not latest_link.startswith('http'):
            latest_link = f"https://www.openscad.org{latest_link}"
        
        logging.info(f"Latest Windows 64-bit installer URL: {latest_link}")
        print(f"Latest Windows 64-bit installer found: {latest_link}")
        return latest_link
    
    except requests.RequestException as e:
        logging.error(f"Failed to scrape {url}: {e}")
        print(f"Failed to scrape {url}: {e}")
        return None

if __name__ == "__main__":
    logging.debug("Starting scrape_openscad_download.py execution")
    download_url = scrape_openscad_download()
    if download_url:
        with open('openscad_download_url.txt', 'w') as f:
            f.write(download_url)
        logging.info(f"Saved download URL to openscad_download_url.txt")
        print(f"Download URL saved to openscad_download_url.txt")
    input("Press Enter to continue...")
