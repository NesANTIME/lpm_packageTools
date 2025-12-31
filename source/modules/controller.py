import os
import sys
import json
import subprocess

# ~~ modulos internos lpm ~~
from source.logic import load_config
from source.animations import message_animation


# ~~~~ VARIABLES GLOBALES ~~~~
LOCAL_SOURCES = os.path.expanduser(load_config["urls"]["controller"][0])
SOURCE_REGISTRY = load_config["urls"]["controller"][1]



# ~~~ funciones auxiliaries para userConfig ~~~

def return_userConfig():
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    return os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)


def func_userConfig(modo, data):
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    path_registros = os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)

    with open(path_registros, modo, encoding="utf-8") as f:
        if (modo == "w"):
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            return json.load(f)
        



# ~~~ funciones auxiliaries para credentials ~~~

def create_credentials(file_path): 

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

    message_animation("[!] Configurando credenciales locales", "[ OK ] Credenciales establecidas", 3 ,6)

    data = {
        "credentials": {
            "id_client": id_client, 
            "token_secret": token_client
        }, "package_install": {}
    }

    func_userConfig("w", data)
    os.chmod(file_path, 0o600)

    return data




# ~~~ funciones principales ~~~

def verify_userConfig():
    file_path = return_userConfig()
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