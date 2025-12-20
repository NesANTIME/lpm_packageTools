import os
import re
import sys
import shutil
import tempfile
import requests
import subprocess


# ~~ Variables Globales
VERSION = "2.1.0"

URL_REPO = "https://github.com/NesANTIME/lpm_packageTools.git"


# ~~ functions repository ~~

def actualizar_lpm():
    cmd = ["git", "clone", "--depth", "1"]
    temp_dir = tempfile.mkdtemp(prefix="install_")

    print(f"{' '*4}[!] Iniciando actualizacion!")

    cmd.extend([URL_REPO, temp_dir])

    subprocess.run(cmd, check=True, capture_output=True)
    os.chdir(temp_dir)

    subprocess.run([sys.executable, "-m", "pip", "install", "."], check=True, capture_output=True)

    os.chdir("..")
    shutil.rmtree(temp_dir)

    print(f"{' '*4}[ OK ] Actualizado Correctamente!")


def verifyVersion():
    try:
        reponse = requests.get("https://raw.githubusercontent.com/NesANTIME/lpm_packageTools/refs/heads/main/lpm/source/upgrade.py")
        reponse.raise_for_status()

        content = reponse.text
        pattern = rf'{re.escape(VERSION)}\s*=\s*(.+)'
        match = re.search(pattern, content)

        if (match):
            return match.group(1).strip()
        
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
    except Exception as e:
        return False
    
def version_lpm():
    print(f"{' '*4}[!] Version: {VERSION}")