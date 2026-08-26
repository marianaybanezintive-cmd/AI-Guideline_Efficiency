# Historias de Usuario — Morosidad y Reversiones (Confirming Atlas)

> **Versión:** v1.0.0 · **Fecha:** 2026-08-25
> **Fuente única de requerimientos:** Mural Story Mapping (épicas MOROSIDAD / REVERSIONES) · Anexo 70 (factoring confirming adelanto de facturas) · POC https://marianaintive.github.io/atlas-confirming-poc/ (v2.11.4)
> **Autor:** PO (elaboración de historias) · **Producto:** Portal Confirming — Banco Atlas
> **POC / referencia de diseño:** https://marianaintive.github.io/atlas-confirming-poc/
> **Generado con:** skill `po-expert-user-stories` (persona Alex / po-architect-agent)
> **Nota:** Alcance prioriza lo acordado en Mural. Keys locales `MOR-*` / `REV-*` (S-07).

---

## Tabla de contenidos

0. [Qué cambia respecto de versión anterior](#0-qué-cambia-respecto-de-versión-anterior)
1. [Criterio de elaboración y alcance](#1-criterio-de-elaboración-y-alcance)
2. [Matriz de inclusión / desestimación](#2-matriz-de-inclusión--desestimación)
3. [Contexto de solución, actores y supuestos](#3-contexto-de-solución-actores-y-supuestos)
4. [Reglas de negocio transversales (RN)](#4-reglas-de-negocio-transversales-rn)
5. [Catálogo de mensajes de UI](#5-catálogo-de-mensajes-de-ui)
6. [Historias de usuario funcionales (tarjetas de backlog)](#6-historias-de-usuario-funcionales-tarjetas-de-backlog)
7. [Historias técnicas — Endpoints BFF / BE (enablers)](#7-historias-técnicas--endpoints-bff--be-enablers)
8. [Tareas técnicas / habilitadores](#8-tareas-técnicas--habilitadores)
9. [Spikes y decisiones pendientes (columna DUDAS)](#9-spikes-y-decisiones-pendientes-columna-dudas)
10. [Recomendaciones del PO — historias faltantes](#10-recomendaciones-del-po--historias-faltantes)
11. [Observaciones sobre la consistencia del input](#11-observaciones-sobre-la-consistencia-del-input)
12. [Matriz de trazabilidad HU ↔ endpoint ↔ pantalla](#12-matriz-de-trazabilidad-hu--endpoint--pantalla)
13. [Definition of Ready / Definition of Done](#13-definition-of-ready--definition-of-done)

---

## 0. Qué cambia respecto de versión anterior

Primera elaboración de las épicas **Morosidad** y **Reversiones** como paquete aparte del Confirming del Excel (`po-historias-usuario-2026-08-25-confirming-atlas.md`). Criterios de forma: tarjetas Connextra, AC numerados con tags, Gherkin en español, MSG inline, HITL de supuestos y spikes.

---

## 1. Criterio de elaboración y alcance

| Criterio | Decisión aplicada |
|----------|-------------------|
| **Origen** | Mural (alcance acordado) + Anexo 70 (contexto) + POC (UX) |
| **Prioridad Mural vs Anexo** | Mural gana en roles de aprobación (Operador / Supervisor) y en ítems tachados |
| **Ítems tachados en Mural** | Desestimados (§2) |
| **Flujo UI de reversión** | Fuera: no hay flujo de usuario para iniciar/aprobar en Confirming |
| **Skill de reversión** | Cursor skill operativo (S-05) |
| **Identificadores** | Keys locales `MOR-xx` / `REV-xx` / `MOR-HT-xx` / `REV-HT-xx` |
| **Idioma y formato** | Español; Gherkin ES |
| **HITL** | SUP-01…10 confirmados; S-01…07 respondidos |

| Tipo | Significado |
|------|-------------|
| `HU-FE` | Historia con impacto principal en Front End |
| `HU-BE` | Historia de valor vía backend/notificación |
| `HT` | Historia técnica (endpoint BFF/BE / enabler) |
| `TAREA` | Habilitador de infraestructura, POC o configuración |

---

## 2. Matriz de inclusión / desestimación

| Fila | Key | Summary | Tipo | Estado | Motivo |
|-----:|-----|---------|------|--------|--------|
| 1 | MOR-01 | Marca de morosidad del EGP en panel Confirming | HU-FE | ✅ Incluida | Mural + gap POC |
| 2 | MOR-02 | Grilla grisada y bloqueada cuando EGP en mora | HU-FE | ✅ Incluida | Mural + S-02 |
| 3 | MOR-03 | Notificación in-app por bloqueo de mora | HU-FE | ✅ Incluida | Mural + S-03 |
| 4 | MOR-04 | ABM: umbral de días de mora para bloqueo de límite | HU-FE | ✅ Incluida | Sticky ABM Mural |
| 5 | MOR-05 | Levantar bloqueo al acreditar pago | HU-FE | ✅ Incluida | Mural “reversión de bloqueos” |
| 6 | MOR-HT-01 | GET estado mora EGP vía API Prestamos | HT | ✅ Incluida | S-01 |
| 7 | MOR-HT-02 | Evaluar umbral ABM y aplicar/liberar bloqueo de límite | HT | ✅ Incluida | Mural |
| 8 | MOR-HT-03 | Consumir mensaje CORE pago acreditado | HT | ✅ Incluida | Mural |
| 9 | REV-01 | Mostrar estados de reversión en grilla (FNV, solo lectura) | HU-FE | ✅ Incluida | Diagrama estados + S-06 |
| 10 | REV-02 | Filtro Estado incluye estados de reversión | HU-FE | ✅ Incluida | POC Confirming |
| 11 | REV-HT-01 | Máquina de estados BE de reversión | HT | ✅ Incluida | Diagrama Mural |
| 12 | REV-HT-02 | Cursor skill para revertir manualmente | HT | ✅ Incluida | Mural + S-05 |
| 13 | T-01 | Actualizar POC: marca mora + estados reversión | TAREA | ✅ Incluida | Pedido explícito |
| 14 | T-02 | Mock contrato API Prestamos | TAREA | ✅ Incluida | Enabler FE/POC |
| 15 | — | Actualizar estado de facturas a Mora | — | ❌ Desestimada | Tachado en Mural |
| 16 | — | Marcar todas las facturas del préstamo en Mora | — | ❌ Desestimada | Opción ligada al tachado |
| 17 | — | UI Confirming para iniciar/aprobar reversión | — | ❌ Desestimada | “No hay flujo de usuario por ahora” |

**Resumen:** **12** historias elaboradas (7 HU-FE + 5 HT) · **2** tareas · **3** desestimadas.

---

## 3. Contexto de solución, actores y supuestos

### 3.1 Perfiles de usuario (actores / dominios)

| Dominio | Roles | Operación en estas épicas |
|---------|-------|---------------------------|
| BANCO | Operador / Supervisor | Skill de reversión manual; ABM umbral mora; consulta Confirming |
| EGP | Cargador / Aprobador | Ve marca de mora; grilla bloqueada si en mora; ve estados de reversión en FNV (sin acciones) |
| PROVEEDOR | Cliente Atlas / No cliente | Ve estados de reversión en facturas propias (FNV); no inicia reversión desde UI |

### 3.2 Componentes involucrados

- FE Portal Confirming (panel ente, grilla FV/FNV/FNO, filtros, notificaciones in-app)
- FE Gestión ABM (parámetro días de mora)
- BFF Confirming (orquestación, agregación)
- BE Confirming (límite freezado/bloqueado, máquina de estados)
- **API Prestamos** (fuente canónica estado `Al día` / `En mora` + días) — S-01
- **API CORE** (mensaje de pago acreditado / eventos de desbloqueo)
- Cursor skill operativo de reversión (REV-HT-02)

### 3.3 Supuestos (a confirmar con el equipo técnico)

| # | Supuesto | Confirmación *(post HITL)* |
|---|----------|---------------------------|
| SUP-01 | Sujeto de morosidad = **EGP**; marca en panel del ente seleccionado | confirmado — sin cambios |
| SUP-02 | `En mora` → grilla bloqueada; `Al día` → operable | confirmado — sin cambios |
| SUP-03 | Umbral de días en ABM; CORE/API informa días de mora | confirmado — sin cambios |
| SUP-04 | No se actualiza estado de facturas a “Mora” | confirmado — sin cambios |
| SUP-05 | Pago acreditado (CORE) levanta bloqueo de límite y refresca | confirmado — sin cambios |
| SUP-06 | Reversiones: solo estados visibles + skill manual; sin UI de flujo | confirmado — sin cambios |
| SUP-07 | Estados: `Pendiente de Reversión`, `Pendiente aprobación Supervisor`; finales `Habilitada` / `Bloqueada`; solo si no desembolsado ni pagado | confirmado — sin cambios |
| SUP-08 | Roles Mural: Operador (same-day); Operador → Supervisor (a pasado) | confirmado — sin cambios |
| SUP-09 | POC se actualiza después (T-01), no bloquea redacción | confirmado — sin cambios |
| SUP-10 | Prefijos `MOR-*` / `REV-*` | confirmado — sin cambios |

---

## 4. Reglas de negocio transversales (RN)

| ID | Regla | Fuente |
|----|-------|--------|
| **RN-M01** | La mora de este flujo afecta solo a la **EGP** (deudora del préstamo), no al Proveedor | Anexo 70 §5.2 · SUP-01 |
| **RN-M02** | Estado de mora del cliente: `Al día` \| `En mora`, según **API Prestamos** | Mural · S-01 |
| **RN-M03** | Si `Al día` → grilla operable. Si `En mora` → grilla **visible, grisada y bloqueada** (sin acciones de escritura) | Mural · S-02 |
| **RN-M04** | El límite crediticio se bloquea cuando `días_mora ≥ umbral_ABM` | Mural sticky |
| **RN-M05** | API Prestamos expone al menos: estado + días de mora | S-01 · SUP-03 |
| **RN-M06** | **No** se cambia el estado de las facturas a “Mora” | Mural tachado · SUP-04 |
| **RN-M07** | Al acreditar pago (mensaje CORE) se libera el bloqueo de límite por mora y se refresca el estado en UI | Mural · SUP-05 |
| **RN-M08** | Notificación de mora: **solo in-app** en la plataforma (no email en esta entrega) | S-03 |
| **RN-R01** | Reversión solo si el adelanto está **no desembolsado** y **no pagado** | Diagrama Mural |
| **RN-R02** | Same-day = hasta las **17:00 hora Paraguay** del día de la operación; después = “a pasado” | S-04 · Anexo 70 |
| **RN-R03** | Same-day: aprueba **Operador** → `Habilitada`. A pasado: Operador → `Pendiente aprobación Supervisor` → Supervisor aprueba (`Habilitada`) o rechaza (`Bloqueada`) | Diagrama · SUP-08 |
| **RN-R04** | Facturas en proceso/resultado de reversión se muestran en pestaña **Facturas No Vigentes (FNV)**; no vuelven a ser operativas desde FV | S-06 |
| **RN-R05** | En Confirming no hay acciones de usuario para iniciar/aprobar reversión; la ejecución es vía **Cursor skill** | SUP-06 · S-05 |

---

## 5. Catálogo de mensajes de UI

| Código | Contexto | Mensaje |
|--------|----------|---------|
| MSG-M01 | Banner / bloqueo grilla | "El ente seleccionado está en mora. La grilla de facturas está temporalmente bloqueada." |
| MSG-M02 | Detalle límite bloqueado | "Límite crediticio bloqueado por mora ({n} días). Umbral configurado: {umbral} días." |
| MSG-M03 | Desbloqueo por pago | "Se levantó el bloqueo por mora: el pago fue acreditado. El límite vuelve a estar disponible." |
| MSG-M04 | Error consulta mora | "No se pudo obtener el estado de morosidad. No se asume que el ente está al día." |
| MSG-M05 | Toast notificación mora | "Se bloqueó el límite crediticio del ente por mora." |
| MSG-R01 | Fila en reversión | "Esta factura está en proceso de reversión. Solo consulta; no hay acciones disponibles desde Confirming." |
| MSG-A01 | ABM umbral guardado | "Umbral de días de mora actualizado correctamente." |
| MSG-A02 | ABM umbral inválido | "Ingresá un número entero de días mayor o igual a 0." |

---

## 6. Historias de usuario funcionales (tarjetas de backlog)

### MOR-01 — Marca de morosidad del EGP en panel Confirming

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | MOR — Morosidad |
| **Actor** | Usuario Confirming (EGP / Banco / Proveedor según permisos de ente) |
| **Dominios** | Todos |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-HT-01 |
| **Habilita** | MOR-02, MOR-03 |
| **Pantalla POC** | Confirming → panel de información del ente (hoy sin marca de mora) |

#### Historia
```
Como usuario del Portal Confirming
quiero ver en el panel del ente si la EGP está Al día o En mora (y los días de mora)
para conocer el riesgo crediticio antes de operar
```

#### Valor de negocio
Hace visible en Confirming la condición de mora que hoy solo vive en CORE/API Prestamos, alineando la decisión operativa con el estado real del préstamo.

#### Escenarios fuente
> Mural: al entrar a Confirming, API Prestamos responde “al día” o “en mora”. Sticky: API CORE debe informar mora; TBD API Prestamos / API Límites → resuelto S-01 = API Prestamos.

```text
Al día → grilla habilitada
En mora → grilla bloqueada
Marca de morosidad del cliente en Confirming (gap POC)
```

#### Criterios de aceptación
1. **[Feliz]** Al seleccionar un ente EGP, el panel muestra un indicador visual de estado de mora: `Al día` o `En mora`.
2. **[Feliz]** Si está `En mora`, se muestran los **días de mora** devueltos por API Prestamos.
3. **[Alternativo]** Si está `Al día`, no se muestra alerta de riesgo; el indicador es neutro/positivo.
4. **[Error]** Si falla la consulta, se muestra MSG-M04: "No se pudo obtener el estado de morosidad. No se asume que el ente está al día." y **no** se asume `Al día`.
5. **[Validación]** El indicador es distinguible de un vistazo (badge/color) respecto del límite crediticio.

#### Escenarios BDD
```gherkin
Característica: Marca de morosidad del EGP
  Antecedentes:
    Dado que estoy en la pantalla "Confirming"
    Y opero para el ente "Cervepar (EGP)"

  Escenario: EGP al día
    Dado que API Prestamos responde estado "Al día"
    Cuando se carga el panel del ente
    Entonces veo el indicador "Al día"
    Y no veo alerta de mora

  Escenario: EGP en mora
    Dado que API Prestamos responde estado "En mora" con 12 días
    Cuando se carga el panel del ente
    Entonces veo el indicador "En mora"
    Y veo "12" días de mora

  Escenario: Error de consulta
    Dado que API Prestamos no responde
    Cuando se carga el panel del ente
    Entonces veo el mensaje MSG-M04: "No se pudo obtener el estado de morosidad. No se asume que el ente está al día."
```

#### Fuera de alcance
- Bloqueo de grilla (MOR-02).
- Cálculo de intereses moratorios/punitorios (CORE).

#### Notas / preguntas abiertas
- Propuesta UX POC: badge junto a razón social / límite crediticio del panel rosa.

#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### MOR-02 — Grilla grisada y bloqueada cuando el EGP está en mora

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | MOR — Morosidad |
| **Actor** | Usuario Confirming |
| **Dominios** | Todos |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-01, MOR-HT-01 |
| **Habilita** | — |
| **Pantalla POC** | Confirming → grilla FV/FNV/FNO + botonera |

#### Historia
```
Como usuario del Portal Confirming
quiero que, si la EGP está en mora, la grilla se vea grisada y sin acciones operables
para evitar nuevas operaciones sobre un ente con préstamo en mora
```

#### Valor de negocio
Traduce el estado de mora en contención operativa inmediata: se ve el portafolio pero no se puede cargar, habilitar, bloquear ni simular.

#### Escenarios fuente
```text
Al día → grilla habilitada
En mora → grilla bloqueada
S-02: ve la grilla y las facturas grisada y bloqueada
```

#### Criterios de aceptación
1. **[Feliz]** Con EGP `En mora`, la grilla permanece **visible** con las facturas **grisadas** y no seleccionables para acciones.
2. **[Feliz]** Quedan deshabilitados: `+ Cargar Factura`, `Habilitar`, `Bloquear`, `Simular` y acciones de fila operables (editar fecha, aprobar, etc.).
3. **[Feliz]** Se muestra el banner MSG-M01: "El ente seleccionado está en mora. La grilla de facturas está temporalmente bloqueada."
4. **[Alternativo]** Con EGP `Al día`, la grilla y acciones vuelven al comportamiento normal por permisos/estado de factura.
5. **[Validación]** El usuario puede cambiar de pestaña (FV/FNV/FNO) y filtrar en modo consulta; no puede mutar datos.
6. **[Error]** Si el estado de mora es desconocido (fallo API), se aplica el mismo bloqueo preventivo que `En mora` hasta resolver (alineado a MSG-M04 / no asumir al día).

#### Escenarios BDD
```gherkin
Característica: Bloqueo de grilla por mora
  Antecedentes:
    Dado que estoy en "Confirming" operando para "Cervepar"

  Escenario: Grilla grisada en mora
    Dado que el EGP está "En mora"
    Cuando se renderiza la grilla
    Entonces las filas se ven grisadas
    Y el botón "+ Cargar Factura" está deshabilitado
    Y veo el mensaje MSG-M01: "El ente seleccionado está en mora. La grilla de facturas está temporalmente bloqueada."

  Escenario: Grilla operable al día
    Dado que el EGP está "Al día"
    Cuando se renderiza la grilla
    Entonces las acciones globales se habilitan según permisos y selección
```

#### Fuera de alcance
- Bloqueo automático del límite crediticio (MOR-HT-02 / MOR-03).
- Cambio de estado de facturas a Mora (desestimado).

#### Notas / preguntas abiertas
- —
#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### MOR-03 — Notificación in-app por bloqueo de mora

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | MOR — Morosidad |
| **Actor** | Usuario Confirming del ente afectado |
| **Dominios** | EGP / Banco |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-HT-02 |
| **Habilita** | — |
| **Pantalla POC** | Confirming → notificación in-app (plataforma) |

#### Historia
```
Como usuario del Portal Confirming
quiero recibir una notificación en la plataforma cuando se bloquea el límite por mora
para enterarme del bloqueo sin salir del portal
```

#### Valor de negocio
Cierra el circuito “bloqueo automático + aviso” acordado en Mural, solo dentro de la plataforma (sin email).

#### Escenarios fuente
```text
Bloqueo automático del límite de crédito + mostrar una notificación al usuario en la plataforma
S-03: solo en la plataforma
```

#### Criterios de aceptación
1. **[Feliz]** Cuando el sistema aplica bloqueo de límite por mora, el usuario del ente ve una notificación in-app con MSG-M05: "Se bloqueó el límite crediticio del ente por mora."
2. **[Feliz]** La notificación permite navegar o enfocar Confirming / panel del ente.
3. **[Alternativo]** Si el usuario ya está en Confirming, además se muestra/actualiza MSG-M02 con días y umbral.
4. **[Validación]** No se envía email ni canal externo en esta entrega (RN-M08).
5. **[Error]** Si falla el canal in-app, el bloqueo de límite igualmente queda aplicado; el error se registra para soporte.

#### Escenarios BDD
```gherkin
Característica: Notificación in-app de mora
  Escenario: Aviso al bloquear límite
    Dado que el umbral ABM es 5 días
    Y API Prestamos informa 7 días de mora
    Cuando el sistema aplica el bloqueo de límite
    Entonces veo la notificación in-app MSG-M05: "Se bloqueó el límite crediticio del ente por mora."
    Y no se dispara un correo electrónico
```

#### Fuera de alcance
- Email / SMS / push externo.
- Configuración de agrupadores ABM de notificaciones por email.

#### Notas / preguntas abiertas
- —
#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### MOR-04 — ABM: configurar umbral de días de mora para bloqueo de límite

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | MOR — Morosidad |
| **Actor** | Administrador Banco (ABM) |
| **Dominios** | BANCO |
| **Prioridad sugerida** | Must |
| **Depende de** | — |
| **Habilita** | MOR-HT-02 |
| **Pantalla POC** | Gestión (ABM) — parámetro nuevo (no existe en POC) |

#### Historia
```
Como administrador del Banco
quiero configurar en el ABM cuántos días de mora disparan el bloqueo del límite
para adaptar la política de riesgo sin cambiar código
```

#### Valor de negocio
Parametriza la política de contención; el CORE/API informa días y la plataforma decide cuándo bloquear.

#### Escenarios fuente
```text
Definir en un ABM la cantidad de días de mora necesarios para bloquear el límite de crédito
API CORE debe devolver la cantidad de días de mora
```

#### Criterios de aceptación
1. **[Feliz]** En ABM existe un parámetro numérico “Días de mora para bloqueo de límite” (entero ≥ 0).
2. **[Feliz]** Al guardar un valor válido se muestra MSG-A01: "Umbral de días de mora actualizado correctamente."
3. **[Validación]** Valores no enteros o negativos muestran MSG-A02: "Ingresá un número entero de días mayor o igual a 0." y no se persisten.
4. **[Alternativo]** El valor vigente es el que usa MOR-HT-02 en la evaluación.
5. **[Feliz]** Solo roles Banco con permiso ABM pueden editar el parámetro.

#### Escenarios BDD
```gherkin
Característica: Umbral de mora en ABM
  Escenario: Guardar umbral válido
    Dado que soy administrador Banco en Gestión ABM
    Cuando configuro el umbral en 5 días y guardo
    Entonces veo el mensaje MSG-A01: "Umbral de días de mora actualizado correctamente."
    Y el umbral vigente es 5

  Escenario: Umbral inválido
    Cuando intento guardar "-1"
    Entonces veo el mensaje MSG-A02: "Ingresá un número entero de días mayor o igual a 0."
```

#### Fuera de alcance
- Umbral distinto por EGP (global en esta entrega).
- Cálculo de intereses de mora.

#### Notas / preguntas abiertas
- Valor default sugerido: a definir con Riesgos (propuesta PO: 5 días hábiles si no hay input).

#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### MOR-05 — Levantar bloqueo por mora al acreditar el pago

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | MOR — Morosidad |
| **Actor** | Usuario Confirming |
| **Dominios** | EGP / Banco |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-HT-03, MOR-HT-02 |
| **Habilita** | — |
| **Pantalla POC** | Confirming → panel + grilla tras refresh |

#### Historia
```
Como usuario del Portal Confirming
quiero que, al acreditarse el pago, se levante el bloqueo por mora y se actualice la pantalla
para volver a operar cuando el préstamo regulariza
```

#### Valor de negocio
Cierra el ciclo de mora: el desbloqueo no depende de un trámite manual si CORE ya acreditó el pago.

#### Escenarios fuente
```text
Reversión de bloqueos por mora cuando se acredita el pago
Mensaje de API CORE → quitar bloqueo del límite → refresh auto o manual
```

#### Criterios de aceptación
1. **[Feliz]** Tras el evento de pago acreditado, el límite deja de estar bloqueado por mora y el estado del ente pasa a `Al día` cuando API Prestamos lo confirme.
2. **[Feliz]** La UI se actualiza (refresh automático o acción de refresco) y se muestra MSG-M03: "Se levantó el bloqueo por mora: el pago fue acreditado. El límite vuelve a estar disponible."
3. **[Feliz]** La grilla deja de estar grisada y las acciones vuelven según permisos (MOR-02 inverso).
4. **[Alternativo]** Si el usuario fuerza refresh manual antes del evento, se reconsulta API Prestamos y se refleja el estado vigente.
5. **[Error]** Si el desbloqueo de límite falla, se mantiene el bloqueo y se registra error; no se muestra MSG-M03.

#### Escenarios BDD
```gherkin
Característica: Desbloqueo por pago acreditado
  Escenario: Levantamiento exitoso
    Dado que el EGP está "En mora" con grilla bloqueada
    Cuando CORE informa pago acreditado y API Prestamos pasa a "Al día"
    Entonces veo el mensaje MSG-M03: "Se levantó el bloqueo por mora: el pago fue acreditado. El límite vuelve a estar disponible."
    Y la grilla deja de estar grisada
```

#### Fuera de alcance
- Contabilidad de mora / factura de mora (CORE).
- Reversión de operación de adelanto (épica REV).

#### Notas / preguntas abiertas
- —
#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### REV-01 — Mostrar estados de reversión en grilla Confirming (FNV)

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | REV — Reversiones |
| **Actor** | Usuario Confirming |
| **Dominios** | Todos |
| **Prioridad sugerida** | Must |
| **Depende de** | REV-HT-01 |
| **Habilita** | REV-02 |
| **Pantalla POC** | Confirming → pestaña Facturas No Vigentes · columna Estado |

#### Historia
```
Como usuario del Portal Confirming
quiero ver en Facturas No Vigentes los estados de reversión de una factura
para seguir el proceso aunque aún no exista flujo de usuario para revertir
```

#### Valor de negocio
Da trazabilidad visual del proceso de reversión (skill/manual) sin exponer acciones peligrosas en la UI.

#### Escenarios fuente
```text
Estados: Pendiente de Reversión · Pendiente aprobación Supervisor · Habilitada · Bloqueada
Sin flujo de usuario para revertir por ahora
S-06: FNV — no deberían volver a ser operativas
```

#### Criterios de aceptación
1. **[Feliz]** Las facturas en `Pendiente de Reversión` o `Pendiente aprobación Supervisor` aparecen en la pestaña **Facturas No Vigentes (FNV)** con badge de estado.
2. **[Feliz]** Tras aprobación same-day o de supervisor, el estado final `Habilitada` o `Bloqueada` permanece visible según reglas de pestaña vigentes (FNV si no operables).
3. **[Feliz]** En filas de reversión no hay acciones de fila operables; tooltip/ayuda MSG-R01: "Esta factura está en proceso de reversión. Solo consulta; no hay acciones disponibles desde Confirming."
4. **[Validación]** Una factura en reversión **no** aparece en Facturas Vigentes como operable.
5. **[Alternativo]** El detalle de la fila muestra si el caso es same-day o a pasado cuando el BE lo informe.

#### Escenarios BDD
```gherkin
Característica: Estados de reversión en FNV
  Antecedentes:
    Dado que estoy en "Confirming"

  Escenario: Ver pendiente de reversión
    Dado una factura en estado "Pendiente de Reversión"
    Cuando abro la pestaña "Facturas No Vigentes"
    Entonces veo la factura con badge "Pendiente de Reversión"
    Y no veo botones de acción operables
    Y veo el mensaje MSG-R01: "Esta factura está en proceso de reversión. Solo consulta; no hay acciones disponibles desde Confirming."

  Escenario: No aparece en FV operable
    Cuando abro "Facturas Vigentes"
    Entonces no veo esa factura como operable para Simular/Habilitar
```

#### Fuera de alcance
- Botones Operador Aprueba / Supervisor Aprueba-Rechaza en UI.
- Inicio de reversión por EGP desde Confirming.

#### Notas / preguntas abiertas
- POC: agregar badges nuevos al catálogo de estados.

#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### REV-02 — Filtro Estado incluye estados de reversión

| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | REV — Reversiones |
| **Actor** | Usuario Confirming |
| **Dominios** | Todos |
| **Prioridad sugerida** | Should |
| **Depende de** | REV-01, CON-10 (estados) |
| **Habilita** | — |
| **Pantalla POC** | Confirming → filtro “Estado” |

#### Historia
```
Como usuario del Portal Confirming
quiero filtrar la grilla por estados de reversión
para ubicar rápido facturas en ese proceso
```

#### Valor de negocio
Reduce tiempo de búsqueda operativa cuando el volumen de FNV crece.

#### Escenarios fuente
```text
POC: filtro Estado — Todos los Estados / Pendiente / Habilitada / Bloqueada / …
Agregar: Pendiente de Reversión · Pendiente aprobación Supervisor
```

#### Criterios de aceptación
1. **[Feliz]** El combo Estado incluye `Pendiente de Reversión` y `Pendiente aprobación Supervisor`.
2. **[Feliz]** Al elegir uno, la grilla (en FNV) muestra solo facturas en ese estado.
3. **[Alternativo]** “Todos los Estados” incluye también los nuevos.
4. **[Validación]** Los labels coinciden exactamente con los badges de REV-01.

#### Escenarios BDD
```gherkin
Característica: Filtro por estado de reversión
  Escenario: Filtrar pendiente de reversión
    Dado que estoy en FNV
    Cuando selecciono estado "Pendiente de Reversión"
    Entonces solo veo facturas con ese estado
```

#### Fuera de alcance
- Filtro por same-day vs a pasado (Could).

#### Notas / preguntas abiertas
- —
#### Chequeo INVEST
| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 7. Historias técnicas — Endpoints BFF / BE (enablers)

### MOR-HT-01 — GET · Estado de mora del EGP (API Prestamos)

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | MOR — Morosidad |
| **Habilita** | MOR-01, MOR-02 |
| **Contrato** | `GET /v1/entes/{enteId}/morosidad` (BFF) → API Prestamos |
| **Prioridad sugerida** | Must |
| **Depende de** | T-02 |

#### Objetivo técnico
Exponer al FE el estado canónico de mora (`Al día` | `En mora`) y `diasMora` desde **API Prestamos**.

#### Criterios de aceptación
1. Respuesta 200 con `{ "estado": "AL_DIA"|"EN_MORA", "diasMora": number, "fuente": "API_PRESTAMOS" }`.
2. Si API Prestamos no está disponible → 503/424 de negocio; **no** se inventa `AL_DIA`.
3. El BFF no calcula mora; solo adapta el contrato de Prestamos.
4. Autenticación/autorización: solo usuarios con acceso al ente.

#### Escenarios BDD
```gherkin
Característica: GET morosidad EGP
  Escenario: En mora
    Cuando consulto GET /v1/entes/cervepar/morosidad
    Entonces recibo 200 con estado "EN_MORA" y diasMora >= 0
```

#### Errores esperados
| Código HTTP | Código negocio | Cuándo |
|-------------|----------------|--------|
| 200 | — | Consulta OK |
| 404 | ENTE_NO_ENCONTRADO | enteId inválido |
| 503 | PRESTAMOS_NO_DISPONIBLE | API Prestamos caída |
| 424 | FUENTE_MORA_NO_DISPONIBLE | Sin dato de mora |

---

### MOR-HT-02 — Evaluar umbral ABM y aplicar/liberar bloqueo de límite

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | MOR — Morosidad |
| **Habilita** | MOR-03, MOR-05 |
| **Contrato** | Job/servicio BE `evaluarBloqueoMora(enteId)` + flag `limiteBloqueadoPorMora` |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-04, MOR-HT-01 |

#### Objetivo técnico
Comparar `diasMora` vs umbral ABM y persistir bloqueo/liberación del límite crediticio por mora.

#### Criterios de aceptación
1. Si `diasMora >= umbral` → `limiteBloqueadoPorMora = true` y dispara notificación in-app (MOR-03).
2. Si `diasMora < umbral` o estado `AL_DIA` → no aplica / libera bloqueo por mora (sin pisar otros bloqueos).
3. Idempotencia: reevaluar no duplica notificaciones si el estado no cambia.
4. Auditoría: quién/qué/cuándo aplicó el bloqueo.

#### Escenarios BDD
```gherkin
Característica: Evaluación umbral mora
  Escenario: Bloqueo por umbral
    Dado umbral 5 y diasMora 7
    Cuando ejecuto evaluarBloqueoMora
    Entonces limiteBloqueadoPorMora es true
```

#### Errores esperados
| Código HTTP | Código negocio | Cuándo |
|-------------|----------------|--------|
| 200 | — | Evaluación OK |
| 409 | BLOQUEO_OTRA_CAUSA | Hay bloqueo no-mora que debe preservarse |
| 503 | PRESTAMOS_NO_DISPONIBLE | No se pudo evaluar |

---

### MOR-HT-03 — Consumir mensaje CORE de pago acreditado

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | MOR — Morosidad |
| **Habilita** | MOR-05 |
| **Contrato** | Evento/cola o webhook CORE `pagoAcreditado` → BE Confirming |
| **Prioridad sugerida** | Must |
| **Depende de** | MOR-HT-02 |

#### Objetivo técnico
Al recibir acreditación de pago desde CORE, reconsultar API Prestamos y liberar bloqueo de mora si corresponde.

#### Criterios de aceptación
1. Mensaje CORE identificado por ente/préstamo/operación.
2. Tras procesar: llama evaluación MOR-HT-02 / refresco Prestamos.
3. Si Prestamos ya `AL_DIA` → libera `limiteBloqueadoPorMora` y emite señal UI (MSG-M03).
4. Reintentos idempotentes ante duplicados del mensaje.

#### Escenarios BDD
```gherkin
Característica: Evento pago acreditado
  Escenario: Liberación
    Dado un ente bloqueado por mora
    Cuando llega mensaje CORE pagoAcreditado
    Y Prestamos responde AL_DIA
    Entonces limiteBloqueadoPorMora es false
```

#### Errores esperados
| Código HTTP | Código negocio | Cuándo |
|-------------|----------------|--------|
| 202 | — | Evento aceptado |
| 404 | PRESTAMO_NO_ENCONTRADO | Referencia CORE desconocida |
| 409 | ESTADO_INCONSISTENTE | Prestamos sigue EN_MORA tras pago |

---

### REV-HT-01 — Máquina de estados BE de reversión

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | REV — Reversiones |
| **Habilita** | REV-01, REV-HT-02 |
| **Contrato** | Transiciones BE dominio factura/adelanto |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-09 (máquina existente) |

#### Objetivo técnico
Incorporar estados y transiciones del diagrama Mural, con corte same-day 17:00 PY.

#### Criterios de aceptación
1. Estados nuevos: `Pendiente de Reversión`, `Pendiente aprobación Supervisor`.
2. Transiciones:
   - Inicio skill → `Pendiente de Reversión` (solo si no desembolsado y no pagado).
   - Same-day (≤17:00 PY) + Operador aprueba → `Habilitada`.
   - A pasado + Operador aprueba → `Pendiente aprobación Supervisor`.
   - Supervisor aprueba → `Habilitada`; Supervisor rechaza → `Bloqueada`.
3. Facturas en estos estados se clasifican en **FNV** (RN-R04).
4. BE es fuente de verdad; BFF solo proyecta.

#### Escenarios BDD
```gherkin
Característica: Máquina de estados reversión
  Escenario: Same-day a Habilitada
    Dado un adelanto no desembolsado iniciado a las 10:00 PY
    Cuando el Operador aprueba la reversión el mismo día antes de las 17:00
    Entonces el estado es "Habilitada"
```

#### Errores esperados
| Código HTTP | Código negocio | Cuándo |
|-------------|----------------|--------|
| 409 | TRANSICION_INVALIDA | Transición no permitida |
| 422 | YA_DESEMBOLSADO | No cumple RN-R01 |
| 403 | ROL_INSUFICIENTE | Actor sin rol Operador/Supervisor |

---

### REV-HT-02 — Cursor skill para revertir manualmente

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | REV — Reversiones |
| **Habilita** | Operación Banco (sin UI Confirming) |
| **Contrato** | Skill Cursor `confirming-revertir-adelanto` + llamadas a BE/API ops |
| **Prioridad sugerida** | Must |
| **Depende de** | REV-HT-01 |

#### Objetivo técnico
Entregar un **Cursor skill** que permita a operaciones del banco iniciar y avanzar la reversión manual (mismo día / a pasado) según RN-R02/R03, sin pantalla de usuario en Confirming.

#### Criterios de aceptación
1. El skill pide: clave de factura/adelanto, motivo, y valida RN-R01.
2. Clasifica same-day vs a pasado con corte **17:00 PY**.
3. Ejecuta transiciones vía API BE autenticada (Operador / Supervisor según paso).
4. Deja trazabilidad (quién, cuándo, same-day/a pasado) y la factura visible en FNV (REV-01).
5. No crea botones ni flujo en la UI Confirming.
6. Documenta en el skill: precondiciones, roles, mensajes de error y ejemplos de invocación.

#### Escenarios BDD
```gherkin
Característica: Cursor skill de reversión manual
  Escenario: Inicio same-day
    Dado un adelanto no desembolsado creado hoy a las 11:00 PY
    Cuando invoco el skill confirming-revertir-adelanto como Operador
    Entonces la factura queda "Pendiente de Reversión"
    Y aparece en FNV
```

#### Errores esperados
| Código HTTP | Código negocio | Cuándo |
|-------------|----------------|--------|
| 422 | YA_DESEMBOLSADO | Adelanto ya desembolsado/pagado |
| 403 | ROL_INSUFICIENTE | Usuario sin rol adecuado |
| 409 | TRANSICION_INVALIDA | Paso de aprobación incorrecto |

---

## 8. Tareas técnicas / habilitadores

| ID | Key | Tarea | Objetivo | Definition of Done |
|----|-----|-------|----------|--------------------|
| **T-01** | T-01 | Actualizar POC Confirming (marca mora + estados REV) | Visualizar en https://marianaintive.github.io/atlas-confirming-poc/ el badge de mora en panel ente y facturas demo en FNV con `Pendiente de Reversión` / `Pendiente aprobación Supervisor`; grilla grisada en escenario mora | Demo navegable sin backend real; escenarios mock documentados |
| **T-02** | T-02 | Mock contrato API Prestamos | JSON de ejemplo `AL_DIA` / `EN_MORA` + días para FE/BFF/POC | Publicado en repo o `AI-Outputs` con campos alineados a MOR-HT-01 |

---

## 9. Spikes y decisiones pendientes (columna DUDAS)

| ID | Origen | Pregunta abierta | Impacto si no se resuelve | Propuesta del PO | Respuesta *(post HITL)* |
|----|--------|------------------|---------------------------|------------------|-------------------------|
| **S-01** | Mural sticky | ¿Fuente canónica de mora? | Contrato HT / mocks | Adaptador único; fallback CORE | **API Prestamos** |
| **S-02** | MOR-02 | ¿Grilla oculta o visible bloqueada? | UX MOR-02 | Visible solo lectura | **Ve la grilla y facturas grisadas y bloqueadas** |
| **S-03** | MOR-03 | ¿In-app y/o email? | Alcance notificaciones | Must in-app | **Solo en la plataforma** |
| **S-04** | REV | ¿Corte same-day 17:00 PY? | Máquina de estados | Sí, alineado a adelanto | **Sí, 17 hs** |
| **S-05** | Mural REV | ¿Qué es el “skill” de reversión? | REV-HT-02 | Endpoint ops + runbook | **Debe ser un Cursor skill** |
| **S-06** | REV-01 | ¿FV / FNV / FNO? | Clasificación grilla | FV mientras abiertas | **FNV** (no vuelven a ser operativas) |
| **S-07** | Keys | ¿MOR/REV locales o MAGIA? | Trazabilidad Jira | Locales ahora | **Crear keys MOR y REV** |

---

## 10. Recomendaciones del PO — historias faltantes

### 10.1 Imprescindibles antes de salir a producción

| ID | Historia propuesta | Por qué falta / riesgo | Prioridad |
|----|--------------------|------------------------|-----------|
| R-01 | Auditoría / log de bloqueos de mora y de cada paso del skill de reversión | Compliance y soporte Ops | Must |
| R-02 | UI Confirming de aprobación Operador/Supervisor (cuando negocio habilite flujo de usuario) | Hoy solo skill; Anexo 70 y diagrama asumen actores humanos | Should (release posterior) |
| R-03 | Prueba de contrato / sandbox API Prestamos con Banco | Sin esto MOR-HT-01 queda en mock | Must |

### 10.2 Recomendadas para completar la experiencia

| ID | Historia propuesta | Por qué falta / riesgo | Prioridad |
|----|--------------------|------------------------|-----------|
| R-04 | Email opcional de mora vía ABM notificaciones | Pedido explícitamente fuera ahora (S-03) | Could |
| R-05 | Umbral de mora por EGP (no global) | Política de riesgo más fina | Could |
| R-06 | Filtro same-day vs a pasado en FNV | Operación Banco | Could |

---

## 11. Observaciones sobre la consistencia del input

1. **Mural vs Anexo 70 (roles):** Anexo habla de Supervisor (same-day) y Supervisor+Gerente (a pasado); Mural usa Operador / Supervisor. Se adoptó **Mural** (SUP-08).
2. **Ítem tachado:** “Actualización de estado de facturas con préstamo en MORA” queda fuera; no contradice la marca de mora del **cliente** en panel.
3. **API Prestamos TBD en sticky** pero S-01 la fija como fuente; T-02 mitiga mientras el contrato real llega.
4. **POC gap:** no hay badge de mora ni estados `Pendiente de Reversión` / `Pendiente aprobación Supervisor`; T-01 los materializa tras este documento.
5. **Reversión “Habilitada” en FNV:** el nombre de estado final `Habilitada` puede confundir con operable en FV; en esta entrega FNV implica no operativa (S-06). Conviene validar con UX el copy del badge.
6. **Skill Cursor (S-05)** es herramienta de equipo/ops, no producto end-user; debe vivir versionado (p. ej. bajo skills del repo / `~/.agents/skills`) y autenticarse contra APIs reales.

---

## 12. Matriz de trazabilidad HU ↔ endpoint ↔ pantalla

| HU | Historias técnicas | Endpoints / artefactos | Pantalla / paso |
|----|--------------------|------------------------|-----------------|
| MOR-01 | MOR-HT-01 | `GET /v1/entes/{id}/morosidad` | Confirming → panel ente |
| MOR-02 | MOR-HT-01 | idem | Confirming → grilla + botonera |
| MOR-03 | MOR-HT-02 | evaluarBloqueoMora + canal in-app | Notificación plataforma |
| MOR-04 | — | ABM parámetro umbral | Gestión ABM |
| MOR-05 | MOR-HT-02, MOR-HT-03 | evento `pagoAcreditado` | Confirming refresh |
| REV-01 | REV-HT-01 | máquina estados BE | Confirming → FNV · Estado |
| REV-02 | REV-HT-01, CON-10 | catálogo estados | Confirming → filtro Estado |
| (ops) | REV-HT-02 | Cursor skill + API BE | Sin UI Confirming |
| T-01 | — | mocks FE | POC Confirming |
| T-02 | MOR-HT-01 | contrato mock Prestamos | Dev/POC |

---

## 13. Definition of Ready / Definition of Done

**Definition of Ready (por historia)**
- Épica y key asignadas (`MOR-*` / `REV-*`)
- AC numerados con tags y Gherkin en español
- Dependencias HT/API explícitas
- Spikes bloqueantes de la historia resueltos (S-01…07 cerrados para este paquete)
- Diseño/POC referenciado o T-01 planificado

**Definition of Done (por historia)**
- Implementado FE/BFF/BE según capa
- Mensajes UI = catálogo §5
- Pruebas de los escenarios Gherkin principales
- Sin acciones UI de reversión en Confirming (salvo visualización FNV)
- Documentación del Cursor skill publicada si aplica REV-HT-02
- Código/revisión según DoD del equipo MAGIA
)
