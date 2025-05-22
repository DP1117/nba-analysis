import csv

filename = 'players.txt'

with open(filename, 'r') as file:
    players = [line.strip() for line in file]

player_matrices = {}
career_matrices = {}

for player in players:
    player_path = f'player_data/{player}.csv'
    career_path = f'player_data/career/{player}-career.csv'

    player_matrix = []
    career_matrix = []
    
    with open(player_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            player_matrix.append(row)
    player_matrices[player] = player_matrix

    with open(career_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            career_matrix.append(row)
    career_matrices[player] = career_matrix

print(career_matrices['Kyrie Irving'])