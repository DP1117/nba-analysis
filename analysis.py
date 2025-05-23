import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import csv

filename = 'players.txt'

with open(filename, 'r') as file:
    players = [line.strip() for line in file]

player_matrices = {}
career_matrices = {}
stat_names = []

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
            if len(stat_names) == 0:
                stat_names = row[4:]
            if count == 1:
                for data in row[4:]:
                    if data == '':
                        career_matrix.append(0)
                    else:
                        career_matrix.append(float(data))
                break
            count += 1
    career_matrices[player] = career_matrix

# Construct data matrix
player_list = list(career_matrices.keys())
career_data = np.array([career_matrices[player] for player in player_list])

### PCA ###

# Standardize data
mean = np.mean(career_data, axis=0)
std = np.std(career_data, axis=0)
standardized_data = (career_data - mean) / std

# Covariance matrix
cov_matrix = np.cov(standardized_data, rowvar=False)

# Eigen decomposition
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Project data to new basis
top_k = 2
projection_matrix = eigenvectors[:, :top_k]
reduced_data = np.dot(standardized_data, projection_matrix)

plt.figure(figsize=(10, 7))
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], color='purple')
for i, name in enumerate(player_list):
    plt.text(reduced_data[i, 0], reduced_data[i, 1], name, fontsize=8)
plt.title("Player Career Similarity (PCA - Manual)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.show()

coords_3d = career_data @ eigenvectors[:, :3]

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# coords_3d is the N x 3 matrix from projecting data
ax.scatter(coords_3d[:, 0], coords_3d[:, 1], coords_3d[:, 2], color='purple')

for i, name in enumerate(player_list):
    ax.text(coords_3d[i, 0], coords_3d[i, 1], coords_3d[i, 2], name, fontsize=7)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.set_title('Player Career Similarity (3D PCA)')

plt.tight_layout()
plt.show()

plt.tight_layout()
plt.show()

def print_pc_loadings(eigenvectors, stat_names, start=1, end=3):
    print(f"\n=== Principal Component Loadings (PC{start} to PC{end}) ===\n")
    for pc_idx in range(start-1, end):
        print(f"PC{pc_idx+1}:")
        eigenvector = eigenvectors[:, pc_idx]
        for stat, loading in sorted(zip(stat_names, eigenvector), key=lambda x: abs(x[1]), reverse=True):
            print(f"{stat:20s}: {loading:.4f}")
        print()

print_pc_loadings(eigenvectors, stat_names, start=1, end=3)

def plot_pc_loadings_bar(eigenvectors, stat_names, pc_index=0):
    """
    pc_index = 0 for PC1, 1 for PC2, etc.
    """
    loadings = eigenvectors[:, pc_index]
    sorted_idx = np.argsort(loadings)

    plt.figure(figsize=(10, 7))
    plt.barh(np.array(stat_names)[sorted_idx], loadings[sorted_idx], color='skyblue')
    plt.axvline(0, color='gray', linewidth=0.8)
    plt.title(f'PC{pc_index + 1} Loadings')
    plt.xlabel('Loading Value')
    plt.tight_layout()
    plt.show()

plot_pc_loadings_bar(eigenvectors, stat_names, pc_index=0)  # PC1
plot_pc_loadings_bar(eigenvectors, stat_names, pc_index=1)  # PC2
plot_pc_loadings_bar(eigenvectors, stat_names, pc_index=2)  # PC3

def plot_pc_heatmap(eigenvectors, stat_names, num_pcs=3, top_n=10):
    pc_data = {}
    for i in range(num_pcs):
        component = eigenvectors[:, i]
        abs_component = np.abs(component)
        top_stats_idx = np.argsort(abs_component)[-top_n:]
        for idx in top_stats_idx:
            stat = stat_names[idx]
            if stat not in pc_data:
                pc_data[stat] = [0] * num_pcs
            pc_data[stat][i] = component[idx]

    df = pd.DataFrame(pc_data).T
    df.columns = [f'PC{i+1}' for i in range(num_pcs)]

    plt.figure(figsize=(8, max(6, 0.4 * len(df))))
    sns.heatmap(df, annot=True, center=0, cmap='coolwarm')
    plt.title(f'Top {top_n} Stat Loadings for First {num_pcs} PCs')
    plt.tight_layout()
    plt.show()

plot_pc_heatmap(eigenvectors, stat_names, num_pcs=3, top_n=10)