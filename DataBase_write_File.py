import data_Processer
from data_Processer import *
import json

# Open and read the JSON file
with open('config.json', 'r') as file:
    data = json.load(file)


returned_df = process_data(data['softball_file'],data['Golf_file'],data['company_File'])
clean_df = returned_df[0]
companie_df = returned_df[1]
softball_df = returned_df[2]
golf_df = returned_df[3]
import sqlite3
import pandas as pd

# Connect to SQLite database (creates db if not exists)
conn = sqlite3.connect('example.db')  # or ':memory:' for an in-memory DB

clean_df.to_sql('cleaned_data', conn, if_exists='replace', index=False)
companie_df.to_sql('companies_data', conn, if_exists='replace', index=False)
softball_df.to_sql('softball_data', conn, if_exists='replace', index=False)
golf_df.to_sql('golf_data', conn, if_exists='replace', index=False)
print('written SucessFully')