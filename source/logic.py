import os
import sys
import shutil
import tempfile
import requests
import subprocess

# ~~~ modulos internos de lpm ~~~
from source.logics.func_use import main_use
from source.logics.func_list import main_list
from source.logics.func_remove import main_remove
from source.logics.func_search import main_search
from source.logics.func_update import main_update
from source.logics.func_install import main_install

from source.modules.controller import verify_userConfig
from source.modules.load_config import load_config, load_configRepo, check_newVersion




# ~~ VARIABLES GLOBALES ~~
CONFIG_JSON = load_config()



# ~~~~ Funciones Principales ~~~~

def verify_credentials(function, name_package):

    id_client, token_client = verify_userConfig()
    
    if (function == "install"):
        main_install(id_client, token_client, name_package)
    elif (function == "search"):
        main_search(id_client, token_client, name_package)
    elif (function == "list"):
        main_list()
    elif (function == "update"):
        main_update()
    elif (function == "remove"):
        main_remove()
    elif (function == "use"):
        main_use(name_package)
    



def lpm_upgrade():
    home = os.path.expanduser("~")
    config_jsonRepo = load_configRepo()

    repo = CONFIG_JSON["urls"]["logic"]["repo_oficial"]
    program_dir = os.path.join(home, ".lpm", "program")

    temp_dir = tempfile.mkdtemp(prefix="lpm_install_")
    cwd = os.getcwd()

    try:
        print(f"{' '*4}[!] Iniciando autoinstalación")
        print(f"{' '*6}Version actual ---> {CONFIG_JSON['info']['version']}")
        print(f"{' '*6}Version lastest --> {config_jsonRepo['info']['version']}")
        print(f"\n{' '*6}[ {repo} ]")

        subprocess.run(["git", "clone", "--depth", "1", repo, temp_dir], check=True)
        print(f"{' '*4}[!] Instalando actualización")

        if os.path.exists(program_dir):
            shutil.rmtree(program_dir)

        shutil.copytree(temp_dir, program_dir)

        venv_python = os.path.join(program_dir, "lpm_venv", "bin", "python")
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "requests"], check=True)

        print(f"{' '*4}[ OK ] Actualizado correctamente")

    finally:
        os.chdir(cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)

    sys.exit(0)




def lpm_version():
    version = CONFIG_JSON["info"]["version"]
    info_newVersion = check_newVersion()

    print(f"{' '*4}Version: {version}")

    if (info_newVersion != False):
        print(f"{' '*4}{info_newVersion}")
    
    print(f"{' '*6}lpm packages by nesantime")
    sys.exit(0)