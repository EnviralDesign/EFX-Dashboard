import streamlit as st
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Overview Page")
st.markdown(f"Account Overview. You are currently logged in with the role of {st.session_state.role}.")

# Add your overview UI components here
