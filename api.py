import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from brain.agent import agent

app = FastAPI(title="Aelion API", version="1.0.0")

# CORS para que tu frontend no truene
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sirve tu index.html y archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo para recibir mensajes
class ChatMessage(BaseModel):
    message: str
    user_id: str = "default"

# ENDPOINT DE VERIFICACIÓN - Para ver Python version en Render
@app.get("/python-version")
def python_version():
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "env_port": os.getenv("PORT", "No PORT env"),
        "groq_key_exists": bool(os.getenv("GROQ_API_KEY"))
    }

# ENDPOINT STATUS - Health check
@app.get("/status")
def status():
    return {"status": "Aelion online", "lobo": "activo 🐺"}

# ENDPOINT RAÍZ - Sirve tu index.html
@app.get("/")
async def root():
    return FileResponse("index.html")

# ENDPOINT PRINCIPAL DE CHAT - Aquí habla Aelion
@app.post("/chat")
async def chat(chat_msg: ChatMessage):
    try:
        respuesta = agent(chat_msg.message, chat_msg.user_id)
        return JSONResponse(content={"response": respuesta})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Aelion tropezó: {str(e)}"}
        )

# Si corres local: uvicorn api:app --reload
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port)