import pandas as pd
from time import sleep
import random
from bs4 import BeautifulSoup, Tag
import numpy as np
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
_TIMEOUT = 4

def returnSeasonString(season:int) -> str:

    ## This should be a switch statement, but this is an if
    ## statement because people running this code before Python 3.10
    ## don't have access to switch statements.

    if season < 2013:
        print("This function does not currently support seasons before 2013")
    elif season == 2013:
        season_str = "2012-2013"
        return season_str
    elif season == 2014:
        season_str = "2013-2014"
        return season_str
    elif season == 2015:
        season_str = "2014-2015"
        return season_str
    elif season == 2016:
        season_str = "2015-2016"
        return season_str
    elif season == 2017:
        season_str = "2016-2017"
        return season_str
    elif season == 2018:
        season_str = "2017-2018"
        return season_str
    elif season == 2019:
        season_str = "2018-2019"
        return season_str
    elif season == 2020:
        season_str = "2019-2020"
        return season_str
    elif season == 2021:
        season_str = "2020-2021"
        return season_str
    elif season == 2022:
        season_str = "2021-2022"
        return season_str
    elif season == 2023:
        season_str = "2022-2023"
        return season_str
    else:
        raise Exception(f"The {season} season has yet to be played")
        
def getSeasonRoster(season:int,division:str,teamID:str):
    # https://www.njcaa.org/sports/bsb/2021-22/div1/teams/asabrooklynavengers?view=roster
    season_str = returnSeasonString(season)

    if division != "div1" and division != "div2" and division != "div3":
        raise Exception(f"Division must be set to \"div1\", \"div2\", or \"div3\".\nAnything else will raise this error.")

    url = f"https://www.njcaa.org/sports/bsb/{season_str}/{division}/teams/{teamID}?view=roster"
    page =requests.get(url,headers=_HEADERS)
    soup = BeautifulSoup(page.text,'lxml')

    with open("test.html","w+") as f:
        f.write(str(soup))

def getPlayerGamelogs():
    print()

def main():
    getSeasonRoster(2022,"div1","asabrooklynavengers")

if __name__ == "__main__":
    main()