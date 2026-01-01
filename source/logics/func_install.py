import os
import sys
import base64
import zipfile
import requests


# ~~~ modulos internos de lpm ~~~
from source.animations import bar_animation
from source.logics.func_search import main_search
from source.modules.controller import func_userConfig
from source.modules.conections_core import autentificacion_server, URL_BASEDATA




# ~~~ funciones auxiliares ~~~
def addPackage(name_package, version_package, main):
    data = func_userConfig("r", None)

    if (name_package in data.get("package_install", {})):
        if (version_package not in data["package_install"][name_package]["version_instaladas"]):
            data["package_install"][name_package]["version_instaladas"].append(version_package)

        data["package_install"][name_package]["version_use"] = version_package
        data["package_install"][name_package]["__main-use__"] = main

    else:
        data["package_install"][name_package] = {
            "version_use": version_package,
            "version_instaladas": [version_package],
            "__main-use__": main
        }

    func_userConfig("w", data)




def main_install(id_client, token_client, name_package):
    session_id = autentificacion_server(id_client, token_client, "install")
    lastest_package, main_package = main_search(id_client, token_client, name_package)

    if (not lastest_package) or (not main_package):
        sys.exit(1)

    destino = os.path.expanduser(f"~/.lpm/{name_package}/{lastest_package}")
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"{name_package}.zip")

    addPackage(name_package, lastest_package, main_package)

    try:
        response = requests.post(f"{URL_BASEDATA}/install_packet", json={
            "id_session": session_id, 
            "name_packet": name_package, 
            "version_packet": lastest_package
        }, timeout=20)

        response.raise_for_status()
        data = response.json()

        if (data.get("status") != "success"):
            print(f"{' '*14} [ ERROR ] {data.get('status')}")
            sys.exit(1)
            
        nombre_archivo = data.get("nombre_archivo")
        tamaño = data.get("tamaño_bytes")
        contenido_base64 = data.get("contenido_base64")

        contenido = base64.b64decode(contenido_base64)

        validation = input(f"\n{' '*4}[!] Desea continuar a la instalacion del package? (y/n): ").strip
        if (validation == "n"):
            print(f"{' '*6}[ ERROR ] Instalacion cancelada por el usuario! ")
            sys.exit(1)

        bar_animation(4, "Instalando Package... ")
            
        with open(zip_path, "wb") as f:
            f.write(contenido)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destino)

        os.remove(zip_path)

        print(f"[ OK ] Package installed successfully \n{' '*5}Name   : {nombre_archivo}\n{' '*5}Size   : {tamaño} bytes")    
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalles: {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")