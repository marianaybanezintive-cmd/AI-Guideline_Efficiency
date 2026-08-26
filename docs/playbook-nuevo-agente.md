# Playbook — Crear un agente nuevo y pasarlo por la revisión de eficiencia

Guía paso a paso para usar [agent-token-efficiency.md](agent-token-efficiency.md) y el
agente [`agent-efficiency-reviewer`](../AI-Agents/agent-efficiency-reviewer/SKILL.md)
cada vez que creás o modificás un agente en `AI-Agents/`.

**Regla del repo:** ningún agente nuevo o modificado se commitea sin veredicto
`APROBADO` o `APROBADO CON OBSERVACIONES` del reviewer.

---

## Fase 0 — Qué se aplica solo (no tenés que acordarte)

El proceso está cableado como **reglas duras** que Cursor y Claude Code cargan
automáticamente en cada sesión de este repo:

| Archivo | Quién lo carga | Qué impone |
|---------|----------------|------------|
| [`.cursor/rules/agent-efficiency.mdc`](../.cursor/rules/agent-efficiency.mdc) | Cursor (siempre) | Ante cualquier cambio bajo `AI-Agents/`: leer la guía antes de escribir, diseñar dentro de presupuestos, pasar por el reviewer y **bloquear el commit** sin veredicto aprobado |
| [`CLAUDE.md`](../CLAUDE.md) (raíz) | Claude Code (siempre) | Las mismas reglas duras + git sync + convenciones del repo |
| [`.cursor/rules/git-sync.mdc`](../.cursor/rules/git-sync.mdc) | Cursor (siempre) | Commit/push según `config.json` → `git_sync` |

En la práctica: escribís en el chat *«creá un agente que haga X»* y el asistente ya
está obligado a leer la guía, respetar presupuestos, correr el reviewer y frenar el
commit si el veredicto es `MEJORAR`. Este playbook te sirve para **entender y auditar**
ese proceso, y para ejecutarlo a mano cuando escribas el agente vos mismo.

Cadena completa de artefactos:

```
.cursor/rules/agent-efficiency.mdc ─┐
CLAUDE.md ──────────────────────────┤ (reglas duras, siempre en contexto)
                                    ▼
        docs/agent-token-efficiency.md   (presupuestos y reglas — fuente de verdad)
                                    ▼
        AI-Agents/agent-efficiency-reviewer/SKILL.md   (el que mide y da veredicto)
                                    ▼
        AI-Outputs/agent-efficiency-reviewer/*.md      (informes de auditoría)
```

---

## Fase 1 — Diseñar el agente CON los presupuestos a la vista

No escribas primero y recortes después: diseñá directamente dentro de los límites.
Antes de escribir una línea, releé la sección «Presupuestos» y «Reglas de diseño» de
[agent-token-efficiency.md](agent-token-efficiency.md). Resumen operativo:

| Decisión al diseñar | Dónde va |
|---------------------|----------|
| Qué hace + cuándo invocarlo (2–4 líneas) | `description` del frontmatter (≤ 350 chars) |
| Reglas de decisión, workflow, checklists de comportamiento | Cuerpo de `SKILL.md` (≤ 6.000 chars) |
| Plantillas de salida, esquemas, ejemplos largos | `references/*.md` o `.md` hermanos, enlazados |
| Setup de una sola vez (credenciales, instalación) | `references/setup-*.md` |
| Lógica determinista (REST, métricas, render) | `scripts/` con salida a archivo |
| Documentación para humanos | `README.md` del agente (no se carga en contexto) |

Estructura mínima esperada:

```
AI-Agents/<mi-agente>/
├── SKILL.md          # obligatorio
├── README.md         # recomendado (para humanos)
├── config.json       # si el agente tiene configuración
├── references/       # si hay plantillas/esquemas/setup
└── scripts/          # si hay pipeline ejecutable
```

Tips de redacción que el reviewer va a chequear:

- Si el agente solo tiene sentido invocado explícitamente, agregá
  `disable-model-invocation: true` al frontmatter.
- Incluí una sección de «cierre en el chat»: resumen + rutas + conteos, nunca el
  entregable completo.
- Un solo ejemplo por regla; las variantes van a referencia o se eliminan.
- No repitas en el SKILL nada que ya viva en una plantilla o referencia: enlazala.

## Fase 2 — Auto-chequeo rápido (30 segundos, antes de invocar al reviewer)

Desde la raíz del repo:

```bash
# Tamaño del SKILL y de las referencias (archivo completo)
wc -c AI-Agents/<mi-agente>/*.md AI-Agents/<mi-agente>/references/*.md 2>/dev/null

# Longitud del description del frontmatter (chars)
awk '/^description:/{f=1;next} f&&(/^[a-z]/||/^---/){exit} f' AI-Agents/<mi-agente>/SKILL.md | wc -c
```

Semáforo (tokens ≈ caracteres / 4):

| Medida | ✅ | ⚠️ | ❌ |
|--------|----|----|----|
| `description` | ≤ 350 chars | 351–500 | > 500 |
| `SKILL.md` | ≤ 6.000 chars | 6.001–10.000 (necesita justificación) | > 10.000 |

Si estás en ❌, corregí antes de seguir: el reviewer te va a devolver `MEJORAR` seguro.

## Fase 3 — Invocar al reviewer

En el chat del agente (Cursor / Claude Code), con el repo como workspace:

> Usá el skill **agent-efficiency-reviewer** para auditar el agente nuevo
> `AI-Agents/<mi-agente>/`.

Variantes útiles:

- Revisión de una modificación: *«revisá con agent-efficiency-reviewer los cambios que
  hice en AI-Agents/sprint-health-check»*.
- Auditoría completa del repo: *«auditá todos los agentes de AI-Agents/ con
  agent-efficiency-reviewer»* (genera informe consolidado en
  `AI-Outputs/agent-efficiency-reviewer/`).

El reviewer va a: leer `docs/agent-token-efficiency.md` (fuente de los umbrales),
medir con `wc -c`, chequear presupuestos y estructura (duplicación, divulgación
progresiva, disciplina de chat, delegación a scripts) y emitir el informe con
veredicto.

## Fase 4 — Interpretar el veredicto y actuar

| Veredicto | Qué significa | Qué hacés |
|-----------|---------------|-----------|
| **APROBADO** | Dentro de presupuestos, sin duplicación relevante | Seguí a Fase 5 |
| **APROBADO CON OBSERVACIONES** | Excede algún presupuesto con justificación válida (ej. protocolo HITL), o solo hallazgos BAJA | Documentá la justificación en el informe/PR y seguí a Fase 5 |
| **MEJORAR** | Excede límites duros o tiene duplicación/estructura corregible | Aplicá las correcciones propuestas (o pedile al reviewer que las aplique), volvé a Fase 2 |

Para cada hallazgo el reviewer debe darte: severidad, archivo, medida o regla
incumplida, y acción concreta. Si un hallazgo no trae acción, pedila.

**Excepciones:** si el SKILL supera el presupuesto por comportamiento crítico
(pausas HITL, protocolos de confirmación, pipelines con comandos), no lo recortes —
pedí `APROBADO CON OBSERVACIONES` y que la justificación quede escrita en el informe.
El límite duro (10.000) no tiene excepción: por encima, siempre hay algo que mover a
referencias.

## Fase 5 — Registrar y sincronizar

1. Agregá la fila del agente a la tabla de [`AI-Agents/README.md`](../AI-Agents/README.md).
2. Si la revisión cubrió varios agentes, verificá que el informe quedó en
   `AI-Outputs/agent-efficiency-reviewer/{YYYY-MM-DD}-review.md`.
3. Aplicá git sync según `config.json` raíz (`git_sync.mode`: `manual` = confirmar
   antes de commit/push; `automatic` = commit + push directo). Ver [git-sync.md](git-sync.md).

## Checklist final (copiá en tu PR o nota de commit)

```
- [ ] description ≤ 350 chars y responde «qué + cuándo»
- [ ] SKILL.md ≤ 6.000 chars (o justificación escrita si 6.000–10.000)
- [ ] Plantillas/esquemas/setup en references/, enlazados desde el SKILL
- [ ] Sin duplicación entre SKILL y referencias
- [ ] Cierre en chat = resumen + rutas (regla explícita en el SKILL)
- [ ] disable-model-invocation evaluado
- [ ] Veredicto del reviewer: APROBADO / APROBADO CON OBSERVACIONES
- [ ] Fila agregada en AI-Agents/README.md
- [ ] Git sync aplicado según config.json
```

---

## Ejemplo completo (dry-run)

Supongamos que creaste `AI-Agents/release-notes-writer/` con un SKILL.md de 12.400
caracteres que incluye: la plantilla completa del documento de release notes (3.000
chars), instrucciones para configurar el token de GitHub (1.500 chars) y 3 ejemplos
del mismo formato de changelog.

1. **Fase 2**: `wc -c` → 12.400 = ❌ (supera el límite duro).
2. Correcciones antes del reviewer:
   - Plantilla → `references/notes-template.md` (−3.000)
   - Setup del token → `references/setup-credentials.md` (−1.500)
   - 3 ejemplos → 1 ejemplo (−800)
   - SKILL queda en ~7.100 = ⚠️, justificable si el workflow lo amerita.
3. **Fase 3**: invocás al reviewer → `APROBADO CON OBSERVACIONES` (7.100 chars,
   justificación: pipeline de 5 pasos con comandos).
4. **Fase 5**: fila en README, git sync. Listo.
