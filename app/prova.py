from connection import Connection
from DAOusers import DAOusers

conn = Connection().conectar()
dao = DAOusers(conn)

mail_actual = "alex@mail.com"
password = "1234"

# Login
user = dao.autenticar_usuario(mail_actual, password)
if user:
    print("Login correcte!")
    # Mostrar només el seu perfil
    perfil = dao.mostrar_usuario(mail_actual)
    print("El teu perfil:", perfil)

    # Si és admin, veure tots
    usuaris = dao.mostrar_usuarios(mail_actual)
    if usuaris:
        print("Llista completa d'usuaris:", usuaris)
    else:
        print("No tens permisos per veure tots els usuaris.")
else:
    print("Mail o contrasenya incorrectes.")
