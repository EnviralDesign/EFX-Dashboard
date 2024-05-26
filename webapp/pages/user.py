import streamlit as st
import pandas as pd
import traceback
from menu import menu_with_redirect
from datetime import datetime, timedelta, date
from utils import load_data, format_currency, color_net_profit, style_dataframe

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("User Home Page")
st.markdown(f"Welcome to your home page! You are currently logged in with the role of {st.session_state.role}.")

# Path to the .tsv file in the root directory
file_path = 'data.tsv'

# Load the data
df = load_data(file_path)

print("==================")

# Extract the date range
min_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S').min()
max_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S').max()
# min_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y').min()
# max_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y').max()

# Convert 'ServerCloseTime' to datetime
df['ServerCloseTime'] = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S')

# Initialize session state for start_date and end_date if not already set
if 'start_date' not in st.session_state:
    st.session_state.start_date = min_date
if 'end_date' not in st.session_state:
    st.session_state.end_date = max_date

# UI for selecting the date range
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=st.session_state.start_date)
    st.session_state.start_date = start_date
with col2:
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=st.session_state.end_date)
    st.session_state.end_date = end_date

# Adjust end_date to include the entire day
end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
# Filter the data based on the selected date range
filtered_df = df[(df['ServerCloseTime'] >= pd.to_datetime(start_date)) & (df['ServerCloseTime'] <= end_date)]

# Apply styling and formatting to the DataFrame
styled_df = style_dataframe(filtered_df)

# Use st.container to make the table fully wide
with st.container():
    st.dataframe(styled_df, use_container_width=True)
