import streamlit as st
from menu import menu_with_redirect
import pandas as pd
from utils import load_config, load_data, calculate_net_profit_sum

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

st.title("Overview Page")
st.markdown(f"Account Overview. You are currently logged in with the role of {st.session_state.role}.")

# Load the config
config = load_config()

# Path to the .tsv file in the root directory
file_path = './data/data.tsv'

# Load the data
df = load_data(file_path)

# Create a DataFrame for the trade groups
trade_groups = []

for group in config['trade-groups']:
    title = group['title']
    comment_filter = group['comment-filter']
    magic_filter = group['magic-filter']
    net_profit_sum = calculate_net_profit_sum(df, comment_filter, magic_filter)
    trade_groups.append({'Title': title, 'Net Profit Sum': net_profit_sum})

trade_groups_df = pd.DataFrame(trade_groups)

# Display the DataFrame
st.dataframe(trade_groups_df)
