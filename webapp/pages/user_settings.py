import streamlit as st
from menu import menu_with_redirect
from streamlit_ace import st_ace
import json
import os

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.header('Settings', divider='grey')
st.markdown(f"Configure your settings here.")

config_path = os.path.join('data', 'config.json')
template_path = os.path.join('data', 'config.template.json')

if not os.path.exists(config_path):
    with open(template_path, 'r') as template_file:
        template_data = json.load(template_file)
    with open(config_path, 'w') as config_file:
        json.dump(template_data, config_file, indent=4)

with open(config_path, 'r') as config_file:
    st.session_state.json_data = json.load(config_file)

# st.subheader("JSON Editor")
json_data = st_ace(value=json.dumps(st.session_state.json_data, indent=4), language='json', theme='monokai', keybinding='vscode', font_size=14, tab_size=4, show_gutter=True, wrap=True)

try:
    json.loads(json_data)
    json_valid = True
except json.JSONDecodeError:
    json_valid = False

# Only save if the JSON data from the editor is different from the JSON data from the file
if json_valid and json_data != json.dumps(st.session_state.json_data, indent=4):
    st.session_state.json_data = json.loads(json_data)
    with open(config_path, 'w') as config_file:
        json.dump(st.session_state.json_data, config_file, indent=4)
    st.toast("JSON data saved successfully.")
elif not json_valid:
    st.toast("Invalid JSON. Please correct the errors and try again.")