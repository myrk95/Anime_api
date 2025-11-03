import os
import json
from flask import Flask, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIME_JSON_PATH = os.path.join(BASE_DIR, "../data_base/model/matriz_corr.json")

class ListaAnime:
    def __init__(self, app: Flask):
        self.app = app
        self.rutas()

    def rutas(self):
        @self.app.route("/lista_anime", methods=["GET"])
        def lista_anime():
            try:
                with open(ANIME_JSON_PATH, "r", encoding="utf-8") as f:
                    matriz_corr = json.load(f)
                anime_list = list(matriz_corr.keys())
                return jsonify(anime_list)

            except FileNotFoundError:
                return jsonify({"error": f"No se ha encontrado {ANIME_JSON_PATH}"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500

