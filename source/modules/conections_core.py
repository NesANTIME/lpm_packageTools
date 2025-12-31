import sys
import requests

# ~~ modulos internos lpm ~~
from source.logic import load_config
from source.animations import message_animation


# ~~~~ VARIABLES GLOBALES ~~~~
URL_BASEDATA = load_config["url_servidores"][0]




# ~~~ funciones de conexion ~~~
# ~~ authentification ~~
def autentificacion_server(id_client, token_secret, type_consulta):
    message_animation("[!] Conectando con el Servidor...", "[ OK ] Conectado con el Servidor...", 1, 4)
    print(f"{' '*6} Iniciando autentificacion con el dominio: {id_client[:5]}...")

    auth_response = requests.post(f"{URL_BASEDATA}/authenticate", json={
        "client_id": id_client, "type_consultation": type_consulta, "secret_token": token_secret
    }, timeout=10)

    auth_response.raise_for_status()
    auth_data = auth_response.json()

    if (not auth_data.get("authorized")):
        message_animation("[!] Conectado a lpm_DATABASE", f"[ ERROR ] autentificacion fallida con el dominio: {id_client[:5]}", 2, 4)
        sys.exit(1)
    
    session_id = auth_data["ID_session"]

    message_animation("[!] Conectado a lpm_DATABASE", f"[ OK ] Conectado a lpm_DATABASE, Bienvenido {auth_data.get('username')}!", 3, 4)
    print(f"{' '*6} Conexión autentificada con exito...")

    return session_id