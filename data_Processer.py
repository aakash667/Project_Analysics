# hinge_health_project.py

import pandas as pd
import numpy as np
from datetime import datetime
import us

# ------------------ Core Functions ------------------

def split_name(name):
    parts = name.strip().split()
    return pd.Series({'first_name': parts[0], 'last_name': ' '.join(parts[1:]) if len(parts) > 1 else ''})

def standardize_state(state):
    try:
        return us.states.lookup(state).abbr
    except:
        return np.nan

def parse_date(date_str, input_fmt, output_fmt="%Y/%m/%d"):
    try:
        return datetime.strptime(date_str, input_fmt).strftime(output_fmt)
    except:
        return np.nan

def process_data(SOFTBALL_FILE,GOLF_FILE,COMPANIES_FILE):
    # File paths
    #SOFTBALL_FILE = 'us_softball_league.tsv'
    #GOLF_FILE = 'unity_golf_club.csv'
    #COMPANIES_FILE = 'companies.csv'
    OUTPUT_FILE = 'cleaned_master_data.csv'
    BAD_RECORDS_FILE = 'bad_records.csv'

    # Load files
    companies_df = pd.read_csv(COMPANIES_FILE)
    company_map = dict(zip(companies_df['id'], companies_df['name']))

    softball_df = pd.read_csv(SOFTBALL_FILE, sep='\t')
    softball_df[['first_name', 'last_name']] = softball_df['name'].apply(split_name)
    softball_df['dob'] = softball_df['date_of_birth'].apply(lambda x: parse_date(x, "%m/%d/%Y"))
    softball_df['last_active'] = softball_df['last_active'].apply(lambda x: parse_date(x, "%m/%d/%Y"))
    softball_df = softball_df.rename(columns={'joined_league': 'member_since', 'us_state': 'state'})
    softball_df['state'] = softball_df['state'].apply(standardize_state)
    softball_df['source'] = 'softball'
    softball_df = softball_df[['first_name', 'last_name', 'dob', 'company_id', 'last_active', 'score', 'member_since', 'state', 'source']]

    golf_df = pd.read_csv(GOLF_FILE)
    golf_df['dob'] = golf_df['dob'].apply(lambda x: parse_date(x, "%Y/%m/%d"))
    golf_df['last_active'] = golf_df['last_active'].apply(lambda x: parse_date(x, "%Y/%m/%d"))
    golf_df['source'] = 'golf'
    golf_df = golf_df[['first_name', 'last_name', 'dob', 'company_id', 'last_active', 'score', 'member_since', 'state', 'source']]

    combined_df = pd.concat([softball_df, golf_df], ignore_index=True)
    combined_df['company_name'] = combined_df['company_id'].map(company_map)
    combined_df.drop(columns=['company_id'], inplace=True)

    bad_records = combined_df[
        (pd.to_datetime(combined_df['dob'], errors='coerce') > pd.to_datetime(combined_df['member_since'], format='%Y', errors='coerce')) |
        (pd.to_datetime(combined_df['last_active'], errors='coerce') < pd.to_datetime(combined_df['dob'], errors='coerce'))
    ]
    bad_records.to_csv(BAD_RECORDS_FILE, index=False)
    clean_df = combined_df[~combined_df.index.isin(bad_records.index)]
    clean_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Cleaned data saved to {OUTPUT_FILE}")
    print(f"🛑 Bad records saved to {BAD_RECORDS_FILE}")
    return (clean_df,companies_df,softball_df,golf_df)
