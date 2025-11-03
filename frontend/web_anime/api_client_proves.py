import requests, random

API_URL = "http://127.0.0.1:5000"

def registrar():
    print("\n=== Registrar usuario ===")
    nom = input("Nom: ")
    cognoms = input("Cognoms: ")
    mail = input("Correu: ")
    password = input("Contrasenya: ")

    r = requests.post(f"{API_URL}/registrar_usuario", json={
        "nombre": nom,
        "apellidos": cognoms,
        "mail": mail,
        "password": password
    })
    try:
        print("Resposta:", r.json())
    except Exception:
        print("Resposta status:", r.status_code, "text:", r.text)

def login():
    print("\n=== Iniciar sesión ===")
    mail = input("Correo: ")
    password = input("Contraseña: ")

    r = requests.post(f"{API_URL}/autenticar_usuario", json={
        "mail": mail,
        "password": password
    })
    try:
        data = r.json()
    except Exception:
        print("Error parsing response:", r.text)
        return None

    if "mensaje" in data:
        print("Login correcto!")
        return mail
    else:
        print("Error:", data)
        return None

def obtener_animes():
    r = requests.get(f"{API_URL}/lista_anime")
    try:
        data = r.json()
    except Exception as e:
        print("Error parsing lista_anime response:", e)
        return []

    if isinstance(data, list):
        # If server returns list of dicts with "anime" key, extract names
        if len(data) > 0 and isinstance(data[0], dict) and "anime" in data[0]:
            return [item["anime"] for item in data]
        return data
    else:
        print("Error al obtener animes:", data)
        return []

def obtener_top10():

    r = requests.get(f"{API_URL}/top10")
    if r.status_code != 200:
        try:
            print("No se pudo obtener top10:", r.json())
        except Exception:
            print("No se pudo obtener top10, status:", r.status_code, "text:", r.text)
        return []

    try:
        data = r.json()
    except Exception as e:
        print("Error parsing top10 response:", e)
        return []

    if isinstance(data, list):
        if len(data) == 0:
            return []
        first = data[0]
        if isinstance(first, dict) and "anime" in first:
            return [item.get("anime") for item in data]
        elif isinstance(first, str):
            return data
    print("Formato inesperado de top10:", data)
    return []

def pedir_ratings():
    print("\nEvalua mínimo 2 animes para obtener recomendaciones.")

    total_animes = obtener_animes()

    sugeridos = obtener_top10()
    if not sugeridos:
        sugeridos = random.sample(total_animes, min(10, len(total_animes))) if total_animes else []

    print("Sugeridos:", ", ".join(sugeridos))

    myRatings = {}

    while len(myRatings) < 2:
        anime = input("Nombre del anime (o 'fin' per acabar): ").strip()

        if anime.lower() == 'fin':
            if len(myRatings) >= 2:
                break
            else:
                print("Debes evaluar al menos 2 animes.")
                continue

        if anime not in total_animes:
            print("Anime no encontrado en la base de datos.")
            continue

        try:
            rating = int(input(f"Rating de {anime} (1-10): "))
            if 1 <= rating <= 10:
                myRatings[anime] = rating
            else:
                print("Número inválido. Debe estar entre 1 y 10.")
        except ValueError:
            print("Número inválido. Inténtalo de nuevo.")

    return myRatings



def ver_recomendaciones(mail):
    ratings = pedir_ratings()
    r = requests.post(f"{API_URL}/recomendaciones", json={
        "mail": mail,
        "ratings": ratings
    })
    print("Status code:", r.status_code)
    print("Respuesta del servidor:", r.text)
    try:
        data = r.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return

    if isinstance(data, list):
        print("\n=== Recomendaciones ===")
        for idx, item in enumerate(data, start=1):
            if isinstance(item, dict) and "anime" in item:
                print(f"{idx}. {item['anime']} (score: {item.get('score')})")
            else:
                print(f"{idx}. {item}")
    else:
        print("Respuesta:", data)

def listar_top10():
    top10 = obtener_top10()
    if not top10:
        print("No se encontró top10 en el servidor.")
        return
    print("\n=== Top 10 (más famosos presentes en matriz_corr) ===")
    for i, name in enumerate(top10, 1):
        print(f"{i}. {name}")

def main():
    print("=== Front Anime ===")
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión y ver recomendaciones")
        print("3. Salir")
        print("4. Listar Top 10")
        opcio = input("> ")

        if opcio == "1":
            registrar()
        elif opcio == "2":
            usuari = login()
            if usuari:
                ver_recomendaciones(usuari)
        elif opcio == "3":
            print("Adiós!")
            break
        elif opcio == "4":
            listar_top10()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()