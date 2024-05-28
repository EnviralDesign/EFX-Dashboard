import streamlit as st
from menu import menu_with_redirect
import pandas as pd
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates, format_float_as_currency_change, color_net_profit, calculate_positive_net_profit_sum, calculate_negative_net_profit_sum, calculate_profit_factor, format_profit_factor, color_profit_factor, color_neutral_row, calculate_net_swaps_sum, calculate_net_commissions_sum, format_float_as_currency, format_float_as_currency_change_alt, load_header, format_float_as_percent_change, format_float_as_percent_change_sans_percent
from datetime import datetime, timedelta


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


st.header('Live', divider='rainbow')
st.write("Live stats on the acccount.")


# get some data
config = load_config()
initial_balance = config['initial-balance']
header_stats = load_header('./data/data.tsv')

# calc the net profit sum for all trades in the filtered dataframe
col1, col2, col3 = st.columns(3)
col1.metric("Balance", format_float_as_currency(header_stats['account_balance']))

col2.metric("Equity", format_float_as_currency(header_stats['account_equity']))

dd_in_currency = header_stats['account_balance'] - header_stats['account_equity']
dd_in_percentage = format_float_as_percent_change((dd_in_currency / header_stats['account_balance'])*-100)
col3.metric("Drawdown %", dd_in_percentage )
