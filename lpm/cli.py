import os
import sys
import json
import argparse
from importlib import resources
from lpm.source.logic_conection import autentificacion_local
from lpm.source.logic_local import search_packageLpm
from lpm.source.animations import animationsBAR_message


# ~~~ Funciones Auxiliares ~~~

def load_json():
    try:
        with resources.files("lpm.source") \
            .joinpath("config.json") \
            .open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] ERROR... NO SE ENCUENTRAN COMPONENTES INTERNOS DE LPM")
        sys.exit(1)

def icon():
    data = load_json()
    for i in data["icon"]:
        print(f"{' '*6}{i}")

def clear():
    os.system("clear")

def sourcelpm_client():
    enlace = os.path.expanduser("~/.lpm")
    name_credentials = ".credentials"

    os.makedirs(enlace, exist_ok=True)
    return os.path.join(enlace, name_credentials)


# ~~~ Funciones de configuracion de entorno

def create_credentials(file_path):
    id_client = input(f"\n{' '*14} [ID client]: ")
    print(f"{' '*16} |_ID_CLIENT_| -> [ {id_client} ]")
    token_client = input(f"\n{' '*14} [TOKEN Client]: ")
    print(f"{' '*16} |_TOKEN_CLIENT_| -> [ {token_client} ]")

    animationsBAR_message(f"[!] Configurando credenciales locales", "[ OK ] Credenciales establecidas", 12)

    data = { "id_client": id_client, "token_secret": token_client }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    os.chmod(file_path, 0o600)
    return data


def verify_credentials():
    file_path = sourcelpm_client()

    if (not os.path.isfile(file_path)):
        data = create_credentials(file_path)

    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            print(f"{' '*16} [!] Credenciales corruptas, recreando…")
            data = create_credentials(file_path)

    return data["id_client"], data["token_secret"]




# ~~~ Argumentos y funciones ~~~

def delivery_install(args):
    id_client, token_secret = verify_credentials()
    autentificacion_local(id_client, token_secret, "install", args.name)

def delivery_search(args):
    id_client, token_secret = verify_credentials()
    autentificacion_local(id_client, token_secret, "search", args.name)

def delivery_list(args):
    search_packageLpm()

def cmd_publish(args):
    print("Publicando paquete actual…")
    # Tu lógica de publicación




def cmd_remove(args):
    print(f"Desinstalando el paquete {args.name}...")


def main():
    icon()
    print()
    
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
