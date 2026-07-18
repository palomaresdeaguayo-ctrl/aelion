from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from brain.agent import agent
import os

app = FastAPI(title="Aelion Torre")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    user_id: str = "pablo_torre"

@app.get("/", response_class=HTMLResponse)
async def home():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Aelion Torre Activo 🐺</h1>"

@app.post("/chat")
async def chat_endpoint(chat_msg: ChatMessage):
    try:
        respuesta = await agent.procesar(chat_msg.message)
        return JSONResponse(content={"response": respuesta})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/ping")
async def ping():
    return {"status": "Aelion Torre Activo 🐺"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
