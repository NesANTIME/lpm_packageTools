import sys
import requests

# ~~~ modulos internos de lpm ~~~
from source.animations import message_animation
from source.modules.conections_core import autentificacion_server, URL_BASEDATA




def main_search(id_client, token_client, name_package):
    session_id = autentificacion_server(id_client, token_client, "sea")

    try:
        response = requests.post(f"{URL_BASEDATA}/client/search_package", json={ 
            "client_uuidSession": session_id, 
            "client_namePackage": name_package
        }, timeout=10)

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            message_animation(
                f"[!] Consultando por el paquete [{name_package}]", 
                f"[ ERROR ] El paquete [{name_package}] no existe", 3, 4
            )
        sys.exit(1)

    message_animation(f"[!] Consultando por el paquete [{name_package}]", f"[ OK ] El paquete existe!", 2, 4)

    version_package = f"{data.get('version_pkg')} (lastest)"

    print(f"\n{' '*6}Package      : {data.get('name_pkg')}\n{' '*6}Version      : {version_package}")
    print(f"{' '*6}Developer    : {data.get('creador')}\n{' '*6}Description  : {data.get('description')}")
    