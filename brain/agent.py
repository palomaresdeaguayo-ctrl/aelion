from brain.llm import pensar
from memory.charla import guardar, cargar
from brain.libros import buscar_en_libros, leer_libro_completo, leer_libro_inteligente
from tools.ejecutar import crear_archivo, leer_archivo, listar, ejecutar
from tools.web import buscar_web
from tools.code import ejecutar_python
from tools.git import git_comando
from pathlib import Path

class Agent:
    def __init__(self):
        self.historial = cargar()

    async def iniciar(self):
        pass

    async def procesar(self, texto):
        guardar("user", texto)
        self.historial.append({"rol": "user", "texto": texto})

        low = texto.lower()

        if texto.startswith("/crear "):
            try:
                _, resto = texto.split("/crear ", 1)
                nombre, contenido = resto.split("|", 1)
                respuesta = crear_archivo(nombre.strip(), contenido.strip())
            except ValueError:
                respuesta = "ERROR: /crear archivo.txt | contenido"

        elif texto.startswith("/leer "):
            respuesta = leer_archivo(texto.replace("/leer ", "").strip())

        elif texto.startswith("/libro "):
            # /libro nombre | capitulo 2 o /libro nombre | busca amor
            resto = texto.replace("/libro ", "").strip()
            if "|" in resto:
                nombre, pet = resto.split("|", 1)
                p = Path(f"libros/{nombre.strip()}.txt")
                if not p.exists():
                    # busca aproximado
                    from brain.libros import _lista_archivos, _normaliza
                    for a in _lista_archivos():
                        if _normaliza(nombre) in _normaliza(a.stem):
                            p = a
                            break
                if p.exists():
                    respuesta = leer_libro_inteligente(p, busqueda=pet, consulta=pet)
                else:
                    respuesta = f"No encontré libro {nombre}"
            else:
                respuesta = leer_libro_completo(resto)

        elif texto.startswith("/ls"):
            carpeta = texto.split()[1] if len(texto.split())>1 else "sandbox"
            respuesta = listar(carpeta)

        elif texto.startswith("/cmd "):
            respuesta = ejecutar(texto.replace("/cmd ", "").strip())

        elif texto.startswith("/google "):
            q = texto.replace("/google ", "").strip()
            respuesta = buscar_web(q) if q else "ERROR: /google query"

        elif texto.startswith("/python "):
            cod = texto.replace("/python ", "").strip()
            out = ejecutar_python(cod)
            respuesta = f"```python\n{cod}\n```\nOutput:\n```\n{out}\n```"

        elif texto.startswith("/git "):
            args = texto.replace("/git ", "").strip()
            out = git_comando(args)
            respuesta = f"$ git {args}\n{out}"

        else:
            contexto = "\n".join([f"{m['rol']}: {m['texto']}" for m in self.historial[-8:]])

            if any(k in low for k in ['libro','obra','capitulo','capítulo','poema','cuento','novela','vers','arte borin','benito','katherine','pacto','venganza','rosa','brindis','eterna','arrimado']):
                info = buscar_en_libros(texto)
                prompt = f"""Eres Aelion. Agente de Pablo Aguayo, escritor.

Historial:
{contexto}

DATOS REALES DE /libros (USA SOLO ESTO, NO INVENTES):
{info}

Pregunta: {texto}

REGLAS:
- Lista exacta, no inventes títulos.
- Si te piden leer/discutir un capítulo/poema, usa el texto de DATOS REALES para analizar.
- Si el texto es corto (poema), citalo y luego opina.
- Si es largo, resume y discute tema, estilo, símbolos.
- Habla como carnal culto de Puebla, directo, sin rodeos.
"""
            else:
                prompt = f"""Eres Aelion. Agente de Pablo Aguayo.
Historial:
{contexto}
Pregunta: {texto}
Responde directo, útil. Comandos: /crear /leer /libro nombre | capitulo X /ls /cmd /google /python /git"""

            respuesta = pensar(prompt)

        guardar("assistant", respuesta)
        self.historial.append({"rol": "assistant", "texto": respuesta})
        return respuesta

agent = Agent()
