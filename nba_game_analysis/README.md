# Welcome to My Nba Game Analysis
***

## Task
TODO - Summarize play by play data from an NBA game scraped from the web

## Description
First, we read the data from a CSV file (sample data is in file `game_data.csv`) into a hash. 
* Data has a pipe (`|`) delimiter
```
{
    "home_team": {"name": TEAM_NAME, "players_data": DATA}, 
    "away_team": {"name": TEAM_NAME, "players_data": DATA}
}

DATA will be an array of hashes with this format:
{
    "player_name": XXX, "FG": XXX, "FGA": XXX, "FG%": XXX, "3P": XXX, "3PA": XXX, 
    "3P%": XXX, "FT": XXX, "FTA": XXX, "FT%": XXX, "ORB": XXX, "DRB": XXX, 
    "TRB": XXX, "AST": XXX, "STL": XXX, "BLK": XXX, "TOV": XXX, "PF": XXX, "PTS": XXX
}
```
Next, we print this data to the console following these conventions:
```
Players	FG	FGA	FG%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS
Player00	XX	XX	.XXX	X	XX	.XXX	XX	XX	.XXX	XX	XX	XX	XX	X	X	XX	XX	XX
Team Totals	XX	XX	.XXX	X	XX	.XXX	XX	XX	.XXX	XX	XX	XX	XX	X	X	XX	XX	XX

```

## Installation
- There is a virtual env for this project, which can be installed following these guidelines:
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- e.g. on Mac or Unix: `python3 -m pip install --user virtualenv`, `python3 -m venv env`

## Usage
To run the program, first activate the virtual environment, e.g.
`source env/bin/activate`

Then use cli to runt the program with a required argument `-f {csv_filename}` e.g.
```
python3 my_nba_game_analysis.py -f game_data.csv
```

## Test
There is a test file to ensure data accuracy in the game analysis.
The data for this test is contained in two files:
`test_data.csv` is the data to test accuracy of the home_team data from `game_data.csv`

The test can be run from the cli with pytest: `pytest nba_game_analysis_test.py`

### The Core Team
- Solo Project: Alex Rosenfeld

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px'></span>
