import json, os, random, re, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

token = os.environ.get("GITHUB_TOKEN")   # <-- lee el token de la variable de entorno
headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

# --- sesión con reintentos automáticos ---
session = requests.Session()
retries = Retry(total=4, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

with open("servidores_mcp.json", encoding="utf-8") as f:
    servidores = json.load(f)          # {url: nombre}

urls = list(servidores.keys())
random.seed(42)                        # misma muestra cada vez que lo ejecutes
random.shuffle(urls)

piloto = []
counter = 0
for url in urls:
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)$", url)
    if not m:
        continue
    owner, repo = m.groups()
    try:
        r = session.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=headers,
            timeout=15          # corta a los 15 s en vez de esperar indefinidamente
        )
    except requests.exceptions.RequestException as e:
        print(f"  fallo de red en {owner}/{repo}: {e}")
        continue                # salta este repo y sigue con el siguiente
    if r.status_code != 200:
        continue

    if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
    
        reset = int(r.headers.get("X-RateLimit-Reset", 0))
        espera = max(reset - int(time.time()), 0)
        print(f"\nCuota agotada. Se renueva en {espera} segundos (~{espera//60} min).")
        print(f"Guardados {len(piloto)} repos hasta ahora.")
        with open("piloto_repos.json", "w", encoding="utf-8") as f:
            json.dump(piloto, f, indent=2, ensure_ascii=False)
        break

    info = r.json()
    if info.get("language") == "Python" and not info.get("archived"):
        piloto.append({"url": url, "owner": owner, "repo": repo, "rama": info["default_branch"]})
        counter += 1
        print("Repositorio añadido: ", repo, "[", counter, "]")
        if len(piloto) % 10 == 0:
            with open("piloto_repos.json", "w", encoding="utf-8") as f:
                json.dump(piloto, f, indent=2, ensure_ascii=False)
        print("Rate limit restante:", r.headers.get("X-RateLimit-Remaining"))