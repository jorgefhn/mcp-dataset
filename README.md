Repositorio piloto para crear un dataset grande que aglutinará pares D-C para prueba DCI Probe Checker.

Piloto: 
~130 servidores
~2k pares descripción código

Este es el funcionamiento del pipeline (el orden en que se ejecutan y se obtienen los resultados): 
<img width="926" height="464" alt="image" src="https://github.com/user-attachments/assets/2c2bc93b-7e15-465c-9b3c-fe67ca8ea108" />

También hay un script `sanitize_piloto_pares.py` que te dice información sobre:
- Descripciones cortas
- MCP Servers duplicados
- Reparto de MCP Servers por repositorio (para analizar el concepto de "locality" del que habla DCI Checker)

