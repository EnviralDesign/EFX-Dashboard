import streamlit as st
import pandas as pd
import io
import os
import json
import re

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # print("File encoding: utf-8")
        tsv_string = file.read()
    
    # Split the string by the custom header separator and take the second part
    split_tsv = tsv_string.split("|+|")
    
    tsv_data = split_tsv[1]
    
    # Read the data into a pandas DataFrame
    data = pd.read_csv(io.StringIO(tsv_data), sep='\t')

    data['Comment'] = data['Comment'].fillna('')  # Fill NaN values with empty string

    # Convert 'ServerCloseTime' and 'ServerOpenTime' to datetime
    data['ServerCloseTime'] = pd.to_datetime(data['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S')
    data['ServerOpenTime'] = pd.to_datetime(data['ServerOpenTime'], format='%d-%m-%Y %H:%M:%S')
    
    # Convert numeric columns to appropriate data types
    data['NetProfit'] = pd.to_numeric(data['NetProfit'])
    data['Profit'] = pd.to_numeric(data['Profit'])
    data['Swap'] = pd.to_numeric(data['Swap'])
    
    return data

def start_and_end_dates(df, optional_start_time='', optional_end_time=''):
    # Extract the date range
    min_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S').min()
    max_date = pd.to_datetime(df['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S').max()

    # If optional start and end times are provided and not blank, use them to clamp the start and end times
    if optional_start_time != '':
        optional_start_time = pd.to_datetime(optional_start_time, format='%d-%m-%Y %H:%M:%S')
        min_date = max(min_date, optional_start_time)
    if optional_end_time != '':
        optional_end_time = pd.to_datetime(optional_end_time, format='%d-%m-%Y %H:%M:%S')
        max_date = min(max_date, optional_end_time)

    # Initialize session state for start_date and end_date if not already set
    st.session_state.start_date = min_date
    st.session_state.end_date = max_date

    # UI for selecting the date range
    col1, col2 = st.columns([1, 1])
    with col1:
        start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=st.session_state.start_date)
    with col2:
        end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=st.session_state.end_date)

    # Adjust end_date to include the entire day
    end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    return start_date, end_date

def parse_magic_number_pattern(pattern):
    """ Convert a pattern like '1000-1004' or '100,101,103' into a regex pattern for exact matches. """
    if not pattern:
        return None  # Return None if the pattern is empty
    ranges = []
    items = pattern.split(',')
    for item in items:
        if '-' in item:
            start, end = item.split('-')
            range_regex = '|'.join(str(x) for x in range(int(start), int(end)+1))
            ranges.append(range_regex)
        else:
            ranges.append(r'\b' + re.escape(item) + r'\b')
    return '|'.join(ranges)

def wildcard_to_regex(pattern):
    """ Convert multiple wildcard patterns to a regex pattern, ensure non-empty matches if not explicitly wild. """
    if not pattern:
        return ".*"  # Match everything if comment is empty
    patterns = pattern.split(';')  # Split multiple patterns using ';'
    regex_patterns = []
    for pat in patterns:
        if pat:  # Ensure we do not create regex for empty patterns
            pat = re.escape(pat)
            pat = pat.replace(r'\*', '.*')
            pat = pat.replace(r'\?', '.')
            regex_patterns.append(f"^{pat}$")
    if regex_patterns:
        return '|'.join(regex_patterns)
    return "$^"  # This regex matches nothing, used if all patterns are empty

def filter_dataframe(df, magic_filter="", comment_filter="", start_time="", end_time=""):     
    """Filter the DataFrame based on magic number, comment filters, and time window."""       
    magic_regex = parse_magic_number_pattern(magic_filter) if magic_filter else None
    comment_regex = wildcard_to_regex(comment_filter)

    filtered_df = df.copy()

    if magic_regex:
        filtered_df = filtered_df[ filtered_df['MagicNumber'].astype(str).str.match(magic_regex) ]
    if comment_regex:
        filtered_df = filtered_df[ filtered_df['Comment'].str.match(comment_regex) ]
    if start_time:
        filtered_df = filtered_df[ filtered_df['ServerOpenTime'] >= pd.to_datetime(start_time) ]
    if end_time:
        filtered_df = filtered_df[ filtered_df['ServerOpenTime'] <= pd.to_datetime(end_time) ]

    return filtered_df

def load_config():
    """Load the JSON configuration from the config file."""
    config_path = os.path.join('data', 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        config['start-date'] = pd.to_datetime(config['start-date'])
        config['end-date'] = pd.to_datetime(config['end-date'])
        return config

def calculate_net_profit_sum(filtered_df):
    """Calculate the sum of net profits for a given trade group."""
    return filtered_df['NetProfit'].sum()

def color_net_profit(val, pos_rgb=(0, 255, 128), neg_rgb=(255, 0, 128)):
    """Apply color formatting based on the value."""
    pos_color = f'rgb{pos_rgb}'
    neg_color = f'rgb{neg_rgb}'
    color = neg_color if val < 0 else pos_color
    return f'color: {color};'
