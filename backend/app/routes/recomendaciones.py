from flask import Flask, jsonify, request
from services.recommender import Recommender

class Recomendaciones:
    def __init__(self, app: Flask):
        self.app = app
        self.recommender = Recommender()
        try:
            self.recommender.load_correlation()
        except FileNotFoundError:
            pass
        self.rutas()

    def rutas(self):
        @self.app.route("/recomendaciones", methods=["POST"])
        def recomendaciones():
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "Request JSON missing"}), 400

                mail = data.get("mail")
                ratings = data.get("ratings")

                if not ratings:
                    return jsonify({"error": "Faltan valoraciones"}), 400

                recomendaciones = self.recommender.recommend(ratings)

                out = []
                try:
                    for name, score in recomendaciones.items():
                        try:
                            s = float(score)
                        except Exception:
                            s = None
                        out.append({"anime": name, "score": s})
                except Exception:
                    return jsonify({"error": "Formato de recomendaciones inesperado"}), 500

                return jsonify(out)
            except Exception as e:
                return jsonify({"error": str(e)}), 500