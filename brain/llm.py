from groq import Groq
from core.config import config

client = Groq(api_key=config.get('GROQ_API_KEY'))

def pensar(prompt, sistema="Eres Aelion. Respondes directo, en español mexicano, cabrón pero útil."):
    respuesta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )
    return respuesta.choices[0].message.content