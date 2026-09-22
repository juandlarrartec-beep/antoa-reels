#!/usr/bin/env python3
"""Genera las copias publicables de los documentos de Peter U Cook.

Las fuentes son los HTML de la raiz. De ahi salen dos juegos:

  peter-u-cook/  paginas autocontenidas (CSS embebido, sin dependencias).
                 Es lo que sirve GitHub Pages y tambien lo que se abre
                 con doble clic o se manda por mail.
  pub/           las mismas paginas sin etiquetas de documento, listas
                 para publicar como artifact (la plataforma las envuelve).

No editar a mano lo que hay en esas carpetas: se regenera con `python3 build.py`.
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
CSS = (ROOT / "print.css").read_text(encoding="utf-8")

# (fuente, nombre publicado, ¿usa print.css?)
DOCS = [
    ("hub-peter-u-cook.html",            "index.html",       False),
    ("peter-u-cook.html",                "radiografia.html", False),
    ("propuesta-peter-u-cook.html",      "propuesta.html",   True),
    ("informe-peter-u-cook.html",        "informe.html",     True),
    ("anexo-ejecucion-peter-u-cook.html","anexo.html",       True),
]

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'

site = ROOT / "peter-u-cook"
pub = ROOT / "pub"
for d in (site, pub):
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir()

for src_name, out_name, inlines_css in DOCS:
    html = (ROOT / src_name).read_text(encoding="utf-8")

    if inlines_css:
        link = '<link rel="stylesheet" href="print.css">'
        assert link in html, f"{src_name}: no enlaza print.css"
        html = html.replace(link, "<style>\n" + CSS + "\n</style>", 1)

    for meta in (VIEWPORT, NOINDEX):
        if meta not in html:
            html = html.replace("<head>", "<head>\n" + meta, 1)

    (site / out_name).write_text(html, encoding="utf-8")

    # version para artifact: sin etiquetas de documento, que las pone la plataforma
    title = re.search(r"<title>.*?</title>", html, re.S).group(0)
    styles = re.findall(r"<style>.*?</style>", html, re.S)
    body = re.search(r"<body>\n?(.*)\n?</body>", html, re.S).group(1)
    out = title + "\n" + "\n".join(styles) + "\n\n" + body.strip() + "\n"
    for bad in ("<!DOCTYPE", "<html", "</html>", "<head>", "</head>", "<body>", "</body>"):
        assert bad not in out, f"{out_name}: quedo {bad} en la version de artifact"
    (pub / out_name).write_text(out, encoding="utf-8")

    print(f"  {out_name:<18} {len(html)//1024:>3} KB")

print(f"\nListo. {len(DOCS)} paginas en peter-u-cook/ y en pub/")
