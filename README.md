# Antoá — Investigación de contenido (Reels)

Presentación de estrategia de contenido para Antoá: 5 modelos de reels reales,
referencias analizadas y plan de acción. Página estática (GitHub Pages).

---

# Prospecto Peter U Cook

Relevamiento y material comercial para el prospecto Peter U Cook (@peterucook),
cocina de autor a puerta cerrada, CABA.

## Para compartir

La carpeta `peter-u-cook/` es el sitio publicable: cinco páginas autocontenidas,
sin dependencias externas. Se abren con doble clic, se mandan por mail o las
sirve GitHub Pages.

Para que queden con URL pública: **Settings → Pages → Source**, y elegir rama.

- Si se apunta Pages a `claude/prospect-digital-analysis-vty1mh` con carpeta
  `/ (root)`, publica sin tocar `master`.
- Si Pages ya sirve desde `master`, hay que mergear la rama primero.

En cualquiera de los dos casos las direcciones quedan:

| Documento | Ruta |
|---|---|
| Índice | `/antoa-reels/peter-u-cook/` |
| Radiografía (con radar) | `/antoa-reels/peter-u-cook/radiografia.html` |
| Propuesta — **para el cliente** | `/antoa-reels/peter-u-cook/propuesta.html` |
| Informe de salud digital | `/antoa-reels/peter-u-cook/informe.html` |
| Anexo de ejecución | `/antoa-reels/peter-u-cook/anexo.html` |

`robots.txt` bloquea a los buscadores y cada página lleva `noindex`, así que no
se indexan — pero quien tenga el link entra. El Informe y el Anexo son internos:
tienen el enfoque comercial y el manejo de objeciones.

## Links privados (claude.ai)

Las mismas páginas, visibles solo para la cuenta dueña y para quien reciba
acceso desde el menú *Share* de cada una:

| Documento | Link |
|---|---|
| Radiografía | https://claude.ai/artifact/9WwuDdrDETx7AqpSgmDTKH |
| Propuesta | https://claude.ai/artifact/MiKuGVaM1aoDNd4xFDUHU1 |
| Informe | https://claude.ai/artifact/JXcxARqAVkZavtv4zLfd4M |
| Anexo | https://claude.ai/artifact/KR1Vxh738DEQYdGLov74aR |

## Estructura

| Ruta | Qué es |
|---|---|
| `hub-peter-u-cook.html` | Fuente del índice |
| `peter-u-cook.html` | Fuente de la radiografía con motion graphics |
| `propuesta-peter-u-cook.html` | Fuente de la propuesta |
| `informe-peter-u-cook.html` | Fuente del informe |
| `anexo-ejecucion-peter-u-cook.html` | Fuente del anexo |
| `print.css` | Estilos compartidos de los tres documentos imprimibles |
| `build.py` | Genera `peter-u-cook/` y `pub/` desde las fuentes |
| `peter-u-cook/` | **Generado.** Sitio publicable, autocontenido |
| `pub/` | **Generado.** Mismas páginas para publicar como artifact |
| `*.pdf` | Versiones imprimibles |

Editar siempre las fuentes de la raíz y correr `python3 build.py`; lo que hay en
`peter-u-cook/` y en `pub/` se sobrescribe.

## Cómo se generan los PDF

Desde las fuentes con Chromium en modo impresión, márgenes A4 y pie con número
de página. El índice del informe se numera en dos pasadas: se renderiza, se leen
las páginas reales de cada sección, se reemplazan los tokens y se vuelve a
renderizar.
