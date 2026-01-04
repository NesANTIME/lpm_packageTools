import sys
import requests

# ~~~ modulos internos de lpm ~~~
from source.animations import message_animation
from source.modules.conections_core import autentificacion_server, URL_BASEDATA




def main_search(id_client, token_client, name_package, mode_session):
    if (mode_session == None):
        session_id = autentificacion_server(id_client, token_client, "search")
    else:
        session_id = mode_session

    try:
        mode_delivery = None
        if (name_package == list):
            mode_delivery = "list"

        response = requests.post(f"{URL_BASEDATA}/search_packet", json={ 
            "id_session": session_id, 
            "name_packet": name_package, 
            "mode_delivery": mode_delivery
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

    version_package = data.get("version_pkg")
    
    if (name_package != list):
        version_package = f"{data.get('version_pkg')} (lastest)"

    main_package = data.get("__main__")

    print(f"\n{' '*6}Package      : {data.get('name_pkg')}\n{' '*6}Version      : {version_package}")
    print(f"{' '*6}Developer    : {data.get('creador')}")
    
    if (mode_session != None):
        print(f"{' '*6}Description  : {data.get('description')}")

    return version_package, main_package