from data_Processer import *
def test_process_data_integration():
    import os
    SOFTBALL_FILE = 'us_softball_league.tsv'
    GOLF_FILE = 'unity_golf_club.csv'
    COMPANIES_FILE = 'companies.csv'

    # Clean up existing files before test
    if os.path.exists('cleaned_master_data.csv'): os.remove('cleaned_master_data.csv')
    if os.path.exists('bad_records.csv'): os.remove('bad_records.csv')

    # Run the processing function
    clean_df, companies_df, softball_df, golf_df = process_data(SOFTBALL_FILE, GOLF_FILE, COMPANIES_FILE)

    # Assertions
    assert not clean_df.empty, "❌ Cleaned DataFrame is empty"
    assert 'company_name' in clean_df.columns, "❌ 'company_name' column not found in cleaned DataFrame"
    assert os.path.exists('cleaned_master_data.csv'), "❌ Output file 'cleaned_master_data.csv' not created"
    assert os.path.exists('bad_records.csv'), "❌ Output file 'bad_records.csv' not created"

    print("✅ Integration test passed: process_data correctly generates outputs")

# ------------------ Main Runner ------------------


SOFTBALL_FILE = 'us_softball_league.tsv'
GOLF_FILE = 'unity_golf_club.csv'
COMPANIES_FILE = 'companies.csv'
process_data(SOFTBALL_FILE, GOLF_FILE, COMPANIES_FILE)