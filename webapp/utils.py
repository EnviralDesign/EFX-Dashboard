import streamlit as st
import pandas as pd
import io
import os
import json
import re

pos_rgb=(0, 230, 128)
neg_rgb=(255, 0, 82)

color_lookup = [(255,7,82),(254,23,83),(253,36,83),(251,46,84),(250,53,85),(249,60,86),(247,66,86),(246,72,87),(244,77,88),(243,82,88),(241,86,89),(240,90,90),(238,95,91),(237,99,91),(235,102,92),(234,106,93),(232,110,93),(230,113,94),(229,117,95),(227,120,96),(225,123,96),(223,126,97),(221,129,98),(219,132,98),(217,135,99),(215,138,100),(213,141,101),(211,144,101),(209,147,102),(207,149,103),(204,152,103),(202,155,104),(199,158,105),(197,160,106),(194,163,106),(192,165,107),(189,168,108),(186,170,109),(183,173,109),(181,175,110),(177,178,111),(174,180,112),(171,183,112),(168,185,113),(164,187,114),(161,190,115),(157,192,115),(153,194,116),(149,197,117),(144,199,118),(140,201,118),(135,204,119),(130,206,120),(125,208,120),(119,210,121),(113,213,122),(106,215,123),(99,217,123),(91,219,124),(82,221,125),(71,224,126),(58,226,126),(39,228,127),(13,230,128)]

def load_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # print("File encoding: utf-8")
        tsv_string = file.read()
    
    # Split the string by the custom header separator and take the first part
    split_tsv = tsv_string.split("|+|")
    
    tsv_header = split_tsv[0]

    pairs = [x for x in tsv_header.split("|") if x != '']

    kv = [x.split(":") for x in pairs]

    d = {}
    for k, v in kv:
        d[k] = v
    
    d['account_equity'] = float(d['account_equity'])
    d['account_balance'] = float(d['account_balance'])
    
    return d

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

def comment_and_magic_filter_strings():
    # UI for entering the filters
    col1, col2 = st.columns([1, 1])
    with col1:
        comment_filter = st.text_input("Enter comment filter")
    with col2:
        magic_filter = st.text_input("Enter magic filter")

    return comment_filter, magic_filter

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

def calculate_net_swaps_sum(filtered_df):
    """Calculate the sum of swaps for a given trade group."""
    return filtered_df['Swap'].sum()

def calculate_net_commissions_sum(filtered_df):
    """Calculate the sum of commissions for a given trade group."""
    return filtered_df['Commission'].sum()

def calculate_positive_net_profit_sum(filtered_df):
    """Calculate the sum of positive net profits for a given trade group."""
    return filtered_df['NetProfit'].clip(lower=0).sum()

def calculate_negative_net_profit_sum(filtered_df):
    """Calculate the sum of negative net profits for a given trade group."""
    return filtered_df['NetProfit'].clip(upper=0).sum()

def calculate_profit_factor(profit_sum, loss_sum):
    """Calculate the profit factor."""
    return -profit_sum / loss_sum if loss_sum != 0 else 99999

def format_profit_factor(val):
    """Format the profit factor."""
    # format the profit factor with 2 decimal places. if the value is 99999, then return the symbol for infinity
    return '∞' if val == 99999 else f'{val:.2f}'

def color_net_profit(val):
    """Apply color formatting based on the value."""
    # pos_rgb=(0, 230, 128)
    # neg_rgb=(255, 0, 82)
    pos_color = f'rgb{pos_rgb}'
    neg_color = f'rgb{neg_rgb}'

    # Remove the dollar sign and comma, then convert to float
    val_float = float(val.replace('$', '').replace(',', ''))

    if val_float < 0:
        color = neg_color
    elif val_float > 0:
        color = pos_color
    else:
        return ''
    return f'color: {color};'

def color_profit_factor(val):
    # using the color lookup which has a gradeitn of 64 colors, we can color the profit factor
    # if the profit factor is the infinity symbol, automatically consider that the last color in the gradient
    # otherwise, values will map from 0-3 of the profit factor to 0-63 of the gradient
    if val == '∞':
        color = f'color: rgb{color_lookup[-1]};'
        # print(color)
        return color
    else:
        val = float(val)
        val = min(val, 3)
        color_index = int((val/3) * 63)
        return f'color: rgb{color_lookup[color_index]};'

def format_float_as_currency_change(value):
    sign = '+' if value > 0 else '-' if value < 0 else ''
    return f"$ {sign}{abs(value):,.2f}"

def format_float_as_currency_change_no_prefix(value):
    sign = '+' if value > 0 else '-' if value < 0 else ''
    return f"{sign}{abs(value):,.2f}"

def format_float_as_currency_change_alt(value):
    sign = '+' if value > 0 else '-' if value < 0 else ''
    return f"{sign} ${abs(value):,.2f}"

def format_float_as_percent_change(value):
    sign = '+' if value > 0 else '-' if value < 0 else ''
    return f"{sign}{abs(value):,.2f}%"

def format_float_as_percent_change_sans_percent(value):
    sign = '+' if value > 0 else '-' if value < 0 else ''
    return f"{sign}{abs(value):,.2f}"

def format_float_as_currency(value):
    return f"$ {value:,.2f}"

def color_neutral_row(row, column_name):
    color = 'color: dimgray' if row[column_name] == 0 else ''
    return [color] * len(row)