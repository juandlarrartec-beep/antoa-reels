# Antoá — Investigación de contenido (Reels)

Presentación de estrategia de contenido para Antoá: 5 modelos de reels reales,
referencias analizadas y plan de acción. Página estática (GitHub Pages).

## Dossier Peter U Cook

`peter-u-cook.html` — radiografía digital del prospecto Peter U Cook (@peterucook):
presencia por canal, mercado turístico de Buenos Aires y servicios a proponer.
Página estática, `noindex`, de uso interno.

## Prospecto Peter U Cook

Relevamiento y material comercial para el prospecto Peter U Cook (@peterucook),
cocina de autor a puerta cerrada, CABA.

| Archivo | Qué es | Para quién |
|---|---|---|
| `peter-u-cook.html` | Radiografía web con motion graphics | Interno |
| `Informe-Peter-U-Cook.pdf` | Informe de salud digital, 24 págs. | Interno |
| `Propuesta-Peter-U-Cook.pdf` | Propuesta de trabajo, 10 págs. | **Se le envía a él** |
| `Anexo-Ejecucion-Peter-U-Cook.pdf` | Keywords, campañas, flujos y checklists, 11 págs. | Interno |

### Para ver en el navegador

`ver/informe.html`, `ver/propuesta.html` y `ver/anexo.html` son copias
autocontenidas (CSS embebido, sin dependencias) de los tres documentos, con
estilos de pantalla. Se abren con doble clic y se pueden mandar por mail.
Se regeneran desde los `*.html` de la raíz; no editarlas a mano.

Los PDF se generan desde los `*.html` homónimos con Chromium en modo impresión;
`print.css` es la hoja de estilos compartida. El índice del informe se numera en
dos pasadas (render, se leen las páginas reales, se reemplazan los tokens y se
vuelve a renderizar).

La propuesta tiene campos en blanco a completar antes de enviarla: nombre de la
agencia, precios de los paquetes y datos de contacto.
