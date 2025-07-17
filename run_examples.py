import os
import subprocess
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(filename='run_examples_debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def set_environment():
    logging.debug("Setting up environment")
    print("Setting up environment...")
    os.chdir(Path(__file__).parent)
    os.environ["PYTHONPATH"] = "."
    logging.info("Changed directory to script location and set PYTHONPATH to current directory")
    print("Environment set up successfully.")

def run_example_script(script_name):
    logging.debug(f"Attempting to run {script_name}")
    print(f"Running {script_name}...")
    example_path = os.path.join("parametric_cad", "examples", script_name)
    if not os.path.exists(example_path):
        logging.error(f"{example_path} not found")
        print(f"Error: {example_path} not found.")
        return False
    try:
        subprocess.run([sys.executable, example_path], check=True)
        logging.info(f"Successfully ran {script_name}")
        print(f"Successfully ran {script_name}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run {script_name}: {e}")
        print(f"Failed to run {script_name}: {e}")
        return False

def check_output_folder(folder_name):
    logging.debug(f"Checking output folder: {folder_name}")
    print(f"Checking {folder_name} folder...")
    output_path = os.path.join("output", folder_name)
    if os.path.exists(output_path) and os.path.isdir(output_path):
        for item in os.listdir(output_path):
            print(f"  {item}")
        logging.info(f"Found and listed contents of {output_path}")
    else:
        logging.error(f"ERROR: {folder_name} folder does not exist!")
        print(f"ERROR: {folder_name} folder does not exist!")

if __name__ == "__main__":
    logging.debug("Starting run_examples.py execution")
    set_environment()
    
    examples = [
        "box_with_door.py",
        "hollow_box.py",
        "spur_gear_example.py",
        "sprocket_example.py",
    ]
    
    for example in examples:
        run_example_script(example)
        check_output_folder(f"{example.split('.')[0]}_output")
        print()  # Add newline for readability
    
    logging.info("All example execution and output checks completed")
    print("All examples executed and output folders checked.")
    input("Press Enter to continue...")
