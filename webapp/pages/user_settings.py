import streamlit as st
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Settings Page")
st.markdown(f"Configure your settings here. You are currently logged in with the role of {st.session_state.role}.")

# Add your settings UI components here
