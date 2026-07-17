import json
from pathlib import Path

BASE = Path(__file__).parent.parent
MEMORY_FILE = BASE / "memory" / "historial.json"
MEMORY_FILE.parent.mkdir(exist_ok=True)

def guardar(rol: str, texto: str):
    historial = cargar()
    historial.append({"rol": rol, "texto": texto})
    # Mantiene solo últimos 200 mensajes
    if len(historial) > 200:
        historial = historial[-200:]
    MEMORY_FILE.write_text(json.dumps(historial, ensure_ascii=False, indent=2))

def cargar():
    try:
        if not MEMORY_FILE.exists() or MEMORY_FILE.stat().st_size == 0:
            return []
        return json.loads(MEMORY_FILE.read_text())
    except json.JSONDecodeError:
        # Si está corrupto, lo resetea
        MEMORY_FILE.write_text("[]")
        return []