import os
import sys
import base64
import zipfile
import requests
from lpm.source.animations import animationBAR_barra, animationsBAR_message
from lpm.source.logic_local import add_package


URL_BASEDATA = "https://fastapi-production-c7c6.up.railway.app".rstrip('/')



# ~~~ Funciones Auxiliares

def auth_conection(client_id, type_consultation, token_secret):
    return {"client_id": client_id, "type_consultation": type_consultation, "secret_token": token_secret}

def delivery_search(id_session, name_packet):
    return {"id_session": id_session, "name_packet": name_packet}

def delivery_install(id_session, name_packet, version_packet):
    return {"id_session": id_session, "name_packet": name_packet, "version_packet": version_packet}


# Funciones de conexion y autentificacion

def autentificacion_local(id_client, token_secret, type_consulta, name_packet):
    animationsBAR_message("[!] Conectando con el Servidor...", "[ OK ] Conectado con el Servidor...", 1, 4)

    print(f"{' '*6} Iniciando autentificacion con el dominio: {id_client[:5]}...")

    auth_response = requests.post(f"{URL_BASEDATA}/authenticate", json=auth_conection(id_client, type_consulta, token_secret), timeout=10)

    auth_response.raise_for_status()
    auth_data = auth_response.json()

    if (not auth_data.get("authorized")):
        animationsBAR_message("[!] Conectado a lpm_DATABASE", f"[ ERROR ] autentificacion fallida con el dominio: {id_client[:5]}", 2, 4)
        sys.exit(1)
    
    session_id = auth_data["ID_session"]

    animationsBAR_message("[!] Conectado a lpm_DATABASE", f"[ OK ] Conectado a lpm_DATABASE, Bienvenido {auth_data.get('username')}!", 3, 4)

    print(f"{' '*6} Conexión autentificada con exito...")

    if (type_consulta == "search"):
        funcDelivery_search(session_id, name_packet, type_consulta)
    elif (type_consulta == "install"):
        funcDelivery_install(session_id, name_packet, type_consulta)




# ~~~ Funciones delivery

def funcDelivery_search(session_id, name_packet, type_consulta=None):
    print()
    
    try:
        response = requests.post(f"{URL_BASEDATA}/search_packet", json=delivery_search(session_id, name_packet), timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            animationsBAR_message(f"[!] Consultando por el paquete [{name_packet}]", f"[ ERROR ] El paquete [{name_packet}] no existe", 3, 4)
        sys.exit(1)

    animationsBAR_message(f"[!] Consultando por el paquete [{name_packet}]", f"[ OK ] El paquete existe!", 2, 4)

    print(f"{' '*6}[ Name Package ] --> [{name_packet}]  \n{' '*6}[ Version ] -------> [{data.get('lastest')}]")
    print(f"{' '*6}[ Desarrollador ] -> [{data.get('creador')}]  \n{' '*6}[ Descripcion ] ---> [{data.get('description')}]")

    return data.get("lastest"), data.get("__main__")
    


def funcDelivery_install(session_id, name_packet, type_consulta):
    versionLastest_packet, main_packet = funcDelivery_search(session_id, name_packet, type_consulta)

    if (not versionLastest_packet):
        sys.exit(1)

    destino = os.path.expanduser(f"~/.lpm/{name_packet}/{versionLastest_packet}")
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"{name_packet}.zip")

    add_package(name_packet, versionLastest_packet, main_packet)

    try:
        response = requests.post(f"{URL_BASEDATA}/install_packet", json=delivery_install(session_id, name_packet, versionLastest_packet), timeout=20)
        response.raise_for_status()
        data = response.json()


        if (data.get("status") != "success"):
            print(f"{' '*14} [ ERROR ] {data.get('status')}")
            sys.exit(1)
            
        nombre_archivo = data.get("nombre_archivo")
        tamaño = data.get("tamaño_bytes")
        contenido_base64 = data.get("contenido_base64")

        contenido = base64.b64decode(contenido_base64)
            
        with open(zip_path, "wb") as f:
            f.write(contenido)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destino)

        os.remove(zip_path)

        print()
        animationBAR_barra(4, "Instalando Package... ")
        print(f"{' '*4}[ OK ] lpm instalo el package completamente!\n {' '*6}[NAME]: {nombre_archivo} -- [TAMAÑO]: {tamaño} bytes")
    
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalles: {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")