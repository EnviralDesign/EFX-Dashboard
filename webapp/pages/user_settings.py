import streamlit as st
from menu import menu_with_redirect
from streamlit_ace import st_ace
import json

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Settings Page")
st.markdown(f"Configure your settings here. You are currently logged in with the role of {st.session_state.role}.")

# Add your settings UI components here

# Initialize session state for JSON data if not already set
if 'json_data' not in st.session_state:
    st.session_state.json_data = json.dumps({"key": "value"}, indent=4)

# JSON Editor
st.subheader("JSON Editor")
json_data = st_ace(value=st.session_state.json_data, language='json', theme='monokai', keybinding='vscode', font_size=14, tab_size=4, show_gutter=True, wrap=True)

# Save the JSON data to session state
st.session_state.json_data = json_data

# Display the JSON data
st.subheader("JSON Output")
st.json(json.loads(json_data))
