import os
import sys
import time
import json
import subprocess

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
    
def verifypackage_use(name):
    data = lpm_Userpackage()

    if (name in data.get("package_install", {})):
        package = data["package_install"][name]

        main = package.get("__main-use__")
        version = package.get("version_use")

        rut = os.path.join(LOCAL_SOURCES, name, version, main)

        if os.path.isfile(rut):
            return rut
        else:
            print(f"{' '*4}[ ERROR ] Archivo principal no encontrado")

    else:
        print(f"{' '*4}[ ERROR ] El paquete no se encuentra instalado o no existe!")

    



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


def use_packageLpm(comando):
    print(f"{' '*4}[ OK ] Running...")
    time.sleep(2)
    subprocess.run(comando)
    

def remove_packageLpm(name_package):
    data = lpm_Userpackage()
    if (name_package in data.get("package_install", {})):
        package = data["package_install"][name_package]
        version = package.get("version_use")

        rut = os.path.join(LOCAL_SOURCES, name_package, version)
        if os.path.isfile(rut):
            os.remove(rut)
            
            if (name_package in data.get("package_install", {})):
                if (version in data["package_install"][name_package]["version_instaladas"]):
                    data["package_install"][name_package]["version_instaladas"].remove(version)
                    data["package_install"][name_package]["version_use"] = data["package_install"][name_package]["version_instaladas"][-1]
                
                else:
                    data["package_install"][name_package].remove()

                save_lpm(data)
            
        else:
            print(f"{' '*4}[ ERROR ] No se puede eliminar un paquete que no existe!")

    else:
        print(f"{' '*4}[ ERROR ] El paquete no se encuentra instalado o no existe!")

