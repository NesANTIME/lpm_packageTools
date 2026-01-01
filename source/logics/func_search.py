import sys
import requests

# ~~~ modulos internos de lpm ~~~
from source.animations import message_animation
from source.modules.conections_core import autentificacion_server, URL_BASEDATA




def main_search(id_client, token_client, name_package):
    session_id = autentificacion_server(id_client, token_client, "search")
        
    try:
        response = requests.post(f"{URL_BASEDATA}/search_packet", json={
            "id_session": session_id, 
            "name_packet": name_package
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

    print(f"{' '*6}Package      : {name_package}\n{' '*6}Version      : {data.get('lastest')} (latest)")
    print(f"{' '*6}Developer    : {data.get('creador')}\n{' '*6}Description  : {data.get('description')}")

    return data.get("lastest"), data.get("__main__")