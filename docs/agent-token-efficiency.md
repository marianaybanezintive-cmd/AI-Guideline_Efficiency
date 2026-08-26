# Eficiencia de tokens en agentes (AI-Agents)

Guía de presupuestos y reglas para que los agentes del repo consuman la menor cantidad
de tokens posible sin perder calidad de resultados. La aplica el agente
[`agent-efficiency-reviewer`](../AI-Agents/agent-efficiency-reviewer/SKILL.md) cada vez
que se agrega o modifica un agente.

> **¿Vas a crear un agente nuevo?** Seguí el paso a paso en
> [playbook-nuevo-agente.md](playbook-nuevo-agente.md): diseño dentro de presupuestos,
> auto-chequeo, invocación del reviewer, interpretación del veredicto y git sync.

**Enforcement:** estas reglas se cargan automáticamente en cada sesión vía
[`.cursor/rules/agent-efficiency.mdc`](../.cursor/rules/agent-efficiency.mdc) (Cursor)
y [`CLAUDE.md`](../CLAUDE.md) (Claude Code). Ambas remiten aquí como fuente de verdad:
si cambiás un presupuesto, cambialo **en este documento** y verificá que los umbrales
citados en esas reglas sigan coincidiendo.

## Cómo consume tokens un agente

| Momento | Qué se carga | Frecuencia |
|---------|--------------|------------|
| Siempre | El `description` del frontmatter de **todos** los skills (listado de skills disponibles) | Cada sesión, se use o no el agente |
| Al invocar | El cuerpo completo de `SKILL.md` | Una vez por invocación |
| Bajo demanda | `reference.md`, plantillas, esquemas enlazados | Solo si el flujo los necesita |
| Durante la corrida | Salidas de scripts, archivos leídos, texto que el agente repite en el chat | Variable — suele ser el mayor costo real |

Conclusión: el `description` es el único costo **permanente**; el `SKILL.md` es el costo
fijo por corrida; los archivos de referencia son gratis mientras no se lean. Por eso la
estrategia es **divulgación progresiva**: SKILL.md corto con las reglas de decisión, y el
detalle (plantillas, ejemplos, setup) en archivos de referencia que se leen solo cuando
tocan.

## Presupuestos (budgets)

Medición canónica: **`wc -c` sobre el archivo completo** (incluye frontmatter);
el `description` se mide solo, extrayendo el bloque del frontmatter.

| Artefacto | Presupuesto | Límite duro |
|-----------|-------------|-------------|
| `description` (frontmatter) | ≤ 350 caracteres (~4 líneas) | 500 caracteres |
| `SKILL.md` (archivo completo) | ≤ 6.000 caracteres (~1.500 tokens) | 10.000 caracteres |
| Archivo de referencia individual | ≤ 12.000 caracteres | — (se lee solo bajo demanda) |
| Salida en chat al cerrar | Resumen + rutas + conteos | Nunca pegar el entregable completo |

Estimación rápida: `tokens ≈ caracteres / 4` (en español tiende a `/ 3,5`).

## Reglas de diseño

1. **Description = disparador, no manual.** Qué hace + cuándo usarlo, en 2–4 líneas.
   Se paga en cada sesión de cada usuario del repo.
2. **SKILL.md contiene decisiones, no plantillas.** Formatos de salida, esquemas,
   ejemplos largos y guías de setup van en `references/` o archivos `.md` hermanos,
   enlazados desde el SKILL.
3. **Cero duplicación.** Una regla vive en un solo archivo; los demás la enlazan.
   Si el SKILL repite la estructura que ya define una plantilla, se recorta el SKILL.
4. **Un ejemplo por regla.** Un formato preferido basta; las variantes aceptables se
   omiten o van a referencia.
5. **README.md es para humanos.** No se carga en contexto: no duplicar ahí contenido
   del SKILL pensando que "ayuda al agente", ni meter en el SKILL contenido que solo
   sirve a humanos (árboles de estructura del propio agente, historia del proyecto).
6. **Delegar cómputo a scripts.** Todo lo determinista (llamadas REST, métricas,
   render) va a scripts que emiten archivos, no texto masivo al chat. El agente lee
   el resultado mínimo necesario (ej. `metrics.json`, no `raw.json`).
7. **Disciplina de chat.** El entregable canónico es el archivo en `AI-Outputs/`;
   el chat resume, enlaza rutas y da conteos. Prohibido volcar el documento completo,
   diagramas o descriptions en el chat salvo pedido explícito.
8. **Setup de una sola vez → referencia.** Instrucciones de credenciales, instalación
   o primera configuración no se pagan en cada corrida: van a un archivo de setup.
9. **No releer lo ya leído.** El SKILL debe indicar qué referencia leer y cuándo,
   para evitar lecturas especulativas de todos los archivos del paquete.
10. **`disable-model-invocation: true`** cuando el agente solo tiene sentido invocado
    explícitamente por el usuario (evita disparos accidentales y su costo).

## Línea base del repo (auditoría 2026-08-25)

Estado tras la optimización inicial (caracteres del cuerpo; el ahorro principal fue
recortar descriptions ~50–60 % y mover duplicaciones a referencias):

| Agente | SKILL.md antes | SKILL.md después | Cambios |
|--------|---------------:|-----------------:|---------|
| po-expert-user-stories | 11.432 | 9.626 | Description −45 %; tabla 13 secciones, formato de tarjetas y ejemplos MSG deduplicados contra `md-template.md` |
| sprint-health-check | 9.136 | 7.889 | Description −50 %; setup de credenciales y racional REST-vs-MCP movidos a `references/setup-credentials.md` |
| jira-stories-to-architecture | 7.644 | 7.036 | Description −45 %; plantilla README movida a `reference.md` |
| jira-load-user-stories | 6.928 | 6.677 | Description −45 % |
| sm-mass-clone | 6.359 | 5.896 | Description −35 %; árbol de estructura eliminado |
| po-architect-agent | 2.486 | 2.306 | Description −50 % |

Cuatro agentes quedan por encima del presupuesto de 6.000, todos dentro del límite
duro y aceptados con justificación: `po-expert-user-stories` (9.626 — dos pausas HITL
con protocolo textual), `sprint-health-check` (7.889 — pipeline de 6 pasos con
comandos), `jira-stories-to-architecture` (7.036 — especificación de 24 artefactos de
salida) y `jira-load-user-stories` (6.677 — protocolo de dos fases con reglas de
sustitución de códigos). Cualquier crecimiento futuro de estos SKILL debe compensarse
moviendo contenido a referencias.

## Mayor costo restante (no es el SKILL)

En los agentes generadores (`po-expert-user-stories`, `jira-stories-to-architecture`)
el costo dominante es la **generación del entregable** (documentos de 10–40 k tokens),
no las instrucciones. Palancas: no regenerar documentos completos por correcciones
menores (editar secciones), y en las pausas HITL presentar los ítems en bloque numerado
único en lugar de uno por mensaje.
