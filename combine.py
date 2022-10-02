import os
import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
from multiprocessing import Pool

def reader(filename):
        
        return pd.read_csv(filename, encoding='latin-1')

def mergeFilesMultithreaded(filePath=""):
    #global filecount
    #filecount = 0
    num_cpus = os.cpu_count()
    print(f'{num_cpus} cpu cores advalible to this script.')

    pool = Pool(num_cpus-1)
    main_df = pd.DataFrame()
    
    l = filePath
    file_list = glob.iglob(l+"/*csv")
    file_list = list(file_list)
    df_list = pool.map(reader,tqdm(file_list))

    main_df = pd.concat(df_list)

    return main_df

def mergeRostersDivOne():
    f = "rosters/div1"
    df = mergeFilesMultithreaded(f)
    df.to_csv("rosters/div1_rosters.csv",index=False)

def mergeRostersDivTwo():
    f = "rosters/div2"
    df = mergeFilesMultithreaded(f)
    df.to_csv("rosters/div2_rosters.csv",index=False)

def mergeRostersDivThree():
    f = "rosters/div3"
    df = mergeFilesMultithreaded(f)
    df.to_csv("rosters/div3_rosters.csv",index=False)

def main():
    mergeRostersDivOne()
    mergeRostersDivTwo()
    mergeRostersDivThree()

if __name__ == "__main__":
    main()