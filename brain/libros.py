from pathlib import Path
import re

LIBROS_PATH = Path(__file__).parent.parent / "libros"

def _lista_archivos():
    if not LIBROS_PATH.exists():
        return []
    return sorted(LIBROS_PATH.glob("*.txt"))

def _normaliza(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())

def buscar_en_libros(consulta):
    archivos = _lista_archivos()
    if not archivos:
        return "No hay carpeta /libros"

    q = consulta.lower()

    # 1. Si solo quiere la lista
    if any(x in q for x in ["que libros", "qué libros", "cuantos libros", "cuántos libros", "lista de libros", "cuales tienes", "cuáles tienes", "que tienes", "que hay en libros"]):
        lista = "\n".join([f"- {a.stem.replace('_',' ')}" for a in archivos])
        return f"Tengo {len(archivos)} libros en /libros:\n{lista}"

    # 2. Si menciona un libro específico, búscalo exacto
    q_norm = _normaliza(q)
    for archivo in archivos:
        nombre_norm = _normaliza(archivo.stem)
        # si el nombre del libro está contenido en la consulta
        if nombre_norm[:8] in q_norm or any(p in nombre_norm for p in q_norm.split() if len(p)>4):
            try:
                contenido = archivo.read_text(encoding='utf-8', errors='ignore')
                # Detecta si pide capitulo/poema/parte específica
                # Ejemplo: "capitulo 3", "poema 2", "parte de la rosa"
                match_cap = re.search(r'(capitulo|capítulo|poema|parte|verso)\s*(\d+|[^\n]+)', q)
                if match_cap:
                    # Devuelve fragmento grande con contexto
                    return leer_libro_inteligente(archivo, busqueda=match_cap.group(0), consulta=q)
                else:
                    # Si no pide parte, da inicio + índice si existe
                    inicio = contenido[:2000]
                    return f"📖 LEYENDO: {archivo.stem.replace('_',' ')}\nTamaño: {len(contenido)} caracteres\n\nINICIO:\n{inicio}\n\n... [Pide 'capitulo X' o 'sigue leyendo' o 'busca Y dentro del libro']"
            except Exception as e:
                return f"Error leyendo {archivo.name}: {e}"

    # 3. Búsqueda temática general
    palabras = [p for p in q.split() if len(p) > 3]
    resultados = []
    for archivo in archivos:
        try:
            contenido = archivo.read_text(encoding='utf-8', errors='ignore').lower()
            if any(p in contenido for p in palabras):
                idx = next((contenido.find(p) for p in palabras if p in contenido), 0)
                frag = contenido[max(0, idx-200): idx+800]
                resultados.append(f"📖 {archivo.stem.replace('_',' ')}:\n...{frag}...\n")
        except:
            continue

    if not resultados:
        return ""
    return "\n---\n".join(resultados[:2])

def leer_libro_inteligente(archivo: Path, busqueda="", consulta=""):
    """Lee un libro y busca una parte específica"""
    contenido = archivo.read_text(encoding='utf-8', errors='ignore')

    # Intenta separar por capítulos comunes
    partes = re.split(r'\n(?=(?:CAP[IÍ]TULO|Capitulo|Poema|CANTO|Parte)\s+\d+|---+|###)', contenido, flags=re.IGNORECASE)

    if busqueda:
        b_norm = busqueda.lower()
        # Busca número
        num = re.search(r'\d+', b_norm)
        if num and int(num.group()) <= len(partes):
            n = int(num.group()) - 1
            return f"📖 {archivo.stem.replace('_',' ')} - {busqueda.upper()}:\n\n{partes[n][:3000]}"
        # Busca texto dentro del libro
        else:
            term = re.sub(r'(capitulo|capítulo|poema|parte|busca|lee|muestrame)\s*', '', consulta, flags=re.I).strip()
            if term:
                idx = contenido.lower().find(term.lower())
                if idx!= -1:
                    return f"📖 {archivo.stem.replace('_',' ')} - encontrado '{term}':\n\n...{contenido[max(0,idx-300):idx+2500]}..."

    # Si no encontró, devuelve info de estructura
    preview = "\n".join([f" {i+1}. {p[:60].strip()}..." for i, p in enumerate(partes[:15])])
    return f"📖 {archivo.stem.replace('_',' ')} tiene {len(partes)} secciones detectadas:\n{preview}\n\nPídeme: 'lee capitulo 2 de {archivo.stem.replace('_',' ')}' o 'busca [tema] en {archivo.stem.replace('_',' ')}'"

def leer_libro_completo(nombre_parcial: str):
    archivos = _lista_archivos()
    q_norm = _normaliza(nombre_parcial)
    for a in archivos:
        if q_norm in _normaliza(a.stem) or _normaliza(a.stem)[:6] in q_norm:
            return a.read_text(encoding='utf-8', errors='ignore')[:8000] # tope seguro
    return "No encontré ese libro"
