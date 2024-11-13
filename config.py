#Configuracion que servira para guardar y borrar datos

import json

archive_name = "config.json"

def load_settings():
    try:
        with open(archive_name, "r") as archive:
            settings = json.load(archive)
        return settings
    except FileNotFoundError:
        #Config predeterminada si el archivo no existe
        return {"volume": 0.5, "skin": "default", "score": 0}

def save_settings(settings):
    with open(archive_name, "w") as archive:
        json.dump(settings, archive, indent=4)
        
def reset_score():
    settings = load_settings()
    settings["score"] = 0
    save_settings(settings)

