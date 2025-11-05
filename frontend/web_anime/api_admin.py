import requests
import json
import os
from getpass import getpass

API_URL = "http://127.0.0.1:5000"

def admin_login():
    """
    Admin login
    """
    print("\n=== Admin Login ===")
    mail = input("Email: ")
    password = input("Password: ")

    try:
        response = requests.post(f"{API_URL}/autenticar_usuario", json={
            "mail": mail,
            "password": password
        })
        data = response.json()

        if "mensaje" not in data:
            print("Fallo en login:", data.get("error", "Error desconocido"))
            return None

        if data.get('rol') != 'admin':
            print("Acceso denegado: Se requieren privilegios de administrador")
            return None
            
        print("Login de administrador correcto!")
        return mail
            
    except Exception as e:
        print(f"Error durante el login: {e}")
        return None

def obtener_usuarios():
    """
    Lista de todos los usuarios registrados
    """
    try:
        response = requests.get(f"{API_URL}/admin/users")
        if response.status_code == 200:
            users = response.json()
            print("\n=== Registered Users ===")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user['nombre']} {user['apellidos']}")
                print(f"   Email: {user['mail']}")
                print("   " + "-"*30)
            return users
        else:
            print(f"Error al intentar obtener usuarios: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def train_model():
    """
    Se entrena el modelo de nuevo.
    Devuelve True si tiene éxito, False en caso contrario.
    """
    try:
        print("Entrenando modelo... Puede tardar un rato...")
        response = requests.post(f"{API_URL}/admin/train")
        if response.status_code == 200:
            print("Modelo entrenado!")
            return True
        else:
            print(f"Error en training: {response.status_code}")
            print(response.text)
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el servidor: {e}")
        return False

def get_matrix():
    """
    Obtiene la matriz de correlación del servidor.
    Devuelve la matriz.
    """
    try:
        print("Cargando matriz...")
        response = requests.get(f"{API_URL}/admin/matrix")
        if response.status_code == 200:
            matrix = response.json()
            print("Matriz cargada correctamente!")
            return matrix
        elif response.status_code == 404:
            print("Matriz no encontrada, prueba a cargar el modelo.")
            return None
        else:
            print(f"Error al cargar la matriz: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el servidor: {e}")
        return None

def get_matrix_status():
    """
    Comprueba el estado de la matriz de correlación en el servidor.
    Devuelve información de estado si tiene éxito; de lo contrario, None.
    """
    try:
        response = requests.get(f"{API_URL}/admin/matrix/status")
        if response.status_code == 200:
            status = response.json()
            if status["exists"]:
                print(f"MAtriz existe en: {status['path']}")
            else:
                print("La matriz no existe.")
            return status
        else:
            print(f"Error al comrpobar el estatus de la matriz: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el servidor: {e}")
        return None

def test_recommendations():
    """
    Testea el sistema de recomendaciones con valoraciones de ejemplo.
    """
    sample_ratings = {
        "Death Note": 5,
        "Fullmetal Alchemist: Brotherhood": 5,
        "Attack on Titan": 4
    }
    
    try:
        print("Testeano recomendaciones con valoraciones de ejemplo...")
        response = requests.post(f"{API_URL}/recomendaciones", 
                              json={"ratings": sample_ratings})
        
        if response.status_code == 200:
            recommendations = response.json()
            print("\Test de recomendaciones obtenido:")
            for rec in recommendations:
                print(f"- {rec['anime']}: {rec['score']}")
            return recommendations
        else:
            print(f"Error al obtener recomendaciones: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de consexión con el servidor: {e}")
        return None

def main():
    print("=== Admin API: Anime Recommender ===")
    
    admin = admin_login()
    if not admin:
        print("Se requiere login de admin!")
        return

    while True:
        print("\nOpciones de administrador:")
        print("1. Ver estado de la matriz")
        print("2. Entrenar nuevo modelo")
        print("3. Ver información de la matriz")
        print("4. Probar recomendaciones")
        print("5. Ver usuarios registrados")
        print("6. Salir")

        
        option = input("\Selecciona una opcion (1-6): ")
        
        if option == "1":
            print("\nComprobando estado de matriz...")
            get_matrix_status()
            
        elif option == "2":
            if input("\Quiere entrenar el modelo (y/n): ").lower() == 'y':
                train_model()
                get_matrix_status()
                
        elif option == "3":
            print("\nCargando información de matriz...")
            matrix = get_matrix()
            if matrix:
                print(f"Matriz cargada. Contiene: {len(matrix)} entradas de anime.")
                
        elif option == "4":
            print("\nTesteo de recomendaciones del siestema...")
            test_recommendations()
            
        elif option == "5":
            obtener_usuarios()
            
        elif option == "6":
            print("\n Adiós!")
            break
            
        else:
            print("\nOpción inválida, vuelva a intentar.")

if __name__ == "__main__":
    main()
