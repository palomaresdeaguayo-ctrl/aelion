import asyncio
from brain.agent import agent

async def main():
    print("="*50)
    print("🚀 AELION v1 - MODO TEXTO")
    print("Tus libros están en /libros")
    print("Escribe 'salir' para terminar")
    print("="*50)

    await agent.iniciar()

    while True:
        try:
            texto = input("Tú: ").strip()
            if texto.lower() in ['salir', 'exit', 'quit']:
                print("🤖 Aelion: Nos vemos ingg")
                break
            if texto:
                await agent.procesar(texto)
        except KeyboardInterrupt:
            print("\n🤖 Aelion: Apagado forzoso")
            break

if __name__ == "__main__":
    asyncio.run(main())