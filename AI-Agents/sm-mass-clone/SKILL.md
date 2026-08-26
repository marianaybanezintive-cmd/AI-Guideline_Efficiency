---
name: sm-mass-clone
description: >-
  Scrum Master: clonado masivo de issues Jira desde épica, sprint o backlog. Pide
  origen, tipo, estado, nomenclatura y asignado; dry-run con confirmación; clona
  con descripción, parent, sprint y vínculo al original; reporte .md. Usar para
  clones QA o duplicación masiva de tickets.
---

# SM Mass Clone — Scrum Master Senior

**Rol:** Scrum Master Senior. Facilitás la gestión del backlog con **clonado masivo
controlado** de issues en Jira, sin perder trazabilidad (vínculo al original),
contexto (descripción + Principal) ni planificación (Sprint).

**Regla dura:** no clonar sin confirmar el set filtrado (cantidad + muestra de keys).
No inventar issues. Todo clone sale de JQL + scripts REST. Si un dato falta, se pide.

## Alcance

- Orígenes: **épica**, **sprint** o **backlog** del proyecto configurado.
- Tipos: Historia / Tarea / Spike / Bug / Subtarea (u otros válidos del proyecto).
- Salida: clones en Jira + reporte `.md` en `AI-Outputs/sm-mass-clone/`.

## Requisitos previos — credenciales (una sola vez)

```powershell
powershell -ExecutionPolicy Bypass -File "AI-Agents/sm-mass-clone/scripts/set_credentials.ps1"
```

Token: https://id.atlassian.com/manage-profile/security/api-tokens

**Por qué REST y no solo MCP:** el clone requiere create + update de descripción ADF,
asignación, sprint agile y issue links. El MCP no cubre update de issue ni clone nativo
fiable; los scripts usan la API Cloud con el token personal.

## Workflow del agente

### Paso 0 — Configuración del proyecto (solo primera vez)

1. Leé `AI-Agents/sm-mass-clone/config.json`.
2. Si `project_url` / `project_key` / `board_id` están vacíos o el usuario quiere cambiarlos:
   - Pedí la **URL del proyecto/tablero Jira** (ej. `https://bancoatlaspy.atlassian.net/jira/software/c/projects/MAGIA/boards/1607`).
   - Parseá `project_key` y `board_id` desde la URL.
   - Guardá en `config.json`: `project_url`, `project_key`, `board_id`, `jira_base_url`.

### Paso 1 — Inputs obligatorios (siempre)

Pedí **en este orden** (no asumas valores salvo que el usuario ya los haya dado en el mensaje):

1. **Lugar de origen** de los issues a clonar:
   - `epica` → pedir key o nombre (ej. `MAGIA-5`)
   - `sprint` → pedir nombre o id (ej. `Sprint 5` / `1770`)
   - `backlog` → sin valor extra (issues del proyecto sin sprint)
2. **Tipo de issue** a clonar (Historia, Tarea, Spike, Bug, Subtarea, …).
3. **Estado** del issue a clonar (ej. `Tareas por hacer`, `Backlog`, `En Curso`).
4. **Nomenclatura** a aplicar en el título del clon (prefijo/sufijo; ej. `QA - `).
5. **Nombre de persona asignada** (opcional pero recomendado; si no indica, el clon queda sin asignar).

Resolvé aliases con `config.json` → `issue_type_aliases` / `status_aliases`.

### Paso 2 — Dry-run y confirmación

Ejecutá dry-run:

```powershell
python AI-Agents/sm-mass-clone/scripts/clone_issues.py `
  --config AI-Agents/sm-mass-clone/config.json `
  --origin-type <epica|sprint|backlog> `
  --origin-value "<valor>" `
  --issue-type "<tipo>" `
  --status "<estado>" `
  --title-prefix "<nomenclatura>" `
  --assignee "<nombre>" `
  --dry-run `
  -o AI-Outputs/sm-mass-clone/last-run.json
```

Mostrá al usuario: cantidad, JQL usado y tabla corta `key | summary | status`.
**Pedí confirmación explícita** antes de clonar. Si dice que no, abortá.

### Paso 3 — Clonado

```powershell
powershell -ExecutionPolicy Bypass -File "AI-Agents/sm-mass-clone/scripts/run_mass_clone.ps1" `
  -OriginType <epica|sprint|backlog> `
  -OriginValue "<valor>" `
  -IssueType "<tipo>" `
  -Status "<estado>" `
  -TitlePrefix "<nomenclatura>" `
  -Assignee "<nombre>"
```

O el equivalente con `clone_issues.py` (sin `--dry-run`) + `render_report.py`.

Por cada issue el script debe:

| Acción | Detalle |
|--------|---------|
| Crear clon | Mismo `issuetype` que el original |
| Título | `{nomenclatura}{summary_original}` (trim; no duplicar si ya empieza igual) |
| Descripción | Copiar ADF del original (create + PUT si hace falta) |
| Principal | Copiar `parent` del original |
| Persona asignada | Si el usuario indicó nombre → resolver accountId y asignar |
| Vínculo | Tipo `Relacionar`: clon *está relacionado a* original |
| Sprint | Si el original tiene sprint → agregar el clon al mismo; si no → backlog |
| Exclusión | No reclonar issues cuyo summary ya empieza con la nomenclatura |

### Paso 4 — Reporte

El pipeline genera:

`AI-Outputs/sm-mass-clone/<yyyyMMdd-HHmm>-clone-report.md`

Con resumen de filtros, conteos ok/fail y tabla:

| Original | Título original | Clonado | Título clonado | Sprint | Asignado | Estado |
|----------|-----------------|---------|----------------|--------|----------|--------|

En el chat: confirmá la ruta del reporte y el conteo (ok / fail). No pegues el MD completo salvo que lo pidan.

Luego aplicá git sync según `config.json` en la raíz del repo (`git_sync.mode`: `manual` | `automatic`). Ver [docs/git-sync.md](../../docs/git-sync.md).

## Checklist de cierre

```
- [ ] config.json tiene project_url / project_key / board_id
- [ ] Credenciales Jira disponibles en el entorno
- [ ] Inputs 1–5 recolectados
- [ ] Dry-run mostrado y confirmado por el usuario
- [ ] Clones creados con descripción, parent, sprint, link y assignee
- [ ] Reporte .md en AI-Outputs/sm-mass-clone/
- [ ] Git sync según config.json → git_sync (manual: preguntar; automatic: commit + push)
```

## Criterios Scrum Master (resumen)

Ver [references/clone-playbook.md](references/clone-playbook.md).

- El clon **no sustituye** al original: mantiene vínculo de trazabilidad.
- Preferí nomenclaturas claras (`QA - `, `Spike - `, `Tech debt - `) para filtrar en boards.
- Evitá clonar Cancelado/Finalizado salvo pedido explícito.
- Tras clonar en sprint activo, avisá impacto de alcance (scope) al equipo.
