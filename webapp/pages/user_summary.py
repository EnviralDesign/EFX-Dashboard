import streamlit as st
from menu import menu_with_redirect
import pandas as pd
from utils import load_config, load_data, calculate_net_profit_sum, filter_dataframe, start_and_end_dates, format_float_as_currency_change, color_net_profit, calculate_positive_net_profit_sum, calculate_negative_net_profit_sum, calculate_profit_factor, format_profit_factor, color_profit_factor, color_neutral_row, calculate_net_swaps_sum, calculate_net_commissions_sum, format_float_as_currency, format_float_as_currency_change_alt, format_float_as_percent_change, format_float_as_percent_change_sans_percent, format_float_as_currency_change_no_prefix, calculate_max_dd, color_drawdown_factor
from datetime import datetime, timedelta


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()


# st.title("Overview")
# st.header(':violet[Overview]', divider='rainbow')
st.header('Summary', divider='rainbow')
st.write("Trade history for the given period clustered by trade group.")
# st.header(':orange[Overview]', divider='orange')
# st.header(':blue[Overview]', divider='grey')
# st.header('Overview', divider='grey')
# st.markdown(f"Account Overview. You are currently logged in with the role of {st.session_state.role}.")


# get some data
config = load_config()
initial_balance = config['initial-balance']
df = load_data(config['path-to-trade-history'])
start_date, end_date = start_and_end_dates(df, config['start-date'], config['end-date'])

# calculate the net profit up to the start date
filtered_pre_df = filter_dataframe(df, "", "", config["start-date"], start_date)
balance_right_before_start_date = initial_balance + calculate_net_profit_sum(filtered_pre_df)
fees_paid_up_to_start_date = calculate_net_swaps_sum(filtered_pre_df) + calculate_net_commissions_sum(filtered_pre_df)

# variables
trade_groups = []
total_trades = 0
total_net_profit = 0
total_fees_paid = 0

for group in config['trade-groups']:
    title = group['title']
    comment_filter = group['comment-filter']
    magic_filter = group['magic-filter']
    filtered_df = filter_dataframe(df, magic_filter, comment_filter, start_date, end_date)
    net_profit_sum = calculate_net_profit_sum(filtered_df)
    net_profit_sum_formatted = format_float_as_currency_change_no_prefix(net_profit_sum)

    profit_sum = calculate_positive_net_profit_sum(filtered_df)
    profit_sum_formatted = format_float_as_currency_change_no_prefix(profit_sum)
    loss_sum = calculate_negative_net_profit_sum(filtered_df)
    loss_sum_formatted = format_float_as_currency_change_no_prefix(loss_sum)
    profit_factor = calculate_profit_factor(profit_sum, loss_sum)
    profit_factor_formatted = format_profit_factor(profit_factor)
    swaps_sum = calculate_net_swaps_sum(filtered_df)
    swaps_sum_formatted = format_float_as_currency_change_no_prefix(swaps_sum)
    comission_sum = calculate_net_commissions_sum(filtered_df)
    comission_sum_formatted = format_float_as_currency_change_no_prefix(comission_sum)
    max_dd = calculate_max_dd(filtered_df, initial_balance)
    max_dd_formatted = format_float_as_currency_change_no_prefix(max_dd)

    pl_percent = (net_profit_sum / balance_right_before_start_date) * 100
    net_profit_percentage = format_float_as_currency_change_no_prefix(pl_percent)
    
    data = {
        'Title': title, 
        '% P/L': net_profit_percentage,
        '$ P/L': net_profit_sum_formatted,
        '$ Profit': profit_sum_formatted,
        '$ Loss': loss_sum_formatted,
        'PF': profit_factor_formatted,
        '% Max DD': max_dd_formatted,
        '# Trades': len(filtered_df),
        '# Longs': len(filtered_df[filtered_df['Type'] == 'OP_BUY']),
        '# Shorts': len(filtered_df[filtered_df['Type'] == 'OP_SELL']),
        '$ Swaps': swaps_sum_formatted,
        '$ Commissions': comission_sum_formatted,

        'P/L_Float': net_profit_sum,
    }

    total_trades += len(filtered_df)
    total_net_profit += net_profit_sum
    total_fees_paid += swaps_sum + comission_sum

    trade_groups.append(data)

# sort rows by P/L_Float highest to lowest
trade_groups = sorted(trade_groups, key=lambda x: x['P/L_Float'], reverse=True)

# drop the P/L_Float column
for group in trade_groups:
    group.pop('P/L_Float')

# calc the net profit sum for all trades in the filtered dataframe
balance_by_end_of_period = balance_right_before_start_date+total_net_profit
col1, col2, col3 = st.columns(3)
col1.metric("Balance", 
            format_float_as_currency(balance_by_end_of_period), 
            format_float_as_currency_change_alt(total_net_profit))
col2.metric("Max Drawdown", 
            "%", 
            "")
col3.metric("Fees",
            format_float_as_currency(total_fees_paid))

# Display the DataFrame
trade_groups_df = pd.DataFrame(trade_groups)
with st.container():

    # Apply styling to the DataFrame
    styled_df = (trade_groups_df.style
                .map(lambda val: color_net_profit(val), subset=['$ P/L'])
                .map(lambda val: color_net_profit(val), subset=['% P/L'])
                .map(lambda val: color_profit_factor(val), subset=['PF'])
                .map(lambda val: color_drawdown_factor(val), subset=['% Max DD'])
                # .map(lambda val: color_net_profit(val), subset=['Swaps'])
                # .map(lambda val: color_net_profit(val), subset=['Commissions'])
                .apply(color_neutral_row, args=('# Trades',), axis=1)
    )

    st.dataframe(styled_df, hide_index=True, use_container_width=True)
    # st.table(styled_df)
