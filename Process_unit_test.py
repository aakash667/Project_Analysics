import pytest
import io
import numpy
import pandas
import pytest
import io
from data_Processer import *
def run_tests():
    def test_split_name():
        assert split_name("Jane Doe")['first_name'] == "Jane"
        assert split_name("Jane Doe")['last_name'] == "Doe"
        assert split_name("Prince")['last_name'] == ""

    def test_parse_date():
        assert parse_date("11/02/1966", "%m/%d/%Y") == "1966/11/02"
        assert pd.isna(parse_date("bad_date", "%m/%d/%Y"))

    def test_standardize_state():
        assert standardize_state("California") == "CA"
        assert pd.isna(standardize_state("InvalidState"))

    def test_softball_transformation():
        df = pd.DataFrame({
            'name': ['Jane Doe'],
            'date_of_birth': ['01/01/1990'],
            'last_active': ['05/05/2020'],
            'company_id': [1],
            'score': [95],
            'joined_league': [2010],
            'us_state': ['California']
        })
        df[['first_name', 'last_name']] = df['name'].apply(split_name)
        df['dob'] = df['date_of_birth'].apply(lambda x: parse_date(x, "%m/%d/%Y"))
        df['last_active'] = df['last_active'].apply(lambda x: parse_date(x, "%m/%d/%Y"))
        df['state'] = df['us_state'].apply(standardize_state)
        assert df['first_name'].iloc[0] == "Jane"
        assert df['dob'].iloc[0] == "1990/01/01"
        assert df['state'].iloc[0] == "CA"

    print("✅ Running tests...")
    test_split_name()
    test_parse_date()
    test_standardize_state()
    test_softball_transformation()
    print("✅ All tests passed!")

run_tests()