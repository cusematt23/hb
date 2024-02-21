



import pandas as pd
import os
from functions.generatereport import generate_report




if __name__ == "__main__":

    #In our main function, instantiate the variables we need to call the generate_report function

    #Read in the pnl data
    pnl_file_name = 'pnl_ts_data.xlsx'
    pnl_file_path = os.path.join(os.getcwd(), pnl_file_name)
    pnl_data = pd.read_excel(pnl_file_path)

    #Read in the capital data
    capital_file_name = 'capital_ts_data.xlsx'
    capital_file_path = os.path.join(os.getcwd(), capital_file_name)
    capital_data = pd.read_excel(capital_file_path)
    
    #Set the pnl lookback and lookforward windows for periods you want to capture
    #month and day are split since months have variable number of days and no other way to do it
    #Program will sum days and months to get the total window length
    #Ended up deciding to call the windows just window1 and window2, otherwise the variable naming gets too confusing
    window1_days = 0
    window1_months = 1
    window2_days = 0
    window2_months = 1

    #Set the parameters for when to capture data based on measureables in the pnl_window
    #If you set pnl_thresh_is_percent to True, program ignores pnl_thresh_abs and vice versa
    #For example, if you want greater than a 5% return, set pnl_thresh_is_percent to True and pnl_thresh_percent to .05
    #pnl_thresh_is_greater_than is a boolean that determines if you want to capture data when the pnl is greater than or less than the threshold
    pnl_thresh_abs = 0
    pnl_thresh_percent = 0
    pnl_thresh_is_percent = True
    #PnL greater than or less than our threshold
    pnl_thresh_is_greater_than = True
    if pnl_thresh_is_percent:
        pnl_thresh = pnl_thresh_percent
    else:
        pnl_thresh = pnl_thresh_abs

    #Set the parameters for calculating portfolio pnl concentration
    #If you set conc_param_is_percent to True, program ignores strat_count_top_N and vice versa
    #For example if you want the pnl of the top N strategies, set conc_param_is_percent to False and strat_count_top_N to 5
    #If you want the pnl of the top 20% of strategies, set conc_param_is_percent to True and topN_strat_percentile to .2
    strat_count_top_N = 5
    topN_strat_percentile = .2
    conc_param_is_percent = False
    if conc_param_is_percent:
        conc_param = topN_strat_percentile
    else:
        conc_param = strat_count_top_N


    #overlapping variable is a boolean that determines if the windows overlap or not
    #if you dont want any overlap in window1 periods, set overlapping to False
    overlapping = False


    report = generate_report(
        pnl_data=pnl_data,
        capital_data=capital_data,
        window1_days=window1_days,
        window1_months=window1_months,
        window2_days=window2_days,
        window2_months=window2_months,
        pnl_thresh=pnl_thresh,
        pnl_thresh_is_percent=pnl_thresh_is_percent,
        pnl_thresh_is_greater_than=pnl_thresh_is_greater_than,
        conc_param=conc_param,
        conc_param_is_percent=conc_param_is_percent,
        overlapping=overlapping
    )

    print(report)

    