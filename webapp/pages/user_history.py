import streamlit as st
import pandas as pd
import traceback
from menu import menu_with_redirect
from datetime import datetime, timedelta, date
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates, comment_and_magic_filter_strings, format_float_as_currency_change, format_float_as_currency, format_float_as_currency_change_alt, calculate_net_swaps_sum, calculate_net_commissions_sum, format_float_as_percent_change


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


# st.title("Account History")
st.header('History', divider='grey')
st.write("View and filter your raw account history.")


# get some data
config = load_config()
initial_balance = config['initial-balance']
df = load_data(config['path-to-trade-history'])
start_date, end_date = start_and_end_dates(df, config['start-date'], config['end-date'])
comment_filter, magic_filter = comment_and_magic_filter_strings()

# calculate the net profit up to the start date
filtered_pre_df = filter_dataframe(df, "", "", config["start-date"], start_date)
balance_right_before_start_date = initial_balance + calculate_net_profit_sum(filtered_pre_df)
fees_paid_up_to_start_date = calculate_net_swaps_sum(filtered_pre_df) + calculate_net_commissions_sum(filtered_pre_df)

# filter the dataframe down to what we care about
filtered_df = filter_dataframe(df, magic_filter, comment_filter, start_date, end_date)

# calc the net profit sum for all trades in the filtered dataframe
net_profit_sum = calculate_net_profit_sum(filtered_df)
fees_paid_sum = calculate_net_swaps_sum(filtered_df) + calculate_net_commissions_sum(filtered_df)
balance_by_end_of_period = balance_right_before_start_date+net_profit_sum
col1, col2, col3 = st.columns(3)
col1.metric("Balance", 
            format_float_as_currency(balance_by_end_of_period), 
            format_float_as_currency_change_alt(net_profit_sum))
col2.metric("Max Drawdown", 
            "%", 
            "")
col3.metric("Fees", 
            # format_float_as_currency_change_alt(fees_paid_up_to_start_date), 
            format_float_as_currency(fees_paid_sum), 
            # format_float_as_percent_change( (fees_paid_up_to_start_date/balance_by_end_of_period)*100 ))
            "")

# Convert 'MagicNumber' column to string type
filtered_df['MagicNumber'] = filtered_df['MagicNumber'].astype(str)

# Use st.container to make the table fully wide
with st.container():
    st.dataframe(filtered_df, use_container_width=True)

# write out some debug stuff
st.write("number of trades: ", len(filtered_df))
num_unique_magics = filtered_df['MagicNumber'].nunique()
unique_magics = " , ".join( list(map(str,filtered_df['MagicNumber'].unique().tolist())) )
st.write(f"{ num_unique_magics } unique magics: ", unique_magics)
num_unique_comments = filtered_df['Comment'].nunique()
unique_comments = " , ".join( list(map(str,filtered_df['Comment'].unique().tolist())) )
st.write(f"{ num_unique_comments } unique comments: ", unique_comments)
