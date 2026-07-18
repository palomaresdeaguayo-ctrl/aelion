import asyncio
from brain.agent import agent

async def main():
    print("🐺 AELION TORRE - Modo local activo")
    print("Escribe 'salir' para terminar\n")

    if hasattr(agent, 'iniciar'):
        try:
            await agent.iniciar()
        except Exception as e:
            print(f"Nota iniciar: {e}")

    while True:
        try:
            tu = input("Tú: ")
            if tu.lower() in ["salir", "exit", "quit"]:
                print("Aelion: Nos vemos en la sombra, lobo.")
                break
            if not tu.strip():
                continue
            
            respuesta = await agent.procesar(tu)
            print(f"\nAelion: {respuesta}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
