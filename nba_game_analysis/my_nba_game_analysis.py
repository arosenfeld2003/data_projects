import re
import csv
import argparse


def load_data(filename: str, data_type: str) -> list:
    result = []
    # with (open(filename, 'r') as csvfile):
    # due to python version in DoCode, we can't use 'with' statment...

    csvfile = open(filename, 'r')
    try:
        if data_type == 'game_data':
            csvreader = csv.reader(csvfile, delimiter='|')
        elif data_type == 'test_data':
            csvreader = csv.reader(csvfile)

        for row in csvreader:
            result.append(row)
    finally:
        csvfile.close()

    return result


def update_player_percentages(team_players_data: dict, player_name: str) -> dict:
    data = team_players_data[player_name]

    # Field Goal Percentage
    if data['FGA'] > 0:
        avg = 0 if data['FG'] == 0 else 1
        if data['FGA'] == data['FG']:
            team_players_data[player_name].update({'FG%': avg})
        else:
            team_players_data[player_name].update({'FG%': round((data['FG'] / data['FGA']), 3)})
    else:
        # no fg attempts
        team_players_data[player_name].update({'FG%': ''})

    # 3 Point Percentage
    if data['3PA'] > 0:
        if data['3PA'] == data['3P']:
            team_players_data[player_name].update({'3P%': 1})
        else:
            team_players_data[player_name].update({'3P%': round((data['3P'] / data['3PA']), 3)})
    else:
        # no 3 pt attempts
        team_players_data[player_name].update({'3P%': ''})

    # Free Throw Percentage
    if data['FTA'] > 0:
        if data['FTA'] == data['FT']:
            team_players_data[player_name].update({'FT%': 1})
        else:
            team_players_data[player_name].update({'FT%': round((data['FT'] / data['FTA']), 3)})
    else:
        # no ft attempts
        team_players_data[player_name].update({'FT%': ''})

    return team_players_data


def get_stat(stat: str, desc: str) -> bool:
    # return stat in desc.lower()
    return re.search(stat, desc.lower())


# a list of the player and the secondary player
def get_players(description: str) -> str:
    player_name = ''
    secondary_player_name = ''
    desc = description.split()
    i = 0
    try:
        while i < len(desc):
            if desc[i][-1] == '.':
                player_name = '{} {}'.format(desc[i], desc[i + 1])
                if len(desc) > (i + 2):
                    remainder = desc[i + 2:]
                    remainder_str = ' '.join(remainder)
                    if '(' in remainder_str and ')' in remainder_str:
                        j = 0
                        remainder_list = remainder_str.split()
                        while j < len(remainder_list):
                            if remainder_list[j][-1] == '.':
                                first_name = remainder_list[j]
                                last_name = remainder_list[j + 1][:-1]
                                secondary_player_name = '{} {}'.format(first_name, last_name)
                            j += 1
                break
            i += 1
    except (Exception,):
        print(Exception)

    player_name = player_name or 'Team'
    return [player_name, secondary_player_name]


def analyse_nba_game(play_by_play_moves: list) -> dict:
    # initialize variables
    headers = play_by_play_moves[0]
    home_team_name = headers[4]
    away_team_name = headers[3]
    home_team_players_data = {}
    away_team_players_data = {}
    result = {
        'home_team': {'name': home_team_name, 'players_data': []},
        'away_team': {'name': away_team_name, 'players_data': []}
    }

    # loop through plays to update team and player data
    # PERIOD|REMAINING_SEC|RELEVANT_TEAM|AWAY_TEAM|HOME_TEAM|AWAY_SCORE|HOME_SCORE|DESCRIPTION
    for play in play_by_play_moves:
        description = play[7]
        relevant_team = play[2]
        # update relevant team and player data
        data = home_team_players_data if relevant_team == home_team_name else away_team_players_data
        players = get_players(description)
        # add players to team_players_data
        for player in players:
            if player not in data:
                player = {player: {'player_name': player, 'FG': 0, 'FGA': 0, 'FG%': 0, '3P': 0, '3PA': 0,
                                   '3P%': 0, 'FT': 0, 'FTA': 0, 'FT%': 0, 'ORB': 0, 'DRB': 0, 'TRB': 0,
                                   'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, 'PTS': 0
                                   }}
                data.update(player)
        # add team totals to team_players_data
        if 'Team' not in data:
            team = {'Team': {'player_name': 'Team', 'FG': 0, 'FGA': 0, 'FG%': 0, '3P': 0, '3PA': 0,
                             '3P%': 0, 'FT': 0, 'FTA': 0, 'FT%': 0, 'ORB': 0, 'DRB': 0, 'TRB': 0,
                             'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, 'PTS': 0
                             }}
            data.update(team)

        # several stats will be listed under secondary_player name, specifically: 'steal', 'assist', 'block'
        player_name, secondary_player_name = players[0], players[1]
        if get_stat('makes', description):
            if get_stat('3-pt', description):
                # player
                data[player_name]['3P'] += 1
                data[player_name]['3PA'] += 1
                data[player_name]['FG'] += 1
                data[player_name]['FGA'] += 1
                data[player_name]['PTS'] += 3
                # team
                data['Team']['3P'] += 1
                data['Team']['3PA'] += 1
                data['Team']['FG'] += 1
                data['Team']['FGA'] += 1
                data['Team']['PTS'] += 3
            elif get_stat('free throw', description):
                # player
                data[player_name]['FT'] += 1
                data[player_name]['FTA'] += 1
                data[player_name]['FT'] += 1
                # team
                data['Team']['FT'] += 1
                data['Team']['FTA'] += 1
                data['Team']['PTS'] += 1
            else:
                # player
                data[player_name]['FG'] += 1
                data[player_name]['FGA'] += 1
                data[player_name]['PTS'] += 2
                # team
                data['Team']['FG'] += 1
                data['Team']['FGA'] += 1
                data['Team']['PTS'] += 2
        elif get_stat('misses', description):
            if get_stat('3-pt', description):
                # player
                data[player_name]['3PA'] += 1
                data[player_name]['FGA'] += 1
                # team
                data['Team']['3PA'] += 1
                data['Team']['FGA'] += 1
            elif get_stat('free throw', description):
                # player
                data[player_name]['FTA'] += 1
                # team
                data['Team']['FTA'] += 1
            else:
                # player
                data[player_name]['FGA'] += 1
                # team
                data['Team']['FGA'] += 1
        elif get_stat('rebound', description):
            # player
            data[player_name]['TRB'] += 1
            # team
            data['Team']['TRB'] += 1
            if get_stat('offensive', description):
                # player
                data[player_name]['ORB'] += 1
                # team
                data['Team']['ORB'] += 1

            elif get_stat('defensive', description):
                # player
                data[player_name]['DRB'] += 1
                # team
                data['Team']['DRB'] += 1

        if get_stat('assist', description):
            # assist is secondary player name
            data[secondary_player_name]['AST'] += 1
            # team
            data['Team']['AST'] += 1

        if get_stat('steal', description):
            # steal is secondary player name
            data[secondary_player_name]['STL'] += 1
            # team
            data['Team']['STL'] += 1

        if get_stat('block', description):
            # block is secondary player name
            data[secondary_player_name]['BLK'] += 1
            # team
            data['Team']['BLK'] += 1

        if get_stat('turnover', description):
            # player
            data[player_name]['TOV'] += 1
            # team
            data['Team']['TOV'] += 1

        if get_stat('foul by', description):
            # player
            data[player_name]['PF'] += 1
            # team
            data['Team']['PF'] += 1
        
        if relevant_team == home_team_name:
            home_team_players_data.update(data)
        else:
            away_team_players_data.update(data)

    # update percentages
    # home_data, away_data = result['home_team']['players_data'], result['away_team']['players_data']
    for player_name in home_team_players_data:
        update_player_percentages(home_team_players_data, player_name)

    for player_name in away_team_players_data:
        update_player_percentages(away_team_players_data, player_name)

    # build list of player data dicts
    for player in home_team_players_data:
        result['home_team']['players_data'].append(home_team_players_data[player])
    for player in away_team_players_data:
        result['away_team']['players_data'].append(away_team_players_data[player])

    return result


def print_nba_game_stats(team_dict: dict) -> None:
    headers = ['Players', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST',
               'STL', 'BLK', 'TOV', 'PF', 'PTS']
    print(' '.join(headers))
    player_data = team_dict['players_data']
    team_totals = ''
    for data in player_data:
        player = data['player_name']
        if len(player) > 0:
            player_str = 'Team Totals' if player == 'Team' else player
            i = 0
            while i < len(headers):
                if headers[i] in data:
                    val = str(data[headers[i]])

                    if headers[i][-1] == '%':
                        if val == '1':
                            # add trailing zeros to 100%
                            val += '.000'
                        elif len(val) > 1 and val[1] == '.':
                            # remove leading 0 from decimal percentages
                            val = val[1:]
                            # add trailing zeros to decimal percentages
                            if len(val) < 3:
                                val += '00'

                    player_str += ' ' + val
                i += 1
            if player == 'Team':
                team_totals = player_str
            else:
                print(player_str)

    print(team_totals)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--filename',
        help='the name of csv file containing game data',
        type=str,
        required=True,
    )
    args = parser.parse_args()
    game_data = load_data(args.filename, 'game_data')
    processed_data = analyse_nba_game(game_data)
    print_nba_game_stats(processed_data['home_team'])
    print('\n')
    print_nba_game_stats(processed_data['away_team'])


if __name__ == '__main__':
    _main()
