


import pandas as pd
from classes.window import TimeWindow





def calc_pofo_pnl(pnl_data: pd.DataFrame, time_window: TimeWindow) -> float:

    #Filter the dataframe to the date range
    date_start = time_window.date_start
    date_end = time_window.date_end
    pofo_pnl = pnl_data[(pnl_data['Date'] >= date_start) & (pnl_data['Date'] <= date_end)]['PnL'].sum()

    return pofo_pnl





def calc_num_strats(pnl_data: pd.DataFrame, time_window: TimeWindow) -> float:

    #Filter the dataframe to the date range
    date_start = time_window.date_start
    date_end = time_window.date_end
    num_strats = len(pnl_data[(pnl_data['Date'] >= date_start) & (pnl_data['Date'] <= date_end)]['Strategy'].unique())

    return num_strats





def calc_strat_pnl(pnl_data: pd.DataFrame, time_window: TimeWindow, strategy: int) -> float:

    #Filter the dataframe to the date range
    date_start = time_window.date_start
    date_end = time_window.date_end
    strat_pnl = pnl_data[(pnl_data['Date'] >= date_start) & (pnl_data['Date'] <= date_end) & (pnl_data['Strategy'] == strategy)]['PnL'].sum()

    return strat_pnl





def calc_topN_pnl(pnl_data: pd.DataFrame, time_window: TimeWindow, topN: int) -> float:

    #Filter the dataframe to the date range
    date_start = time_window.date_start
    date_end = time_window.date_end

    period_pnl_by_strat = pnl_data[(pnl_data['Date'] >= date_start) & (pnl_data['Date'] <= date_end)].groupby('Strategy')['PnL'].sum().reset_index()
    period_total_pnl = period_pnl_by_strat['PnL'].sum()

    #If period pnl is positive, take the top N strategies by pnl and sum their pnl. If period pnl is negative, take the bottom N strategies by pnl and sum their pnl
    if period_total_pnl > 0:
        topN_pnl = period_pnl_by_strat.nlargest(topN, 'PnL')['PnL'].sum()
    else:
        topN_pnl = period_pnl_by_strat.nsmallest(topN, 'PnL')['PnL'].sum()
    
    return topN_pnl





def calc_avg_capital(merged_data: pd.DataFrame, time_window: TimeWindow) -> float:

    #Filter the dataframe to the date range
    date_start = time_window.date_start
    date_end = time_window.date_end
    avg_capital = merged_data[(merged_data['Date'] >= date_start) & (merged_data['Date'] <= date_end)]['Capital'].mean()

    return avg_capital






def satisfies_pnl_constraints(actual_pnl: float, needed_pnl: float, pnl_thresh_is_greater_than: bool) -> bool:

    if pnl_thresh_is_greater_than:
        return actual_pnl >= needed_pnl
    return actual_pnl <= needed_pnl










