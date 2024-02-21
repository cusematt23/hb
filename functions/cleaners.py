import numpy as np
import pandas as pd


def clean_time_series(time_series: pd.DataFrame, min_strategy_threshold: int = 5) -> pd.DataFrame:
    
    #For days with very little data, roll that pnl into the next day
    #First, create a primary key for unique row identification
    primary_key_series = time_series['Date'].astype(str) + '_' + time_series['Strategy'].astype(str)


    unique_date_series = time_series['Date'].unique()

    T = unique_date_series.shape[0]

    dates_to_drop=[]

    for i in range(T):
        date_i = unique_date_series[i]
        date_df = time_series.groupby('Date').get_group(date_i)
        if date_df.shape[0] < min_strategy_threshold:
            print(date_df)
            print('\n')
            dates_to_drop.append(date_i)
            for strat in date_df['Strategy']:
                print('Strat: ' + str(strat))
                print('Date: ' + str(unique_date_series.astype(str)[i]))
                needed_pk = str(unique_date_series.astype(str)[i+1]) + '_' + str(strat)
                print('Needed PK: ' + needed_pk )
                index_needed_pk = primary_key_series[primary_key_series == str(unique_date_series.astype(str)[i+1]) + '_' + str(strat)].index[0] 
                print('Index of Needed PK: ' + str(index_needed_pk))
                print(time_series.loc[index_needed_pk])
                print('\n'*3)

            
            

    print(dates_to_drop)

        


    return time_series