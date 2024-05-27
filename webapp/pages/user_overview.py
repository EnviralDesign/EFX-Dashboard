import streamlit as st
from menu import menu_with_redirect
import pandas as pd
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates, format_float_as_currency_change, color_net_profit, calculate_positive_net_profit_sum, calculate_negative_net_profit_sum, calculate_profit_factor, format_profit_factor
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
    net_profit_sum_formatted = format_float_as_currency_change(net_profit_sum)

    profit_sum = calculate_positive_net_profit_sum(filtered_df)
    profit_sum_formatted = format_float_as_currency_change(profit_sum)
    loss_sum = calculate_negative_net_profit_sum(filtered_df)
    loss_sum_formatted = format_float_as_currency_change(loss_sum)
    profit_factor = calculate_profit_factor(profit_sum, loss_sum)
    profit_factor_formatted = format_profit_factor(profit_factor)
    
    data = {
        'Title': title, 
        '% P/L': "% +0.0",
        '$ P/L': net_profit_sum_formatted,
        'PF': profit_factor_formatted,
        '$ Profit': profit_sum_formatted,
        '$ Loss': loss_sum_formatted,
        'Trades': len(filtered_df),
        'Longs': len(filtered_df[filtered_df['Type'] == 'OP_BUY']),
        'Shorts': len(filtered_df[filtered_df['Type'] == 'OP_SELL']),

        'P/L_Float': net_profit_sum,
    }

    total_trades += len(filtered_df)
    total_net_profit += net_profit_sum

    trade_groups.append(data)

# sort rows by P/L_Float highest to lowest
trade_groups = sorted(trade_groups, key=lambda x: x['P/L_Float'], reverse=True)

# drop the P/L_Float column
for group in trade_groups:
    group.pop('P/L_Float')


trade_groups_df = pd.DataFrame(trade_groups)

# Display the DataFrame
with st.container():
    # st.dataframe(trade_groups_df, hide_index=True, use_container_width=True)


    # Apply styling to the DataFrame
    # styled_df = trade_groups_df.style.applymap(lambda val: 'color: red' if '-' in val else 'color: green')
    styled_df = trade_groups_df.style.map(lambda val: color_net_profit(val), subset=['$ P/L'])
    # trade_groups_df.styler.applymap

    # Convert the styled DataFrame to HTML
    # html_df = styled_df.render()
    # st.write(html_df, unsafe_allow_html=True)

    st.table(styled_df)
