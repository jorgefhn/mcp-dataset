import ast,os,json

def nombre_decorador(dec):
    """Devuelve el attr del decorador si es una llamada a un método, p.ej. 'tool'."""
    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
        return dec.func.attr
    return None

def descripcion_del_decorador(dec):
    """Busca description="..." dentro de @mcp.tool(...)."""
    if isinstance(dec, ast.Call):
        for kw in dec.keywords:
            if kw.arg == "description" and isinstance(kw.value, ast.Constant):
                return kw.value.value
    return None

pares = []

for raiz, _, archivos in os.walk("repos"):
    if ".git" in raiz:
        continue
    # owner__repo es la primera carpeta dentro de repos/
    partes = os.path.relpath(raiz, "repos").split(os.sep)
    repo_id = partes[0] if partes and partes[0] != "." else "?"

    for a in archivos:
        if not a.endswith(".py"):
            continue
        ruta = os.path.join(raiz, a)
        fuente = open(ruta, encoding="utf-8", errors="ignore").read()
        try:
            arbol = ast.parse(fuente)
        except SyntaxError:
            continue

        for nodo in ast.walk(arbol):
            if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not any(nombre_decorador(d) == "tool" for d in nodo.decorator_list):
                continue

            # 1) descripción: primero el decorador, si no el docstring
            desc = None
            for d in nodo.decorator_list:
                desc = descripcion_del_decorador(d)
                if desc:
                    break
            if not desc:
                desc = ast.get_docstring(nodo)

            # 2) código: cuerpo completo de la función
            code = ast.get_source_segment(fuente, nodo)

            pares.append({
                "repo": repo_id,
                "tool": nodo.name,
                "description": desc,       # puede ser None
                "code": code
            })

print("Pares extraídos:", len(pares))
sin_desc = sum(1 for p in pares if not p["description"])
print("Sin descripción:", sin_desc)

with open("piloto_pares.json", "w", encoding="utf-8") as f:
    json.dump(pares, f, indent=2, ensure_ascii=False)