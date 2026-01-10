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

    data.setdefault("package_install", {})

    if name_package in data["package_install"]:
        pkg = data["package_install"][name_package]

        if version_package not in pkg["version_instaladas"]:
            pkg["version_instaladas"].append(version_package)

        pkg["version_use"] = version_package
        pkg["__main-use__"] = main

    else:
        data["package_install"][name_package] = {
            "version_use": version_package,
            "version_instaladas": [version_package],
            "__main-use__": main
        }

    func_userConfig("w", data)


# ~~~ flujo principal de instalación ~~~
def main_install(id_client, token_client, package):
    session_id = autentificacion_server(id_client, token_client, "ins")

    # ---- resolver nombre y versión ----
    if isinstance(package, list):
        namePackage = package[0]
        versionPackage = package[1]
    else:
        namePackage = package
        versionPackage = "latest"

    # ---- paso 1: pre-instalación ----
    try:
        response = requests.post(
            f"{URL_BASEDATA}/client/search/install_package",
            json={
                "client_uuidSession": session_id,
                "client_namePackage": namePackage,
                "client_versionPackage": versionPackage
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.HTTPError as e:
        message_animation(
            f"[!] Consultando por el paquete [{namePackage}]",
            f"[ ERROR ] El paquete o la versión no existe",
            3, 4
        )
        sys.exit(1)

    # ---- mostrar información ----
    version_pkg = data.get("version_pkg")
    main_pkg = data.get("__main__")

    message_animation(
        f"[!] Consultando por el paquete [{namePackage}]",
        f"[ OK ] El paquete existe!",
        2, 4
    )

    print(
        f"\n{' '*6}Package      : {data.get('name_pkg')}"
        f"\n{' '*6}Version      : {version_pkg}"
        f"\n{' '*6}Developer    : {data.get('creador')}"
    )

    if not version_pkg or not main_pkg:
        print(f"{' '*6}[ ERROR ] Información incompleta del paquete")
        sys.exit(1)

    # ---- confirmación ----
    validation = input(
        f"\n{' '*4}[!] Desea continuar a la instalacion del package? (y/n): "
    ).strip().lower()

    if validation not in ("y", "s"):
        print(f"{' '*6}[ CANCELADO ] Instalacion abortada por el usuario")
        sys.exit(0)

    # ---- preparar destino ----
    destino = os.path.expanduser(f"~/.lpm/packages/{namePackage}/{version_pkg}")
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"{namePackage}.zip")

    # ---- paso 2: instalación real ----
    try:
        response = requests.post(
            f"{URL_BASEDATA}/client/install_package",
            json={
                "client_uuidSession": session_id,
                "client_namePackage": namePackage,
                "client_versionPackage": version_pkg
            },
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "success":
            print(f"{' '*6}[ ERROR ] Fallo en la instalación")
            sys.exit(1)

        contenido = base64.b64decode(data["contenido_base64"])

        print()
        bar_animation(4, f"Instalando Package {namePackage}... ")

        with open(zip_path, "wb") as f:
            f.write(contenido)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destino)

        os.remove(zip_path)

        # ---- guardar configuración SOLO si todo salió bien ----
        addPackage(namePackage, version_pkg, main_pkg)

        print(
            f"\n{' '*4}[ OK ] Package instalado correctamente"
            f"\n{' '*5}Name   : {data.get('nombre_archivo')}"
            f"\n{' '*5}Size   : {data.get('tamaño_bytes')} bytes"
        )

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        if e.response is not None:
            print(f"   Detalles: {e.response.text}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
