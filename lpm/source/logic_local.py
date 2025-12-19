import os
import sys
import json

# ~~ Variables Globales
LOCAL_SOURCES = os.path.expanduser("~/.lpm")
SOURCE_REGISTRY = ".lpm_Userpackage"


# ~ Funciones de administrador de package

def save_lpm(data):
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    path_registros = os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)

    with open(path_registros, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def lpm_Userpackage():
    os.makedirs(LOCAL_SOURCES, exist_ok=True)
    path_registros = os.path.join(LOCAL_SOURCES, SOURCE_REGISTRY)

    with open(path_registros, "r", encoding="utf-8") as f:
        return json.load(f)
    



# ~~ funciones de administrador de registros

def add_package(name_package, version_package, main):
    data = lpm_Userpackage()

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

    save_lpm(data)


def search_packageLpm():
    data = lpm_Userpackage()

    print(f"{' '*4}[!] Listando todos los paquetes\n")

    print(f"{' '*6}[Name Package]{' '*9}[Version]  \n{' '*6}{'-'*22} {'-'*12}")

    for name, info in data["package_install"].items():
        for clave, valor in info.items():
            if (clave == "version_use"):
                print(f"{' '*7}{name}{' '*(22 - len(name))}{valor}\n")








