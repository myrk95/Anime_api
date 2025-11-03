from flask import Flask, jsonify, request
from services.recommender import Recommender

class Recomendaciones:
    def __init__(self, app: Flask):
        self.app = app
        self.recommender = Recommender()  # inicialitza el teu recommender habitual
        self.rutas()

    def rutas(self):
        @self.app.route("/recomendaciones", methods=["POST"])
        def recomendaciones():
            try:
                data = request.get_json()
                mail = data.get("mail")
                ratings = data.get("ratings")

                if not ratings:
                    return jsonify({"error": "Falten valoracions"}), 400

                recomendaciones = self.recommender.recomendar(ratings)
                return jsonify(recomendaciones)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
