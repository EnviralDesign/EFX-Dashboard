import streamlit as st
from menu import menu_with_redirect
from streamlit_ace import st_ace
import json
import os

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Settings Page")
st.markdown(f"Configure your settings here. You are currently logged in with the role of {st.session_state.role}.")

# Add your settings UI components here

# Path to the config file
config_path = os.path.join('data', 'config.json')
template_path = os.path.join('data', 'config.template.json')

# Check if config file exists, if not create it using the template
if not os.path.exists(config_path):
    with open(template_path, 'r') as template_file:
        template_data = json.load(template_file)
    with open(config_path, 'w') as config_file:
        json.dump(template_data, config_file, indent=4)

# Load the JSON data from config file
with open(config_path, 'r') as config_file:
    st.session_state.json_data = json.load(config_file)

# JSON Editor
st.subheader("JSON Editor")
json_data = st_ace(value=json.dumps(st.session_state.json_data, indent=4), language='json', theme='monokai', keybinding='vscode', font_size=14, tab_size=4, show_gutter=True, wrap=True)

# Validate JSON
try:
    json.loads(json_data)
    json_valid = True
except json.JSONDecodeError:
    json_valid = False

# Save the JSON data to session state if valid
if json_valid:
    st.session_state.json_data = json_data
    # Save the JSON data to config file
    with open(config_path, 'w') as config_file:
        json.dump(json.loads(json_data), config_file, indent=4)
else:
    st.warning("Invalid JSON. Please correct the errors and try again.")

# Display the JSON data
st.subheader("JSON Output")
if json_valid:
    st.json(json.loads(json_data))
else:
    st.error("Invalid JSON")
