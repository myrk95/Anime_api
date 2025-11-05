from flask import Flask, jsonify, request
from services.recommender import Recommender
from data_base.DAOusers import DAOusers
import os

class AdminRoutes:
    def __init__(self, app: Flask, dao: DAOusers):
        self.app = app
        self.dao = dao
        self.recommender = Recommender()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/admin/train", methods=["POST"])
        def train_model():
            try:
                self.recommender.train()
                return jsonify({"message": "Modelo entrenado y guardado correctamente"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/admin/matrix", methods=["GET"])
        def get_matrix():
            try:
                matrix = self.recommender.load_correlation()
                return jsonify(matrix.to_dict()), 200
            except FileNotFoundError:
                return jsonify({"error": "No se encontró la matriz. Entrene el modelo primero."}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/admin/matrix/status", methods=["GET"])
        def get_matrix_status():
            try:
                matrix_exists = os.path.exists(self.recommender.correlation_file)
                return jsonify({
                    "exists": matrix_exists,
                    "path": self.recommender.correlation_file if matrix_exists else None
                }), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/admin/users", methods=["GET"])
        def get_users():
            try:
                users = self.dao.mostrar_usuarios()
                return jsonify(users), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
