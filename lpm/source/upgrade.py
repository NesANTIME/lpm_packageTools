import os
import sys
import shutil
import tempfile
import subprocess


# ~~ Variables Globales
VERSION = "1.2.0"

LOCAL_SOURCES = os.path.expanduser("~/.lpm")
URL_REPO = "https://github.com/NesANTIME/lpm_packageTools.git"


# ~~ functions repository ~~

def clone_repository():
    cmd = ["git", "clone", "--depth", "1"]
    temp_dir = tempfile.mkdtemp(prefix="install_")

    print(f"{' '*4}[!] Iniciando actualizacion!")

    cmd.extend([URL_REPO, temp_dir])

    subprocess.run(cmd, check=True, capture_output=True)
    os.chdir(temp_dir)

    subprocess.run([sys.executable, "-m", "pip", "install", "."], check=True, capture_output=True)

    os.chdir("..")
    shutil.rmtree(temp_dir)


def verityVersion():
    return