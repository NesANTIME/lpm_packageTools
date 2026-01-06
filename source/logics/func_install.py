import os
import sys
import base64
import zipfile
import requests


# ~~~ modulos internos de lpm ~~~
from source.modules.controller import func_userConfig
from source.animations import bar_animation, message_animation
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




def main_install(id_client, token_client, package):
    session_id = autentificacion_server(id_client, token_client, "ins")

    if (package == list):
        namePackage = package[0]
        versionPackage = package[1]
    else:
        namePackage = package
        versionPackage = "lastest"


    try:
        response = requests.post(f"{URL_BASEDATA}/client/search/install_package", json={ 
            "client_uuidSession": session_id, 
            "client_namePackage": namePackage,
            "client_versionpackage": versionPackage
        }, timeout=10)

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            message_animation(
                f"[!] Consultando por el paquete [{namePackage}]", 
                f"[ ERROR ] El paquete [{namePackage}] no existe", 3, 4
            )
        sys.exit(1)

    message_animation(f"[!] Consultando por el paquete [{namePackage}]", f"[ OK ] El paquete existe!", 2, 4)

    version_pkg = data.get('version_pkg')
    main_pkg = data.get('__main__')

    if (versionPackage == "lastest"):
        version_package = f"{data.get('version_pkg')} (lastest)"
    else:
        version_package = f"{data.get('version_pkg')}"
    

    print(f"\n{' '*6}Package      : {data.get('name_pkg')}\n{' '*6}Version      : {version_package}")
    print(f"{' '*6}Developer    : {data.get('creador')}")

    if (not version_pkg) or (not main_pkg):
        sys.exit(1)

    validation = input(f"\n{' '*4}[!] Desea continuar a la instalacion del package? (y/n): ").strip()
    if (validation != "y") or (validation != "s"):
        print(f"{' '*6}[ ERROR ] Instalacion cancelada por el usuario! ")
        sys.exit(1)


    destino = os.path.expanduser(f"~/.lpm/packages/{namePackage}/{version_pkg}")
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"{namePackage}.zip")

    addPackage(namePackage, version_pkg, main_pkg)

    try:
        response = requests.post(f"{URL_BASEDATA}/client/install_package", json={
            "client_uuidSession": session_id, 
            "client_namePackage": namePackage,
            "client_versionpackage": version_pkg
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

        print()
        bar_animation(4, "Instalando Package... ")
            
        with open(zip_path, "wb") as f:
            f.write(contenido)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destino)

        os.remove(zip_path)

        print(f"\n{' '*4}[ OK ] Package installed successfully \n{' '*5}Name   : {nombre_archivo}\n{' '*5}Size   : {tamaño} bytes")    
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Detalles: {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")