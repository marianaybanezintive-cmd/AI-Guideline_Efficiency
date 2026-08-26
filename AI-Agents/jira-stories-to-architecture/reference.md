# Referencia — plantillas Mermaid y convenciones

## Convenciones de nomenclatura

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Contenedores C4 | FE, BFF, BE, DB, EXT | `BFF_Notificaciones` |
| Entidades ER | PascalCase singular | `Usuario`, `Notificacion` |
| Endpoints REST | `/v1/{recurso-plural}` | `GET /v1/notificaciones` |
| Actores flujo | emoji + nombre | `👤 Usuario`, `🏢 Ente`, `🔔 Sistema Notificaciones` |

## 01 — C4 Context (contexto)

```mermaid
C4Context
  title Diagrama de Contexto — {Proyecto}

  Person(usuario, "Usuario", "Descripción del rol")
  Person_Ext(ente, "Ente externo", "Organismo / tercero")
  System(sistema, "Sistema objetivo", "Valor principal entregado")
  System_Ext(notif, "Servicio de Notificaciones", "Email, push, SMS")
  System_Ext(idp, "Identity Provider", "Autenticación OAuth2/OIDC")

  Rel(usuario, sistema, "Usa")
  Rel(ente, sistema, "Intercambia datos vía API")
  Rel(sistema, notif, "Envía notificaciones")
  Rel(usuario, idp, "Autentica")
  Rel(sistema, idp, "Valida tokens")
```

## 02 — C4 Container (FE / BFF / BE separados)

```mermaid
C4Container
  title Contenedores — {Proyecto}

  Person(usuario, "Usuario")

  Container_Boundary(c1, "Frontend") {
    Container(fe, "Web App", "React/Vue/Angular", "UI para usuarios")
  }

  Container_Boundary(c2, "BFF Layer") {
    Container(bff, "BFF API", "Node/Nest/FastAPI", "Agregación, adaptación de respuestas para FE")
  }

  Container_Boundary(c3, "Backend Domain") {
    Container(be, "Domain API", "Java/Spring, .NET, Go", "Lógica de negocio y persistencia")
    ContainerDb(db, "Base de datos", "PostgreSQL", "Datos transaccionales")
  }

  Container_Ext(notif, "Notification Service", "Message broker / SMTP / FCM")

  Rel(usuario, fe, "HTTPS")
  Rel(fe, bff, "REST/JSON")
  Rel(bff, be, "REST/JSON interno")
  Rel(be, db, "SQL/ORM")
  Rel(be, notif, "Eventos / API")
```

## 03–05 — Componentes por capa

Usar `flowchart TB` o `C4Component` según complejidad. Un diagrama por capa:

- **FE**: páginas, stores, servicios HTTP hacia BFF
- **BFF**: controllers, DTO mappers, clients hacia BE
- **BE**: controllers REST, services, repositories, entities

## 06 — Modelo ER (base de datos)

```mermaid
erDiagram
  USUARIO ||--o{ NOTIFICACION : recibe
  USUARIO {
    uuid id PK
    string email UK
    string nombre
    datetime created_at
  }
  ENTE ||--o{ TRAMITE : gestiona
  ENTE {
    uuid id PK
    string codigo UK
    string razon_social
  }
  NOTIFICACION {
    uuid id PK
    uuid usuario_id FK
    string canal
    string estado
    json payload
    datetime enviado_at
  }
```

Reglas:
- PK/FK explícitos; tipos alineados al motor (PostgreSQL por defecto)
- Tablas en MAYÚSCULAS en diagrama; nombres físicos en snake_case en `07-database-schema.sql` si se genera

## 07 — Diagrama de secuencia

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant FE as Frontend
  participant BFF as BFF API
  participant BE as Backend
  participant DB as Database
  participant N as Notificaciones

  U->>FE: Acción en UI
  FE->>BFF: POST /v1/recurso
  BFF->>BE: POST /internal/v1/recurso
  BE->>DB: INSERT ...
  DB-->>BE: OK
  BE->>N: Publicar evento notificacion.creada
  BE-->>BFF: 201 Created
  BFF-->>FE: DTO adaptado
  FE-->>U: Confirmación UI
```

Un `.mmd` por flujo principal identificado en las historias (happy path + variantes críticas).

## 08 — User flow — Entes

```mermaid
flowchart TD
  Start([Ente inicia sesión]) --> Auth{Autenticado?}
  Auth -->|No| Login[Pantalla login]
  Login --> Auth
  Auth -->|Sí| Dashboard[Panel ente]
  Dashboard --> Accion[Operación de negocio]
  Accion --> Resultado{Resultado}
  Resultado -->|OK| NotifOk[Notificación confirmación]
  Resultado -->|Error| NotifErr[Notificación error]
```

## 09 — User flow — Usuarios

Misma estructura; actores y pantallas según historias. Incluir ramas de permisos/roles.

## 10 — User flow — Notificaciones

```mermaid
flowchart LR
  subgraph Triggers
    T1[Evento de dominio]
    T2[Job programado]
    T3[Acción manual admin]
  end

  subgraph Pipeline
    Q[Cola / outbox]
    R[Router por canal]
    E[Email]
    P[Push]
    S[SMS]
  end

  subgraph Estados
    ST1[pending]
    ST2[sent]
    ST3[failed]
    ST4[read]
  end

  T1 --> Q
  T2 --> Q
  T3 --> Q
  Q --> R
  R --> E & P & S
  E & P & S --> ST2
  ST2 --> ST4
```

## REST API — plantilla OpenAPI (markdown)

Por cada recurso:

```markdown
### GET /v1/{recurso}
- **Historia:** HU-XX.01
- **Descripción:** ...
- **Auth:** Bearer JWT
- **Query:** page, size, filter
- **Response 200:** `{ "data": [...], "meta": { "total": N } }`
- **Errores:** 401, 403, 404

### POST /v1/{recurso}
- **Body:** `{ ... }`
- **Response 201:** `{ "id": "uuid", ... }`
- **Errores:** 400, 409, 422
```

BFF expone contratos orientados a pantallas; BE expone contratos de dominio. Documentar mapeo BFF→BE cuando difieran.

## Checklist de calidad

- [ ] Cada endpoint referencia al menos una HU
- [ ] FE no llama directamente a BE (siempre vía BFF salvo excepción documentada)
- [ ] Entidades ER cubren sustantivos del dominio en las historias
- [ ] Flujos de notificación cubren trigger, canal, estado y reintentos
- [ ] Todos los `.mmd` tienen `.png` correspondiente
- [ ] IDs Mermaid sin espacios ni caracteres especiales (usar `_`)

## Plantilla README.md de la carpeta de salida

```markdown
# Arquitectura — {título}

| Campo | Valor |
|-------|--------|
| **Fecha** | {YYYY-MM-DD} |
| **Historias Jira** | PROJ-101, PROJ-102 |
| **Generado con** | skill `jira-stories-to-architecture` |

## Artefactos

| Archivo | Descripción |
|---------|-------------|
| [00-summary.md](./00-summary.md) | Síntesis y decisiones |
| [01-c4-context.mmd](./01-c4-context.mmd) / [.png](./01-c4-context.png) | Contexto C4 |
| ... | ... |

## Cómo regenerar PNG

\`\`\`bash
python AI-Agents/jira-stories-to-architecture/scripts/render_mermaid.py .
\`\`\`
```

(Ejecutar el comando desde la carpeta de salida, o pasar la ruta a esa carpeta.)
