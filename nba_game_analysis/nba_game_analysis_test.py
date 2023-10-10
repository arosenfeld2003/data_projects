import re
import csv
import argparse
from my_nba_game_analysis import load_data, analyse_nba_game


def format_test_data(test_data: list) -> list:
    for player in test_data:
        name = player[0].split()
        if name != 'PLAYERS' and len(name) > 1:
            player_first_name, player_last_name = name[0], name[1]
            processed = '{}. {}'.format(player_first_name[0], player_last_name)
            player[0] = processed
    return test_data


def test_data_validity():
    game_data = 'game_data.csv'
    test_data = 'test_data.csv'
    game_data = load_data(game_data, 'game_data')
    home_team_test_data = load_data(test_data, 'test_data')

    # test that data is imported as a list
    assert type(game_data) is list
    assert type(home_team_test_data) is list

    processed_test_data = format_test_data(home_team_test_data)
    for row in processed_test_data:
        if row[0] != 'PLAYERS':
            assert (row[0][1]) == '.'

    processed_game_data = analyse_nba_game(game_data)
    home_team_data_dict = processed_game_data['home_team']

    # Test Data Headers is HOME TEAM for this game (Warriors):
    # PLAYERS,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,-9999
    test_headers = processed_test_data[0][1:]
    test_player_data = processed_test_data[1:]
    game_player_data = home_team_data_dict['players_data']
    for player in test_player_data:
        player_name = player[0]
        player_stats = player[1:]
        i = 0
        while i < len(test_headers):
            stat = test_headers[i]
            for game_player in game_player_data:
                if player_name in game_player:
                    print('Player: {}, Stat: {}, Val: {}, Test_Val: {}'.format(
                        player_name,
                        stat,
                        game_player[player_name][stat],
                        float(player_stats[i])
                    ))
                    assert game_player_data[player_name][stat] == float(player_stats[i])
            i += 1


def _main():
    test_data_validity()


if __name__ == '__main__':
    _main()
