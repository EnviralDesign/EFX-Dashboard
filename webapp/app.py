import streamlit as st
from menu import menu
import sys

st.set_page_config(layout="wide")  # Set the page layout to wide

# hide_st_style = """
#                 <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;} I
#                 </style>
#                 """

# st.markdown(hide_st_style, unsafe_allow_html=True)

# st write the directory of this application
# st.write(__file__)
# sys.exit()

# write the entire directory tree of files in the current directory
# import os
# for root, dirs, files in os.walk("."):
#     for file in files:
#         st.write(os.path.join(root, file))

# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = None

# Temporary override to always load as user
if st.session_state.role is None:
    st.session_state.role = "user"

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


# Selectbox to choose role
# st.selectbox(
#     "Select your role:",
#     [None, "user", "admin"],
#     key="_role",
#     on_change=set_role,
# )

menu() # Render the dynamic menu!

# st.title("Hello World!")
