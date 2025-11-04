import pandas as pd
import os

MIN_RATINGS_ANIME = 100
MIN_RATINGS_USER = 10
MAX_RATINGS_USER = 617
MIN_PERIODS_CORR = 500

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORRELATION_FILE = os.path.normpath(os.path.join(BASE_DIR, "..", "data_base", "data", "matriz_corr.json"))
ANIME_CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "data_base", "data", "anime.csv"))
RATINGS_CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "data_base", "data", "ratings.csv"))


class Recommender:
    def __init__(self, anime_path = ANIME_CSV_PATH, 
                 ratings_path = RATINGS_CSV_PATH,
                 min_ratings_anime=MIN_RATINGS_ANIME,
                 min_ratings_user=MIN_RATINGS_USER,
                 max_ratings_user=MAX_RATINGS_USER,
                 min_periods_corr=MIN_PERIODS_CORR,
                 correlation_file=CORRELATION_FILE):
        self.anime_path = anime_path
        self.ratings_path = ratings_path
        self.correlation_file = correlation_file
        self.min_ratings_anime = min_ratings_anime
        self.min_ratings_user = min_ratings_user
        self.max_ratings_user = max_ratings_user
        self.min_periods_corr = min_periods_corr

        self.userRatings = None
        self.corrMatrix = None
        self.name_map = None

    def train(self):
        ratings = pd.read_csv(self.ratings_path, header = 0)
        anime = pd.read_csv(self.anime_path, usecols=[0, 1], names=['anime_id', 'name'], header=0)

        # Limpieza -1
        ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')
        ratings = ratings.dropna(subset=['rating'])
        ratings = ratings[ratings['rating'] >= 0]

        # Filtrar anime
        counts = ratings['anime_id'].value_counts()
        anime_significatius = counts[counts >= self.min_ratings_anime].index
        ratings_filtrat = ratings[ratings['anime_id'].isin(anime_significatius)]

        # Filtrar usuarios
        users = ratings_filtrat['user_id'].value_counts()
        usuaris_actius = users[(users >= self.min_ratings_user) & (users <= self.max_ratings_user)].index
        ratings_filtrat = ratings_filtrat[ratings_filtrat['user_id'].isin(usuaris_actius)]

        # Pivotar 
        self.userRatings = ratings_filtrat.pivot_table(index='user_id', columns='anime_id', values='rating')

        # Matriz
        corrMatrix = self.userRatings.corr(method='pearson', min_periods=self.min_periods_corr)

        # Conversión ids a names
        name_map = anime.set_index('anime_id')['name'].to_dict()
        corrMatrix_names = corrMatrix.rename(index=name_map, columns=name_map)

        # Guardar matriz en JSON
        self.corrMatrix = corrMatrix_names
        self.name_map = name_map
        self._save_correlation()

    def _save_correlation(self):
        """Guarda la matriu de correlació en un fitxer JSON"""
        if self.corrMatrix is not None:
            self.corrMatrix.fillna(0, inplace=True)  # JSON no suporta NaN
            # ensure directory exists
            dirname = os.path.dirname(self.correlation_file)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)
            # save with orient='columns' so keys are names
            self.corrMatrix.to_json(self.correlation_file, orient='columns')
        else:
            raise ValueError("No hi ha matriu de correlació per guardar")

    def load_correlation(self):
        """Carrega la matriu de correlació ja calculada"""
        if not os.path.exists(self.correlation_file):
            raise FileNotFoundError("No hi ha cap matriu entrenada. L'admin ha de cridar train() primer")
        # read with pandas (orientation should match save)
        self.corrMatrix = pd.read_json(self.correlation_file)
        return self.corrMatrix

    def recommend(self, myRatings: dict, top_n=10):
        """
        Genera recomanacions a partir dels ratings de l'usuari.
        myRatings: dict {anime_name: rating}
        """
        if self.corrMatrix is None:
            raise ValueError("Cal carregar la matriu de correlació abans de recomanar")

        myRatingsSeries = pd.Series(myRatings, name=0)
        simCandidates = pd.Series(dtype='float64')

        for anime, rating in myRatingsSeries.items():
            if anime in self.corrMatrix.columns:
                sims = self.corrMatrix[anime].dropna()
                sims = sims * rating
                simCandidates = pd.concat([simCandidates, sims])

        # Sumem similituds per anime
        simCandidates = simCandidates.groupby(simCandidates.index).sum()

        # Excloem els que l'usuari ja ha valorat
        filteredSims = simCandidates.drop(myRatingsSeries.index, errors='ignore')

        # Ordenem descendent
        filteredSims = filteredSims.sort_values(ascending=False)

        return filteredSims.head(top_n)