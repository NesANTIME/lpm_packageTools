import sys
import requests

from source.modules.controller import func_userConfig
from source.modules.conections_core import autentificacion_server, URL_BASEDATA


def funcDelivery_update(id_client, token_client, list_packages):
    session_id = autentificacion_server(id_client, token_client, "upd")

    try:
        response = requests.post(f"{URL_BASEDATA}/client/search/update_package", json={
            "client_uuidSession": session_id, 
            "client_listPackages": list_packages
        }, timeout=10)

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
           print(f"{' '*4}[!] Error en la peticion")         
        sys.exit(1)

    return data





def main_update(id_client, token_client):
    data = func_userConfig("r", None)
    list_packages = []

    print(f"{' '*4}[!] Verificando versiones de los paquetes instalados!\n")

    for name, info in data["package_install"].items():
        list_packages.append(name)

    print(f"{' '*6}[Name Package]{' '*9}[Version]{' '*13}[Lastest]    \n{' '*6}{'-'*20}{' '*3}{'-'*19}{' '*3}{'-'*20}")

    result_packages = funcDelivery_update(id_client, token_client, list_packages)
    list_packages_server = result_packages["list_packages"]

    for name_package, version_package in list_packages_server.items():
        print(name_package, version_package)
