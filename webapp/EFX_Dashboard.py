import os
import sys
import subprocess
import shutil
# import streamlit.web.bootstrap
from streamlit.web import cli 
# from streamlit.web import cli
# import streamlit as st
# import streamlit_ace
# import pandas as pd

# Read the version number from version.txt
def read_version():
    with open("data/version.txt") as f:
        return f.read().strip()

def main():


    __version__ = read_version()

    # Get the absolute path to the directory containing the executable
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # exposes this attribute and the value is the absolute path to the bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Path to your Streamlit app
    app_path = os.path.join(base_path, 'app.py')

    # # Ensure streamlit is available
    # streamlit_executable = shutil.which("streamlit")
    # if not streamlit_executable:
    #     print("Streamlit is not available. Please ensure Streamlit is installed.")
    #     sys.exit(1)

    # Create an ASCII comment box
    print("#############################################")
    print("#                                           #")
    print(f"#    Running EFX Dashboard version {__version__}    #")
    print("#                                           #")
    print("#############################################")

    # Run the Streamlit app
    subprocess.run(["streamlit", "run", app_path])

    # cli._main_run_clExplicit(app_path, 'streamlit run')
    # cli._main_run_clExplicit('app.py', 'streamlit run')

if __name__ == "__main__":
    main()