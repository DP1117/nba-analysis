import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_cell_text(row, tag, attr):
    cell = row.find(tag, {'data-stat': attr})
    return cell.text if cell else ''

def team_data(team_name, season):
  # URL for the Team's Basketball Reference page
  url = (f'https://www.basketball-reference.com/teams/{team_name}/{season}.html')
  
  # The requests library can send a GET request to the url
  res = requests.get(url)
  
  # BeautifulSoup library parses the content of an HTML document, in this case res
  soup = BeautifulSoup(res.content, 'lxml')
  
  # BeautifulSoup's .find() method searches for a tag and specified attributes; returns the first match
  team_per_game = soup.find(name='table', attrs={'id': 'per_game_stats'})
  
  # Making a list of dictionaries to then convert into a pd.DataFrame
  team_info = []
  for row in team_per_game.find_all(
      'tr')[1:]:  # Excluding the first 'tr', since that's the table's title head
  
    player = {}
    player['Name'] = row.find('td', {'data-stat': 'name_display'}).text
    player['Age'] = row.find('td', {'data-stat': 'age'}).text
    player['Min PG'] = row.find('td', {'data-stat': 'mp_per_g'}).text
    player['Field Goal %'] = row.find('td', {'data-stat': 'fg_pct'}).text
    player['Rebounds PG'] = row.find('td', {'data-stat': 'trb_per_g'}).text
    player['Assists PG'] = row.find('td', {'data-stat': 'ast_per_g'}).text
    player['Steals PG'] = row.find('td', {'data-stat': 'stl_per_g'}).text
    player['Blocks PG'] = row.find('td', {'data-stat': 'blk_per_g'}).text
    player['Turnovers PG'] = row.find('td', {'data-stat': 'tov_per_g'}).text
    player['Points PG'] = row.find('td', {'data-stat': 'pts_per_g'}).text
  
    team_info.append(player)
  
  df = pd.DataFrame(team_info)
  df.to_csv(f'team_data/{team_name}-{season}.csv', index=False)

  return team_info

def player_data(player_name, player_url):
    print(player_name)
    url = f'https://www.basketball-reference.com/players/{player_url}'

    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'lxml')

    player_per_game = soup.find(name='table', attrs={'id': 'per_game_stats'})

    player_info = []
    career_info = []

    if player_per_game:
        for row in player_per_game.find_all('tr')[1:]:
            season = {}

            if row.find('td', {'data-stat': 'age'}) is None:
                
                if row.find('td', {'data-stat': 'games'}) is None:
                    continue

                career = {}

                career['Season'] = get_cell_text(row, 'th', 'year_id')
                career['G'] = get_cell_text(row, 'td', 'games')
                career['GS'] = get_cell_text(row, 'td', 'games_started')
                career['MP'] = get_cell_text(row, 'td', 'mp_per_g')
                career['FG'] = get_cell_text(row, 'td', 'fg_per_g')
                career['FGA'] = get_cell_text(row, 'td', 'fga_per_g')
                career['FG%'] = get_cell_text(row, 'td', 'fg_pct')
                career['3P'] = get_cell_text(row, 'td', 'fg3_per_g')
                career['3PA'] = get_cell_text(row, 'td', 'fg3a_per_g')
                career['3P%'] = get_cell_text(row, 'td', 'fg3_pct')
                career['2P'] = get_cell_text(row, 'td', 'fg2_per_g')
                career['2PA'] = get_cell_text(row, 'td', 'fg2a_per_g')
                career['2P%'] = get_cell_text(row, 'td', 'fg2_pct')
                career['eFG%'] = get_cell_text(row, 'td', 'efg_pct')
                career['FT'] = get_cell_text(row, 'td', 'ft_per_g')
                career['FTA'] = get_cell_text(row, 'td', 'fta_per_g')
                career['FT%'] = get_cell_text(row, 'td', 'ft_pct')
                career['ORB'] = get_cell_text(row, 'td', 'orb_per_g')
                career['DRB'] = get_cell_text(row, 'td', 'drb_per_g')
                career['TRB'] = get_cell_text(row, 'td', 'trb_per_g')
                career['AST'] = get_cell_text(row, 'td', 'ast_per_g')
                career['STL'] = get_cell_text(row, 'td', 'stl_per_g')
                career['BLK'] = get_cell_text(row, 'td', 'blk_per_g')
                career['TOV'] = get_cell_text(row, 'td', 'tov_per_g')
                career['PF'] = get_cell_text(row, 'td', 'pf_per_g')
                career['PTS'] = get_cell_text(row, 'td', 'pts_per_g')

                career_info.append(career)
                break

            season['Season'] = get_cell_text(row, 'th', 'year_id')
            season['Age'] = get_cell_text(row, 'td', 'age')
            season['Pos'] = get_cell_text(row, 'td', 'pos')
            season['G'] = get_cell_text(row, 'td', 'games')
            season['GS'] = get_cell_text(row, 'td', 'games_started')
            season['MP'] = get_cell_text(row, 'td', 'mp_per_g')
            season['FG'] = get_cell_text(row, 'td', 'fg_per_g')
            season['FGA'] = get_cell_text(row, 'td', 'fga_per_g')
            season['FG%'] = get_cell_text(row, 'td', 'fg_pct')
            season['3P'] = get_cell_text(row, 'td', 'fg3_per_g')
            season['3PA'] = get_cell_text(row, 'td', 'fg3a_per_g')
            season['3P%'] = get_cell_text(row, 'td', 'fg3_pct')
            season['2P'] = get_cell_text(row, 'td', 'fg2_per_g')
            season['2PA'] = get_cell_text(row, 'td', 'fg2a_per_g')
            season['2P%'] = get_cell_text(row, 'td', 'fg2_pct')
            season['eFG%'] = get_cell_text(row, 'td', 'efg_pct')
            season['FT'] = get_cell_text(row, 'td', 'ft_per_g')
            season['FTA'] = get_cell_text(row, 'td', 'fta_per_g')
            season['FT%'] = get_cell_text(row, 'td', 'ft_pct')
            season['ORB'] = get_cell_text(row, 'td', 'orb_per_g')
            season['DRB'] = get_cell_text(row, 'td', 'drb_per_g')
            season['TRB'] = get_cell_text(row, 'td', 'trb_per_g')
            season['AST'] = get_cell_text(row, 'td', 'ast_per_g')
            season['STL'] = get_cell_text(row, 'td', 'stl_per_g')
            season['BLK'] = get_cell_text(row, 'td', 'blk_per_g')
            season['TOV'] = get_cell_text(row, 'td', 'tov_per_g')
            season['PF'] = get_cell_text(row, 'td', 'pf_per_g')
            season['PTS'] = get_cell_text(row, 'td', 'pts_per_g')


            player_info.append(season)

    # df = pd.DataFrame(player_info)
    dfCareer = pd.DataFrame(career_info)

    # df.to_csv(f'player_data/{player_name}.csv', index=False)
    dfCareer.to_csv(f'player_data/career/{player_name}-career.csv', index=False)


def gen_player_data():
    players = []

    with open('players.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue        

            parts = line.split(',', 1)
            if len(parts) != 2:
                print(f"Line format incorrect: {line}")
                continue

            player = {}

            player['Name'] = parts[0].strip()
            player['URL'] = parts[1].strip()

            players.append(player)

    for player in players:
        player_data(player['Name'], player['URL'])

gen_player_data()