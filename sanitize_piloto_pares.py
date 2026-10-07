import json
from collections import Counter

pares = json.load(open("piloto_pares.json", encoding="utf-8"))


# Analizamos descripciones cortas < 10 caracteres 

print("Total:", len(pares))
cortas = [p for p in pares if len(p["description"].strip()) < 10]
print("Descripciones muy cortas:", len(cortas))
for p in cortas[:10]:
    print(f"  [{p['tool']}] {p['description']!r}")

# Analizamos duplicados
codigos = Counter(p["code"].strip() for p in pares)
dups = {c: n for c, n in codigos.items() if n > 1}
print("Bloques de código que aparecen más de una vez:", len(dups))
print("Tools afectadas:", sum(dups.values()))

# Y por último analizamos reparto de servers por repositorio
por_repo = Counter(p["repo"] for p in pares)
for repo, n in por_repo.most_common():
    print(f"  {n:4d}  {repo}")