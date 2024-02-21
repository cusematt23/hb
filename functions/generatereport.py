



from classes.window import TimeWindow
from functions.calc_pnl import calc_pofo_pnl, calc_avg_capital, satisfies_pnl_constraints, calc_num_strats, calc_topN_pnl
import pandas as pd



def generate_report(
    pnl_data: pd.DataFrame,
    capital_data: pd.DataFrame,
    window1_days: int,
    window1_months: int,
    window2_days: int,
    window2_months: int,
    pnl_thresh: float,
    pnl_thresh_is_percent: bool,
    pnl_thresh_is_greater_than: bool,
    conc_param: float,
    conc_param_is_percent: bool,
    overlapping: bool=False
    ) -> pd.DataFrame:

    #First create a daily time series of pnl and join it with the capital data
    pnl_by_date = pnl_data.groupby('Date')['PnL'].sum().reset_index()

    #Get a daily df with both pnl and capital
    daily_df = pd.merge_asof(left=pnl_by_date, right=capital_data, on='Date', direction='backward')
    daily_df.to_csv('merged_df.csv')
    
    #Check if the pnl_window_days and pnl_window_months are valid
    date_earliest = min(daily_df['Date'])
    date_latest = max(daily_df['Date'])
    combined_window_length = pd.DateOffset(days=window1_days+window2_days,months=window1_months+window2_months)
    print('combined_window_length: '+str(combined_window_length))

    if date_earliest + combined_window_length > date_latest:
        raise ValueError('The pnl_window_days and pnl_window_months are too large')
    
    #Instantiate the report_df
    report_df = pd.DataFrame({
            'window1Start': [],
            'window1End': [],
            'window1PnL': [],
            'window1Capital': [],
            'window1Return': [],
            'window1NumStrats': [],
            'window1topN':[],
            'window1topNPnL':[],
            'window1topNConc':[],
            'window2Start': [],
            'window2End': [],
            'window2PnL': [],
            'window2Capital': [],
            'window2Return': [],
            'window2NumStrats': [],
            'window2topN':[],
            'window2topNPnL':[],
            'window2topNConc':[]
        })
    


    
    #Now, need to loop over all the possible periods 
    #calculate the pnl and concentration if the period matches our constraints
    date_i = date_earliest
    while date_i <= date_latest - combined_window_length + pd.DateOffset(days=1):

        #First calculate our windows, which are inclusive
        window1= TimeWindow(date_start=date_i, date_end=date_i + pd.DateOffset(days=window1_days-1, months=window1_months))
        window2 = TimeWindow(date_start=window1.date_end+pd.DateOffset(days=1),date_end=window1.date_end+pd.DateOffset(days=window2_days, months=window2_months))

        #Calculate the average capital for each window in case our threshold is a % and we need return
        avg_capital_window1 = calc_avg_capital(daily_df, window1)
        avg_capital_window2 = calc_avg_capital(daily_df, window2)


        #Calculate the pnl we need in window1 to satisfy our threshold
        if pnl_thresh_is_percent:
            needed_pnl_window1 = avg_capital_window1 * pnl_thresh
        else:
            needed_pnl_window1 = pnl_thresh
        print('needed_pnl_window1: '+str(needed_pnl_window1))


        #Calculate the actual pnl for window1
        actual_pnl_window1 = calc_pofo_pnl(pnl_data, window1)
        print('actual_pnl_window1: '+str(actual_pnl_window1))


        #Check if the pnl for window1 satisfies our constraints
        #If it does, calculate the stats for the report
        if satisfies_pnl_constraints(actual_pnl_window1, needed_pnl_window1, pnl_thresh_is_greater_than):
            
            #If pnl constraint is satisfied, calculate the stats for the report
            window1_return = actual_pnl_window1 / avg_capital_window1

            #Calculate the total number of strategies in window1
            window1_num_strats = calc_num_strats(pnl_data, window1)

            #Calculate the topN pnl and concentration for window1
            if conc_param_is_percent:
                window1_topN = round(window1_num_strats * conc_param)
            else:
                window1_topN = conc_param
            window1_topN_pnl = calc_topN_pnl(pnl_data, window1, window1_topN)

            if actual_pnl_window1 != 0:
                window1_topN_percent = window1_topN_pnl / actual_pnl_window1
            else:
                window1_topN_percent = 0

            

            #Now, calculate our stats for the second window!!!
            actual_pnl_window2 = calc_pofo_pnl(pnl_data, window2)
            window2_return = actual_pnl_window2 / avg_capital_window2
            window2_num_strats = calc_num_strats(pnl_data, window2)
            if conc_param_is_percent:
                window2_topN = round(window2_num_strats * conc_param)
            else:
                window2_topN = conc_param
            
            window2_topN_pnl = calc_topN_pnl(pnl_data, window2, window2_topN)
            if actual_pnl_window2 != 0:
                window2_topN_percent = window2_topN_pnl / actual_pnl_window2
            else:
                window2_topN_percent = 0

            report_row_to_add = pd.DataFrame({
                'window1Start': [window1.date_start],
                'window1End': [window1.date_end],
                'window1PnL': [actual_pnl_window1],
                'window1Capital': [avg_capital_window1],
                'window1Return': [window1_return],
                'window1NumStrats': [window1_num_strats],
                'window1topN':[window1_topN],
                'window1topNPnL':[window1_topN_pnl],
                'window1topNConc':[window1_topN_percent],
                'window2Start': [window2.date_start],
                'window2End': [window2.date_end],
                'window2PnL': [actual_pnl_window2],
                'window2Capital': [avg_capital_window2],
                'window2Return': [window2_return],
                'window2NumStrats': [window2_num_strats],
                'window2topN':[window2_topN],
                'window2topNPnL':[window2_topN_pnl],
                'window2topNConc':[window2_topN_percent]
            })

            #Add row to report_df
            report_df = pd.concat([report_df, report_row_to_add], ignore_index=True)

            #Determine what date to iterate to next
            if overlapping:
                date_i += pd.DateOffset(days=1)
            else:
                date_i += pd.DateOffset(days=window1_days,months=window1_months)
        else:

            #If pnl constraint is not satisfied, move to the next date
            print('PnL constraint not satisfied\n')
            date_i += pd.DateOffset(days=1)


    report_df.to_csv('report_df.csv', index=False)
    
    
    
    


    return report_df


