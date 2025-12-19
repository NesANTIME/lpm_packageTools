import os
import sys
import json
import argparse
from lpm.source.logic_conection import autentificacion_local
from lpm.source.logic_local import search_packageLpm, save_lpm, use_packageLpm
from lpm.source.animations import animationsBAR_message


# ~~ Variables Globales 
LOCAL_SOURCES = os.path.expanduser("~/.lpm")
SOURCE_REGISTRY = ".lpm_Userpackage"

DATA = { "icon": [ "┬  ┌─┐┌┬┐", "│  ├─┘│││", "┴─┘┴  ┴ ┴" ], "version": "1.2.0" }


# ~~~ Funciones Auxiliares ~~~

def icon():
    for i in DATA["icon"]:
        print(f"{' '*4}{i}")

def clear():
    os.system("clear")

def userPackage():
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    return os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)

def validate_idClient(id):
    if (len(id) != 14):
        return False
    if (id[0] != "l"):
        return False
    if (id[7] != "p"):
        return False
    if (id[-1] != "m"):
        return False
    return True

def validate_tokenClient(token):
    return token.startswith("L") and len(token) >= 30



# ~~~ Funciones de credenciales lpm

def create_credentials(file_path): 
    print(f"{' '*4}[!] Iniciando configuración de LPM\n")

    id_client = input(f"{' '*6}[ID Client]: ").strip()

    if (not validate_idClient(id_client)):
        print(f"{' '*4}[LPM][CONFIG][ID_CLIENT] --> ID_Client inválido")
        sys.exit(1)
    print(f"{' '*7}[LPM][CONFIG]>[ID_CLIENT] --> [ {id_client} ]")

    token_client = input(f"\n{' '*6}[TOKEN Client]: ").strip()

    if (not validate_tokenClient(token_client)):
        print(f"{' '*4}[LPM][CONFIG][TOKEN_CLIENT] --> Token inválido")
        sys.exit(1)
    print(f"{' '*7}[LPM][CONFIG]>[TOKEN_CLIENT] --> [ OK ]\n")

    animationsBAR_message("[!] Configurando credenciales locales", "[ OK ] Credenciales establecidas", 3 ,6)

    data = {"credentials": {"id_client": id_client, "token_secret": token_client}, "package_install": {}}

    save_lpm(data)

    os.chmod(file_path, 0o600)
    return data


def verify_credentials():
    file_path = userPackage()

    if (not os.path.isfile(file_path)):
        data = create_credentials(file_path)

    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            print(f"{' '*6} [!] Credenciales corruptas, recreando…")
            data = create_credentials(file_path)

    return data["credentials"]["id_client"], data["credentials"]["token_secret"]




# ~~~ Argumentos y funciones ~~~

def delivery_install(args):
    id_client, token_secret = verify_credentials()
    autentificacion_local(id_client, token_secret, "install", args.name)

def delivery_search(args):
    id_client, token_secret = verify_credentials()
    autentificacion_local(id_client, token_secret, "search", args.name)

def delivery_list(args):
    id_client, token_secret = verify_credentials()
    search_packageLpm()

def delivery_use(args):
    id_client, token_secret = verify_credentials()
    use_packageLpm(args.name)
    






def cmd_remove(args):
    print(f"Desinstalando el paquete {args.name}...")


def main():
    icon()
    
    parser = argparse.ArgumentParser(
        prog="lpm",
        description="Administrador de paquetes privado hecho por NesAnTime."
    )
    subparsers = parser.add_subparsers(dest="command")

    # lpm install <paquete>
    install_parser = subparsers.add_parser("install", help="[!] Instala un paquete.")
    install_parser.add_argument("name")
    install_parser.set_defaults(func=delivery_install)

    # lpm update <paquete>
    search_parser = subparsers.add_parser("search", help="Busca un paquete.")
    search_parser.add_argument("name")
    search_parser.set_defaults(func=delivery_search)

    # lpm use <paquete>
    search_parser = subparsers.add_parser("use", help="Ejecuta un paquete.")
    search_parser.add_argument("name")
    search_parser.set_defaults(func=delivery_use)

    # lpm remove <paquete>
    remove_parser = subparsers.add_parser("remove", help="Desinstalar un paquete.")
    remove_parser.add_argument("name")
    remove_parser.set_defaults(func=cmd_remove)

    # lpm list
    list_parser = subparsers.add_parser("list", help="Listar los paquetes instalados.")
    list_parser.set_defaults(func=delivery_list)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
