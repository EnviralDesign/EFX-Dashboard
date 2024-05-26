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

    # Convert 'ServerCloseTime' and 'ServerOpenTime' to datetime
    data['ServerCloseTime'] = pd.to_datetime(data['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S')
    data['ServerOpenTime'] = pd.to_datetime(data['ServerOpenTime'], format='%d-%m-%Y %H:%M:%S')
    
    # Convert numeric columns to appropriate data types
    data['NetProfit'] = pd.to_numeric(data['NetProfit'])
    data['Profit'] = pd.to_numeric(data['Profit'])
    data['Swap'] = pd.to_numeric(data['Swap'])
    
    return data

def format_currency(val):
    pass
    return val

def style_dataframe(df):
    """Apply styling and formatting to the DataFrame."""

    styled_df = df.copy()

    # Format the NetProfit column as currency
    if(False):
        styled_df['NetProfit'] = styled_df['NetProfit'].apply(format_currency)
    
    # Apply color formatting to the NetProfit column
    if(False):
        styled_df = df.style.map(
            lambda val: color_net_profit(float(val.replace('$', '').replace(',', ''))), subset=['NetProfit']
        )
    return styled_df


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

def filter_dataframe(df, magic_filter, comment_filter):
    """Filter the DataFrame based on magic number and comment filters."""
    magic_regex = parse_magic_number_pattern(magic_filter) if magic_filter else None
    comment_regex = wildcard_to_regex(comment_filter)

    filtered_df = df.copy()

    if magic_regex:
        filtered_df = filtered_df[filtered_df['MagicNumber'].astype(str).str.match(magic_regex)]

    if comment_regex:
        filtered_df = filtered_df[filtered_df['Comment'].str.match(comment_regex)]

    return filtered_df

def load_config():
    """Load the JSON configuration from the config file."""
    config_path = os.path.join('data', 'config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def calculate_net_profit_sum(df, comment_filter, magic_filter):
    """Calculate the sum of net profits for a given trade group."""
    filtered_df = df[(df['Comment'].str.contains(comment_filter)) & (df['MagicNumber'] == magic_filter)]
    return filtered_df['NetProfit'].sum()

def color_net_profit(val, pos_rgb=(0, 255, 128), neg_rgb=(255, 0, 128)):
    """Apply color formatting based on the value."""
    pos_color = f'rgb{pos_rgb}'
    neg_color = f'rgb{neg_rgb}'
    color = neg_color if val < 0 else pos_color
    return f'color: {color};'
