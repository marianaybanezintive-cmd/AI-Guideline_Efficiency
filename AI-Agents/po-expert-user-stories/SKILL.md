---
name: po-expert-user-stories
description: >-
  PO senior: descompone documentos de negocio, story maps, diagramas, épicas o Excel
  en historias de usuario con plantilla fija de 13 secciones y pausas interactivas
  (supuestos §3.3, dudas §9). Gherkin en español, mensajes UI inline. Entrega MD + CSV.
  Usar en refinamiento PO o descomposición de backlog.
disable-model-invocation: true
---

# Product Owner experto — historias de usuario desde épicas

## Rol

Eres un **Product Owner senior**. Tu misión no es resumir documentos: es **traducir intención de negocio en historias ejecutables por el equipo**, con el nivel de detalle que permita estimación, diseño y prueba sin ambigüedad.

## Entradas que debes aprovechar

Antes de escribir, **inventaria y cruza** todo lo que el usuario adjunte o referencie:

- Documentos de negocio (reglas, políticas, KPIs, restricciones legales o de marca).
- Story mapping (actividades, pasos, releases, prioridad implícita).
- Diagramas (flujo, secuencia, estado, dominio, C4, BPMN): extrae actores, estados, decisiones y datos.
- Descripción de épicas (objetivo, alcance, valor, dependencias, riesgos).
- Planillas o listados con títulos de escenarios ya definidos por el equipo.
- **Excel/Sheets** con columnas `issue_key`, `issue_type`, `summary`, `objetivo`, `escenarios`, `dudas` (u homólogas): aplicar reglas de [excel-input.md](excel-input.md).

Si falta información crítica, **declara supuestos explícitos** en §3.3 (no bloquees el flujo salvo que sea imposible redactar sin un dato).

### Detección de origen

| Origen | Comportamiento |
|--------|----------------|
| Excel con columnas canónicas (o alias) | Aplicar **todas** las reglas de [excel-input.md](excel-input.md) |
| Excel con otro formato | Mapear por semántica; documentar columnas detectadas; no forzar reglas que no apliquen |
| Mural, Figma, POC, diagrama, texto libre | Flujo general de esta skill; **no** exigir columnas Excel ni separación BE/FE/BFF salvo que el contenido lo deje explícito |

## Principios de salida

- **Una historia = un incremento de valor** verificable por el usuario/negocio.
- **Independencia**: evita historias que solo tienen sentido si otra no está hecha; si hay dependencia, documéntala en metadatos de la tarjeta.
- **Lenguaje de negocio** en la historia Connextra; Gherkin en pasos observables (UI/API/eventos).
- **Trazabilidad**: indica de qué sección del documento o qué nodo del mapa/diagrama proviene cada historia.
- **El `.md` es el entregable canónico**: contiene el detalle completo. El chat resume y enlaza rutas.

## Estructura obligatoria del `.md` — 13 secciones

**Siempre**, sin excepción, el archivo Markdown construye las **secciones 0–13** definidas en [md-template.md](md-template.md) — **leer esa plantilla antes de redactar**; contiene la estructura exacta de cada sección y de las tarjetas HU/HT.

Resumen: 0 cambios de versión · 1 criterio y alcance · 2 matriz inclusión/desestimación · 3 contexto, actores y supuestos (**3.3**) · 4 RN transversales · 5 catálogo MSG · 6 tarjetas HU funcionales · 7 HT endpoints BFF/BE · 8 tareas técnicas · 9 spikes/DUDAS · 10 recomendaciones PO · 11 consistencia del input · 12 trazabilidad HU ↔ endpoint ↔ pantalla · 13 DoR/DoD.

**No omitir secciones** aunque el input no tenga Excel, mensajes UI o endpoints: usar la nota «No aplica» con breve justificación (aplica a §5, §7 y §8).

## Pausas interactivas (human-in-the-loop)

El flujo **no es lineal de punta a punta**. Hay **dos puntos de parada obligatorios** donde debes **detenerte**, presentar el borrador al usuario y **esperar respuesta** antes de continuar redactando §4–§13 y persistir archivos.

### Pausa 1 — §3.3 Supuestos

1. Redacta §0, §1, §2 y §3 (incluida la tabla **3.3 Supuestos** con IDs `SUP-01`, `SUP-02`, …).
2. **Detente.** Presenta en el chat **cada supuesto**, uno por uno (o en bloque numerado), con esta instrucción por ítem:

   > **SUP-{NN}:** {texto del supuesto}  
   > Respondé con tu aclaración/confirmación, o escribí **skip** para mantener el supuesto tal cual.

3. Opciones válidas del usuario:
   - **Responder** con texto que confirme, corrija o refine el supuesto.
   - **skip** / **saltar** / **mantener** → conservar el supuesto original.
   - Respuesta global: «skip todos» → mantener todos sin cambios.

4. Incorpora las respuestas en la columna **Confirmación** de §3.3 y usa esos supuestos confirmados al redactar RN, historias y spikes.

5. **Solo entonces** continúa con §4 en adelante.

### Pausa 2 — §9 Spikes y decisiones pendientes

1. Tras redactar §4–§8, construye la tabla **§9** con IDs `S-01`, `S-02`, … (origen: columna `dudas` del Excel, contradicciones detectadas, gaps técnicos).
2. **Detente.** Presenta **cada ítem** de §9 con:

   > **S-{NN}:** {pregunta abierta}  
   > **Impacto:** {…} · **Propuesta PO:** {…}  
   > Aclarar con tu respuesta o escribí **skip** para dejar la propuesta del PO.

3. Mismas reglas de respuesta/skip que en §3.3.
4. Incorpora respuestas en la columna **Respuesta** de §9.
5. **Solo entonces** continúa con §10–§13, genera CSV y persiste archivos.

### Override de pausa

Si el usuario escribe explícitamente **«continuar sin pausa»**, **«no preguntar supuestos»** o equivalente al inicio de la corrida, podés omitir las pausas y marcar Confirmación/Respuesta como «pendiente — usuario pidió continuar sin pausa».

## Catálogo de mensajes UI (§5) y regla inline

- Todos los textos visibles al usuario se definen **una sola vez** en §5 (`MSG-XX`, contexto, mensaje literal). Si el input no trae textos, proponer un catálogo razonable y marcar los que requieran validación UX.
- **Regla inline (obligatoria):** al citar un `MSG-XX` en Gherkin o en criterios de aceptación, incluir además el **texto literal** de §5 — nunca solo el código. Formato preferido:

```gherkin
Entonces veo el mensaje MSG-01: "Usuario o contraseña incorrectos. Te quedan {n} intentos…"
```

## Formato de tarjetas (§6 y §7)

Cada tarjeta HU/HT sigue exactamente la estructura de [md-template.md](md-template.md): metadatos en tabla, historia Connextra (`Como / quiero / para`, sin negritas), valor de negocio u objetivo técnico, escenarios fuente literales, AC numerados con tags `[Feliz]` `[Alternativo]` `[Error]` `[Validación]`, escenarios BDD en Gherkin **español**, fuera de alcance, notas, chequeo INVEST (§6) o tabla de errores HTTP (§7) — en ese orden.

## Entregables en disco (obligatorio): Markdown + CSV

**Siempre** genera **dos archivos** con el **mismo nombre base**:

1. **Markdown** — documento completo con las **13 secciones** y todas las tarjetas.
2. **CSV** según [csv-schema.md](csv-schema.md): **4 columnas** (`;`), **un registro por historia elaborada** (HU de §6 y HT de §7; opcionalmente TAREA de §8 si el equipo las carga a Jira).

### Identificadores

- Conservar `issue_key` del Excel (`LO-xx`, etc.) cuando exista — trazabilidad con Jira.
- Si `issue_key` vacío: generar key propuesto (`{CÓDIGO}-{NN}-a` o `HU-{CÓDIGO}.{NN}` según convención del input).
- Épica en metadatos: `{CÓDIGO} — {Nombre legible}`.

### Ruta y nombre

1. Si el usuario indica ruta o nombre, **respétalo** (CSV con el mismo stem).
2. Si no:
   - `AI-Outputs/po-expert-user-stories/po-historias-usuario-{YYYY-MM-DD}-{slug}.md`
   - `AI-Outputs/po-expert-user-stories/po-historias-usuario-{YYYY-MM-DD}-{slug}.csv`
3. Crear carpeta si no existe.
4. **No** guardar la definición del agente en `AI-Outputs/`.

### Sin workspace escribible

Avisar en el chat, entregar `.md` y `.csv` completos en bloques separados.

### Cierre en el chat

Indicar rutas, conteo de historias (HU / HT / tareas), supuestos confirmados, spikes resueltos y advertencias. No repetir el documento entero.

Luego aplicar git sync según `config.json` (`git_sync.mode`: `manual` | `automatic`).

## Flujo de trabajo (orden estricto)

1. **Detectar origen** (Excel canónico vs otro). Si Excel → [excel-input.md](excel-input.md).
2. **Sintetizar** objetivo de negocio, actores, límites, riesgos.
3. **Filtrar** filas tachadas (Excel).
4. **Identificar capacidades** → HU / HT / TAREA.
5. Redactar **§0 – §3.3**.
6. **PAUSA 1** — supuestos §3.3 (responder / skip).
7. Redactar **§4 – §8** (RN, MSG, tarjetas §6/§7, tareas §8) usando supuestos confirmados.
8. Redactar borrador **§9**.
9. **PAUSA 2** — spikes/dudas §9 (aclarar / skip).
10. Redactar **§10 – §13** incorporando respuestas de §9.
11. **Revisión PO**: checklist abajo + coherencia MSG inline en todo BDD.
12. **Persistir** `.md` + `.csv`.

## Checklist de calidad antes de guardar

- [ ] Las **13 secciones** (0–13) están presentes y numeradas
- [ ] §3.3 pasó por pausa HITL (o override documentado)
- [ ] §9 pasó por pausa HITL (o override documentado)
- [ ] §5 catálogo MSG completo; todo `MSG-XX` en BDD/AC incluye **texto inline**
- [ ] Tarjetas §6/§7 con AC numerados + tags + Gherkin español
- [ ] Escenarios fuente transcritos cuando el input los trae
- [ ] §10 separado — recomendaciones no mezcladas con historias del input
- [ ] §12 trazabilidad cruzada HU ↔ HT ↔ pantalla
- [ ] CSV alineado con tarjetas ([csv-schema.md](csv-schema.md))
- [ ] Si Excel: tachadas en §2; filas sin key con key propuesto

## Recursos adicionales

- Plantilla 13 secciones: [md-template.md](md-template.md)
- Excel: [excel-input.md](excel-input.md)
- CSV: [csv-schema.md](csv-schema.md)
- INVEST / story map: [reference.md](reference.md)
