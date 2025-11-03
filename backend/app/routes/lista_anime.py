import os
import json
from flask import Flask, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANIME_JSON_PATH = os.path.normpath(os.path.join(BASE_DIR, "../data_base/model/matriz_corr.json"))
TOP10_JSON_PATH = os.path.normpath(os.path.join(BASE_DIR, "../data_base/model/top10.json"))

class ListaAnime:
    def __init__(self, app: Flask):
        self.app = app
        self.rutas()

    def rutas(self):
        @self.app.route("/lista_anime", methods=["GET"])
        def lista_anime():
            if not os.path.isfile(ANIME_JSON_PATH):
                return jsonify({"error": f"No se ha encontrado {ANIME_JSON_PATH}"}), 404

            try:
                with open(ANIME_JSON_PATH, "r", encoding="utf-8") as f:
                    matriz_corr = json.load(f)
            except Exception as e:
                return jsonify({"error": f"Error leyendo {ANIME_JSON_PATH}: {e}"}), 500

            try:
                anime_list = list(matriz_corr.keys())
            except Exception:
                return jsonify({"error": "Formato inesperado."}), 500

            return jsonify(anime_list)

        @self.app.route("/top10", methods=["GET"])
        def top10_matriz_corr():

            if not os.path.isfile(TOP10_JSON_PATH):
                return jsonify({"error": f"No se ha encontrado el archivo {TOP10_JSON_PATH}."}), 404

            try:
                with open(TOP10_JSON_PATH, "r", encoding="utf-8") as f:
                    top10 = json.load(f)
            except Exception as e:
                return jsonify({"error": f"Error leyendo {TOP10_JSON_PATH}: {e}"}), 500

            return jsonify(top10)