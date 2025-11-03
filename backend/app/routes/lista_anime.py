import os
from flask import Flask, jsonify
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIME_CSV_PATH = os.path.join(BASE_DIR, "../data_base/data/anime.csv")

class ListaAnime:
    def __init__(self, app: Flask):
        self.app = app
        self.rutas()

    def rutas(self):
        @self.app.route("/lista_anime", methods=["GET"])
        def lista_anime():
            try:
                anime_df = pd.read_csv(ANIME_CSV_PATH, usecols=[1], names=["name"], header=0)
                anime_list = anime_df["name"].tolist()
                return jsonify(anime_list)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

