import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def buscar_web(query: str) -> str:
    try:
        # DuckDuckGo HTML - no API key, no bloquea
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(r.text, 'html.parser')
        resultados = []

        for result in soup.find_all('div', class_='result')[:3]:
            titulo = result.find('a', class_='result__a')
            snippet = result.find('a', class_='result__snippet')
            if titulo:
                resultados.append(f"- {titulo.get_text().strip()}")
                if snippet:
                    resultados.append(f" {snippet.get_text().strip()[:150]}...")

        return "\n".join(resultados) if resultados else "Sin resultados"
    except Exception as e:
        return f"ERROR web: {str(e)[:100]}"