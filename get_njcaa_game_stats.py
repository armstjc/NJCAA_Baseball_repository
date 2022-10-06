from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode
import re

def getNjcaaD1BattingGamelogs(webdriverPath="./chromedriver_mac64_m1"):
	teams_df = pd.read_csv('rosters/div1_rosters.csv')
	teams_df = teams_df[teams_df['team_season'] != 2023]
	school_name = teams_df['team_name'].tolist()
	school_njcaa_season = teams_df['team_njcaa_season'].tolist()
	school_njcaa_division = teams_df['team_njcaa_division'].tolist()
	school_team_id = teams_df['team_id'].tolist()
	school_season = teams_df['team_season'].tolist()
	#player_numbers = teams_df['No.'].tolist()
	player_names = teams_df['Name'].tolist()
	#player_positions = teams_df['Position'].tolist()
	player_ids = teams_df['PlayerID'].tolist()
	player_urls = teams_df['PlayerURL'].tolist()

	player_count = len(player_urls)
	driver = webdriver.Chrome(
		executable_path=webdriverPath)
	count = 8226
	for i in tqdm(range(count,player_count)):
		count += 1
		print(f'{count}/{player_count}')
		## Ensure that we have a brand new DataFame in each iteration.
		gamelog_batting_df = pd.DataFrame()
		gamelog_ex_batting_df = pd.DataFrame()
		gamelog_pitching_df = pd.DataFrame()
		gamelog_fielding_df = pd.DataFrame()
		
		# 	# Info related to the player
		# 	team_name = school_name[i]

		#This data will be in every row, for every DataFrame used in this
		# function.
		game_season = school_season[i]
		game_njcaa_season = school_njcaa_season[i]
		game_njcaa_division = school_njcaa_division[i]		
		game_team = school_name[i]
		game_team_id = school_team_id[i]		
		game_player_id = player_ids[i]
		game_player_name = player_names[i]


		# Set everything to null before getting any data for this table.
		game_date = None
		game_opponent = None
		game_score = None
		game_loc = None

		## Hitting Stats
		game_batting_AB = None # At-Bats
		game_batting_R = None # Runs
		game_batting_H = None # Hits
		game_batting_2B = None # 2 base hits
		game_batting_3B = None # 3 base hits
		game_batting_HR = None # Home Runs
		game_batting_RBI = None # Runs Batted In
		game_batting_BB = None # Base on Balls (walks)
		game_batting_K = None # Strikeout
		game_batting_SB = None # Stolen Bases
		game_batting_CS = None # Caught Stealing
		## Extended Hitting Stats
		game_batting_HBP = None # Hit By Pitch
		game_batting_SF = None # Sac. Fly
		game_batting_SH = None # Sac. Hit
		game_batting_TB = None # Total Bases
		game_batting_XBH = None # eXtra Base Hit
		game_batting_HDP = None # TODO: Figure out what on earth this stat is for.
		game_batting_GO = None # Ground Out
		game_batting_FO = None # Fly Out
		game_batting_GO_FO = None # Ground Out/Fly Out ratio
		game_batting_PA = None # Plate Apperances (For some reason, this is in Extedned Hitting).
		# Pitching
		game_pitching_GS = None # Games Started (pitching)
		game_pitching_W = None # Wins (pitching)
		game_pitching_L = None # Losses (pitching)
		game_pitching_SV = None # Saves
		game_pitching_IP = None # Innings Pitched
		game_pitching_H = None # Hits allowed
		game_pitching_R = None # Runs allowed
		game_pitching_ER = None # Earned Runs allowed
		game_pitching_ERA = None # Earned Run Average
		game_pitching_BB = None # Base on Balls (walks) allowed
		game_pitching_K = None # Strikeouts (pitching)
		game_pitching_HR = None # Home Runs allowed
		## Fielding
		game_fielding_TC = None # Total fielding Chances
		game_fielding_PO = None # Put Outs
		game_fielding_A = None # fielding Assists
		game_fielding_E = None # fielding Errors
		game_fielding_FPCT = None # Fielding Pct%
		game_fielding_DP = None # Double Plays
		game_fielding_SBA = None # Stolen Bases Attempted against a catcher
		game_fielding_RCS = None # TODO: Figure out what on earth this stat is for.
		game_fielding_RCS_PCT = None # TODO: Figure out what on earth this stat is for.
		game_fielding_PB = None # Passed Balls
		game_fielding_CI = None # Catcher's Interference

		url = player_urls[i]
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, features='lxml')
		# soup.find_all('table')[2] = Batting
		# soup.find_all('table')[3] = Extended Hitting
		# soup.find_all('table')[4] = Pitching
		# soup.find_all('table')[5] = Fielding
		batting_table = soup.find_all('table')[2]
		#print(table)
		# cols = []

		# for j in table.tr.find_all('th'):
		# 		cols.append(j.text.strip())
		# print(cols)

		for k in batting_table.tbody.find_all('tr'):
			row = k.find_all('td')
			if len(row) < 2:
				pass
			else:
				game_date = row[0].text.strip()
				game_opponent = row[1].text.strip()
				game_opponent = str(game_opponent).replace('                       ',' ')
				game_score_raw = str(row[2].text.strip()).split()
				try:
					game_result = str(game_score_raw[0]).replace(',','')
				except:
					game_result = None
				try:
					game_score = str(game_score_raw[1]).replace(',','')
				except:
					game_score = None
				try:
					game_team_score = str(game_score.split('-',-1)[0])
				except:
					game_team_score = None
				try:
					game_opp_score = str(game_score.split('-',-1)[0])
				except:
					game_opp_score = None
				game_batting_AB = str(row[3].text.strip()).replace('-','')
				game_batting_R = str(row[4].text.strip()).replace('-','')
				game_batting_H = str(row[5].text.strip()).replace('-','')
				game_batting_2B = str(row[6].text.strip()).replace('-','')
				game_batting_3B = str(row[7].text.strip()).replace('-','')
				game_batting_HR = str(row[8].text.strip()).replace('-','')
				game_batting_RBI = str(row[9].text.strip()).replace('-','')
				game_batting_BB = str(row[10].text.strip()).replace('-','')
				game_batting_K = str(row[11].text.strip()).replace('-','')
				game_batting_SB = str(row[12].text.strip()).replace('-','')
				game_batting_CS = str(row[13].text.strip()).replace('-','')

				if "at " in game_opponent:
					#print('away')
					game_loc = 'away'
					game_opponent = game_opponent.replace('at ','')
				else:
					game_loc = 'home'

				gamelog_batting_df = gamelog_batting_df.append({
					'date':game_date,'location':game_loc,'opponent':game_opponent,
					'result':game_result,'score':game_score,
					'team_score':game_team_score,'opp_score':game_opp_score,
					'AB':game_batting_AB,'R':game_batting_R,'H':game_batting_H,
					'2B':game_batting_2B,'3B':game_batting_3B,
					'HR':game_batting_HR,'RBI':game_batting_RBI,
					'BB':game_batting_BB,'K':game_batting_K,'SB':game_batting_SB,
					'CS':game_batting_CS},ignore_index=True)

		#print(gamelog_batting_df)
		# soup.find_all('table')[3] = Extended Hitting
		ex_batting_table = soup.find_all('table')[3]
		for k in ex_batting_table.tbody.find_all('tr'):
			row = k.find_all('td')
			if len(row) < 2:
				pass
			else:
				#print(row)
				game_date = row[0].text.strip()
				game_opponent = row[1].text.strip()
				game_opponent = str(game_opponent).replace('                       ',' ')
				game_score_raw = str(row[2].text.strip()).split()
				try:
					game_result = str(game_score_raw[0]).replace(',','')
				except:
					game_result = None
				try:
					game_score = str(game_score_raw[1]).replace(',','')
				except:
					game_score = None
				try:
					game_team_score = str(game_score.split('-',-1)[0])
				except:
					game_team_score = None
				try:
					game_opp_score = str(game_score.split('-',-1)[0])
				except:
					game_opp_score = None
				game_batting_HBP = str(row[3].text.strip()).replace('-','')
				game_batting_SF = str(row[4].text.strip()).replace('-','')
				game_batting_SH = str(row[5].text.strip()).replace('-','')
				game_batting_TB = str(row[6].text.strip()).replace('-','')
				game_batting_XBH = str(row[7].text.strip()).replace('-','')
				game_batting_HDP = str(row[8].text.strip()).replace('-','')
				game_batting_GO = str(row[9].text.strip()).replace('-','')
				game_batting_FO = str(row[10].text.strip()).replace('-','')
				game_batting_GO_FO = str(row[11].text.strip()).replace('-','')
				game_batting_PA = str(row[12].text.strip()).replace('-','')

				if "at " in game_opponent:
					#print('away')
					game_loc = 'away'
					game_opponent = game_opponent.replace('at ','')
				else:
					game_loc = 'home'

				gamelog_ex_batting_df = gamelog_ex_batting_df.append({
					'date':game_date,'location':game_loc,'opponent':game_opponent,
					'result':game_result,'score':game_score,
					'team_score':game_team_score,'opp_score':game_opp_score,
					'HBP':game_batting_HBP,'SF':game_batting_SF,'SH':game_batting_SH,
					'TB':game_batting_TB,'XBH':game_batting_XBH,
					'HDP':game_batting_HDP,'GO':game_batting_GO,
					'FO':game_batting_FO,'GO/FO':game_batting_GO_FO,
					'PA':game_batting_PA},ignore_index=True)
		
		#print(gamelog_ex_batting_df)

		gamelog_batting_df = pd.merge(gamelog_batting_df,gamelog_ex_batting_df,
			on=['date','location','opponent','result','score','team_score','opp_score'])
		
		gamelog_batting_df['season'] = game_season
		gamelog_batting_df['njcaa_season'] = game_njcaa_season
		gamelog_batting_df['njcaa_division'] = game_njcaa_division
		gamelog_batting_df['team'] = game_team
		gamelog_batting_df['team_id'] = game_team_id
		gamelog_batting_df['player_id'] = game_player_id
		gamelog_batting_df['player_name'] = game_player_name

		#gamelog_batting_df = gamelog_batting_df.dropna(subset=['PA'], inplace=True)
		gamelog_batting_df.to_csv(f'gamelogs/batting/{game_season}_{game_player_id}.csv',index=False)
		del gamelog_batting_df, gamelog_ex_batting_df, batting_table, ex_batting_table

		pitching_table = soup.find_all('table')[4]
		for k in pitching_table.tbody.find_all('tr'):
			row = k.find_all('td')
			if len(row) < 2:
				pass
			else:
				#print(row)
				game_date = row[0].text.strip()
				game_opponent = row[1].text.strip()
				game_opponent = str(game_opponent).replace('                       ',' ')
				game_score_raw = str(row[2].text.strip()).split()
				try:
					game_result = str(game_score_raw[0]).replace(',','')
				except:
					game_result = None
				try:
					game_score = str(game_score_raw[1]).replace(',','')
				except:
					game_score = None
				try:
					game_team_score = str(game_score.split('-',-1)[0])
				except:
					game_team_score = None
				try:
					game_opp_score = str(game_score.split('-',-1)[0])
				except:
					game_opp_score = None
				game_pitching_GS = str(row[3].text.strip()).replace('-','')
				game_pitching_W = str(row[4].text.strip()).replace('-','')
				game_pitching_L = str(row[5].text.strip()).replace('-','')
				game_pitching_SV = str(row[6].text.strip()).replace('-','')
				game_pitching_IP = str(row[7].text.strip()).replace('-','')
				game_pitching_H = str(row[8].text.strip()).replace('-','')
				game_pitching_R = str(row[9].text.strip()).replace('-','')
				game_pitching_ER = str(row[10].text.strip()).replace('-','')
				game_pitching_ERA = str(row[11].text.strip()).replace('-','')
				game_pitching_BB = str(row[12].text.strip()).replace('-','')
				game_pitching_K = str(row[13].text.strip()).replace('-','')
				game_pitching_HR = str(row[14].text.strip()).replace('-','')

				if "at " in game_opponent:
					#print('away')
					game_loc = 'away'
					game_opponent = game_opponent.replace('at ','')
				else:
					game_loc = 'home'

				gamelog_pitching_df = gamelog_pitching_df.append({
					'date':game_date,'location':game_loc,'opponent':game_opponent,
					'result':game_result,'score':game_score,
					'team_score':game_team_score,'opp_score':game_opp_score,
					'GS':game_pitching_GS,'W':game_pitching_W,'L':game_pitching_L,
					'SV':game_pitching_SV,'IP':game_pitching_IP,'H':game_pitching_H,
					'R':game_pitching_R,'ER':game_pitching_ER,'ERA':game_pitching_ERA,
					'BB':game_pitching_BB,'K':game_pitching_K,'HR':game_pitching_HR}
					,ignore_index=True)

		gamelog_pitching_df['season'] = game_season
		gamelog_pitching_df['njcaa_season'] = game_njcaa_season
		gamelog_pitching_df['njcaa_division'] = game_njcaa_division
		gamelog_pitching_df['team'] = game_team
		gamelog_pitching_df['team_id'] = game_team_id
		gamelog_pitching_df['player_id'] = game_player_id
		gamelog_pitching_df['player_name'] = game_player_name

		gamelog_pitching_df.to_csv(f'gamelogs/pitching/{game_season}_{game_player_id}.csv',index=False)
		del gamelog_pitching_df,pitching_table

		fielding_table = soup.find_all('table')[4]
		for k in fielding_table.tbody.find_all('tr'):
			row = k.find_all('td')
			if len(row) < 2:
				pass
			else:
				#print(row)
				game_date = row[0].text.strip()
				game_opponent = row[1].text.strip()
				game_opponent = str(game_opponent).replace('                       ',' ')
				game_score_raw = str(row[2].text.strip()).split()
				try:
					game_result = str(game_score_raw[0]).replace(',','')
				except:
					game_result = None
				try:
					game_score = str(game_score_raw[1]).replace(',','')
				except:
					game_score = None
				try:
					game_team_score = str(game_score.split('-',-1)[0])
				except:
					game_team_score = None
				try:
					game_opp_score = str(game_score.split('-',-1)[0])
				except:
					game_opp_score = None
				game_fielding_TC = str(row[3].text.strip()).replace('-','')
				game_fielding_PO = str(row[4].text.strip()).replace('-','')
				game_fielding_A = str(row[5].text.strip()).replace('-','')
				game_fielding_E = str(row[6].text.strip()).replace('-','')
				game_fielding_FPCT = str(row[7].text.strip()).replace('-','')
				game_fielding_DP = str(row[8].text.strip()).replace('-','')
				game_fielding_SBA = str(row[9].text.strip()).replace('-','')
				game_fielding_RCS = str(row[10].text.strip()).replace('-','')
				game_fielding_RCS_PCT = str(row[11].text.strip()).replace('-','')
				game_fielding_PB = str(row[12].text.strip()).replace('-','')
				game_fielding_CI = str(row[13].text.strip()).replace('-','')

				if "at " in game_opponent:
					#print('away')
					game_loc = 'away'
					game_opponent = game_opponent.replace('at ','')
				else:
					game_loc = 'home'

				gamelog_fielding_df = gamelog_fielding_df.append({
					'date':game_date,'location':game_loc,'opponent':game_opponent,
					'result':game_result,'score':game_score,
					'team_score':game_team_score,'opp_score':game_opp_score,
					'TC':game_fielding_TC,'PO':game_fielding_PO,'A':game_fielding_A,
					'E':game_fielding_E,'FPCT':game_fielding_FPCT,
					'DP':game_fielding_DP,'SBA':game_fielding_SBA,
					'RCS':game_fielding_RCS,'RCS_PCT':game_fielding_RCS_PCT,
					'PB':game_fielding_PB,'CI':game_fielding_CI}
					,ignore_index=True)

		gamelog_fielding_df['season'] = game_season
		gamelog_fielding_df['njcaa_season'] = game_njcaa_season
		gamelog_fielding_df['njcaa_division'] = game_njcaa_division
		gamelog_fielding_df['team'] = game_team
		gamelog_fielding_df['team_id'] = game_team_id
		gamelog_fielding_df['player_id'] = game_player_id
		gamelog_fielding_df['player_name'] = game_player_name

		gamelog_fielding_df.to_csv(f'gamelogs/fielding/{game_season}_{game_player_id}.csv',index=False)
		time.sleep(5)

def main():
	getNjcaaD1BattingGamelogs()

if __name__ == "__main__":
	main()