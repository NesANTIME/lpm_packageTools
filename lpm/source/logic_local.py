import os
import sys
import json

# ~ Funciones de administrador de package json

def save_lpm(data):
    enlace = os.path.expanduser("~/.lpm")
    name_registreLpm = ".packageRegistre_lpm"

    os.makedirs(enlace, exist_ok=True)
    path_registros = os.path.join(enlace, name_registreLpm)

    with open(path_registros, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def registre_lpm():
    enlace = os.path.expanduser("~/.lpm")
    name_registreLpm = ".packageRegistre_lpm"

    os.makedirs(enlace, exist_ok=True)
    path_registros = os.path.join(enlace, name_registreLpm)

    if (not os.path.isfile(path_registros)):
        date = { "list_package": {} }
        save_lpm(date)

        os.chmod(path_registros, 0o600)
    
    else:
        try:
            with open(path_registros, "r", encoding="utf-8") as f:
                data = json.load(f)

        except (json.JSONDecodeError, ValueError):
            registre_lpm()
        
        return data
    



# ~~ funciones de administrador de registros

def add_packageAtLpm(name_package, version_package, main):
    data = registre_lpm()

    if (name_package in data.get("list_package", {})):

        if (not name_package in data.get("list_package", {}).get("version_instaladas", [])):
            data["list_package"][name_package]["version_instaladas"].append(version_package)
        data["list_package"][name_package]["version_use"] = version_package
        data["list_package"][name_package]["__main-use__"] = main

    else:
        data["list_package"][name_package] = {
            "version_use": version_package,
            "version_instaladas": [version_package],
            "__main-use__": main
        }

    save_lpm(data)


def search_packageLpm():
    data = registre_lpm()

    print(f"{' '*12} [!] [ LPM ] Listando los paquetes\n")

    for name, info in data["list_package"].items():
        print(f"{' '*14} PAQUETE INSTALADO --> [{name}]")

        for clave, valor in info.items():
            print(f"{' '*16}{clave}: {valor}")

        print()








