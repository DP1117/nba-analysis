from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
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
        count = 0
        for row in reader:
            if count == 1:
                for data in row[4:]:
                    if data == '':
                        career_matrix.append(0)
                    else:
                        career_matrix.append(float(data))
                break
            count += 1
    career_matrices[player] = career_matrix


player_list = list(career_matrices.keys())
career_data = np.array([career_matrices[player] for player in player_list])

scaled_data = StandardScaler().fit_transform(career_data)

pca = PCA(n_components=2)
coords = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 7))
plt.scatter(coords[:, 0], coords[:, 1], color='purple')
for i, name in enumerate(player_list):
    plt.text(coords[i, 0], coords[i, 1], name, fontsize=8)
plt.title("Player Career Similarity (PCA)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.show()

