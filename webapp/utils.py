import pandas as pd
import io
import os
import json

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


def load_config():
    """Load the JSON configuration from the config file."""
    config_path = os.path.join('data', 'config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)
    """Format the value as currency with two decimal places."""
    return f"${val:,.2f}"

def color_net_profit(val, pos_rgb=(0, 255, 128), neg_rgb=(255, 0, 128)):
    """Apply color formatting based on the value."""
    pos_color = f'rgb{pos_rgb}'
    neg_color = f'rgb{neg_rgb}'
    color = neg_color if val < 0 else pos_color
    return f'color: {color};'
