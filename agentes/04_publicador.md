# AGENTE 4 · PUBLICADOR
1. Ejecuta `python build.py` (genera /docs, que es la carpeta que GitHub Pages sirve desde la rama main: artículos, índice, sitemap.xml, rss.xml, robots.txt).
2. Comprueba que no hay marcadores {{afiliado:...}} sin resolver ni enlaces rotos.
3. git add/commit/push a main → GitHub Pages publica /docs automáticamente (gratis).
4. Marca el tema "publicado" en backlog.json y añádelo a data/published.json.
