from pathlib import Path

LIBROS_PATH = Path(__file__).parent.parent / "libros"

def buscar_en_libros(consulta):
    resultados = []
    if not LIBROS_PATH.exists():
        return "No hay carpeta /libros"
    
    for archivo in LIBROS_PATH.glob("*.txt"):
        try:
            contenido = archivo.read_text(encoding='utf-8', errors='ignore')
            if any(palabra in contenido.lower() for palabra in consulta.lower().split()):
                fragmento = contenido[:600] + "..."
                resultados.append(f"📖 {archivo.name}:\n{fragmento}")
        except:
            continue
    
    return "\n\n".join(resultados[:2]) if resultados else "No encontré nada sobre eso en tus libros"