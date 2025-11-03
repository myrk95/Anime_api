import pandas as pd
import os
import json

MIN_RATINGS_ANIME = 100
MIN_RATINGS_USER = 10
MAX_RATINGS_USER = 617
TOP_10_FILE = "backend/app/data_base/model/top_10.json"

ANIME_CSV_PATH = "backend/app/data_base/data/anime.csv"
RATINGS_CSV_PATH = "backend/app/data_base/data/rating.csv"

# Llegir fitxers
ratings = pd.read_csv(RATINGS_CSV_PATH, header=0)
anime = pd.read_csv(ANIME_CSV_PATH, usecols=[0, 1], names=['anime_id', 'name'], header=0)

# Limpieza -1
ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')
ratings = ratings.dropna(subset=['rating'])
ratings = ratings[ratings['rating'] >= 0]

# Filtrar anime
counts = ratings['anime_id'].value_counts()
anime_significatius = counts[counts >= MIN_RATINGS_ANIME].index
ratings_filtrat = ratings[ratings['anime_id'].isin(anime_significatius)]

# Filtrar usuarios
users = ratings_filtrat['user_id'].value_counts()
usuaris_actius = users[(users >= MIN_RATINGS_USER) & (users <= MAX_RATINGS_USER)].index
ratings_filtrat = ratings_filtrat[ratings_filtrat['user_id'].isin(usuaris_actius)]

# Map anime_id a noms
name_map = anime.set_index('anime_id')['name'].to_dict()
ratings_filtrat['anime_name'] = ratings_filtrat['anime_id'].map(name_map)

# Top 10 anime més valorats
top10_counts = ratings_filtrat['anime_name'].value_counts().head(10)
top10_list = [{"anime": name, "count": count} for name, count in top10_counts.items()]

# Guardar JSON
with open(TOP_10_FILE, 'w', encoding='utf-8') as f:
    json.dump(top10_list, f, ensure_ascii=False, indent=2)

print(f"Top 10 guardat en {TOP_10_FILE}")
print(top10_list)