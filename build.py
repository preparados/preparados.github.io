import json, re, pathlib, datetime, html
import markdown

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"
cfg = json.loads((ROOT/"data/config.json").read_text(encoding="utf-8"))
afil = json.loads((ROOT/"data/afiliados.json").read_text(encoding="utf-8"))
SITE.mkdir(exist_ok=True)
BASE = cfg["url"].rstrip("/")

CSS = "body{font:18px/1.7 Georgia,serif;max-width:760px;margin:0 auto;padding:16px;color:#222}a{color:#0b5}h1,h2,h3{font-family:system-ui,sans-serif;line-height:1.25}header,footer{font-family:system-ui,sans-serif;border-bottom:1px solid #ddd;padding:8px 0;margin-bottom:24px}footer{border:0;border-top:1px solid #ddd;font-size:14px;color:#666;margin-top:40px}.aviso{background:#f6f6f0;padding:8px 12px;font-size:15px}"

def page(title, desc, body, path):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}/{path}"><style>{CSS}</style></head><body>
<header><a href="{BASE}/"><strong>{html.escape(cfg['nombre'])}</strong></a> · {html.escape(cfg['lema'])}</header>
<main>{body}</main>
<footer>Participamos en programas de afiliados: si compras a través de nuestros enlaces podemos recibir una comisión, sin coste adicional para ti. La información es orientativa; ante una emergencia sigue las indicaciones de Protección Civil y las autoridades.</footer></body></html>"""

def parse(p):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":"); meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2)

def resolve(md):
    def r(m):
        i = m.group(1)
        if i not in afil: raise SystemExit(f"Afiliado sin definir: {i}")
        a = afil[i]
        return f"[{a['texto']}]({a['url']})"
    return re.sub(r"\{\{afiliado:([\w-]+)\}\}", r, md)

posts = []
for p in sorted((ROOT/"content").glob("*.md")):
    meta, body = parse(p)
    slug = p.stem
    h = markdown.markdown(resolve(body), extensions=["tables"])
    h = h.replace('<a href="http', '<a rel="sponsored nofollow noopener" href="http')
    out = f"<article><h1>{html.escape(meta['title'])}</h1>{h}</article>"
    (SITE/f"{slug}.html").write_text(page(meta["title"], meta["description"], out, f"{slug}.html"), encoding="utf-8")
    posts.append((meta.get("date",""), slug, meta))
posts.sort(reverse=True)

lis = "".join(f'<li><a href="{BASE}/{s}.html">{html.escape(m["title"])}</a><br><small>{html.escape(m["description"])}</small></li>' for _, s, m in posts)
(SITE/"index.html").write_text(page(cfg["nombre"], cfg["descripcion"], f"<h1>{html.escape(cfg['nombre'])}</h1><p>{html.escape(cfg['descripcion'])}</p><ul>{lis}</ul>", ""), encoding="utf-8")
(SITE/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+f"<url><loc>{BASE}/</loc></url>"+"".join(f"<url><loc>{BASE}/{s}.html</loc><lastmod>{d}</lastmod></url>" for d,s,_ in posts)+"</urlset>", encoding="utf-8")
(SITE/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
items = "".join(f"<item><title>{html.escape(m['title'])}</title><link>{BASE}/{s}.html</link><description>{html.escape(m['description'])}</description></item>" for _, s, m in posts[:20])
(SITE/"rss.xml").write_text(f'<?xml version="1.0"?><rss version="2.0"><channel><title>{html.escape(cfg["nombre"])}</title><link>{BASE}/</link><description>{html.escape(cfg["descripcion"])}</description>{items}</channel></rss>', encoding="utf-8")
left = [f for f in SITE.glob("*.html") if "{{afiliado" in f.read_text(encoding="utf-8")]
assert not left, left
print(f"OK: {len(posts)} artículos")
