# Confluence — Morosidad y Reversiones

**Fecha:** 2026-08-26  
**Script:** `AI-Outputs/confluence-epics-hus/publish_pages.py --only MAGIA-350 MAGIA-547`

## Épicas publicadas

| Épica | Jira | Funcional | Técnica |
|-------|------|-----------|---------|
| Morosidad | [MAGIA-350](https://bancoatlaspy.atlassian.net/browse/MAGIA-350) | [Morosidad](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687901/Morosidad) | [Morosidad — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625688673/Morosidad+T+cnica) |
| Reversiones | [MAGIA-547](https://bancoatlaspy.atlassian.net/browse/MAGIA-547) | [Reversiones](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669431297/Reversiones) | [Reversiones — Técnica](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669693441/Reversiones+T+cnica) *(creada)* |

> Nota: la épica Reversiones en Jira es **MAGIA-547** (no MAGIA-347, que corresponde a Gestión de Facturas).

Formato de cada página épica: `JIRA = <url>` + descripción completa de Jira (tablas incluidas; texto tachado omitido).

## Historias bajo Documentación Funcional

### Morosidad (5)

| Jira | Confluence |
|------|------------|
| MAGIA-577 | [FE-Marca de morosidad del EGP en panel Confirming](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669332995/FE-Marca+de+morosidad+del+EGP+en+panel+Confirming) |
| MAGIA-578 | [FE-Grilla grisada y bloqueada cuando el EGP está en mora](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669365762/FE-Grilla+grisada+y+bloqueada+cuando+el+EGP+est+en+mora) |
| MAGIA-579 | [FE-Notificación in-app por bloqueo de mora](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669365781/FE-Notificaci+n+in-app+por+bloqueo+de+mora) |
| MAGIA-580 | [FE-ABM: configurar umbral de días de mora para bloqueo de límite](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669627905/FE-ABM+configurar+umbral+de+d+as+de+mora+para+bloqueo+de+l+mite) |
| MAGIA-581 | [BFF/BE-Levantar bloqueo por mora al acreditar el pago](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669660673/BFF+BE-Levantar+bloqueo+por+mora+al+acreditar+el+pago) |

### Reversiones (2)

| Jira | Confluence |
|------|------------|
| MAGIA-582 | [FE-Mostrar estados de reversión en grilla Confirming (FNV)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669693459/FE-Mostrar+estados+de+reversi+n+en+grilla+Confirming+FNV) |
| MAGIA-583 | [FE-Filtro Estado incluye estados de reversión](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669595144/FE-Filtro+Estado+incluye+estados+de+reversi+n) |

Formato de cada HU: `JIRA: <url>` + línea en blanco + descripción Jira.

## Tareas bajo Documentación Técnica

### Morosidad — Técnica (4)

| Jira | Confluence |
|------|------------|
| MAGIA-584 | [BFF/BE-GET · Estado de mora del EGP (API Prestamos)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1670119425/BFF+BE-GET+Estado+de+mora+del+EGP+API+Prestamos) |
| MAGIA-585 | [BFF/BE-Evaluar umbral ABM y aplicar/liberar bloqueo de límite](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669365809/BFF+BE-Evaluar+umbral+ABM+y+aplicar+liberar+bloqueo+de+l+mite) |
| MAGIA-586 | [BFF/BE-Consumir mensaje CORE de pago acreditado](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669955594/BFF+BE-Consumir+mensaje+CORE+de+pago+acreditado) |
| MAGIA-589 | [TBD (en caso de no tener la API) - Mock contrato API Prestamos](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669955613/TBD+en+caso+de+no+tener+la+API+-+Mock+contrato+API+Prestamos) |

### Reversiones — Técnica (2)

| Jira | Confluence |
|------|------------|
| MAGIA-587 | [BFF/BE-Máquina de estados BE de reversión](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669857281/BFF+BE-M+quina+de+estados+BE+de+reversi+n) |
| MAGIA-588 | [Cursor skill para revertir manualmente](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1669890049/Cursor+skill+para+revertir+manualmente) |

Formato: `JIRA: <url>` + línea en blanco + descripción Jira (mismo patrón que las HUs).

## Omitidas

- **10 historias QA** en Jira (MAGIA-590…594, MAGIA-599…600): no se crearon páginas.
- **0 páginas QA** existentes bajo las épicas funcionales (no había nada que borrar).

## Resultado

- Épicas actualizadas/creadas: **5** acciones (2 funcional + 2 técnica Morosidad; 1 funcional + 2 técnica Reversiones)
- HUs creadas: **7**
- Tareas técnicas Morosidad: **4** (MAGIA-584…586, MAGIA-589)
- Tareas técnicas Reversiones: **2** (MAGIA-587, MAGIA-588)
- Errores: **0**

Detalle JSON: `publish-report-MAGIA-350-MAGIA-547.json`
