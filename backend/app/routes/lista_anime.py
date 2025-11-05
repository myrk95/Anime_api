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
        # --- LISTA COMPLETA DE ANIMES ---
        @self.app.route("/lista_anime", methods=["GET"])
        def lista_anime():
            if not os.path.isfile(ANIME_JSON_PATH):
                return jsonify({"error": f"No se ha encontrado {ANIME_JSON_PATH}"}), 404

            try:
                with open(ANIME_JSON_PATH, "r", encoding="utf-8") as f:
                    matriz_corr = json.load(f)
            except Exception as e:
                return jsonify({"error": f"Error leyendo {ANIME_JSON_PATH}: {e}"}), 500

            # Creamos una lista de objetos con campo 'title'
            try:
                anime_list = [{"title": name} for name in matriz_corr.keys()]
            except Exception:
                return jsonify({"error": "Formato inesperado en la matriz de correlación."}), 500

            return jsonify(anime_list)

        # --- TOP 10 ANIMES ---
        @self.app.route("/top10", methods=["GET"])
        def top10_matriz_corr():
            if not os.path.isfile(TOP10_JSON_PATH):
                return jsonify({"error": f"No se ha encontrado el archivo {TOP10_JSON_PATH}."}), 404

            try:
                with open(TOP10_JSON_PATH, "r", encoding="utf-8") as f:
                    top10 = json.load(f)
            except Exception as e:
                return jsonify({"error": f"Error leyendo {TOP10_JSON_PATH}: {e}"}), 500

            # Normalizamos el formato para que siempre devuelva: {"anime": "Nombre", "count": valoraciones}
            try:
                formatted_top10 = []
                for item in top10:
                    if isinstance(item, dict):
                        anime = item.get("anime") or item.get("title") or item.get("nombre") or "Título desconocido"
                        count = item.get("count") or 0
                    elif isinstance(item, (list, tuple)) and len(item) == 2:
                        anime, count = item
                    else:
                        anime, count = str(item), 0

                    formatted_top10.append({
                        "anime": anime,
                        "count": count
                    })

                return jsonify(formatted_top10)

            except Exception as e:
                return jsonify({"error": f"Error procesando Top 10: {e}"}), 500
