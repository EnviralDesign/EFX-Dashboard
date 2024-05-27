import streamlit as st
import pandas as pd
import traceback
from menu import menu_with_redirect
from datetime import datetime, timedelta, date
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates, comment_and_magic_filter_strings


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


st.title("Account History")
# st.markdown(f"Raw ! You are currently logged in with the role of {st.session_state.role}.")


# get some data
config = load_config()
df = load_data('./data/data.tsv')
start_date, end_date = start_and_end_dates(df, config['start-date'], config['end-date'])
comment_filter, magic_filter = comment_and_magic_filter_strings()

filtered_df = filter_dataframe(df, magic_filter, comment_filter, start_date, end_date)

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
