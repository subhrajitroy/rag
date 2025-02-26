import pandas as pd
import glob
import os
import logger
from datetime import datetime
import re

DATA_PATH=os.environ["DATA_PATH"]
files_path=os.path.join(DATA_PATH,"*.csv")
logger.info(f"Data path is {files_path}")
files = glob.glob(os.path.join(DATA_PATH,"*.csv"))
files.sort()

logger.info(f"Number of files discovered is {len(files)}")

def is_date_valid(date):
    match_found = re.search("^(o|O)n.*$", date.strip())
    # print(f"for {date} search is {match_found}")
    return match_found

def is_date_blank(date):
    if date is None:
        return True

    date = date.strip()
    if date == "":
        return True
    return False

def process_date(date):
    
    if is_date_blank(date):
        return None
    if not is_date_valid(date):
        return None
    try:
        # print(date)
        on_date = " ".join(date.strip().split(" ")[1])
        # str(datetime.strptime(on_date,"%m/%d/%y %H:%M")) 
        return on_date
    except ValueError:
        return None
    # print(on_date)
    

def load_data(file):
    logger.info(f"Loading file {file}")
    df = pd.read_csv(file,sep=",",
                     header=0,
                    #  quoting=1,
                    #  escapechar='\\',
                    #  encoding='utf-8',
                    #  on_bad_lines='skip',
                     engine="python",
                     names=["Review_Date","Author_Name","Vehicle_Title","Review_Title","Review","Rating"])
    df["Review_Date"]=df["Review_Date"].apply(process_date)
    # df["Review_Date"] = datetime.strptime(review_date.split(" "),"%d/%m/%y")
    # print(df["Review_Date"][0:2])
    return df


# for file in files:
#     df = load_data(file)

# extracted data frame
def extract_data():
    e_df = load_data(files[0])
    return e_df

