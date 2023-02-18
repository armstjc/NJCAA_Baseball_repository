import pandas as pd
import numpy as np
import datetime

#####################################################################################################################################################################################################################
## League stats
##
#####################################################################################################################################################################################################################

def generate_leauge_batting_stats(save=False):
    main_df = pd.DataFrame()
    s_df = pd.DataFrame()

    for season in range(2013,2024):
        s_df = pd.read_parquet(f'game_stats/player/batting_game_stats/parquet/{season}_batting.parquet')
        main_df = pd.concat([main_df,s_df], ignore_index=True)
        
def main():
    print('starting up')

if __name__ == "__main__":
    main()