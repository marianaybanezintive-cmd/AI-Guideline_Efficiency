# Confluence — épicas y HUs MAGIA-346 / 347 / 348 / 349

Publicado: 2026-08-20. Espacio: [Servicios Digitales Atlas](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121).

## POC — Atlas Trade

Resumen funcional de Login, Mi perfil, ABM y Confirming (entregable de la POC v2.11.4):

- Página: [POC - Atlas Trade](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1664876548/POC+-+Atlas+Trade)
- Fuente: `poc-atlas-trade-resumen-funcional.md`
- Publicación: `python publish_poc_page.py`


## Qué se hizo

- Se actualizaron las páginas de cada épica bajo **Documentación Funcional** y **Documentación Técnica**.
- Primera línea: `JIRA = <url>`. Debajo: descripción completa de Jira (tablas incluidas).
- Bajo cada épica **funcional** se creó una subpágina por Historia de Usuario (no tareas, no clones QA).
- Primera línea HU: `JIRA: <url>`. Tercera línea: descripción (texto, tablas, imágenes). Texto tachado omitido.
- No había páginas QA de HUs para borrar. Se omitieron 41 historias cuyo título empieza con `QA`.

Las páginas técnicas usan el sufijo `— Técnica` porque Confluence no permite dos páginas con el mismo título en el mismo espacio.

## Épicas

| Épica | Funcional | Técnica |
|-------|-----------|---------|
| MAGIA-346 Confirming | [Confirming](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687845/Confirming) | [Confirming — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625688617/Confirming+T+cnica) |
| MAGIA-347 Gestión de Facturas | [Gestión de Facturas](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687859/Gesti+n+de+Facturas) | [Gestión de Facturas — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625688631/Gesti+n+de+Facturas+T+cnica) |
| MAGIA-348 Simulación de Adelantos | [Simulación de Adelantos](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687873/Simulaci+n+de+Adelantos) | [Simulación de Adelantos — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625688645/Simulaci+n+de+Adelantos+T+cnica) |
| MAGIA-349 Desembolso | [Desembolso](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687887/Desembolso) | [Desembolso — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625688659/Desembolso+T+cnica) |

## Historias publicadas

- Confirming (MAGIA-346): **21** HUs
- Gestión de Facturas (MAGIA-347): **9** HUs
- Simulación de Adelantos (MAGIA-348): **12** HUs
- Desembolso (MAGIA-349): **3** HUs ([MAGIA-544](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1654849560/API+Integraci+n+CORE+Banking+-+Solicitud+de+Cr+dito), [MAGIA-545](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1654751254/BE-Notificaci+n+al+EGP+del+prestamo+generado), [MAGIA-546](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1653932067/Notificaci+n+al+Proveedor+de+la+factura+generada))
- Total: **45** páginas de HUs
- Imágenes copiadas desde Jira: 9 archivos en 7 HUs
- Omitidas QA: 41 (ninguna en Desembolso)
- Errores: 0

Detalle de URLs: `publish-report.json` y `publish-report-MAGIA-349.json`.
