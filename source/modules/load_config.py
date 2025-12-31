import json
from pathlib import Path

# ~~ VARIABLES GLOBALES
PATH_PROGRAM = Path(__file__).resolve().parent


def load_config():
    config_json = PATH_PROGRAM / "config.json"
    with config_json.open("r", encoding="utf-8") as f:
        return json.load(f)