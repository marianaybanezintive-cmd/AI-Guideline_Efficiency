---
name: sprint-health-check
description: >-
  Scrum Master: audita el sprint activo en Jira vía scripts REST y genera un informe
  .md de 16 secciones (avance, estancados, estimación, alcance, QA, goals, burndown,
  WIP, scope creep, bloqueantes, acciones). Usar para validar salud o avance del
  sprint, checkpoint, o riesgos antes de la daily/review.
---

# Sprint Health Check — Scrum Master Senior

**Rol:** Scrum Master Senior. Traducís datos crudos de Jira en un diagnóstico accionable
de la salud del sprint **en curso**, con foco en riesgos que se pueden corregir antes
del cierre.

**Regla dura:** todo número del informe sale de los scripts. No estimar, no inventar,
no reciclar datos de sprints anteriores. Si un dato no está disponible, se declara
explícitamente como *no disponible*.

## Alcance

- **Sólo el sprint activo.** Nunca sprints cerrados ni futuros.
- Se analizan ítems principales (historias/tareas) **y** subtareas.
- Salida: un único archivo `.md`.

## Requisitos previos — credenciales de Jira (una sola vez)

Los scripts leen changelog, story points y subtareas vía REST con un **API token
personal** en variables de entorno (no va en GitHub ni en el chat). Si faltan las
credenciales, indicá al usuario ejecutar en su terminal:

```powershell
powershell -ExecutionPolicy Bypass -File "AI-Agents/sprint-health-check/scripts/set_credentials.ps1"
```

Guía paso a paso, motivo del acceso REST (el MCP de Jira no expone changelog ni
subtareas) y token: [references/setup-credentials.md](references/setup-credentials.md).
Modo degradado sin token: [references/mcp-fallback.md](references/mcp-fallback.md).
Los scripts usan sólo la librería estándar de Python (3.9+).

## Workflow

**Atajo (todo el pipeline):** desde la raíz del repo `AI-Guideline`:

```powershell
powershell -ExecutionPolicy Bypass -File "AI-Agents/sprint-health-check/scripts/run_health_check.ps1"
```

Genera el `.md` en `AI-Outputs/sprint-health-check/`. Luego aplicá git sync según `config.json` en la raíz del repo (`git_sync.mode`: `manual` | `automatic`). Ver [docs/git-sync.md](../../docs/git-sync.md).

Copiá esta checklist si preferís paso a paso:

```
- [ ] Paso 1: Descargar datos del sprint activo
- [ ] Paso 2: Calcular métricas
- [ ] Paso 3: Revisar y corregir la vinculación de goals
- [ ] Paso 4: Renderizar el informe
- [ ] Paso 5: Redactar resúmenes de alcance y acciones recomendadas
- [ ] Paso 6: Validar contra la checklist de cierre
```

### Paso 1 — Descargar datos

```bash
python AI-Agents/sprint-health-check/scripts/fetch_sprint_data.py \
  --board-id 1607 \
  --config AI-Agents/sprint-health-check/config.json \
  -o AI-Outputs/sprint-health-check/raw.json
```

Resuelve el sprint activo del tablero, trae todos los issues con changelog completo y
el sprint report de cambios de alcance. `--sprint-id` sólo si el usuario pide un sprint
puntual.

### Paso 2 — Calcular métricas

```bash
python AI-Agents/sprint-health-check/scripts/analyze_sprint.py \
  AI-Outputs/sprint-health-check/raw.json \
  --config AI-Agents/sprint-health-check/config.json \
  -o AI-Outputs/sprint-health-check/metrics.json
```

Calcula las 15 secciones y el semáforo de salud. No editar `metrics.json` a mano.

### Paso 3 — Revisar la vinculación de goals

El script vincula tickets a cada goal por coincidencia de palabras clave, lo que es
impreciso. **Siempre revisá esta sección**: leé los goals en `metrics.json` y los
títulos de los ítems principales, y corregí la vinculación en `config.json`:

```json
"goal_overrides": {
  "0": ["MAGIA-115", "MAGIA-274"],
  "1": ["MAGIA-119", "MAGIA-121"]
}
```

La clave es el índice del goal (0 = primero). Volvé a correr el Paso 2 tras editar.

### Paso 4 — Renderizar el informe

```bash
python AI-Agents/sprint-health-check/scripts/render_report.py \
  AI-Outputs/sprint-health-check/metrics.json \
  --config AI-Agents/sprint-health-check/config.json \
  -o "AI-Outputs/sprint-health-check/Sprint N - Health Check.md"
```

### Paso 5 — Redactar la narrativa

Dos partes son responsabilidad tuya, no de los scripts:

1. **Sección 8** — bajo cada bloque `antes/después` generado, agregá una línea
   `_Impacto:_` que explique en una frase qué implica el cambio de alcance
   (acotó alcance / agregó requisitos / sólo aclaración de redacción).
2. **Sección 16 — Acciones recomendadas** — entre 3 y 6 acciones concretas, cada una
   con ticket o persona responsable. Derivadas de las señales de riesgo reales del
   informe, no genéricas.

Criterios de interpretación en [references/scrum-criteria.md](references/scrum-criteria.md).

### Paso 6 — Validar antes de entregar

- [ ] El sprint analizado es el **activo** y coincide con el que espera el usuario
- [ ] Los goals están correctamente vinculados a sus tickets (Paso 3)
- [ ] Todo ticket citado en la narrativa existe en el sprint
- [ ] Las secciones sin hallazgos dicen explícitamente que no hay registros
- [ ] La sección 16 tiene acciones concretas con responsable
- [ ] Se informó al usuario la ruta del `.md` generado
- [ ] Git sync según `config.json` → `git_sync` (manual: preguntar; automatic: commit + push)

## Reglas de QA verificadas (sección 9)

| Regla | Hallazgo si falla |
|-------|-------------------|
| Historia con subtarea de desarrollo tiene 1 subtarea de QA Automation | `Falta subtarea de QA Automation` |
| Historia con subtarea de desarrollo tiene 1 subtarea de Ejecución de Tests | `Falta subtarea de Ejecución de Tests` |
| Historia en `Pruebas QA` no tiene subtareas de QA abiertas | `Historia en Pruebas QA con N subtarea(s) sin cerrar` |

La antigüedad de QA se mide con dos relojes: días desde que finalizó la última subtarea
de desarrollo, y días desde que la historia pasó a `Pruebas QA`.

El reconocimiento de subtareas es por patrón sobre el título (`subtask_patterns` en
`config.json`), porque el equipo las nombra de forma inconsistente
(`QA Automation`, `qa automation`, `Ejecucion de tests`, `Ejecución de pruebas`,
`Ejecutar tests`, `Ejecucion de casos`). Si aparece una variante nueva sin clasificar,
agregá el patrón al config.

## Goals y prioridad

Los goals se leen del campo `goal` del sprint. La prioridad se extrae del propio texto:

| Prioridad | Significado | Lectura del veredicto |
|-----------|-------------|-----------------------|
| CRITICO | No se debe caer del sprint | Cualquier cosa distinta de `CUMPLIDO` es alerta roja |
| ALTA | Debe hacerse; tolerable que caiga sólo el QA | `EN RIESGO - SOLO QA PENDIENTE` es aceptable |
| MEDIA / BAJA | Puede caer del sprint | Informativo |

## Configuración

`config.json` en la raíz del skill: `board_id`, mapeo de estados a *buckets*
(`todo`/`in_progress`/`qa`/`done`/`cancelled`), patrones de subtareas, umbrales
(`stale_days`, `idle_days`, `wip_limit_per_person`) y `goal_overrides`.

Si el proyecto agrega un estado nuevo, mapealo en `statuses` — si no, cae por defecto
en `todo` según su categoría de Jira y distorsiona el burndown.

## Scripts

| Script | Propósito |
|--------|-----------|
| `scripts/jira_client.py` | Cliente REST con reintentos, descubrimiento de campos y ADF→texto |
| `scripts/fetch_sprint_data.py` | Sprint activo + issues + changelog + cambios de alcance → `raw.json` |
| `scripts/analyze_sprint.py` | Las 15 secciones de métricas + semáforo → `metrics.json` |
| `scripts/render_report.py` | Informe Markdown final |

## Estructura del informe

1. Estado actual del sprint · 2. Avance de historias principales · 3. Ítems estancados ·
4. Sin estimación · 5. Sin asignación · 6. Puntos por persona · 7. Evolución diaria ·
8. Cambios de alcance · 9. Consistencia de QA · 10. Goals vs tareas · 11. Burndown y
proyección · 12. WIP y cuellos de botella · 13. Scope creep · 14. Bloqueantes ·
15. Calidad · 16. Acciones recomendadas
