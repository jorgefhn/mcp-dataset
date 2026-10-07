import json, os, subprocess

with open("piloto_repos.json", encoding="utf-8") as f:
    repos = json.load(f)

os.makedirs("repos", exist_ok=True)

for r in repos:
    destino = os.path.join("repos", f"{r['owner']}__{r['repo']}")
    if os.path.exists(destino):
        print(f"ya estaba: {r['owner']}/{r['repo']}")
        continue
    print(f"clonando {r['owner']}/{r['repo']}...")
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", r["rama"], r["url"], destino],
        capture_output=True
    )