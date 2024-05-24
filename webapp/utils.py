import pandas as pd
import io

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        print("File encoding: utf-8")
        tsv_string = file.read()
        # print("Raw content of the TSV file:")
        # print(raw_content[:500])  # Print the first 500 characters for inspection
        # tsv_string = file.read()
    
    # Split the string by the custom header separator and take the second part
    # print(tsv_string[:500])
    #split_tsv = tsv_string.split("|+|")
    split_tsv = tsv_string.split("|+|")
    
    tsv_data = split_tsv[1]
    
    # Read the data into a pandas DataFrame
    # BUG IS HERE
    data = pd.read_csv(io.StringIO(tsv_data), sep='\s+')
    
    # Convert 'ServerCloseTime' and 'ServerOpenTime' to datetime
    data['ServerCloseTime'] = pd.to_datetime(data['ServerCloseTime'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    data['ServerOpenTime'] = pd.to_datetime(data['ServerOpenTime'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    
    # Convert numeric columns to appropriate data types
    data['NetProfit'] = pd.to_numeric(data['NetProfit'], errors='coerce')
    data['Profit'] = pd.to_numeric(data['Profit'], errors='coerce')
    data['Swap'] = pd.to_numeric(data['Swap'], errors='coerce')
    
    return data

def style_dataframe(df):
    """Apply styling and formatting to the DataFrame."""
    # Format the NetProfit column as currency
    df['NetProfit'] = df['NetProfit'].apply(format_currency)
    
    # Apply color formatting to the NetProfit column
    styled_df = df.style.applymap(
        lambda val: color_net_profit(float(val.replace('$', '').replace(',', ''))), subset=['NetProfit']
    )
    
    return styled_df

def format_currency(val):
    """Format the value as currency with two decimal places."""
    return f"${val:,.2f}"

def color_net_profit(val, pos_rgb=(0, 255, 128), neg_rgb=(255, 0, 128)):
    """Apply color formatting based on the value."""
    pos_color = f'rgb{pos_rgb}'
    neg_color = f'rgb{neg_rgb}'
    color = neg_color if val < 0 else pos_color
    return f'color: {color};'
