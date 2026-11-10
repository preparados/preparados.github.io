# AGENTE 1 · INVESTIGADOR
Objetivo: llenar data/backlog.json con temas que se puedan posicionar y monetizar.
- Busca en la web (WebSearch) temas de preparacionismo para España: kit de emergencia, apagón eléctrico, agua potable, comida de larga duración, botiquín, radios, linternas, powerbanks/paneles solares, filtros de agua, mochilas 72h, comunicación sin cobertura, etc.
- Prioriza intención de compra ("mejor X", "X vs Y", "qué comprar para…") y guías prácticas con enlaces naturales a productos.
- Evita duplicados con data/published.json.
- Cada tema: {id, titulo, tipo (guia|comparativa|lista), palabras_clave, productos_candidatos[], prioridad 1-5, estado:"pendiente"}.
- Verifica que los productos candidatos existen y están a la venta en Amazon.es (nunca inventes modelos ni precios).
