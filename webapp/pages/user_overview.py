import streamlit as st
from menu import menu_with_redirect
import pandas as pd
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates
from datetime import datetime, timedelta


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


st.title("Overview")
# st.markdown(f"Account Overview. You are currently logged in with the role of {st.session_state.role}.")


# get some data
config = load_config()
df = load_data('./data/data.tsv')
start_date, end_date = start_and_end_dates(df, config['start-date'], config['end-date'])


# variables
trade_groups = []
total_trades = 0
total_net_profit = 0


for group in config['trade-groups']:
    title = group['title']
    comment_filter = group['comment-filter']
    magic_filter = group['magic-filter']
    filtered_df = filter_dataframe(df, magic_filter, comment_filter, start_date, end_date)
    net_profit_sum = calculate_net_profit_sum(filtered_df)
    net_profit_sum_formatted = f"$ {'+' if net_profit_sum >= 0 else '-'}{net_profit_sum:,.2f}"
    
    data = {
        'Title': title, 
        '% P/L': "% +0.0",
        '$ P/L': net_profit_sum_formatted,
    }

    total_trades += len(filtered_df)
    total_net_profit += net_profit_sum

    trade_groups.append(data)

trade_groups_df = pd.DataFrame(trade_groups)

# Display the DataFrame
with st.container():
    st.dataframe(trade_groups_df, use_container_width=True)
