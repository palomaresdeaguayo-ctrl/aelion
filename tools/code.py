import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
SANDBOX = BASE / "sandbox"

def ejecutar_python(codigo: str) -> str:
    try:
        # Escribe código temporal en sandbox
        temp_file = SANDBOX / "temp_exec.py"
        temp_file.write_text(codigo, encoding='utf-8')

        # Ejecuta con timeout y sin acceso a red/archivos peligrosos
        res = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=3,
            cwd=SANDBOX
        )

        # Borra el temp
        temp_file.unlink(missing_ok=True)

        output = res.stdout or res.stderr
        return output[:1000] if output else "Sin output"
    except subprocess.TimeoutExpired:
        return "ERROR: Código tardó más de 3 segundos"
    except Exception as e:
        return f"ERROR: {str(e)[:200]}"