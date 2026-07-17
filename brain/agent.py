from brain.llm import pensar
from memory.charla import guardar, cargar
from brain.libros import buscar_en_libros
from tools.ejecutar import crear_archivo, leer_archivo, listar, ejecutar
from tools.web import buscar_web
from tools.code import ejecutar_python
from tools.git import git_comando

class Agent:
    def __init__(self):
        self.historial = cargar()

    async def iniciar(self):
        pass

    async def procesar(self, texto):
        # 1. Guarda input del user
        guardar("user", texto)
        self.historial.append({"rol": "user", "texto": texto})

        # 2. COMANDOS DE TOOLS - Prioridad sobre LLM
        if texto.startswith("/crear "):
            try:
                _, resto = texto.split("/crear ", 1)
                nombre, contenido = resto.split("|", 1)
                respuesta = crear_archivo(nombre.strip(), contenido.strip())
            except ValueError:
                respuesta = "ERROR: Formato: /crear archivo.txt | contenido aquí"

        elif texto.startswith("/leer "):
            nombre = texto.replace("/leer ", "").strip()
            respuesta = leer_archivo(nombre)

        elif texto.startswith("/ls"):
            partes = texto.split()
            carpeta = partes[1] if len(partes) > 1 else "sandbox"
            respuesta = listar(carpeta)

        elif texto.startswith("/cmd "):
            comando = texto.replace("/cmd ", "").strip()
            respuesta = ejecutar(comando)

        elif texto.startswith("/google "):
            query = texto.replace("/google ", "").strip()
            if not query:
                respuesta = "ERROR: Uso: /google tu búsqueda"
            else:
                respuesta = buscar_web(query)

        elif texto.startswith("/python "):
            codigo = texto.replace("/python ", "").strip()
            if not codigo:
                respuesta = "ERROR: Uso: /python print('hola')"
            else:
                resultado = ejecutar_python(codigo)
                respuesta = f"```python\n{codigo}\n```\n\nOutput:\n```\n{resultado}\n```"

        elif texto.startswith("/git "):
            args = texto.replace("/git ", "").strip()
            if not args:
                respuesta = "ERROR: Uso: /git status | /git add. | /git commit -m 'msg'"
            else:
                resultado = git_comando(args)
                respuesta = f"```bash\n$ git {args}\n```\n\n```\n{resultado}\n```"

        else:
            # 3. FLUJO NORMAL CON LLM
            contexto = "\n".join([f"{m['rol']}: {m['texto']}" for m in self.historial[-6:]])

            # Detecta si pregunta por libros
            if any(p in texto.lower() for p in ['libro', 'obra', 'escribí', 'capítulo', 'cuento', 'novela', 'arte', 'benito']):
                info_libros = buscar_en_libros(texto)
                prompt = f"""Eres Aelion. Agente de Pablo Aguayo.

Historial reciente:
{contexto}

Información encontrada en /libros:
{info_libros}

Pregunta actual: {texto}

Instrucciones: Responde directo, mexicano, sin rodeos. Si te piden hacer algo, usa tus comandos disponibles."""

            else:
                prompt = f"""Eres Aelion. Agente de Pablo Aguayo.

Historial reciente:
{contexto}

Pregunta actual: {texto}

Instrucciones: Responde directo, mexicano, útil. Tienes estos comandos:
- /crear archivo.txt | contenido
- /leer ruta/archivo.txt
- /ls carpeta
- /cmd comando
- /google búsqueda web
- /python código a ejecutar
- /git status|add|commit|log|diff

Si el user pide algo que puedes hacer con comandos, hazlo o explícale cómo."""

            respuesta = pensar(prompt)

        # 4. Guarda respuesta
        guardar("assistant", respuesta)
        self.historial.append({"rol": "assistant", "texto": respuesta})
        return respuesta

agent = Agent()

# Modo consola opcional
async def modo_consola():
    await agent.iniciar()
    print("🧠 Aelion v1.4 online. Tools avanzadas: /google /python /git")
    while True:
        texto = input("Tú: ")
        if texto.lower() in ['salir', 'exit']:
            break
        respuesta = await agent.procesar(texto)
        print(f"\n🤖 Aelion: {respuesta}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(modo_consola())