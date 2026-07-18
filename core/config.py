import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

# Este utf-8-sig le quita el maldito ﻿ automáticamente
load_dotenv(dotenv_path=ENV_PATH, encoding="utf-8-sig", override=True)

# Fallback manual por si dotenv falla
if not os.getenv("GROQ_API_KEY"):
    try:
        with open(ENV_PATH, "r", encoding="utf-8-sig") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    k = k.strip().lstrip("\ufeff").strip()
                    os.environ[k] = v.strip().strip('"').strip("'")
    except Exception as e:
        print(f"Error leyendo.env manual: {e}")

class Config:
    def get(self, key):
        value = os.getenv(key)
        if not value:
            raise ValueError(f"❌ Falta {key} en.env")
        return value.strip().strip('"').strip("'").lstrip("\ufeff")

config = Config()