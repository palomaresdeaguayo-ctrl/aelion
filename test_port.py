fastapi
uvicorn
groq
python-dotenv
' | Set-Content -Path "requirements.txt" -Encoding UTF8

@'
import os
port = int(os.environ.get("PORT", 8000))
