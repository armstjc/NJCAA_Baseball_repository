from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode
import re

def getNjcaaD1BattingGamelogs(webdriverPath="./chromedriver_mac64_m1"):
	# teams_df = pd.read_csv('rosters/div1_rosters.csv')
	# school_name = teams_df['school_name'].tolist()
	# school_njcaa_season = teams_df['njcaa_season'].tolist()
	# school_njcaa_division = teams_df['division'].tolist()
	# school_team_id = teams_df['team_id'].tolist()
	# school_season = teams_df['season'].tolist()
	# player_numbers = teams_df['No.'].tolist()
	# player_names = teams_df['season'].tolist()
	# player_positions = teams_df['season'].tolist()
	# player_ids = teams_df['season'].tolist()
	# player_urls = teams_df['season'].tolist()

	driver = webdriver.Chrome(
		executable_path=webdriverPath)
	
	# for i in tqdm(range(0,len(player_urls))):
	## Ensure that we have a brand new DataFame in each iteration.
	gamelog_batting_df = pd.DataFrame()
	gamelog_ex_batting_df = pd.DataFrame()
	gamelog_pitching_df = pd.DataFrame()
	gamelog_fielding_df = pd.DataFrame()
	
	# 	# Info related to the player
	# 	team_name = school_name[i]
	
	# Set everything to null before getting any data for this table.
	game_date = None
	game_opponent = None
	game_score = None
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

	url = "https://www.njcaa.org/sports/bsb/2012-13/div2/players/zacherystampleyxnae"
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
			#print(row)
			game_date = row[0].text.strip()
			game_opponent = row[1].text.strip()
			game_opponent = str(game_opponent).replace('                       ',' ')
			game_score = row[2].text.strip()
			game_batting_AB = row[3].text.strip()
			game_batting_R = row[4].text.strip()
			game_batting_H = row[5].text.strip()
			game_batting_2B = row[6].text.strip()
			game_batting_3B = row[7].text.strip()
			game_batting_HR = row[8].text.strip()
			game_batting_RBI = row[9].text.strip()
			game_batting_BB = row[10].text.strip()
			game_batting_K = row[11].text.strip()
			game_batting_SB = row[12].text.strip()
			game_batting_CS = row[13].text.strip()
			


			gamelog_batting_df = gamelog_batting_df.append({
				'Date':game_date,'Opponent':game_opponent,'Score':game_score,
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
			game_score = row[2].text.strip()
			game_batting_HBP = row[3].text.strip()
			game_batting_SF = row[4].text.strip()
			game_batting_SH = row[5].text.strip()
			game_batting_TB = row[6].text.strip()
			game_batting_XBH = row[7].text.strip()
			game_batting_HDP = row[8].text.strip()
			game_batting_GO = row[9].text.strip()
			game_batting_FO = row[9].text.strip()
			game_batting_GO_FO = row[9].text.strip()
			game_batting_PA = row[9].text.strip()

			gamelog_ex_batting_df = gamelog_ex_batting_df.append({
				'Date':game_date,'Opponent':game_opponent,'Score':game_score,
				'HBP':game_batting_HBP,'SF':game_batting_SF,'SH':game_batting_SH,
				'TB':game_batting_TB,'XBH':game_batting_XBH,
				'HDP':game_batting_HDP,'GO':game_batting_GO,
				'FO':game_batting_FO,'GO/FO':game_batting_GO_FO,
				'PA':game_batting_PA},ignore_index=True)
	
	#print(gamelog_ex_batting_df)

	gamelog_batting_df = pd.merge(gamelog_batting_df,gamelog_ex_batting_df,
		on=['Date','Opponent','Score'])
	
	gamelog_batting_df.to_csv('test_bat.csv',index=False)
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
			game_score = row[2].text.strip()
			game_pitching_GS = row[3].text.strip()
			game_pitching_W = row[4].text.strip()
			game_pitching_L = row[5].text.strip()
			game_pitching_SV = row[6].text.strip()
			game_pitching_IP = row[7].text.strip()
			game_pitching_H = row[8].text.strip()
			game_pitching_R = row[9].text.strip()
			game_pitching_ER = row[10].text.strip()
			game_pitching_ERA = row[11].text.strip()
			game_pitching_BB = row[12].text.strip()
			game_pitching_K = row[13].text.strip()
			game_pitching_HR = row[14].text.strip()
			
			gamelog_pitching_df = gamelog_pitching_df.append({
				'Date':game_date,'Opponent':game_opponent,'Score':game_score,
				'GS':game_pitching_GS,'W':game_pitching_W,'L':game_pitching_L,
				'SV':game_pitching_SV,'IP':game_pitching_IP,'H':game_pitching_H,
				'R':game_pitching_R,'ER':game_pitching_ER,'ERA':game_pitching_ERA,
				'BB':game_pitching_BB,'K':game_pitching_K,'HR':game_pitching_HR}
				,ignore_index=True)
	
	gamelog_pitching_df.to_csv('test_pitching.csv',index=False)
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
			game_score = row[2].text.strip()
			game_fielding_TC = row[3].text.strip()
			game_fielding_PO = row[4].text.strip()
			game_fielding_A = row[5].text.strip()
			game_fielding_E = row[6].text.strip()
			game_fielding_FPCT = row[7].text.strip()
			game_fielding_DP = row[8].text.strip()
			game_fielding_SBA = row[9].text.strip()
			game_fielding_RCS = row[10].text.strip()
			game_fielding_RCS_PCT = row[11].text.strip()
			game_fielding_PB = row[12].text.strip()
			game_fielding_CI = row[13].text.strip()
			gamelog_fielding_df = gamelog_fielding_df.append({
				'Date':game_date,'Opponent':game_opponent,'Score':game_score,
				'TC':game_fielding_TC,'PO':game_fielding_PO,'A':game_fielding_A,
				'E':game_fielding_E,'FPCT':game_fielding_FPCT,
				'DP':game_fielding_DP,'SBA':game_fielding_SBA,
				'RCS':game_fielding_RCS,'RCS_PCT':game_fielding_RCS_PCT,
				'PB':game_fielding_PB,'CI':game_fielding_CI}
				,ignore_index=True)
	
	gamelog_fielding_df.to_csv('test_fielding.csv',index=False)
	time.sleep(5)

def main():
	getNjcaaD1BattingGamelogs()

if __name__ == "__main__":
	main()