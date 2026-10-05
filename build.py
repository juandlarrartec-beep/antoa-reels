#!/usr/bin/env python3
"""Genera las copias publicables de los documentos de Peter U Cook.

Las fuentes son los HTML de la raiz. De ahi salen dos juegos:

  peter-u-cook/  paginas autocontenidas (CSS embebido, sin dependencias).
                 Es lo que sirve GitHub Pages y tambien lo que se abre
                 con doble clic o se manda por mail.
  pub/           las mismas paginas sin etiquetas de documento, listas
                 para publicar como artifact (la plataforma las envuelve).

No editar a mano lo que hay en esas carpetas: se regenera con `python3 build.py`.

La hoja de ruta (hoja-de-ruta/) se escribe como fragmento de artifact y usa la
base de datos de la plataforma para guardar. En GitHub Pages esa base no existe,
asi que alli se publica envuelta y con la bandera window.__PUBLICO: solo lectura,
sin formularios y sin bitacora.
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
CSS = (ROOT / "print.css").read_text(encoding="utf-8")

# (fuente, nombre publicado, ¿usa print.css?)
DOCS = [
    ("hub-peter-u-cook.html",            "index.html",       False),
    ("peter-u-cook.html",                "radiografia.html", False),
    ("presentacion-primera-etapa.html",  "primera-etapa.html", False),
    ("presentacion-primera-etapa-v2.html", "primera-etapa-visual.html", False),
    ("propuesta-peter-u-cook.html",      "propuesta.html",   True),
    ("informe-peter-u-cook.html",        "informe.html",     True),
    ("anexo-ejecucion-peter-u-cook.html","anexo.html",       True),
]

# Paginas escritas como fragmento de artifact (sin etiquetas de documento).
# (fuente, nombre publicado)
FRAGMENTS = [
    ("hoja-de-ruta/hoja-de-ruta.html",   "hoja-de-ruta.html"),
]

NOINDEX = '<meta name="robots" content="noindex, nofollow">'
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'

def envolver(fragmento: str) -> str:
    """Convierte un fragmento de artifact en una pagina completa, en modo publico."""
    corte = fragmento.index('<div class="wrap">')
    cabeza, cuerpo = fragmento[:corte].strip(), fragmento[corte:].strip()
    return (
        '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + NOINDEX + "\n"
        "<style>html,body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        "<script>window.__PUBLICO = true;</script>\n"
        + cabeza + "\n</head>\n<body>\n" + cuerpo + "\n</body>\n</html>\n"
    )

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

for src_name, out_name in FRAGMENTS:
    frag = (ROOT / src_name).read_text(encoding="utf-8")
    page = envolver(frag)
    for bad in ("<!DOCTYPE", "<html", "<body>"):
        assert bad not in frag, f"{src_name}: ya trae {bad}"
    (site / out_name).write_text(page, encoding="utf-8")
    (pub / out_name).write_text(frag, encoding="utf-8")
    print(f"  {out_name:<18} {len(page)//1024:>3} KB  (modo publico)")

# las fotos viajan junto al sitio
src_img = ROOT / "img"
if src_img.is_dir():
    dst = site / "img"
    shutil.copytree(src_img, dst, dirs_exist_ok=True)
    fotos = [f.name for f in dst.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    print(f"\n  img/: {len(fotos)} foto(s)" + (" — " + ", ".join(fotos) if fotos else " (ninguna todavia)"))

print(f"\nListo. {len(DOCS) + len(FRAGMENTS)} paginas en peter-u-cook/ y en pub/")
