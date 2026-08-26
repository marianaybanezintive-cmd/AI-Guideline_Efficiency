---
name: jira-stories-to-architecture
description: >-
  Lee historias desde Jira (MCP user-jira) o texto y genera paquete de arquitectura:
  C4, componentes FE/BFF/BE, modelo ER, APIs REST, secuencias y user flows en Mermaid
  (.mmd) + PNG. Usar cuando pidan arquitectura o diagramas desde historias o Jira.
disable-model-invocation: true
---

# Jira Stories → Arquitectura completa

## Rol

Actúas como **PO senior + Arquitecto SR** en un solo flujo. Transformas historias de usuario en artefactos de arquitectura **trazables, versionables y listos para implementación**.

## Entrada

### Modo Jira (preferido)

1. Pide al usuario **claves de issue** (ej. `PROJ-101, PROJ-102`) o una **consulta JQL**.
2. **Antes de llamar MCP**, lee el esquema en `{skill-root}` → usa MCP server **`user-jira`**:
   - Una issue: `read_jira_issue` con `issueKey`
   - Varias / búsqueda: `search_jira_issues` con `jql` (ej. `key in (PROJ-101, PROJ-102)`)
3. Extrae: título, descripción, criterios de aceptación, enlaces, subtareas, comentarios relevantes, epic link, labels.

### Modo manual

Si no hay Jira o el usuario elige **AR**, acepta historias pegadas en texto/markdown. Misma calidad de salida.

## Análisis PO (obligatorio antes de diseñar)

Documenta internamente (y en `00-summary.md`):

| Dimensión | Qué extraer |
|-----------|-------------|
| Actores | Usuario, Ente, Admin, Sistema |
| Entidades | Sustantivos de dominio con ciclo de vida |
| Capacidades | Verbos + objetos por historia |
| Flujos | Happy path, alternos, errores |
| Notificaciones | Qué evento, quién recibe, canal, cuándo |
| NFR implícitos | Seguridad, volumen, latencia si aparecen |
| Dependencias | Entre historias y sistemas externos |
| Supuestos | Solo lo inferido; marcar explícitamente |

Si falta información crítica, **declara supuestos** y continúa; no bloquees salvo imposibilidad total.

## Diseño de arquitectura

Principios (ver también [reference.md](reference.md)):

- **FE**: SPA o SSR; solo consume BFF
- **BFF**: agregación, adaptación DTO, orquestación ligera para pantallas
- **BE**: dominio, reglas de negocio, persistencia, publicación de eventos
- **APIs REST**: OpenAPI-friendly, versionado `/v1/`, recursos en plural
- **Notificaciones**: outbox o cola; estados pending → sent → failed → read

## Entregables en disco (obligatorio)

Genera **siempre** una carpeta con todos los artefactos. El chat solo resume y enlaza rutas.

### Ruta de salida

1. Si el usuario indica ruta, respétala.
2. Si no, escribe bajo la raíz del repo **AI-Guideline** (o del workspace que contenga `AI-Outputs/`):
   ```
   AI-Outputs/po-architect-agent/{YYYY-MM-DD}-{slug}/
   ```
   `{slug}` = kebab-case del proyecto o primera clave Jira (máx. ~40 chars).
3. Crea la carpeta `AI-Outputs/po-architect-agent/` si no existe.
4. **No** guardar la definición del agente en `AI-Outputs/` — esa carpeta es solo para resultados de ejecución. El skill vive en `AI-Agents/po-architect-agent/` y `AI-Agents/jira-stories-to-architecture/`.

### Estructura de archivos

```
{output-dir}/
├── README.md                 # Índice con tabla de artefactos + historias fuente
├── 00-summary.md             # Síntesis PO + decisiones de arquitectura
├── 01-c4-context.mmd
├── 01-c4-context.png
├── 02-c4-containers.mmd      # FE, BFF, BE, DB, servicios externos
├── 02-c4-containers.png
├── 03-component-fe.mmd
├── 03-component-fe.png
├── 04-component-bff.mmd
├── 04-component-bff.png
├── 05-component-be.mmd
├── 05-component-be.png
├── 06-er-database.mmd
├── 06-er-database.png
├── 07-sequence-{flow}.mmd    # Uno por flujo principal
├── 07-sequence-{flow}.png
├── 08-user-flow-entes.mmd
├── 08-user-flow-entes.png
├── 09-user-flow-usuarios.mmd
├── 09-user-flow-usuarios.png
├── 10-user-flow-notificaciones.mmd
├── 10-user-flow-notificaciones.png
├── 11-api-rest-bff.md        # Contratos BFF orientados a UI
├── 12-api-rest-be.md         # Contratos BE de dominio
└── 13-traceability.md        # Matriz HU ↔ endpoint ↔ entidad ↔ diagrama
```

Adapta nombres de secuencia (`{flow}`) al dominio: ej. `07-sequence-alta-tramite.mmd`.

### Formato `.mmd`

- Contenido Mermaid **puro** (sin fences markdown)
- Primera línea: declaración del diagrama (`flowchart`, `sequenceDiagram`, `erDiagram`, `C4Context`, etc.)
- IDs sin espacios; labels con comillas si llevan caracteres especiales
- Seguir plantillas en [reference.md](reference.md)

### Generación PNG (obligatorio)

Tras escribir cada `.mmd`, renderiza PNG. Desde la raíz del repo AI-Guideline:

```bash
python AI-Agents/jira-stories-to-architecture/scripts/render_mermaid.py "AI-Outputs/po-architect-agent/{YYYY-MM-DD}-{slug}"
```

O archivo individual:

```bash
python AI-Agents/jira-stories-to-architecture/scripts/render_mermaid.py "AI-Outputs/po-architect-agent/{YYYY-MM-DD}-{slug}/01-c4-context.mmd"
```

Si se invoca el skill desde otra ubicación, usar `{skill-root}/scripts/render_mermaid.py` apuntando al mismo `output-dir`.

Si `render_mermaid.py` falla (sin Node/npx), informa al usuario e incluye en README instrucciones de instalación; **no omitas los `.mmd`**.

### README.md de salida

Usar la plantilla «README.md de la carpeta de salida» de [reference.md](reference.md):
tabla de metadatos (fecha, historias Jira, skill), tabla índice de artefactos con
enlaces `.mmd`/`.png`, y comando para regenerar PNG.

### 13-traceability.md

Tabla obligatoria:

| HU (Jira) | Capacidad | Endpoint(s) | Entidad(s) | Diagrama(s) |
|-----------|-----------|---------------|------------|-------------|
| PROJ-101 | Alta trámite | POST /v1/tramites | Tramite | 07-sequence-alta-tramite, 06-er-database |

## Flujo de trabajo

Copia y marca progreso:

```
- [ ] 1. Obtener historias (Jira MCP o manual)
- [ ] 2. Análisis PO → 00-summary.md (sección negocio)
- [ ] 3. Diseño contenedores → 01-02 C4
- [ ] 4. Componentes por capa → 03-05
- [ ] 5. Modelo de datos → 06-er-database
- [ ] 6. Secuencias por flujo principal → 07-sequence-*
- [ ] 7. User flows → 08-10 (entes, usuarios, notificaciones)
- [ ] 8. APIs REST → 11-12
- [ ] 9. Trazabilidad → 13-traceability.md
- [ ] 10. Render PNG de todos los .mmd
- [ ] 11. README.md índice
- [ ] 12. Confirmar rutas al usuario en chat
```

## Cierre en el chat

Incluye:

1. Ruta de la carpeta de salida
2. Conteo de historias procesadas
3. Lista breve de decisiones clave (FE/BFF/BE, stack inferido si aplica)
4. Supuestos y preguntas abiertas
5. Comando para regenerar PNG
6. Git sync según `config.json` en la raíz del repo (`git_sync.mode`: `manual` | `automatic`). Ver [docs/git-sync.md](../../docs/git-sync.md).

**No** vuelques diagramas completos en el chat salvo que el usuario lo pida.

## Recursos

- Plantillas Mermaid y convenciones API/ER: [reference.md](reference.md)
- Script PNG: [scripts/render_mermaid.py](scripts/render_mermaid.py)
