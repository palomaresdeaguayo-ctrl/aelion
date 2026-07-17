import os
import subprocess
from pathlib import Path

BASE = Path(__file__).parent.parent  # Raíz de Aelion
SAFE_PATHS = [BASE / "sandbox", BASE / "libros", BASE / "memory"]

def es_seguro(path: Path) -> bool:
    """Anti-Lobo: Solo toca carpetas permitidas"""
    path = path.resolve()
    return any(str(path).startswith(str(s.resolve())) for s in SAFE_PATHS)

def crear_archivo(nombre: str, contenido: str) -> str:
    path = (BASE / "sandbox" / nombre).resolve()
    if not es_seguro(path):
        return "ERROR: Ruta no permitida. Solo /sandbox"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contenido, encoding='utf-8')
    return f"Archivo creado: sandbox/{nombre}"

def leer_archivo(nombre: str) -> str:
    path = (BASE / nombre).resolve()
    if not es_seguro(path):
        return "ERROR: Ruta no permitida. Solo /sandbox, /libros, /memory"
    if not path.exists():
        return f"ERROR: {nombre} no existe"
    return path.read_text(encoding='utf-8')[:2000]  # Límite 2KB pa que no se ahogue

def listar(carpeta: str = "sandbox") -> str:
    path = (BASE / carpeta).resolve()
    if not es_seguro(path):
        return "ERROR: Ruta no permitida"
    if not path.exists():
        return f"Carpeta {carpeta} no existe"
    archivos = [f.name for f in path.iterdir()]
    return f"Contenido de {carpeta}/: {', '.join(archivos) if archivos else 'vacía'}"

def ejecutar(comando: str) -> str:
    """Comandos básicos seguros. Nada de rm -rf /"""
    if any(p in comando for p in ['rm ', 'del ', 'format', 'shutdown']):
        return "ERROR: Comando peligroso bloqueado"
    try:
        res = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=5, cwd=BASE)
        return res.stdout or res.stderr or "Sin output"
    except Exception as e:
        return f"ERROR: {str(e)}"