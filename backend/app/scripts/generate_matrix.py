import pandas as pd
import os

MIN_RATINGS_ANIME = 100
MIN_RATINGS_USER = 10
MAX_RATINGS_USER = 617
MIN_PERIODS_CORR = 500
CORRELATION_FILE = "backend/app/data_base/model/matriz_corr.json"

ANIME_CSV_PATH = "backend/app/data_base/data/anime.csv"
RATINGS_CSV_PATH = "backend/app/data_base/data/rating.csv"


ratings = pd.read_csv(RATINGS_CSV_PATH, header = 0)
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

        # Pivotar 
userRatings = ratings_filtrat.pivot_table(index='user_id', columns='anime_id', values='rating')

        # Matriz
corrMatrix = userRatings.corr(method='pearson', min_periods=MIN_PERIODS_CORR)

        # Conversión ids a names
name_map = anime.set_index('anime_id')['name'].to_dict()
corrMatrix_names = corrMatrix.rename(index=name_map, columns=name_map)

        # Guardar matriz en JSON
if not os.path.exists(os.path.dirname(CORRELATION_FILE)):
    os.makedirs(os.path.dirname(CORRELATION_FILE))

corrMatrix_names.to_json(CORRELATION_FILE, orient='index')
print(f"Matriz de correlación guardada en {CORRELATION_FILE}")
