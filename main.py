import pandas as pd
from combine import *
from get_njcaa_game_stats import getNjcaaGamelogs
from get_njcaa_rosters import getNjcaaRosters

if __name__ == "__main__":
    season = 2023
    getNjcaaRosters(season)
    mergeRostersDivOne()
    mergeRostersDivTwo()
    mergeRostersDivThree()
    
    print('\n\n\n\n\n\n\nDownloading NJCAA D1 stats.\n\n')
    roster_df = pd.read_csv('rosters/div1_rosters.csv')
    roster_df = roster_df[roster_df['team_season']==season]
    getNjcaaGamelogs(roster_df)
    
    print('\n\n\n\n\n\n\nDownloading NJCAA D2 stats.\n\n')
    roster_df = pd.read_csv('rosters/div2_rosters.csv')
    roster_df = roster_df[roster_df['team_season']==season]
    getNjcaaGamelogs(roster_df)

    print('\n\n\n\n\n\n\nDownloading NJCAA D3 stats.\n\n')
    roster_df = pd.read_csv('rosters/div3_rosters.csv')
    roster_df = roster_df[roster_df['team_season']==season]
    getNjcaaGamelogs(roster_df)

    mergeBattingStats()
    mergePitchingStats()
    mergeFieldingStats()