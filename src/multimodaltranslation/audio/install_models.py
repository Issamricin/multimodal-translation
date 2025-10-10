import os
import zipfile
from pathlib import Path

import requests
from appdirs import user_data_dir

APP_NAME = "multimodaltranslator"

def install_model(model_name: str) -> None:
    base_url = "https://alphacephei.com/vosk/models/"
    model_url = f"{base_url}{model_name}.zip"

    base_dir = Path(user_data_dir(APP_NAME))
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)


    model_dir = os.path.join(models_dir, model_name)
    zip_path = os.path.join(models_dir, f"{model_name}.zip")

    if os.path.exists(model_dir):
        print(f"Model '{model_name}' already exists in '{models_dir}'")
        return

    os.makedirs(models_dir, exist_ok=True)
    print(f"Downloading {model_name}...")

    try:
        with requests.get(model_url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("Extracting model...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(models_dir)

        os.remove(zip_path)
        print(f"Download completed! Model available at: {model_dir}")

    except requests.exceptions.RequestException:
        print("Failed to download model")
        if os.path.exists(zip_path):
            os.remove(zip_path)

