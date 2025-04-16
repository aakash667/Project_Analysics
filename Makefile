# Makefile for Hinge Health Project

# Run the main script
run:
	pipenv run python data_Processer.py

# Run unit or integration tests
unit-test:
	pipenv run python Process_unit_test.py test

test:
	pipenv run pytest Test_Intergartion_Data_end_to_end.py

# Lint the code
lint:
	pipenv run flake8 data_Processer.py

# Format the code
format:
	pipenv run black data_Processer.py

# Clean generated files
clean:
	rm -f cleaned_master_data.csv bad_records.csv hinge_data.db

# All in one
all: clean format lint test run
