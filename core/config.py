import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    def get(self, key, default=None):
        val = os.getenv(key, default)
        if val is None:
            raise ValueError(f"❌ Falta {key} en.env")
        return val

config = Config()