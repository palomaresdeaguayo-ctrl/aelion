import subprocess
from pathlib import Path

BASE = Path(__file__).parent.parent

def git_comando(args: str) -> str:
    # Solo comandos seguros
    permitidos = ['status', 'add', 'commit', 'log', 'diff', 'branch']
    cmd = args.split()[0] if args else ""

    if cmd not in permitidos:
        return f"ERROR: Solo permito: {', '.join(permitidos)}"

    try:
        res = subprocess.run(
            f"git {args}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            cwd=BASE
        )
        output = res.stdout or res.stderr
        return output[:1500] if output else "Sin cambios"
    except Exception as e:
        return f"ERROR git: {str(e)[:100]}"