from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

def getNjcaaRosters(webdriverPath="./chromedriver_mac64_m1"):
	teams_df = pd.read_csv('njcaa_schools.csv')
	school_name = teams_df['school_name'].tolist()
	school_njcaa_season = teams_df['njcaa_season'].tolist()
	school_njcaa_division = teams_df['division'].tolist()
	school_team_id = teams_df['team_id'].tolist()
	school_season = teams_df['season'].tolist()
	driver = webdriver.Chrome(
		executable_path=webdriverPath)
	
	roster_df = pd.DataFrame()
	for i in tqdm(range(3590,len(school_name))):
		roster_df = pd.DataFrame()
		## Declarations to prevent "local variable referenced before assignment" errors
		player_num = None
		player_name = None
		player_position = None
		player_year = None
		player_url = None
		player_id = None

		## This data is in teams_df
		team_name = school_name[i]
		team_njcaa_season = school_njcaa_season[i]
		team_njcaa_division = school_njcaa_division[i]
		team_id = school_team_id[i]
		team_season = school_season[i]
		print(team_njcaa_season,team_njcaa_division,team_name)
		url = f"https://www.njcaa.org/sports/bsb/{team_njcaa_season}/{team_njcaa_division}/teams/{team_id}?view=roster"
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, features='lxml')
		table = soup.find_all('table')[1]
		#print(f"\n{table}")

		cols = []
		for j in table.tr.find_all('th'):
			cols.append(j.text.strip())
			#print(f"{j}\n")
		cols.append('PlayerURL')
		cols.append('PlayerID')
		#print(cols)
		count = 0
		try:
			for k in table.tbody.find_all('tr'):
				row = k.find_all('td')
				if count == 0:
					pass
				else:
					player_num = row[0].text.strip()
					player_name = row[1].text.strip()
					player_position = row[2].text.strip()
					player_year = row[3].text.strip()
					player_url = "https://www.njcaa.org/" + str(row[1].find("a").get("href")) #
					player_id = player_url.split('/')[9]
					roster_df = roster_df.append({'No.':player_num,'Name':player_name,'Position':player_position,'Year':player_year,'PlayerURL':player_url,'PlayerID':player_id},ignore_index=True)

					#print(player_num,player_name,player_position,player_year)
				count += 1
				#print(row)
				#playerNum = row[0].text.strip()
			roster_df['team_name'] = team_name
			roster_df['team_njcaa_season'] = team_njcaa_season
			roster_df['team_njcaa_division'] = team_njcaa_division
			roster_df['team_id'] = team_id
			roster_df['team_season'] = team_season
			roster_df.to_csv(f'rosters/{team_njcaa_division}/{team_njcaa_season}_{team_id}.csv',index=False)
			print(roster_df)
		except:
			print(f"Could not find a roster for the {team_njcaa_season} {team_name} baseball team.")
		# try:
		# 	df = pd.read_html(driver.page_source)[1]
		# 	print(df)
		# except:
		# 	print(f"Could not find a roster for {njcaa_team_name}")
		time.sleep(5)

def main():
	getNjcaaRosters()

if __name__ == "__main__":
	main()