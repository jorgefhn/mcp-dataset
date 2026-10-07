import requests
import re
import json

url = "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md"
readme_texto = requests.get(url).text

patron = r"\[([^\]]+)\]\((https://github\.com/[^\)]+)\)"
coincidencias = re.findall(patron, readme_texto)

servidores = {}
for nombre, link in coincidencias:
    link_limpio = link.rstrip("/")
    match_repo = re.match(r"https://github\.com/([^/]+)/([^/]+)$", link_limpio)
    if not match_repo:
        continue
    usuario, repo = match_repo.groups()
    if repo.lower().startswith("awesome-"):
        continue
    servidores[link_limpio] = nombre

print(f"Servidores únicos: {len(servidores)}")

with open("servidores_mcp.json", "w", encoding="utf-8") as f:
    json.dump(servidores, f, indent=2, ensure_ascii=False)