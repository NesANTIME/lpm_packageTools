import os
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

    result_packages = funcDelivery_update(id_client, token_client, list_packages)

    print(f"{' '*6}[Name Package]{' '*9}[Version]{' '*13}[Lastest]    \n{' '*6}{'-'*20}{' '*3}{'-'*19}{' '*3}{'-'*20}")
    list_packages_server = result_packages["list_packages"]


    for name_package, version_latest_package in list_packages_server.items():
        paquete_local = data["package_install"].get(name_package)
        if (not paquete_local):
            continue 

        version_local = paquete_local.get("version_use")
        if (not version_local):
            continue

        print(f"{' '*6}{name_package:<24}{version_local:<21}{version_latest_package}")

    validation = input(f"\n{' '*4}[!] Desea continuar a la actualizacion de los packages? (y/n): ").strip().lower()
    if validation not in ("y", "s"):
        print(f"{' '*6}[ CANCELADO ] Instalacion abortada por el usuario")
        sys.exit(0)

    for name_package, version_latest_package in list_packages_server.items():
        destino = os.path.expanduser(f"~/.lpm/packages/{name_package}/{version_latest_package}")
        os.makedirs(destino, exist_ok=True)
        zip_path = os.path.join(destino, f"{name_package}.zip")

