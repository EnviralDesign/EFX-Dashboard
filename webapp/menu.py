import streamlit as st

def read_version():
    with open("data/version.txt") as f:
        return f.read().strip()

__version__ = read_version()

def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("app.py", label="Switch accounts")
    # if st.session_state.role in ["user"]:
    st.sidebar.page_link("pages/user_live.py", label="Live")
    st.sidebar.page_link("pages/user_summary.py", label="Summary")
    st.sidebar.page_link("pages/user_history.py", label="History")
    st.sidebar.page_link("pages/user_settings.py", label="Settings")
    # if st.session_state.role in ["admin"]:
    #     st.sidebar.page_link("pages/admin.py", label="Manage users")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():

    # st.sidebar.markdown(f"**Version: {__version__}**")
    st.sidebar.header(f"**:blue[EFX Dashboard] :gray[v{__version__}]**")

    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
