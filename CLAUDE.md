# AI-Guideline — instrucciones para Claude Code

Repo de agentes (skills) de gestión ágil sobre Jira. Cada subcarpeta de `AI-Agents/`
es un agente; los resultados de ejecución van a `AI-Outputs/<agente>/`, nunca la
definición del agente.

## Regla dura — crear o modificar agentes en `AI-Agents/`

1. **Antes de escribir:** leé `docs/agent-token-efficiency.md` y diseñá dentro de sus
   presupuestos: `description` ≤ 350 chars (duro 500); `SKILL.md` ≤ 6.000 chars
   (duro 10.000 con justificación escrita); plantillas/esquemas/setup de una sola vez
   → `references/` enlazados; lógica determinista → `scripts/`; cero duplicación
   SKILL↔referencias; un ejemplo por regla; el SKILL exige cierre en chat = resumen +
   rutas (nunca el entregable completo).
2. **Después de escribir (bloqueante):** ejecutá el skill `agent-efficiency-reviewer`
   sobre el agente tocado. **Prohibido commitear** sin veredicto `APROBADO` o
   `APROBADO CON OBSERVACIONES`. Con `MEJORAR`: corregir y re-medir.
3. Actualizá la tabla de `AI-Agents/README.md`.
4. Paso a paso completo: `docs/playbook-nuevo-agente.md`.

Excepción: cambios menores (typo, enlace) en un agente aprobado → basta verificar con
`wc -c` que no se cruzó ningún umbral.

## Git sync

Antes de commit/push, leé `config.json` raíz → `git_sync`:

- `mode: manual` → no commitear; listar rutas tocadas y preguntar.
- `mode: automatic` → commit + push sin preguntar, solo de los archivos del alcance
  de la corrida; sin secretos; mensaje corto estilo conventional; nunca `--force`.
- `apply_to`: `new_agents` cubre `AI-Agents/`; `agent_outputs` cubre `AI-Outputs/`.
- Lo que el usuario pida en el chat gana sobre `config.json` para esa corrida.

Detalle completo: `docs/git-sync.md` y `.cursor/rules/git-sync.mdc`.

## Convenciones generales

- Idioma de skills, informes y commits descriptivos: español (voseo rioplatense en
  instrucciones al usuario).
- Los entregables canónicos son archivos en `AI-Outputs/`; el chat resume y enlaza.
- Credenciales Jira: variables de entorno personales, jamás en el repo ni en el chat.
