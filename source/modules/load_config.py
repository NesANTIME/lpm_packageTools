import json
import requests
from pathlib import Path

# ~~ VARIABLES GLOBALES
PATH_PROGRAM = Path(__file__).resolve().parent.parent


def load_config():
    config_json = PATH_PROGRAM / "config.json"
    with config_json.open("r", encoding="utf-8") as f:
        return json.load(f)
    

def load_configRepo(config_json):
    try:
        response = requests.get(config_json['urls']['logic']['config_jsonRepo'], timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("[!] Tiempo de espera agotado al descargar el JSON")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"[!] Error HTTP al descargar JSON: {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"[!] Error de red: {e}")
    except ValueError:
        raise RuntimeError("[!] El contenido descargado no es un JSON válido")
    
    


# ~~~~~ Funciones auxiliares externas ~~~~~

def check_newVersion():
    config_json = load_config()
    config_jsonRepo = load_configRepo(config_json)
    

    version_local = config_json["info"]["version"]
    version_lastest = config_jsonRepo["info"]["version"]

    if (version_local != version_lastest):
        return f"[!] Nueva version {version_lastest} disponible!"
    
    return False