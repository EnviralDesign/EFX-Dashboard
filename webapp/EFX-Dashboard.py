import os
import sys
import subprocess

def main():
    # Get the absolute path to the directory containing the executable
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # exposes this attribute and the value is the absolute path to the bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Path to your Streamlit app
    app_path = os.path.join(base_path, 'app.py')

    # Run the Streamlit app
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    main()