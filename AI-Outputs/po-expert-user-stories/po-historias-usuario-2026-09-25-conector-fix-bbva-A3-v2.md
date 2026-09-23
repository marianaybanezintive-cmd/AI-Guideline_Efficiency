# Historias de Usuario — Conector FIX ↔ A3 Mercados

> **Versión:** v2.0.0 • **Fecha:** 2026-09-25
> **Fuente única de requerimientos:**
> - `PRD-conector-fix-bbva-a3-fase1-2026-09-15.md` (PRD de Fase 1, elaborado por el PO)
> - `ImplementacionFixBBVA_PropuestaTecnica_20260908 - DRAFT.docx` (propuesta técnica intive v2.0)
> - `ConectorFix_Backlog&Estimation - BBVA.xlsx` (backlog borrador — hojas *Epics*, *User Stories*, *US Details*, *Estimation*, *Roadmap*)
> - `api-trading-fix.pdf` — A3 Mercados, *Rules of Engagement FIX 5.0, FIX-PTP / FIX-PTP-HR*, v2.0.53
> - `Manual de Conectividad A3.pdf` — A3 Mercados
> **Autor:** PO (elaboración de historias) · **Producto:** Conector FIX ↔ A3 Mercados
> **POC / referencia de diseño:** no aplica — el producto no tiene interfaz de usuario
> **Generado con:** skill `po-expert-user-stories`
> **Nota:** Incluye las 13 historias faltantes del §10 de la v1.0.0, elaboradas como tarjetas completas.

**Origen detectado:** Excel con formato **no canónico** (columnas `Epic ID`, `US ID`, `User Story`, `Name`, `Details`, `Acc Crit.`, `Estimacion`, `Obs`), complementado con documentación de negocio y especificación técnica de protocolo. Mapeo por semántica: `Name`/`User Story` → `summary`; `Details` → historia Connextra; `Acc Crit.` → `escenarios`; `Obs` → `dudas`; `Estimacion` → referencia de esfuerzo. **No se aplica** la regla de separación BE/FE/BFF de `excel-input.md`: la solución es un componente backend único sin front end; se reemplaza por una clasificación **HU (capacidad funcional observable por el negocio) / HT (enabler técnico) / TAREA (habilitador de infraestructura)**.

---

## Tabla de contenidos

0. [Qué cambia respecto de versión anterior](#0-qué-cambia-respecto-de-versión-anterior)
1. [Criterio de elaboración y alcance](#1-criterio-de-elaboración-y-alcance)
2. [Matriz de inclusión / desestimación](#2-matriz-de-inclusión--desestimación)
3. [Contexto de solución, actores y supuestos](#3-contexto-de-solución-actores-y-supuestos)
4. [Reglas de negocio transversales (RN)](#4-reglas-de-negocio-transversales-rn)
5. [Catálogo de mensajes](#5-catálogo-de-mensajes)
6. [Historias de usuario funcionales (tarjetas de backlog)](#6-historias-de-usuario-funcionales-tarjetas-de-backlog)
7. [Historias técnicas — enablers](#7-historias-técnicas--enablers)
8. [Tareas técnicas / habilitadores](#8-tareas-técnicas--habilitadores)
9. [Spikes y decisiones pendientes](#9-spikes-y-decisiones-pendientes)
10. [Recomendaciones del PO — historias faltantes](#10-recomendaciones-del-po--historias-faltantes)
11. [Observaciones sobre la consistencia del input](#11-observaciones-sobre-la-consistencia-del-input)
12. [Matriz de trazabilidad](#12-matriz-de-trazabilidad)
13. [Definition of Ready / Definition of Done](#13-definition-of-ready--definition-of-done)

---

## 0. Qué cambia respecto de versión anterior

**Primera elaboración — no hay documento anterior.**

Criterios de forma adoptados:

- Tarjetas de backlog con metadatos en tabla, historia Connextra, valor de negocio, escenarios fuente literales del Excel, criterios de aceptación numerados con tags de camino y escenarios BDD en Gherkin español.
- Keys propuestos con el patrón `FIX-{épica}.{NN}`; se conserva la trazabilidad al `US ID` del Excel en los metadatos de cada tarjeta.
- Códigos de épica: **E1** Discovery, Arquitectura y Ambientes · **E2** MVP TCR/ER y Conectividad FIX · **E3** Homologación A3 y Pruebas de Aceptación del cliente · **E4** Order Routing · **E5** Market Data.
- Profundidad de refinamiento diferenciada por prioridad del PO: **E1, E2 y E3 con tarjeta completa**; **E4 y E5 a nivel de historia de cabecera** (objetivo, alcance, dependencias y criterios de aceptación de alto nivel), suficientes para estimar y priorizar pero no para desarrollar.
- El producto no tiene interfaz de usuario. El §5 se reinterpreta como **catálogo de códigos de evento y de error** publicados en MQ y registrados en auditoría, manteniendo la regla de citar el texto literal inline en cada referencia.
### Historias incorporadas
- Se incorporan las 13 historias faltantes del backlog original (FIX-2.15 a FIX-2.25 y T-21, T-22).

### Códigos nuevos
- Se añaden los códigos MSG-26 a MSG-38.

### Pausas interactivas ejecutadas

| Pausa | Fecha | Resultado |
|---|---|---|
| **§3.3 Supuestos** | 2026-09-15 | 14 supuestos confirmados sin cambios por el PO |
| **§9 Spikes — primera ronda** | 2026-09-16 | 4 resueltos: `S-01` Drop Copy, `S-02` credenciales fuera de banda, `S-12` IBM WebSphere Liberty, `S-15` homologación parcial aceptada por A3. Emerge `S-16` |
| **§9 Spikes — segunda ronda** | 2026-09-16 | 4 resueltos más: `S-03` reinicio diario de secuencias, `S-05` TCR sólo por consulta, `S-06` consulta asincrónica a demanda, `S-10` persistencia por archivos. Se define además que **las credenciales se obtienen por una API del banco**. `S-04` queda declarado «sin definir» y `S-07` con respuesta ambigua pendiente de aclaración. Emerge `S-17` |
| **Alineación editorial** | 2026-09-18 | Se aplicó al documento el mismo criterio del commit manual sobre el PRD: **se quita la atribución de responsabilidades operativas al proveedor por nombre**. Se conservan los endpoints técnicos, el nombre del ambiente de pruebas y las referencias a A3 Mercados y a eTrader, que son del mercado |
| **§9 Spikes — tercera ronda** | 2026-09-18 | `S-07` cerrado: **la cola de entrada queda desestimada del MVP**. El conector dispara sus propias consultas y **SUP-04 vuelve a estar plenamente vigente**. Se revierten la historia `FIX-2.15`, la regla RN-20 y los códigos MSG-26 y MSG-27 incorporados el 16-09. `S-17` cerrado en su parte de comportamiento ante indisponibilidad |

Las resoluciones modificaron el contenido en dos rondas: se agregaron las reglas **RN-17** (oyente pasivo en Drop Copy), **RN-18** (*hard stop* de credenciales) y **RN-19** (reinicio diario de secuencias); se reescribió **RN-06** (credenciales por API del banco); se agregaron los códigos **MSG-23**, **MSG-24** y **MSG-25**; se reescribió **MSG-19**; **SUP-14 quedó superado**; y se sumaron criterios de aceptación en `FIX-2.01`, `FIX-2.04` y `FIX-2.09`. El detalle está en §9.1.

---

## 1. Criterio de elaboración y alcance

| Criterio | Decisión aplicada |
|----------|-------------------|
| **Filas tachadas** (Excel) | No se detectaron filas tachadas ni marcadas como desestimadas. Todas las filas de *User Stories* y *US Details* tienen `Scope = 1` en la hoja *Estimation* |
| **Filas puntuadas / detalladas** | Elaboradas como tarjeta completa cuando pertenecen a E1, E2 o E3 |
| **Escenarios del input** | Transcritos literalmente en *Escenarios fuente*; expandidos a criterios de aceptación numerados y a Gherkin español |
| **Historias faltantes** | Sólo en §10, no mezcladas con las del input. Son numerosas: el Excel no cubre la Épica 1 ni el manejo de errores de protocolo |
| **Identificadores** | El Excel no tiene `issue_key` tipo Jira, sólo `US ID` numérico. Se generan keys propuestos `FIX-{épica}.{NN}` y se conserva el `US ID` original como trazabilidad |
| **Reclasificación de épicas** | Las 12 épicas del Excel se remapean a las 5 épicas del plan de trabajo de la propuesta técnica, que es la estructura que pidió el PO |
| **Regla del corte MVP** | Definida en el PRD §5: entra en E2 todo mensaje FIX que **no modifica el estado del mercado**. Todo mensaje que crea, modifica o cancela una orden va a E4; toda suscripción continua de precios va a E5 |
| **Alcance de «TCR»** | Exclusivamente Trade Capture Report de **operaciones regulares** (`TrdType=0`). Block trades, allocations, giveups, confirmaciones y reporte de posiciones quedan fuera del alcance del proyecto |
| **Separación BE/FE/BFF** | No aplica — componente backend único sin front end. Se reemplaza por HU / HT / TAREA |
| **Idioma y formato** | Español; Gherkin con palabras clave en español |

### Convención de tipos

| Tipo | Significado |
|------|-------------|
| `HU` | Historia de usuario: capacidad cuyo valor es observable por el negocio (un evento llega a los sistemas del cliente, un estado queda disponible, una consulta se responde) |
| `HT` | Historia técnica (*enabler*): capacidad interna del conector sin valor directo para el negocio pero necesaria para que las HU funcionen (persistencia de secuencias, recuperación de gaps, auditoría) |
| `TAREA` | Habilitador de infraestructura, ambiente, configuración o gestión (ambientes, pipeline, credenciales, gestiones con A3) |

### Mapeo de épicas: Excel → plan de trabajo

| Épica del Excel | US del Excel | Épica destino | Justificación |
|---|---|---|---|
| 1 — Gestión de Sesión FIX | 1, 2, 3 | **E2** | Capa de sesión: núcleo del MVP |
| 2 — Recuperación y Consistencia | 4, 5, 6 | **E2** | *Recoverability* básica, comprometida en la etapa MVP del plan de trabajo |
| 3 — Administración de Órdenes | 7, 8, 9, 10 | **E4** | Mensajes que modifican el libro |
| 3 — Administración de Órdenes | 11 (consultar estado) | **E2** | Es consulta de sólo lectura (`H` / `AF`), no modifica el libro. Se reescribe: el conector no tiene UI |
| 4 — Procesamiento de Execution Reports | 12 | **E2** | Publicación de estados en MQ: sentido saliente, núcleo del MVP |
| 5 — Market Data A3 | 13 (Procesamiento de TCR) | **E2** | Reclasificada: TCR es post-trade, no market data. Es el corazón del MVP |
| 5 — Market Data A3 | 14, 15 | **E5** | Suscripción y publicación de precios |
| 6 — Monitoreo | 16 | **E2** | Observabilidad de sesión, comprometida en el MVP |
| 7 — Auditoría y Compliance | 17 | **E2** | Logging FIX *raw*, exigido por A3 |
| 8 — Alta Disponibilidad | 18, 19 | **E5** | Tolerancia a fallas, ubicada en T0+5 por el plan de trabajo |
| 9 — Configuración ambiente intive | 20 | **E1** | Entregable «Ambientes de despliegue» de la etapa Discovery |
| 10 — Configuración ambiente del cliente | 21 | **E1** / soporte continuo | Ídem; ejecuta el cliente con soporte del equipo |
| 11 — Prueba de despliegue el cliente | 22 | **E3** | Precede a la aceptación del cliente |
| 12 — Certificación, Pruebas y Homologación | 23, 24, 25 | **E3** | Homologación y pruebas |
| 12 — Certificación, Pruebas y Homologación | 26 (validación TRD/RF/Cauciones) | **E4** / **E5** | Requiere operatoria real; además Cauciones no está disponible en A3 hasta fines de 2026 |

---

## 2. Matriz de inclusión / desestimación

Una fila por ítem del input. `US` = `US ID` del Excel. Estado ✅ = se elabora tarjeta en este documento; 🔶 = se elabora a nivel de cabecera (E4/E5, prioridad diferida); ❌ = se desestima o se reubica fuera del alcance.

| US | Summary (Excel) | Épica Excel | Épica destino | Tipo | Estado | Motivo |
|---:|---|---|---|---|---|---|
| 1 | Iniciar sesión FIX | 1 | E2 | HU | ✅ Incluida | Núcleo del MVP; prioridad máxima declarada por el cliente |
| 2 | Mantener viva la sesión | 1 | E2 | HU | ✅ Incluida | Heartbeat y Test Request |
| 3 | Cerrar sesión FIX | 1 / 2 (desalineado) | E2 | HU | ✅ Incluida | Logout controlado |
| 4 | Persistir secuencias | 2 | E2 | HT | ✅ Incluida | *Recoverability* del MVP |
| 5 | Recuperar mensajes perdidos | 2 | E2 | HT | ✅ Incluida | Resend Request |
| 6 | Detectar gaps de secuencia | 2 | E2 | HT | ✅ Incluida | Detección de discontinuidad |
| 7 | Recibir órdenes desde MQ | 3 | E4 | HU | 🔶 Cabecera | Sentido MQ → FIX de instrucciones: abre el riesgo de escritura |
| 8 | Enviar nueva orden | 3 | E4 | HU | 🔶 Cabecera | `NewOrderSingle` (`35=D`) modifica el libro |
| 9 | Cancelar una orden | 3 | E4 | HU | 🔶 Cabecera | `OrderCancelRequest` (`35=F`) modifica el libro |
| 10 | Modificar una orden | 3 | E4 | HU | 🔶 Cabecera | `OrderCancelReplaceRequest` (`35=G`) modifica el libro |
| 11 | Consultar estado de una orden | 3 | **E2** | HU | ✅ Incluida **reescrita** | Es sólo lectura (`35=H` / `35=AF`). Los criterios originales asumen una UI que no existe |
| 12 | Publicar estados de órdenes en MQ | 4 | E2 | HU | ✅ Incluida | Sentido saliente: el entregable de valor del MVP |
| 13 | Procesamiento de TCR | 5 | **E2** | HU | ✅ Incluida **elaborada desde cero** | Sin ningún detalle en el Excel. Es la historia que da nombre al MVP |
| 14 | Suscribirse a Market Data de A3 | 5 | E5 | HU | 🔶 Cabecera | `MarketDataRequest` (`35=V`) |
| 15 | Publicar Market Data en MQ | 5 | E5 | HU | 🔶 Cabecera | *Fan-out* de precios |
| 16 | Registrar estado de sesiones | 6 | E2 | HU | ✅ Incluida | Observabilidad de sesión |
| 17 | Registrar mensajes FIX completos | 7 | E2 | HT | ✅ Incluida | A3 puede solicitar los registros en casos de soporte |
| 18 | Reconexión automática | 8 | E5 | HT | 🔶 Cabecera | Tolerancia a fallas, etapa T0+5 |
| 19 | Recuperación después de reinicio | 8 | E5 | HT | 🔶 Cabecera **acotada** | Se elimina «recupera posiciones locales»: el conector no mantiene posiciones |
| 20 | Configuración de ambiente intive | 9 | E1 | TAREA | ✅ Incluida | Precondición del MVP |
| 21 | Configuración de ambiente del cliente | 10 | E1 | TAREA | ✅ Incluida | Ejecuta el cliente; el equipo da soporte |
| 22 | Prueba de despliegue el cliente | 11 | E3 | TAREA | ✅ Incluida | Precede a la aceptación |
| 23 | Certificación A3 | 12 | E3 | TAREA | ✅ Incluida | Gestión con A3; es la actividad de mayor prioridad del proyecto |
| 24 | Creación casos de prueba | 12 | E1 + E3 | TAREA | ✅ Incluida | Se adelanta parcialmente a E1 (entregable «escenarios y casos principales de prueba») |
| 25 | Pruebas de recuperación, duplicados y colas | 12 | E3 | TAREA | ✅ Incluida | Validación de los escenarios de riesgo del MVP |
| 26 | Validación funcional TRD, Renta Fija y Cauciones | 12 | E4 / E5 | TAREA | ❌ Fuera de Fase 1 | Requiere operatoria real. Además, Cauciones estará disponible en A3 recién a fines de 2026 |

**Resumen del input:** 26 ítems · 16 incluidos con tarjeta completa (E1/E2/E3) · 9 a nivel de cabecera (E4/E5) · 1 fuera de la Fase 1.
*(El conteo final por tipo HU / HT / TAREA se cierra en §12 una vez elaboradas las tarjetas, e incluye las historias de §10 que el input no contempla.)*

---

## 3. Contexto de solución, actores y supuestos

### 3.1 Actores

| Actor | Tipo | Interacción con el conector |
|---|---|---|
| **Sistemas consumidores del cliente** | Sistema interno | Consumen desde MQ los eventos de orden, operaciones concertadas, estado de mercado y errores que el conector publica |
| **Conector FIX** | El producto | Gestiona la sesión, consulta, normaliza, publica y audita |
| **A3 Mercados — gateway FIX-PTP** | Sistema externo | Emite Execution Reports, Trade Capture Reports, estado de sesión de negociación, avisos y rechazos |
| **A3 Mercados — Operaciones** | Organización externa | Provee credenciales y coordenadas, entrega el paquete de certificación y conduce la homologación |
| **Operador de mesa el cliente** | Persona | En la Fase 1 origina, desde eTrader, las órdenes cuyos eventos el conector observa |
| **Equipo de operaciones y soporte** | Persona | Consume el estado de sesión, las métricas y las alertas |
| **Arquitectura y seguridad del cliente** | Organización interna | Define el framework MQ, aprueba los contratos de mensajes y administra el secret de credenciales |
| **Equipo de proyecto (intive)** | Organización | Desarrolla, prueba, homologa y da soporte al despliegue |

### 3.2 Componentes involucrados

| Componente | Responsabilidad | Épica |
|---|---|---|
| **FIX Session Layer** | Logon, Logout, Heartbeat, Test Request, Resend Request, Sequence Reset, Reject de sesión | E2 |
| **Adaptador A3** | Particularidades del diccionario de A3 respecto del estándar FIX 5.0 SP2 (campos custom, `SecurityExchange=ROFX`, `Parties`) | E2 |
| **Motor de normalización** | Traduce mensajes FIX al modelo canónico del cliente | E2 |
| **Publicador MQ** | Publica eventos normalizados en las colas del cliente | E2 |
| **Consumidor MQ** | Consume instrucciones desde el cliente | **E4** |
| **Store de sesión** | Persistencia de `MsgSeqNum` entrante y saliente, resistente a reinicio | E2 |
| **Auditoría** | Log *raw* de todo mensaje FIX, log de mensajes MQ, correlación | E2 |
| **Observabilidad** | Estado de sesión, métricas, alertas | E2 |
| **Proveedor de credenciales** | Lectura del secret administrado por seguridad del cliente | E1 + E2 |
| **Pipeline CI/CD** | Construcción y despliegue en ambiente intive | E1 + E2 |

### 3.3 Supuestos (a confirmar)

| # | Supuesto | Confirmación *(post HITL)* |
|---|----------|---------------------------|
| **SUP-01** | **El corte del MVP es «el conector observa, no actúa».** Ningún mensaje que cree, modifique o cancele una orden (`35=D`, `35=F`, `35=G`, `35=q`) entra en las épicas 1 a 3, ni siquiera `Order Mass Cancel Request` en su uso como *kill switch* operativo | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-02** | **«TCR» en el MVP significa exclusivamente Trade Capture Report de operaciones regulares (`TrdType=0`).** Block trades, allocations, giveups, confirmaciones y reporte de posiciones quedan fuera del alcance del proyecto, no sólo de la Fase 1 | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-03** | **El tráfico de Execution Reports de la Fase 1 provendrá de una sesión de drop copy de A3 y de consultas `Order Mass Status Request`**, y el tráfico de prueba se generará cargando órdenes manualmente en eTrader sobre el ambiente reMarkets. Sin esto no hay ER que procesar, porque el conector no rutea órdenes | ✅ **Confirmado y ampliado (2026-09-16).** La modalidad es **FIX Drop Copy**: A3 configura la sesión del conector con un **perfil de sólo lectura** asociado a determinados IDs de cuentas o de operadores, y el motor de negociación **duplica en tiempo real** hacia esa sesión cada ER de las órdenes operadas, canceladas o modificadas en esas cuentas. El conector es un **oyente pasivo**. En homologación el tráfico se genera por inyección de órdenes de un tercero sobre cuentas espejo mapeadas a la sesión. Ver `S-01` |
| **SUP-04** | **El MVP es puramente saliente hacia MQ** (conector → el cliente). No se implementa consumo de instrucciones ni de comandos desde MQ en la Fase 1; la cola de entrada se abre recién en la Épica 4 | ✅ **Vigente y reconfirmado (2026-09-18).** La definición del 16-09 que incorporaba una cola de entrada de comandos al MVP **quedó desestimada**. El flujo del MVP es: A3 envía los reportes TCR y ER → el conector los recibe, procesa y deposita en la MQ del cliente. Ver `S-07` |
| **SUP-05** | **La persistencia de secuencias se resuelve con almacenamiento en archivos**, que es el patrón estándar de los motores FIX y lo que anota el propio Excel («se utiliza file storage»). Sybase se incorpora sólo si el cliente lo exige por política | ✅ **Confirmado con motivo explícito (2026-09-16): persistencia por archivos, deliberadamente para no impactar la base de datos.** Sybase queda **fuera del alcance del MVP**. Ver `S-10` |
| **SUP-06** | **La rotación diaria de contraseña se resolverá fuera del protocolo FIX.** El ROE de A3 v2.0.53 no define el tag `NewPassword` (925) ni ningún mensaje de cambio de credenciales, por lo que el esquema de secret con `<contraseña actual>` + `<nueva contraseña>` de la propuesta técnica no es implementable tal como está redactado. Se asume un secret con la contraseña vigente y rotación gestionada por acuerdo con A3 | ✅ **Confirmado y ampliado (2026-09-16).** La gestión de contraseñas es **puramente administrativa y fuera de banda**: en homologación se tratarán manualmente; en producción las gestiona el cliente. **El conector no debe intentar cambiar contraseñas de forma programática.** **Ampliación del 2026-09-16:** el conector **no lee un secret**, sino que **obtiene las credenciales de A3 desde una API del banco**. Ver `S-02`, `S-17`, RN-06 y RN-18 |
| **SUP-07** | **Se usa exclusivamente el gateway FIX-PTP**: `fix.remarkets.primary.com.ar:9876` para pruebas y `fixgw.ptp.primary.com.ar:9876` para producción. Los gateways FIX-PTP-HR y FIX-PTP-LL no se contemplan en ninguna de las cinco épicas | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-08** | **A3 acepta una homologación de alcance parcial** limitada a capa de sesión, consulta de estado, post-trade regular y manejo de errores, sin envío de órdenes ni suscripción a market data. Si A3 exige certificar el conjunto completo, la fecha del 31-dic no es alcanzable con este alcance | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-09** | **Los productos TRD, Renta Fija y Cauciones no requieren tratamiento diferenciado en el MVP.** El conector normaliza y publica lo que recibe sin aplicar reglas por producto; esas reglas aparecen recién en la Épica 4 | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-10** | **La API REST asincrónica de consulta de estado queda fuera de la Fase 1.** Está identificada como capacidad deseable y no mandatoria, y su definición depende de decisiones de modelo de información que se toman en la Épica 1 | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-11** | **Las historias de configuración de ambiente del Excel (US 20, 21, 22) se tratan como tareas técnicas con dueño y fecha explícitos, no como backlog del equipo de desarrollo.** Representan entre el 28% y el 29% del esfuerzo estimado y su ejecución depende mayormente del cliente | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-12** | **El producto no tiene interfaz de usuario.** El catálogo §5 se reinterpreta como catálogo de **códigos de evento y de error** publicados en MQ y registrados en auditoría, manteniendo la regla de citar el texto literal inline | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-13** | **Las épicas 4 y 5 se refinan sólo a nivel de historia de cabecera** —objetivo, alcance, dependencias y criterios de aceptación de alto nivel—, suficiente para estimar y priorizar pero no para desarrollar. El detalle completo se elabora al cerrar la Épica 3, incorporando el aprendizaje de la Fase 1 | ✅ Confirmado por el PO, sin cambios (2026-09-15) |
| **SUP-14** | ~~Los números de secuencia se diseñan de forma configurable entre reinicio diario y continuidad entre jornadas~~ | ✅ **Superado por definición concreta (2026-09-16): el reinicio es DIARIO.** Ya no hace falta que sea configurable. La persistencia pasa a ser **intra-jornada**. Ver `S-03` y RN-19 |

> **Pausa obligatoria (skill):** ejecutada el 2026-09-15. El PO confirmó los 14 supuestos sin cambios. Las historias de §6 a §8 se redactaron sobre esa base.

---

## 4. Reglas de negocio transversales (RN)

Referenciadas desde los criterios de aceptación y los escenarios BDD para no repetir texto.

| ID | Regla | Fuente |
|----|-------|--------|
| **RN-01** | **Ningún mensaje emitido por el conector en las épicas 1 a 3 puede modificar el estado del mercado.** Los únicos mensajes salientes permitidos son los de capa de sesión y los de consulta (`35=H`, `35=AF`, `35=AD`) | PRD §5 · SUP-01 |
| **RN-02** | Las consultas y el procesamiento de Trade Capture Report se limitan a **operaciones regulares** (`TrdType=0`). Todo TCR con otro `TrdType` se registra en auditoría y no se publica en MQ | PRD §5.2 · SUP-02 |
| **RN-03** | **Todo mensaje FIX enviado y recibido se registra en formato *raw***, con *timestamp*, dirección, `MsgSeqNum` y sesión asociada, de forma que pueda reconstruirse la actividad diaria completa. A3 puede solicitar estos registros en casos de soporte | Manual de Conectividad A3 · US 17 |
| **RN-04** | **Todo evento publicado en MQ lleva un `correlation ID`** que permite vincularlo con el mensaje FIX de origen y con su registro de auditoría | Plan de trabajo, etapa MVP («Correlation IDs») |
| **RN-05** | **El procesamiento es idempotente.** Un mensaje FIX identificado como reenvío (`PossDupFlag=Y`) o cuyo identificador de negocio (`ExecID` para ER, `TradeReportID` para TCR) ya fue procesado, no se vuelve a publicar en MQ | RAID de la propuesta técnica, riesgos 4 y 5 |
| **RN-06** | **El conector obtiene las credenciales de A3 desde una API del banco**, en cada apertura de sesión y en cada reanudación tras un *hard stop*. Las mantiene únicamente en memoria durante la jornada: **nunca las persiste en disco ni las registra** en logs, trazas, mensajes de error ni en el repositorio | Propuesta técnica, «Manejo de contraseñas» · Definición del PO del 2026-09-16 (`S-17`) |
| **RN-07** | La **ventana de sesión FIX de A3 es de 09:30 a 19:00** y la de negociación de 10:00 a 17:30. El conector no intenta conectarse fuera de la ventana de sesión, y distingue ambas ventanas al interpretar los eventos | ROE A3, *Connection information* |
| **RN-08** | El conector respeta los **límites de caudal de A3**: 1 solicitud masiva de estado por segundo, 1 cancelación masiva por segundo y 100 solicitudes de estado de orden por segundo. Aplica control de caudal propio antes de emitir | Manual de Conectividad A3, *Volumen de Mensajes soportados* |
| **RN-09** | **No puede existir más de una sesión FIX simultánea** con la misma combinación de `SenderCompID`, `TargetCompID` y `OnBehalfOfCompID`. Si A3 recibe un mensaje con valores que no corresponden a la sesión, lo rechaza y cierra la conexión | ROE A3, *Identification of the FIX session* |
| **RN-10** | El `HeartBtInt` (108) negociado en el `Logon` debe ser **mayor o igual a 10 segundos** | ROE A3, *Logon* |
| **RN-11** | **Ningún evento se descarta en silencio.** Todo mensaje FIX de negocio recibido resulta en un mensaje publicado en MQ, o en un error registrado y alertado. La única excepción es el duplicado, que se registra explícitamente (MSG-12) | RNF-01 del PRD |
| **RN-12** | Los instrumentos se identifican por **`Symbol` (55)**, único en cada mercado, con **`SecurityExchange` (207) = `ROFX`** | ROE A3, *Instrument Identification* |
| **RN-13** | La sesión usa **FIX 5.0 SP2** (`DefaultApplVerID` = 9) sobre transporte FIXT, con **`EncryptMethod` (98) = 0** (sin cifrado a nivel de protocolo) | ROE A3, *Logon* |
| **RN-14** | Los valores de `SenderCompID` y `TargetCompID` se **repiten** en `OnBehalfOfCompID` y `DeliverToCompID` respectivamente, y se invierten cuando el mensaje lo emite A3 | ROE A3, *Standard Message Trailer* e *Identification of the FIX session* |
| **RN-15** | **El conector no es un OMS.** No mantiene posiciones, no calcula tenencias y no es la fuente de verdad del estado de una orden: refleja y publica el estado que A3 informa | Excel, observación de US 11 |
| **RN-16** | El conector **no aplica reglas de negocio diferenciadas por producto** (TRD, Renta Fija, Cauciones) en las épicas 1 a 3: normaliza y publica lo que recibe | SUP-09 |
| **RN-17** | **El conector opera como oyente pasivo sobre una sesión FIX Drop Copy de sólo lectura.** A3 asocia la sesión a un conjunto de IDs de cuentas o de operadores y duplica en tiempo real los eventos de esas cuentas. En consecuencia: los Execution Reports llegan **no solicitados**, el `ClOrdID` (11) que traen fue generado por **sistemas de terceros** (terminales de sistemas propios del cliente o plataformas DMA) y **no pertenece al espacio de identificadores del conector**, que por lo tanto no puede asumir su unicidad ni su formato | `S-01`, resuelto el 2026-09-16 |
| **RN-19** | **Los números de secuencia de la sesión FIX se reinician en cada jornada.** En consecuencia, la persistencia de secuencias tiene alcance **intra-jornada**: sirve para sobrevivir a un reinicio del proceso dentro del día de negociación, no para dar continuidad entre días. La detección de gaps, el `Resend Request` y la ventana de deduplicación quedan acotados a la jornada | `S-03`, resuelto el 2026-09-16 |
| **RN-18** | **El conector nunca intenta cambiar credenciales de forma programática.** Ante un `Logout` (`35=5`) de respuesta a un `Logon` cuyo `Text` (58) indique credenciales inválidas, expiradas o usuario bloqueado, el conector aplica **hard stop**: detiene todo reintento automático de conexión para no bloquear el usuario por intentos fallidos, y emite alerta crítica. La reanudación requiere intervención manual explícita de un administrador | `S-02`, resuelto el 2026-09-16 |

---

## 5. Catálogo de mensajes

> **Adaptación declarada:** el producto **no tiene interfaz de usuario** (SUP-12). Este catálogo no contiene textos de pantalla sino los **códigos de evento y de error** que el conector publica en MQ y registra en auditoría. Se mantiene la regla del skill: al citar un `MSG-XX` en criterios de aceptación o en Gherkin, se incluye siempre el **texto literal** inline, nunca sólo el código.
>
> Los textos son una propuesta del PO y **requieren validación de arquitectura del cliente** al cerrar los contratos MQ en la Épica 1 (tarea `T-03`). Los valores entre llaves son parámetros.

| Código | Tipo | Contexto | Mensaje |
|--------|------|----------|---------|
| **MSG-01** | Evento | Sesión establecida | "Sesión FIX establecida con A3. SenderCompID {sender}, HeartBtInt {n}s, secuencia entrante {seqIn}, saliente {seqOut}." |
| **MSG-02** | Error | Logon rechazado por A3 | "No se pudo establecer la sesión FIX con A3: {motivo}. La sesión queda en estado Desconectada." |
| **MSG-03** | Evento | Logout controlado | "Sesión FIX cerrada de forma controlada. Último MsgSeqNum entrante {seqIn}, saliente {seqOut}." |
| **MSG-04** | Alerta | Desconexión sin Logout | "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}." |
| **MSG-05** | Alerta | Ausencia de mensajes | "Sin mensajes de A3 durante {n} segundos. Se emite Test Request {testReqId}." |
| **MSG-06** | Alerta | Gap de secuencia detectado | "Gap de secuencia detectado: se esperaba {esperado}, se recibió {recibido}. Se solicita reenvío del rango {desde}-{hasta}." |
| **MSG-07** | Evento | Secuencia restablecida | "Secuencia restablecida. Rango {desde}-{hasta} recuperado." |
| **MSG-08** | Error | Gap no recuperado | "No se pudo recuperar el rango {desde}-{hasta} tras {n} intentos. Requiere intervención manual." |
| **MSG-09** | Error | Reject de sesión de A3 | "A3 rechazó el mensaje de secuencia {refSeqNum}: {sessionRejectReason} — {text}." |
| **MSG-10** | Error | Business Message Reject de A3 | "A3 rechazó el mensaje {refMsgType}: {businessRejectReason} — {text}." |
| **MSG-11** | Evento | Rechazo de orden informado por A3 | "A3 rechazó la orden {clOrdId}: {text}." |
| **MSG-12** | Auditoría | Duplicado descartado | "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ." |
| **MSG-13** | Error | Fallo de publicación en MQ | "No se pudo publicar el evento {correlationId} en la cola {cola}: {motivo}. Derivado a {colaError}." |
| **MSG-14** | Evento | Reconciliación iniciada | "Reconciliación de estado iniciada tras restablecer la sesión. MassStatusReqID {massStatusReqId}." |
| **MSG-15** | Evento | Reconciliación con diferencias | "Reconciliación completada: {n} órdenes con estado divergente, publicadas como eventos de corrección." |
| **MSG-16** | Evento | Reconciliación sin órdenes | "Reconciliación completada: A3 no reporta órdenes para los criterios solicitados." |
| **MSG-17** | Evento | Consulta TCR sin resultados | "A3 no reporta operaciones concertadas para los criterios solicitados." |
| **MSG-18** | Alerta | Control de caudal | "Límite de solicitudes masivas alcanzado (1 por segundo). La solicitud {requestId} queda encolada." |
| **MSG-19** | Error | Credenciales no disponibles | "No se pudieron obtener las credenciales de A3 desde la API del banco: {motivo}. La sesión no se inicia." |
| **MSG-20** | Evento | Fuera de ventana operativa | "Fuera de la ventana de sesión FIX de A3 (09:30 a 19:00). No se intenta conexión." |
| **MSG-21** | Evento | Operación concertada publicada | "Operación concertada {tradeReportId} publicada: {symbol}, {side}, {lastQty} a {lastPx}." |
| **MSG-22** | Auditoría | TCR fuera de alcance | "Trade Capture Report con TrdType {trdType} fuera del alcance del conector. Registrado, no publicado." |
| **MSG-23** | Error crítico | Credenciales rechazadas — *hard stop* | "A3 rechazó las credenciales: {text}. Se detienen los reintentos automáticos para no bloquear el usuario. Requiere intervención manual de un administrador." |
| **MSG-25** | Evento | Apertura de jornada | "Apertura de jornada: números de secuencia reiniciados. Entrante 1, saliente 1." |
| **MSG-24** | Evento | Sesión en modalidad Drop Copy | "Sesión establecida en modalidad Drop Copy de sólo lectura, asociada a las cuentas {cuentas}. El conector opera como oyente pasivo." |

---
> Continuación del §5 del documento maestro. Los códigos MSG-26 y MSG-27 que existieron transitoriamente el 16-09 (cola de entrada, luego desestimada) quedaron libres. Se reutiliza la numeración.

| Código | Tipo | Contexto | Mensaje |
|--------|------|----------|---------|
| **MSG-26** | Evento | Estado de la sesión de negociación | "Sesión de negociación {tradingSessionId} en fase {tradSesStatus}: {descripción}. MarketSegmentID {segmentId}." |
| **MSG-27** | Alerta | Cambio de fase de negociación | "Cambio de fase de negociación: {tradingSessionId} pasó de {faseAnterior} a {faseActual}. {acción}." |
| **MSG-28** | Evento | Catálogo de cuentas actualizado | "Catálogo de cuentas actualizado: {n} cuentas habilitadas para la sesión Drop Copy." |
| **MSG-29** | Alerta | Cuenta no reconocida en evento Drop Copy | "Execution Report recibido para la cuenta {account} que no está en el catálogo habilitado. Evento publicado con marca de advertencia." |
| **MSG-30** | Alerta | Control de caudal aplicado | "Solicitud {msgType} encolada por control de caudal: {pendientes} solicitudes pendientes. Próximo envío en {ms} ms." |
| **MSG-31** | Evento | Apertura de jornada completada | "Apertura de jornada completada: sesión establecida, secuencias reiniciadas, reconciliación iniciada. Jornada {fecha}." |
| **MSG-32** | Evento | Cierre de jornada completado | "Cierre de jornada completado: sesión cerrada, logs archivados, resumen generado. {totalER} ER procesados, {totalTCR} TCR procesados, {errores} errores." |
| **MSG-33** | Evento | Aviso de mercado publicado | "Aviso de mercado de A3 publicado: {headline}. OrigTime {origTime}, MarketSegmentID {segmentId}." |
| **MSG-34** | Evento | Healthcheck del conector | "Healthcheck: sesión {estadoSesión}, MQ {estadoMQ}, último mensaje A3 hace {segs}s, secuencia entrante {seqIn}, saliente {seqOut}." |
| **MSG-35** | Error | Healthcheck degradado | "Healthcheck degradado: {componente} no disponible. Detalle: {motivo}." |
| **MSG-36** | Evento | Configuración cargada | "Configuración cargada para el ambiente {ambiente}: gateway {host}:{puerto}, SenderCompID {sender}, colas MQ {colas}." |
| **MSG-37** | Error | Configuración inválida | "Configuración inválida: el parámetro {parametro} tiene el valor {valor}, que no cumple la restricción {restriccion}. El conector no arranca." |
| **MSG-38** | Evento | Credencial enmascarada | "Campo sensible enmascarado en el registro de auditoría: tag {tagId} del mensaje {msgType} con secuencia {seqNum}." |

---

## 6. Historias de usuario funcionales (tarjetas de backlog)

> **Hallazgo del refinamiento, relevante para la planificación:** de las tres épicas priorizadas, **sólo la Épica 2 produce software**. La Épica 1 es un bloque de decisiones, definiciones y habilitación de ambientes, y la Épica 3 es un bloque de gestión y validación. Ambas se elaboran como **tareas técnicas en §8**, con Definition of Done concreta, y no como historias de usuario. Forzarlas al formato Connextra produciría historias artificiales que no se estiman ni se prueban mejor por estar escritas así.

### 6.1 Épica 2 — MVP TCR/ER y Conectividad FIX

---

### FIX-2.01 — Iniciar sesión FIX con A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 — MVP TCR/ER y Conectividad FIX |
| **Trazabilidad input** | Excel `US ID = 1` · Plan de trabajo: «FIX Session Layer — Login» |
| **Actor** | Conector FIX |
| **Prioridad sugerida** | Must — prioridad máxima declarada por el cliente |
| **Estimación del input** | 3–5 SP |
| **Depende de** | `T-01` (ambiente intive), `T-05` (alta Drop Copy y mapeo de cuentas), `T-06` (API de credenciales del banco) |
| **Habilita** | Todas las historias de E2 |

#### Historia

```
Como conector FIX del cliente
quiero establecer y autenticar una sesión con el gateway FIX-PTP de A3
para habilitar el intercambio de mensajes de negocio con el mercado
```

#### Valor de negocio

Es la precondición de todo el proyecto: sin sesión establecida no hay ningún otro flujo posible. Es además el primer criterio que A3 evalúa en la certificación («la conexión exitosa»).

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 1):

```text
Se establece una conexión TCP.
Se envía mensaje Logon (35=A).
Se incluyen credenciales configuradas.
Se valida la respuesta Logon recibida.
El estado de la sesión cambia a "Conectada".
Se registra el evento en auditoría.
```

#### Criterios de aceptación

1. **[Feliz]** El conector establece una conexión TCP contra el *host* y puerto configurados para el ambiente (`fix.remarkets.primary.com.ar:9876` en pruebas) y envía un `Logon` (`35=A`) con `EncryptMethod` (98) = 0, `HeartBtInt` (108) ≥ 10 conforme a RN-10, `Username` (553), `Password` (554) y `DefaultApplVerID` (1137) = 9 conforme a RN-13.
2. **[Feliz]** El `Logon` se emite con `SenderCompID`, `TargetCompID`, `OnBehalfOfCompID` y `DeliverToCompID` completados según RN-14, con los valores provistos por A3 para el ambiente.
3. **[Feliz]** Al recibir el `Logon` de respuesta de A3, el estado de la sesión pasa a **Conectada** y se publica MSG-01: "Sesión FIX establecida con A3. SenderCompID {sender}, HeartBtInt {n}s, secuencia entrante {seqIn}, saliente {seqOut}."
4. **[Feliz]** Las credenciales se obtienen de la **API del banco** en el momento de abrir la sesión, se mantienen sólo en memoria durante la jornada y no quedan registradas en ningún log ni traza, conforme a RN-06.
4.1. **[Feliz]** Al abrir la sesión de la jornada, los números de secuencia entrante y saliente **se reinician** conforme a RN-19, y se registra MSG-25: "Apertura de jornada: números de secuencia reiniciados. Entrante 1, saliente 1."
5. **[Feliz]** El `Logon` enviado y el recibido quedan registrados en formato *raw* conforme a RN-03, con las credenciales enmascaradas.
6. **[Alternativo]** Si A3 responde con `Logout` (`35=5`), el conector interpreta el rechazo de autenticación, deja la sesión en estado **Desconectada** y publica MSG-02: "No se pudo establecer la sesión FIX con A3: {motivo}. La sesión queda en estado Desconectada."
6.1. **[Error]** El conector **lee el campo `Text` (58) del `Logout`** para determinar la causa. A3 envía allí cadenas explícitas del tipo `"Invalid username or password"`, `"Password expired"` o `"User locked"`.
6.2. **[Error]** Ante cualquiera de esas causas, el conector aplica **hard stop** conforme a RN-18: **detiene todo reintento automático de conexión** —para no bloquear el usuario por intentos fallidos— y emite alerta crítica con MSG-23: "A3 rechazó las credenciales: {text}. Se detienen los reintentos automáticos para no bloquear el usuario. Requiere intervención manual de un administrador."
6.3. **[Validación]** La salida del *hard stop* requiere una **acción manual explícita** de un administrador tras actualizar la credencial en el secret. El conector no reanuda por sí solo ni por reinicio del proceso.
7. **[Error]** Si A3 responde con `Reject – Session Level` (`35=3`), el conector registra `RefSeqNum` (45), `RefTagID` (371), `RefMsgType` (372) y `SessionRejectReason` (373), y publica MSG-09: "A3 rechazó el mensaje de secuencia {refSeqNum}: {sessionRejectReason} — {text}."
8. **[Error]** Si la API de credenciales del banco no responde o devuelve un error, el conector no intenta la conexión y publica MSG-19: "No se pudieron obtener las credenciales de A3 desde la API del banco: {motivo}. La sesión no se inicia."
9. **[Validación]** Si la solicitud de conexión ocurre fuera de la ventana de 09:30 a 19:00 conforme a RN-07, el conector no intenta conectarse y registra MSG-20: "Fuera de la ventana de sesión FIX de A3 (09:30 a 19:00). No se intenta conexión."
10. **[Validación]** El conector no abre una segunda sesión con la misma combinación de CompIDs conforme a RN-09.

#### Escenarios BDD

```gherkin
Característica: Establecimiento de la sesión FIX con A3
  Como conector FIX del cliente quiero autenticarme contra el gateway FIX-PTP
  para habilitar el intercambio de mensajes de negocio.

  Escenario: Logon exitoso dentro de la ventana operativa
    Dado que son las 09:35 y el gateway FIX-PTP de A3 está disponible
    Y que el secret de credenciales del cliente es legible
    Cuando el conector establece la conexión TCP y envía un Logon con EncryptMethod 0, HeartBtInt 30 y DefaultApplVerID 9
    Entonces A3 responde con un Logon
    Y el estado de la sesión pasa a "Conectada"
    Y se publica el evento MSG-01: "Sesión FIX establecida con A3. SenderCompID {sender}, HeartBtInt {n}s, secuencia entrante {seqIn}, saliente {seqOut}."
    Y el Logon enviado y el recibido quedan registrados en el log raw con la contraseña enmascarada

  Escenario: Credenciales inválidas
    Dado que el conector envía un Logon con credenciales que A3 no reconoce
    Cuando A3 responde con un Logout
    Entonces el estado de la sesión queda en "Desconectada"
    Y se publica el error MSG-02: "No se pudo establecer la sesión FIX con A3: {motivo}. La sesión queda en estado Desconectada."
    Y la contraseña utilizada no aparece en ningún registro

  Esquema del escenario: Rechazo de credenciales con hard stop
    Dado que el conector envía un Logon a A3
    Cuando A3 responde con un Logout cuyo campo Text contiene "<causa>"
    Entonces el conector detiene todos los reintentos automáticos de conexión
    Y emite la alerta crítica MSG-23: "A3 rechazó las credenciales: {text}. Se detienen los reintentos automáticos para no bloquear el usuario. Requiere intervención manual de un administrador."
    Y no vuelve a intentar conectarse aunque el proceso se reinicie

    Ejemplos:
      | causa                          |
      | Invalid username or password   |
      | Password expired               |
      | User locked                    |

  Escenario: Reanudación tras actualizar la credencial
    Dado que el conector está en hard stop por credenciales rechazadas
    Y que un administrador actualizó la contraseña en el sistema del banco que respalda la API de credenciales
    Cuando el administrador ejecuta la acción manual de reanudación
    Entonces el conector vuelve a intentar el Logon con la credencial actualizada

  Escenario: Sesión establecida en modalidad Drop Copy
    Dado que A3 configuró la sesión del conector como perfil de sólo lectura asociado a las cuentas del cliente
    Cuando el Logon se completa correctamente
    Entonces se registra el evento MSG-24: "Sesión establecida en modalidad Drop Copy de sólo lectura, asociada a las cuentas {cuentas}. El conector opera como oyente pasivo."

  Escenario: Logon malformado rechazado por A3
    Dado que el conector envía un Logon al que le falta un campo obligatorio
    Cuando A3 responde con un Reject de nivel de sesión con SessionRejectReason 1
    Entonces se publica el error MSG-09: "A3 rechazó el mensaje de secuencia {refSeqNum}: {sessionRejectReason} — {text}."
    Y el conector no reintenta con el mismo mensaje

  Escenario: La API de credenciales del banco no responde
    Dado que la API de credenciales del banco no responde
    Cuando el conector intenta iniciar la sesión
    Entonces no se establece la conexión TCP
    Y se publica el error MSG-19: "No se pudieron obtener las credenciales de A3 desde la API del banco: {motivo}. La sesión no se inicia."

  Escenario: Apertura de jornada con reinicio de secuencias
    Dado que son las 09:30 y comienza una nueva jornada de negociación
    Cuando el conector completa el Logon
    Entonces los números de secuencia entrante y saliente arrancan en 1
    Y se registra el evento MSG-25: "Apertura de jornada: números de secuencia reiniciados. Entrante 1, saliente 1."

  Escenario: Intento fuera de la ventana de sesión
    Dado que son las 20:15
    Cuando se dispara el inicio de sesión
    Entonces el conector no intenta conectarse
    Y se registra el evento MSG-20: "Fuera de la ventana de sesión FIX de A3 (09:30 a 19:00). No se intenta conexión."
```

#### Fuera de alcance

- Reconexión automática ante fallo: es `FIX-5.03` (Épica 5, Tolerancia a fallas). El *hard stop* de RN-18 **prevalece** sobre cualquier política de reconexión que se implemente allí.
- **Cambio o rotación de contraseña por FIX: excluido del producto, no sólo de la Fase 1.** A3 confirmó que la gestión es puramente administrativa y fuera de banda (`S-02`).
- Conexión a la instancia secundaria de A3 (*disaster recovery*): Épica 5.

#### Notas / preguntas abiertas

- **Pendiente de confirmar con el equipo técnico:** el valor de `HeartBtInt` a configurar debe acordarse con A3; el ROE sólo fija el mínimo de 10 segundos.
- **Resuelto el 2026-09-16 (`S-03`): el reinicio de secuencias es diario.** El diseño deja de necesitar la configurabilidad prevista en SUP-14.
- **Resuelto el 2026-09-16 (`S-02` y credenciales):** la actualización de la credencial tras un *hard stop* implica que un administrador la modifique en el sistema del banco, que es el origen de la API de credenciales. En homologación el cambio se tramita manualmente; en producción lo gestiona el cliente. El conector la vuelve a obtener de la API al reanudar, sin redespliegue. El procedimiento operativo se documenta en `T-06`.
- **Pendiente (`S-17`):** el contrato de la API de credenciales del banco —endpoint, autenticación del conector contra ella, formato de respuesta, códigos de error y política de caché— no está relevado. **Introduce una dependencia de disponibilidad en el arranque:** si la API no responde a las 09:30, no hay sesión.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.02 — Mantener viva la sesión FIX

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 2` · Plan de trabajo: «Heartbeats», «Test Request», «Monitoreo de sesión» |
| **Actor** | Conector FIX |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 3–5 SP |
| **Depende de** | `FIX-2.01` |
| **Habilita** | Todo el procesamiento de mensajes de negocio |

#### Historia

```
Como conector FIX del cliente
quiero intercambiar Heartbeats y Test Requests con A3 de forma automática
para mantener activa la sesión y detectar tempranamente la pérdida del enlace
```

#### Valor de negocio

Una sesión que se cae sin detección deja al cliente ciego frente al mercado sin que nadie se entere. Esta historia convierte una falla silenciosa en una alerta.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 2):

```text
Se envía Heartbeat según HeartBtInt.
Se responde correctamente a TestRequest.
Se generan alertas ante ausencia de mensajes.
```

#### Criterios de aceptación

1. **[Feliz]** El conector emite un `Heartbeat` (`35=0`) cuando transcurre el intervalo `HeartBtInt` negociado sin haber enviado ningún otro mensaje.
2. **[Feliz]** Al recibir un `Test Request` (`35=1`) de A3, el conector responde con un `Heartbeat` que contiene en `TestReqID` (112) exactamente el valor recibido.
3. **[Alternativo]** Si transcurre el intervalo `HeartBtInt` sin recibir ningún mensaje de A3, el conector emite un `Test Request` con un `TestReqID` único y registra MSG-05: "Sin mensajes de A3 durante {n} segundos. Se emite Test Request {testReqId}."
4. **[Error]** Si A3 no responde al `Test Request` dentro del intervalo esperado, el conector considera la sesión caída, la marca como **Desconectada** y publica MSG-04: "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}."
5. **[Validación]** Los `Heartbeat` y `Test Request` enviados y recibidos quedan registrados conforme a RN-03, pero **no** se publican como eventos de negocio en MQ.

#### Escenarios BDD

```gherkin
Característica: Mantenimiento del enlace de la sesión FIX
  Como conector FIX del cliente quiero intercambiar Heartbeats con A3
  para mantener la sesión activa y detectar la pérdida del enlace.

  Escenario: Emisión de Heartbeat por inactividad propia
    Dado que la sesión está "Conectada" con HeartBtInt de 30 segundos
    Y que el conector no envió ningún mensaje durante 30 segundos
    Cuando vence el intervalo
    Entonces el conector envía un Heartbeat a A3
    Y el mensaje queda registrado en el log raw

  Escenario: Respuesta a un Test Request de A3
    Dado que la sesión está "Conectada"
    Cuando A3 envía un Test Request con TestReqID "TRQ-8891"
    Entonces el conector responde con un Heartbeat que contiene TestReqID "TRQ-8891"

  Escenario: Ausencia de mensajes de A3
    Dado que la sesión está "Conectada" con HeartBtInt de 30 segundos
    Y que no se recibe ningún mensaje de A3 durante 30 segundos
    Cuando vence el intervalo
    Entonces el conector emite un Test Request con un TestReqID único
    Y se registra la alerta MSG-05: "Sin mensajes de A3 durante {n} segundos. Se emite Test Request {testReqId}."

  Escenario: A3 no responde al Test Request
    Dado que el conector emitió un Test Request
    Cuando transcurre el intervalo de espera sin recibir Heartbeat de A3
    Entonces el estado de la sesión pasa a "Desconectada"
    Y se publica la alerta MSG-04: "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}."
```

#### Fuera de alcance

- Reconexión automática tras detectar la caída: es `FIX-5.03`.

#### Notas / preguntas abiertas

- El múltiplo de `HeartBtInt` que se tolera antes de declarar la sesión caída es un parámetro a acordar con arquitectura del cliente; la práctica habitual es 2 intervalos.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.03 — Cerrar la sesión FIX de forma controlada

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 3` · Plan de trabajo: «Logout» |
| **Actor** | Conector FIX |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 3–5 SP |
| **Depende de** | `FIX-2.01`, `FIX-2.09` (persistencia de secuencias) |

#### Historia

```
Como conector FIX del cliente
quiero ejecutar un Logout controlado al cerrar la jornada
para finalizar la sesión sin dejar inconsistencias de secuencia
```

#### Valor de negocio

Un cierre sucio obliga a una recuperación costosa al día siguiente y puede dejar mensajes sin procesar. El cierre controlado deja el estado listo para la siguiente jornada.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 3):

```text
Se envía Logout.
Se recibe Logout remoto.
La sesión queda marcada como cerrada.
Se liberan recursos.
```

#### Criterios de aceptación

1. **[Feliz]** Al cierre de la ventana operativa, o ante una solicitud explícita de cierre, el conector envía un `Logout` (`35=5`) a A3.
2. **[Feliz]** Al recibir el `Logout` de confirmación de A3, el conector marca la sesión como **Cerrada**, persiste los `MsgSeqNum` entrante y saliente finales, libera los recursos de conexión y publica MSG-03: "Sesión FIX cerrada de forma controlada. Último MsgSeqNum entrante {seqIn}, saliente {seqOut}."
3. **[Alternativo]** Si A3 inicia el `Logout`, el conector responde con su propio `Logout`, persiste las secuencias y cierra de la misma forma.
4. **[Alternativo]** Si A3 responde al `Logout` con un `Resend Request` (`35=2`), el conector atiende primero el reenvío conforme a `FIX-2.11` y recién después completa el cierre.
5. **[Error]** Si A3 no confirma el `Logout` dentro del tiempo de espera configurado, el conector cierra la conexión igualmente, persiste las secuencias y publica MSG-04: "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}."
6. **[Validación]** Una desconexión sin intercambio de `Logout` se interpreta y registra siempre como **condición anormal**, nunca como cierre normal.

#### Escenarios BDD

```gherkin
Característica: Cierre controlado de la sesión FIX
  Como conector FIX del cliente quiero ejecutar un Logout controlado
  para finalizar la sesión sin inconsistencias de secuencia.

  Escenario: Cierre normal al fin de la ventana operativa
    Dado que la sesión está "Conectada" y son las 19:00
    Cuando el conector envía un Logout y A3 responde con Logout
    Entonces el estado de la sesión pasa a "Cerrada"
    Y los MsgSeqNum entrante y saliente quedan persistidos
    Y se liberan los recursos de conexión
    Y se publica el evento MSG-03: "Sesión FIX cerrada de forma controlada. Último MsgSeqNum entrante {seqIn}, saliente {seqOut}."

  Escenario: Logout iniciado por A3
    Dado que la sesión está "Conectada"
    Cuando A3 envía un Logout
    Entonces el conector responde con su propio Logout
    Y el estado de la sesión pasa a "Cerrada"

  Escenario: A3 solicita reenvío antes de cerrar
    Dado que el conector envió un Logout
    Cuando A3 responde con un Resend Request del rango 1450-1460
    Entonces el conector retransmite los mensajes solicitados
    Y recién después completa el cierre de la sesión

  Escenario: A3 no confirma el Logout
    Dado que el conector envió un Logout
    Cuando transcurre el tiempo de espera sin respuesta de A3
    Entonces el conector cierra la conexión y persiste las secuencias
    Y se publica la alerta MSG-04: "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}."
```

#### Fuera de alcance

- Recuperación del estado operativo tras un reinicio del proceso: es `FIX-5.04`.

#### Notas / preguntas abiertas

- Si la sesión se cierra con secuencias que continúan entre jornadas, el valor persistido es el punto de partida del día siguiente. Depende de `S-03`.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.04 — Publicar en MQ los estados de orden derivados de Execution Reports

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 12` · Plan de trabajo: «ER (Execution Report)», «Flujo MQ → FIX: Publicación de estados, Transformaciones» |
| **Actor** | Sistemas consumidores del cliente |
| **Prioridad sugerida** | Must — **es la mitad del entregable que da nombre al MVP** |
| **Estimación del input** | 3–5 SP *(subestimada: el Excel no contempla las seis variantes del ER)* |
| **Depende de** | `FIX-2.01`, `T-03` (contratos MQ), `T-08` (framework MQ), `S-01` (origen del tráfico de ER) |
| **Habilita** | `FIX-2.06`, `FIX-2.07` |

#### Historia

```
Como sistema consumidor del cliente
quiero recibir por MQ cada cambio de estado de las órdenes que A3 informa
para mantener sincronizada la operatoria interna con la información del mercado
```

#### Valor de negocio

Es el entregable de valor del MVP en el lado de las órdenes: el cliente deja de depender de que un operador mire la pantalla de eTrader para saber qué pasó con una orden, y pasa a tener el estado disponible en sus sistemas de forma automática y auditable.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 12):

```text
Se publican órdenes aceptadas.
Se publican órdenes pendientes.
Se publican órdenes canceladas.
Se publican órdenes reemplazadas.
Se conserva el identificador de correlación de la orden original.
El mensaje publicado cumple el contrato definido con el cliente.
```

#### Criterios de aceptación

1. **[Feliz]** El conector consume los `Execution Report` (`35=8`) recibidos de A3 y determina el evento a partir de la combinación de `ExecType` (150) y `OrdStatus` (39).
2. **[Feliz]** El conector procesa las **seis variantes** que define el ROE de A3: *New* (`ExecType=0`), *Order Canceled Response* (`ExecType=4`), *Order Replaced Response* (`ExecType=5`), *Order Filled / Partially Filled Response* (`ExecType=F`, con `OrdStatus` 1 o 2), *Order Status Response* y *Reject Message Response*.
2.1. **[Feliz]** El conector procesa los Execution Reports que llegan **no solicitados** por la sesión Drop Copy, que son la fuente principal del MVP conforme a RN-17, además de los que llegan como respuesta a sus propias consultas de `FIX-2.06`.
2.2. **[Validación]** El conector **no asume que el `ClOrdID` (11) le pertenece**: fue generado por sistemas de terceros —terminales de sistemas propios del cliente o plataformas DMA— conforme a RN-17. Lo trata como dato opaco de correlación, sin validar su formato ni asumir su unicidad dentro del espacio de identificadores del conector.
2.3. **[Validación]** Cuando un Execution Report llega para una orden que el conector nunca vio antes —caso normal en Drop Copy—, se publica igualmente como evento válido. La ausencia de historia previa **no es un error**.
3. **[Feliz]** El evento normalizado preserva `ClOrdID` (11), `OrigClOrdID` (41), `OrderID` (37), `ExecID` (17), `Account` (1), `Symbol` (55), `Side` (54), `OrdType` (40), `TimeInForce` (59), las cantidades `OrderQty`, `CumQty` (14), `LeavesQty` (151) y `LastQty` (32), los precios `Price` (44), `AvgPx` (6) y `LastPx` (31), y `TransactTime` (60).
4. **[Feliz]** El mensaje publicado cumple el contrato acordado con arquitectura del cliente en `T-03` y lleva el `correlation ID` conforme a RN-04, que permite reconstruir la cadena mensaje FIX *raw* → evento normalizado → mensaje MQ.
5. **[Feliz]** El mensaje FIX de origen queda registrado en formato *raw* conforme a RN-03 **antes** de intentar la publicación.
6. **[Alternativo]** Un `Execution Report` de tipo *Reject Message Response* se publica como evento de rechazo diferenciado, con el motivo informado por A3, y se registra MSG-11: "A3 rechazó la orden {clOrdId}: {text}."
7. **[Alternativo]** Ante una ejecución parcial (`OrdStatus=1`), el evento publicado incluye tanto la cantidad de esta ejecución (`LastQty`) como la acumulada (`CumQty`) y la pendiente (`LeavesQty`), de modo que el consumidor pueda reconstruir el avance sin inferirlo.
8. **[Error]** Si la publicación en MQ falla, el conector no descarta el evento: lo deriva a la cola de error configurada y publica MSG-13: "No se pudo publicar el evento {correlationId} en la cola {cola}: {motivo}. Derivado a {colaError}." Conforme a RN-11.
9. **[Validación]** Un `Execution Report` ya procesado —identificado por `ExecID` o por `PossDupFlag=Y`— **no se vuelve a publicar**, conforme a RN-05, y se registra MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."
10. **[Validación]** El conector no infiere ni calcula estados: publica el estado que A3 informa, conforme a RN-15.

#### Escenarios BDD

```gherkin
Característica: Publicación en MQ de los estados de orden informados por A3
  Como sistema consumidor del cliente quiero recibir cada cambio de estado de las órdenes
  para mantener sincronizada la operatoria interna con el mercado.

  Escenario: Execution Report no solicitado de una orden originada en otro sistema
    Dado que la sesión Drop Copy está "Conectada" y asociada a las cuentas del cliente
    Y que un operador ingresó una orden desde un sistema externo al conector
    Cuando A3 duplica el Execution Report hacia la sesión del conector sin que este lo haya solicitado
    Entonces el conector lo publica como evento válido
    Y no lo trata como error pese a no tener historia previa de esa orden
    Y conserva el ClOrdID recibido como dato opaco de correlación

  Escenario: Orden aceptada por el mercado
    Dado que la sesión FIX está "Conectada"
    Cuando A3 envía un Execution Report con ExecType 0 y OrdStatus 0 para el ClOrdID "CLI-000451"
    Entonces el conector registra el mensaje raw en auditoría
    Y publica en la cola de estados un evento de orden aceptada con ClOrdID "CLI-000451", OrderID, ExecID, Symbol, Side, OrderQty y LeavesQty
    Y el evento lleva un correlation ID que permite recuperar el mensaje FIX de origen

  Escenario: Ejecución parcial
    Cuando A3 envía un Execution Report con ExecType F y OrdStatus 1, LastQty 30, CumQty 30 y LeavesQty 70
    Entonces el evento publicado informa la cantidad ejecutada 30, la acumulada 30 y la pendiente 70
    Y el consumidor no necesita calcular el avance

  Escenario: Orden cancelada
    Cuando A3 envía un Execution Report con ExecType 4 y OrdStatus 4
    Entonces el evento publicado indica que la orden quedó cancelada
    Y conserva el OrigClOrdID de la orden previa de la cadena

  Escenario: Orden rechazada por el mercado
    Cuando A3 envía un Execution Report de tipo rechazo para el ClOrdID "CLI-000452"
    Entonces se publica un evento de rechazo diferenciado con el motivo informado por A3
    Y se registra el evento MSG-11: "A3 rechazó la orden {clOrdId}: {text}."

  Escenario: Execution Report duplicado tras una recuperación de secuencia
    Dado que el Execution Report con ExecID "EX-77120" ya fue publicado en MQ
    Cuando A3 lo reenvía con PossDupFlag en Y
    Entonces el conector no lo vuelve a publicar
    Y registra el evento MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."

  Escenario: Falla la publicación en MQ
    Dado que la cola de estados no está disponible
    Cuando el conector intenta publicar un evento de orden
    Entonces el evento se deriva a la cola de error configurada
    Y se publica el error MSG-13: "No se pudo publicar el evento {correlationId} en la cola {cola}: {motivo}. Derivado a {colaError}."
    Y el evento no se pierde
```

#### Fuera de alcance

- Envío de órdenes que generen estos Execution Reports: Épica 4, conforme a RN-01.
- Manejo de `Order Cancel Reject` (`35=9`): sólo tiene sentido si el conector emite `35=F` o `35=G`, que es Épica 4.
- Enriquecimiento del evento con datos del instrumento más allá del `Symbol`: depende de `S-04`.

#### Notas / preguntas abiertas

- La estimación del Excel (3–5 SP) contempla una sola variante. Con las seis variantes del ROE, más la normalización y la deduplicación, corresponde re-estimar.
- **Resuelto el 2026-09-16 (`S-01`):** el origen del tráfico es la sesión **FIX Drop Copy**. A3 asocia la sesión a un conjunto de IDs de cuentas o de operadores y duplica en tiempo real los Execution Reports de esas cuentas. En homologación, el tráfico se genera por inyección de órdenes de un tercero sobre cuentas espejo mapeadas a la sesión.
- **Pendiente de confirmar con el negocio:** el conjunto de cuentas y de operadores del cliente que deben quedar asociados a la sesión Drop Copy. Es el insumo de `T-05` y condiciona qué eventos verá el conector.
- **Pendiente de confirmar con el equipo técnico (`S-04`):** si el evento publicado necesita enriquecerse con datos del instrumento más allá del `Symbol`.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ⚠️ Conviene partir por variante de `ExecType` si no entra en un sprint | ✅ |

---

### FIX-2.05 — Publicar en MQ las operaciones concertadas obtenidas por Trade Capture Report

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 13` («Procesamiento de TCR», **sin ningún detalle en el input**) · Plan de trabajo: «TCR (Trade Capture Report)» |
| **Actor** | Sistemas consumidores del cliente |
| **Prioridad sugerida** | Must — **es la otra mitad del entregable que da nombre al MVP** |
| **Estimación del input** | 3–5 SP *(sin criterios de aceptación en el Excel; re-estimar)* |
| **Depende de** | `FIX-2.01`, `T-03` (contratos MQ), `T-07` (códigos CNV y estructura de cuentas del cliente) |

#### Historia

```
Como sistema consumidor del cliente
quiero recibir por MQ las operaciones ya concertadas en A3 para nuestras cuentas
para conciliar la operatoria y alimentar los procesos internos posteriores a la negociación
```

#### Valor de negocio

El Execution Report informa qué le pasó a una orden; el Trade Capture Report informa **qué operaciones quedaron efectivamente concertadas**. Es la vista que necesitan los procesos posteriores a la negociación, y es lo que permite conciliar contra el mercado sin depender de reportes manuales.

#### Escenarios fuente

> El Excel **no aporta** historia Connextra, criterios de aceptación ni observaciones para esta fila. Es la única historia del backlog borrador en esa condición, y es precisamente la que da nombre al MVP (ver §11, observación O-1). Los criterios siguientes se elaboraron desde cero a partir del ROE FIX 5.0 de A3, sección *Post Trade Messages*.

```text
(Columnas Details, Acc Crit. y Obs vacías en el input)
```

#### Criterios de aceptación

1. **[Feliz]** El conector emite un `Trade Capture Report Request` (`35=AD`) con `TradeRequestID` (568) único, `TradeRequestType` (569) = 1 (*MatchedTradesMatchingCriteria*) y `TrdType` (828) = 0 (*Regular Trade*), conforme a RN-02.
2. **[Feliz]** El conector soporta la consulta **por símbolo**, completando `Symbol` (55), y la consulta **por cuenta**, completando el bloque `Parties` con los roles que exige A3: `PartyRole` 1 (*Executing Firm* — código CNV del agente de negociación), 3 (*Client ID*), 4 (*Clearing Firm* y *Executing Trader*), 76 (*Desk ID*) y 24 (*Customer Account*), todos con `PartyIDSource` (447) = `D`.
3. **[Feliz]** El conector consume los `Trade Capture Report` (`35=AE`) de respuesta y maneja el **encadenamiento de reportes** usando `TotNumTradeReports` (748) y `LastRptRequested` (912), sin dar por cerrada la consulta hasta recibir el último mensaje.
4. **[Feliz]** Cada operación normalizada preserva `TradeReportID` (571), `TradeRequestID` (568), `TrdMatchID` (880), `LastPx` (31), `LastQty` (32), `Side` (54), `Account` (1), `Symbol` (55), `TradeDate` (75) y `TransactTime` (60), y se publica en la cola acordada con el `correlation ID` conforme a RN-04, registrando MSG-21: "Operación concertada {tradeReportId} publicada: {symbol}, {side}, {lastQty} a {lastPx}."
5. **[Feliz]** El mensaje FIX de origen queda registrado en formato *raw* conforme a RN-03.
6. **[Alternativo]** Si A3 responde sin operaciones para los criterios solicitados, el conector cierra la consulta como completada y registra MSG-17: "A3 no reporta operaciones concertadas para los criterios solicitados."
7. **[Alternativo]** Si el reporte incluye `SecondaryTrdType` (855) = 9, la operación se marca como concertada en fase CPX y el evento publicado lo refleja.
8. **[Error]** Si A3 responde con `Business Message Reject` (`35=j`) a la solicitud, el conector registra `BusinessRejectReason` (380) y publica MSG-10: "A3 rechazó el mensaje {refMsgType}: {businessRejectReason} — {text}."
9. **[Validación]** Todo `Trade Capture Report` con `TrdType` distinto de 0 —operaciones de bloque, *allocations*, *giveups*, operaciones de piso o RFQ— **se registra en auditoría y no se publica en MQ**, conforme a RN-02, con MSG-22: "Trade Capture Report con TrdType {trdType} fuera del alcance del conector. Registrado, no publicado."
10. **[Validación]** Una operación ya publicada, identificada por `TradeReportID`, no se vuelve a publicar conforme a RN-05.
11. **[Validación]** El conector respeta el límite de caudal de A3 conforme a RN-08 al emitir solicitudes sucesivas.

#### Escenarios BDD

```gherkin
Característica: Obtención y publicación de operaciones concertadas en A3
  Como sistema consumidor del cliente quiero recibir las operaciones ya concertadas
  para conciliar la operatoria y alimentar los procesos posteriores a la negociación.

  Escenario: Consulta de operaciones por cuenta con resultados
    Dado que la sesión FIX está "Conectada"
    Y que el conector tiene configurados los códigos CNV del cliente
    Cuando emite un Trade Capture Report Request por cuenta con TradeRequestType 1 y TrdType 0
    Y A3 responde con tres Trade Capture Report, el último con LastRptRequested en Y
    Entonces el conector publica tres eventos de operación concertada en la cola acordada
    Y para cada uno se registra el evento MSG-21: "Operación concertada {tradeReportId} publicada: {symbol}, {side}, {lastQty} a {lastPx}."
    Y la consulta se marca como completada recién al recibir el último reporte

  Escenario: Consulta por símbolo sin operaciones
    Cuando el conector emite un Trade Capture Report Request por el símbolo "DLR/DIC26"
    Y A3 responde sin operaciones para ese criterio
    Entonces la consulta se cierra como completada
    Y se registra el evento MSG-17: "A3 no reporta operaciones concertadas para los criterios solicitados."

  Escenario: Reporte de operación de bloque fuera de alcance
    Cuando A3 envía un Trade Capture Report con TrdType 1
    Entonces el conector no publica el mensaje en MQ
    Y lo registra en auditoría con MSG-22: "Trade Capture Report con TrdType {trdType} fuera del alcance del conector. Registrado, no publicado."

  Escenario: Solicitud rechazada por A3
    Cuando el conector emite un Trade Capture Report Request con un bloque Parties incompleto
    Y A3 responde con un Business Message Reject con BusinessRejectReason 5
    Entonces se publica el error MSG-10: "A3 rechazó el mensaje {refMsgType}: {businessRejectReason} — {text}."

  Escenario: Operación ya publicada que vuelve a llegar
    Dado que la operación con TradeReportID "TCR-40218" ya fue publicada
    Cuando A3 la vuelve a reportar en una consulta posterior
    Entonces el conector no la publica de nuevo
    Y registra el evento MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."
```

#### Fuera de alcance

- *Block trades* (`TrdType=1`), *allocations* y *giveups* (`TrdType=1001/1002`), `TradeCaptureReportAck` (`35=AR`), `AllocationInstruction` (`35=J`), `Confirmation` (`35=AK`) y reporte de posiciones (`35=AN`/`35=AP`): fuera del alcance del proyecto, conforme a SUP-02.
- Suscripción continua a TCR: el ROE sólo documenta `SubscriptionRequestType` para la variante de *allocations y giveups*, que está fuera de alcance. Ver `S-05`.

#### Notas / preguntas abiertas

- **Esta historia no tenía ningún contenido en el backlog borrador.** Los criterios se derivaron del ROE de A3 y **quedan pendientes de validación funcional con los referentes de negocio del cliente**.
- **Resuelto el 2026-09-16 (`S-05`): sólo consulta, no hay suscripción.** El flujo de TCR es exclusivamente *pull*. Queda descartado todo diseño basado en recepción no solicitada de Trade Capture Reports.
- **Resuelto el 2026-09-16 (`S-06`): consulta asincrónica a demanda, sin periodicidad fija.** Se descarta la propuesta de consulta programada al cierre de jornada: el conector **no planifica consultas por horario**, las emite cuando la necesidad se presenta. El criterio de disparo deja de ser temporal y pasa a ser por demanda. ✅ **Resuelto (`S-07`): el disparo lo decide el propio conector**, según su lógica configurable, sin cola de entrada desde el cliente. El MVP es puramente saliente hacia MQ (SUP-04): el conector emite el `35=AD` hacia A3 cuando corresponde y publica el resultado, sin recibir comandos.
- **Pendiente de confirmar con A3 (`S-16`):** que el perfil Drop Copy de sólo lectura admita emitir `Trade Capture Report Request`. Si no lo admitiera, los TCR llegarían únicamente como eventos duplicados y esta historia se simplificaría a consumo pasivo.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ⚠️ Depende de `T-07` (códigos CNV del cliente) | ✅ | ⚠️ El Excel no la estimó con criterios; re-estimar | ⚠️ Candidata a partir en «por símbolo» y «por cuenta» | ✅ |

---

### FIX-2.06 — Consultar el estado de las órdenes en A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 11` — **reescrita**: los criterios originales asumen una interfaz de usuario que el producto no tiene |
| **Actor** | Sistemas consumidores del cliente · Equipo de operaciones |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 3–5 SP |
| **Depende de** | `FIX-2.01`, `FIX-2.04` (la respuesta llega como Execution Report) |
| **Habilita** | `FIX-2.07` |

#### Historia

```
Como sistema consumidor del cliente
quiero consultar en A3 el estado conocido de una orden o del conjunto de órdenes
para verificar la situación real en el mercado sin depender de haber recibido todos los eventos
```

#### Valor de negocio

Es la red de seguridad del flujo de eventos: si un evento se perdió o llegó fuera de orden, la consulta permite recuperar la verdad desde A3. Es además el insumo de la reconciliación tras reconectar.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 11):

```text
Se muestran estados FIX.
Se exponen timestamps.
Se muestran fills parciales.
```

> Observación literal del Excel (`Obs`, US 11):

```text
explicitar que fix es asincronico, la consulta devuelve el estado de fix, no enecesariaente el de la orden (no es un OMS)
```

> **Reescritura del PO:** el conector no tiene interfaz de usuario, por lo que «se muestran» se reinterpreta como «se publican en MQ». La observación del Excel se elevó a regla transversal RN-15.

#### Criterios de aceptación

1. **[Feliz]** El conector emite un `Order Status Request` (`35=H`) para consultar una orden puntual, referenciando su `ClOrdID` (11).
2. **[Feliz]** El conector emite un `Order Mass Status Request` (`35=AF`) con `MassStatusReqID` (584) único y `MassStatusReqType` (585) = 7 (*Status for all orders*), pudiendo acotar por `Account` (1), por bloque `Instrument` o por `SecurityGroup` (1151).
3. **[Feliz]** El conector controla el alcance de la consulta masiva mediante `SecurityStatus` (965): 1 para órdenes activas, 0 para todos los estados. Si no se envía, A3 asume 1.
4. **[Feliz]** Las respuestas llegan como `Execution Report` de tipo *Order Status Response* y se procesan y publican conforme a `FIX-2.04`, correlacionadas con el `MassStatusReqID` de la solicitud.
5. **[Feliz]** El conector reconoce el cierre de la respuesta masiva mediante `LastRptRequested` (912) y no da la consulta por completa hasta recibirlo.
6. **[Alternativo]** Si A3 responde con la variante *Order Status Response – No orders*, el conector cierra la consulta como completada y registra MSG-16: "Reconciliación completada: A3 no reporta órdenes para los criterios solicitados."
7. **[Error]** Si A3 rechaza la solicitud con `Business Message Reject` (`35=j`), se publica MSG-10: "A3 rechazó el mensaje {refMsgType}: {businessRejectReason} — {text}."
8. **[Validación]** El conector **no emite más de una solicitud masiva por segundo**, conforme a RN-08. Si se solicitan consultas por encima del límite, las encola y registra MSG-18: "Límite de solicitudes masivas alcanzado (1 por segundo). La solicitud {requestId} queda encolada."
9. **[Validación]** El resultado publicado refleja el estado que A3 informa y se etiqueta explícitamente como «estado informado por el mercado», conforme a RN-15. El conector no lo presenta como estado consolidado de la orden.

#### Escenarios BDD

```gherkin
Característica: Consulta del estado de órdenes en A3
  Como sistema consumidor del cliente quiero consultar el estado conocido de las órdenes
  para verificar la situación real en el mercado.

  Escenario: Consulta masiva de todas las órdenes
    Dado que la sesión FIX está "Conectada"
    Cuando el conector emite un Order Mass Status Request con MassStatusReqType 7 y SecurityStatus 0
    Y A3 responde con cinco Execution Report de tipo Order Status Response, el último con LastRptRequested en Y
    Entonces se publican cinco eventos de estado de orden en MQ
    Y todos quedan correlacionados con el MassStatusReqID de la solicitud
    Y la consulta se marca como completada al recibir el último reporte

  Escenario: Consulta masiva sin órdenes
    Cuando el conector emite un Order Mass Status Request
    Y A3 responde con la variante Order Status Response sin órdenes
    Entonces la consulta se cierra como completada
    Y se registra el evento MSG-16: "Reconciliación completada: A3 no reporta órdenes para los criterios solicitados."

  Escenario: Control de caudal de consultas masivas
    Dado que el conector ya emitió una solicitud masiva en el último segundo
    Cuando se solicita una segunda consulta masiva
    Entonces la solicitud se encola en lugar de enviarse
    Y se registra la alerta MSG-18: "Límite de solicitudes masivas alcanzado (1 por segundo). La solicitud {requestId} queda encolada."

  Escenario: Consulta puntual de una orden
    Cuando el conector emite un Order Status Request para el ClOrdID "CLI-000451"
    Entonces A3 responde con un Execution Report de tipo Order Status Response
    Y el evento publicado indica que el estado proviene de una consulta al mercado
```

#### Fuera de alcance

- La API REST asincrónica de consulta de estado: fuera de la Fase 1 conforme a SUP-10.
- Consolidación del estado de la orden a partir de múltiples fuentes: el conector no es un OMS, conforme a RN-15.

#### Notas / preguntas abiertas

- ⚠️ **Verificación necesaria en la Épica 1:** la sesión del MVP es un **perfil Drop Copy de sólo lectura** (RN-17). Hay que confirmar con A3 que ese perfil **admite emitir `Order Status Request` y `Order Mass Status Request`**. Ambos son de lectura, pero un perfil restringido podría no habilitarlos. Si A3 no los admite sobre Drop Copy, esta historia y la reconciliación de `FIX-2.07` necesitan rediseñarse sobre el flujo de eventos duplicados. Se agrega como `S-16`.
- ✅ **Resuelto el 2026-09-18 (`S-07`): las consultas las dispara el propio conector**, según su lógica configurable. **No hay cola de entrada en el MVP**: SUP-04 sigue vigente. La alternativa de que el cliente las dispare por MQ quedó **desestimada** y se tratará en la Épica 4, junto con el resto del sentido de entrada.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.07 — Reconciliar el estado de órdenes tras restablecer la sesión

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Plan de trabajo, etapa MVP: «Recoverability — Reconciliación básica». **No está en el Excel** |
| **Actor** | Sistemas consumidores del cliente |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar en el input |
| **Depende de** | `FIX-2.06`, `FIX-2.11` (recuperación de mensajes faltantes) |

#### Historia

```
Como sistema consumidor del cliente
quiero que el conector verifique contra A3 el estado de las órdenes después de cada interrupción de sesión
para tener la certeza de que lo que conozco coincide con lo que el mercado registra
```

#### Valor de negocio

Es la mitigación directa del riesgo que la propia propuesta técnica identifica como crítico: que tras una interrupción quede una inconsistencia entre lo que el cliente cree y lo que A3 registra. Sin esta historia, la recuperación de secuencias resuelve el protocolo pero no garantiza la coherencia del negocio.

#### Escenarios fuente

> No hay escenarios en el input. La capacidad figura como entregable comprometido del plan de trabajo («Recoverability: Persistencia de secuencias, Detección de gaps, Resend Requests, **Reconciliación básica**») pero no tiene historia asociada en el Excel. Escenarios derivados del entregable y del análisis de riesgo RAID de la propuesta técnica.

#### Criterios de aceptación

1. **[Feliz]** Tras restablecer una sesión que se interrumpió, y una vez completada la recuperación de secuencias de `FIX-2.11`, el conector emite automáticamente un `Order Mass Status Request` conforme a `FIX-2.06` y registra MSG-14: "Reconciliación de estado iniciada tras restablecer la sesión. MassStatusReqID {massStatusReqId}."
2. **[Feliz]** El conector compara el estado informado por A3 con el último estado que publicó para cada orden.
3. **[Feliz]** Para cada orden cuyo estado en A3 difiere del último publicado, el conector publica un **evento de corrección** identificado como tal, y al cerrar la comparación registra MSG-15: "Reconciliación completada: {n} órdenes con estado divergente, publicadas como eventos de corrección."
4. **[Alternativo]** Si no hay divergencias, la reconciliación se cierra sin publicar eventos de corrección y se deja constancia en auditoría.
5. **[Alternativo]** Si A3 no reporta órdenes, se registra MSG-16: "Reconciliación completada: A3 no reporta órdenes para los criterios solicitados."
6. **[Error]** Si la reconciliación no puede completarse —porque la sesión se vuelve a caer o A3 rechaza la solicitud— el conector la reintenta al restablecerse la sesión y deja la reconciliación marcada como pendiente hasta lograrlo.
7. **[Validación]** La reconciliación se ejecuta también al iniciar la sesión de la jornada, no sólo tras una caída.
8. **[Validación]** Los eventos de corrección son idempotentes: reconciliar dos veces sin cambios no genera eventos duplicados, conforme a RN-05.

#### Escenarios BDD

```gherkin
Característica: Reconciliación del estado de órdenes tras una interrupción
  Como sistema consumidor del cliente quiero que el conector verifique el estado contra A3 tras cada interrupción
  para tener la certeza de que lo que conozco coincide con lo que el mercado registra.

  Escenario: Reconciliación con divergencias
    Dado que la sesión se interrumpió durante cuatro minutos y se restableció
    Y que la recuperación de secuencias se completó
    Cuando el conector emite la consulta masiva de estado
    Y A3 informa que la orden "CLI-000451" está ejecutada mientras el último evento publicado la daba por activa
    Entonces se publica un evento de corrección para "CLI-000451"
    Y se registra el evento MSG-15: "Reconciliación completada: {n} órdenes con estado divergente, publicadas como eventos de corrección."

  Escenario: Reconciliación sin divergencias
    Dado que la sesión se restableció y la recuperación de secuencias se completó
    Cuando el conector reconcilia y todos los estados coinciden
    Entonces no se publica ningún evento de corrección
    Y queda constancia de la reconciliación en auditoría

  Escenario: Reconciliación al abrir la jornada
    Dado que son las 09:30 y la sesión acaba de establecerse
    Cuando el conector completa el Logon
    Entonces dispara la reconciliación de estado
    Y se registra el evento MSG-14: "Reconciliación de estado iniciada tras restablecer la sesión. MassStatusReqID {massStatusReqId}."

  Escenario: La sesión se cae durante la reconciliación
    Dado que la reconciliación está en curso
    Cuando la sesión se interrumpe antes de recibir el último reporte
    Entonces la reconciliación queda marcada como pendiente
    Y se reintenta automáticamente al restablecerse la sesión
```

#### Fuera de alcance

- Reconciliación de operaciones concertadas (TCR) además de órdenes: se evalúa en `S-06`.
- Reconexión automática que dispara esta reconciliación: es `FIX-5.03`. En la Fase 1 la reconexión es manual u operada.

#### Notas / preguntas abiertas

- Esta historia **no está en el backlog borrador** pese a ser un entregable comprometido del plan de trabajo. Ver §11, observación O-4.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ⚠️ Depende de `FIX-2.06` | ✅ | ✅ | ⚠️ Sin estimar en el input | ✅ | ✅ |

---

### FIX-2.08 — Monitorear el estado de las sesiones FIX

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 16` · Plan de trabajo: «Monitoreo de sesión» |
| **Actor** | Equipo de operaciones y soporte |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 1–3 SP |
| **Depende de** | `FIX-2.01`, `FIX-2.02` |

#### Historia

```
Como integrante del equipo de operaciones
quiero conocer en todo momento el estado de la conectividad FIX con A3
para identificar y actuar sobre los incidentes antes de que impacten en la operatoria
```

#### Valor de negocio

Convierte la conectividad en algo observable. Sin esto, la primera señal de un problema es que un usuario de negocio note que le faltan datos.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 16):

```text
Estado conectado/desconectado.
Último heartbeat.
Secuencia actual.
```

#### Criterios de aceptación

1. **[Feliz]** El conector expone y mantiene actualizado el estado de la sesión con los valores **Conectada**, **Desconectada** y **Cerrada**.
2. **[Feliz]** El conector expone el *timestamp* del último mensaje recibido de A3 y del último enviado.
3. **[Feliz]** El conector expone el `MsgSeqNum` entrante y saliente actuales.
4. **[Feliz]** Cada transición de estado de la sesión se publica como evento y queda registrada en auditoría.
5. **[Alternativo]** El conector emite alerta ante desconexión no controlada (MSG-04), ausencia prolongada de mensajes (MSG-05), gap de secuencia no recuperado (MSG-08) y fallo de publicación en MQ (MSG-13).
6. **[Validación]** Las métricas y el estado expuestos se integran con las herramientas de observabilidad disponibles en el cliente, según lo definido en `T-04`.
7. **[Validación]** Ningún dato expuesto incluye credenciales, conforme a RN-06.

#### Escenarios BDD

```gherkin
Característica: Observabilidad de la sesión FIX
  Como integrante del equipo de operaciones quiero conocer el estado de la conectividad con A3
  para actuar sobre los incidentes antes de que impacten en la operatoria.

  Escenario: Consulta del estado con sesión activa
    Dado que la sesión está "Conectada"
    Cuando se consulta el estado de la conectividad
    Entonces se informa el estado "Conectada", el timestamp del último mensaje recibido y enviado, y los MsgSeqNum entrante y saliente

  Escenario: Alerta por desconexión no controlada
    Dado que la sesión está "Conectada"
    Cuando el enlace se interrumpe sin intercambio de Logout
    Entonces el estado pasa a "Desconectada"
    Y se emite la alerta MSG-04: "Sesión FIX interrumpida sin Logout. Última actividad registrada: {timestamp}."

  Escenario: Las credenciales no se exponen
    Cuando se consulta el estado de la conectividad
    Entonces la respuesta no contiene el usuario ni la contraseña de A3
```

#### Fuera de alcance

- Tableros y análisis avanzado de la información logueada: Épica 5 («Observabilidad — Análisis básico de información logeada»).

#### Notas / preguntas abiertas

- El canal de alertado (correo, herramienta corporativa, cola dedicada) lo define el cliente en `T-04`.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

> Continuación del §6 del documento maestro. Las historias siguientes pertenecen todas a la **Épica 2 — MVP TCR/ER y Conectividad FIX**.

---

### FIX-2.15 — Procesar los rechazos de nivel de sesión de A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 — MVP TCR/ER y Conectividad FIX |
| **Trazabilidad input** | §10 `R-01` · ROE A3 v2.0.53, *Session Level Reject Message* (`35=3`) · Criterio de evaluación de homologación: «manejo de errores» |
| **Actor** | Conector FIX · Equipo de operaciones y soporte |
| **Prioridad sugerida** | Must — **requisito explícito de la certificación de A3** |
| **Estimación del input** | Sin estimar en el backlog borrador |
| **Depende de** | `FIX-2.01` (sesión establecida), `FIX-2.12` (auditoría raw) |
| **Habilita** | Homologación A3 (`T-14`, `T-17`) |

#### Historia

```
Como conector FIX del cliente
quiero identificar, registrar y publicar los rechazos de nivel de sesión que A3 emite
para que el equipo de soporte pueda diagnosticar y corregir los problemas de protocolo antes de que afecten la operatoria
```

#### Valor de negocio

A3 evalúa explícitamente el «manejo de errores» en la certificación. Sin esta historia, un rechazo de protocolo —un mensaje mal formado, un campo obligatorio faltante, un valor fuera de rango— pasa desapercibido: el conector espera una respuesta que nunca llega. **La homologación puede no aprobarse sin esta capacidad.**

#### Criterios de aceptación

1. **[Feliz]** Al recibir un `Reject – Session Level` (`35=3`) de A3, el conector extrae y registra `RefSeqNum` (45), `RefTagID` (371), `RefMsgType` (372), `SessionRejectReason` (373) y `Text` (58).
2. **[Feliz]** El conector publica el rechazo como evento de error diferenciado en la cola de errores operativos, con MSG-09: "A3 rechazó el mensaje de secuencia {refSeqNum}: {sessionRejectReason} — {text}."
3. **[Feliz]** El conector mapea los 18 valores posibles de `SessionRejectReason` a descripciones legibles: 0 = *Invalid tag number*, 1 = *Required tag missing*, 2 = *Tag not defined for this message type*, 3 = *Undefined tag*, 4 = *Tag specified without a value*, 5 = *Value is incorrect*, 6 = *Incorrect data format*, 7 = *Decryption problem*, 8 = *Signature problem*, 9 = *CompID problem*, 10 = *SendingTime accuracy problem*, 11 = *Invalid MsgType*, 12 = *XML validation error*, 13 = *Tag appears more than once*, 14 = *Tag specified out of required order*, 15 = *Repeating group fields out of order*, 16 = *Incorrect NumInGroup count*, 17 = *Non "Data" value includes field delimiter*.
4. **[Feliz]** El mensaje FIX de rechazo queda registrado en formato *raw* conforme a RN-03.
5. **[Alternativo]** Si el rechazo apunta al `MsgSeqNum` de un mensaje saliente que el conector generó, el conector lo marca como **rechazado** en su registro interno y no lo reintenta con los mismos datos.
6. **[Error]** Si el `RefSeqNum` no corresponde a ningún mensaje enviado por el conector, el evento se publica igualmente como error con nota de inconsistencia.
7. **[Validación]** El conector **no cierra la sesión** ante un `Reject` aislado: el rechazo de nivel de sesión es sobre un mensaje individual, no sobre la sesión. La sesión se cierra sólo si A3 envía `Logout` a continuación o si el rechazo implica una inconsistencia de CompID (`SessionRejectReason` = 9).
8. **[Validación]** Ante `SessionRejectReason` = 9 (*CompID problem*), el conector trata la situación como inconsistencia de sesión conforme a RN-09, cierra la conexión y alerta.

#### Escenarios BDD

```gherkin
Característica: Procesamiento de rechazos de nivel de sesión de A3
  Como conector FIX del cliente quiero procesar los rechazos de sesión
  para diagnosticar problemas de protocolo antes de que afecten la operatoria.

  Escenario: Rechazo por campo obligatorio faltante
    Dado que la sesión FIX está "Conectada"
    Y que el conector envió un mensaje con secuencia 1487 al que le falta un campo obligatorio
    Cuando A3 responde con un Reject con RefSeqNum 1487, RefTagID 55, SessionRejectReason 1 y Text "Required tag missing: Symbol"
    Entonces el conector registra el mensaje raw en auditoría
    Y publica el error MSG-09: "A3 rechazó el mensaje de secuencia 1487: Required tag missing — Required tag missing: Symbol."
    Y marca el mensaje 1487 como rechazado en su registro interno
    Y la sesión permanece "Conectada"

  Escenario: Rechazo por valor incorrecto
    Cuando A3 envía un Reject con SessionRejectReason 5 y RefTagID 40
    Entonces el conector publica un error diferenciado que incluye el tag rechazado, la razón "Value is incorrect" y el texto de A3
    Y no reintenta el mensaje con los mismos datos

  Escenario: Rechazo por problema de CompID
    Cuando A3 envía un Reject con SessionRejectReason 9
    Entonces el conector trata la situación como inconsistencia de sesión
    Y cierra la conexión
    Y emite alerta crítica

  Esquema del escenario: Mapeo de las 18 razones de rechazo
    Cuando A3 envía un Reject con SessionRejectReason <código>
    Entonces el evento publicado incluye la descripción "<descripción>"

    Ejemplos:
      | código | descripción                                |
      | 0      | Invalid tag number                         |
      | 1      | Required tag missing                       |
      | 5      | Value is incorrect                         |
      | 9      | CompID problem                             |
      | 11     | Invalid MsgType                            |
```

#### Fuera de alcance

- Corrección automática del mensaje rechazado y reenvío: el conector alerta, no autocorrige.
- Manejo del `Reject` que el propio conector emite hacia A3: se cubre en la historia de procesamiento de mensajes entrantes malformados (pendiente de diseño detallado).

#### Notas / preguntas abiertas

- **El backlog borrador no contempla esta historia** pese a que A3 la evalúa explícitamente en la certificación. Ver §11 del documento maestro, observación 12.
- Se recomienda implementar antes de `T-17` (ejecución de la homologación).

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.16 — Procesar los rechazos de negocio de A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-02` · ROE A3 v2.0.53, *Business Message Reject* (`35=j`) |
| **Actor** | Conector FIX · Sistemas consumidores del cliente |
| **Prioridad sugerida** | Must — **requisito de homologación** |
| **Estimación del input** | Sin estimar |
| **Depende de** | `FIX-2.01`, `FIX-2.12` |
| **Habilita** | Homologación A3 (`T-14`, `T-17`) |

#### Historia

```
Como sistema consumidor del cliente
quiero recibir por MQ los rechazos de negocio que A3 emite ante mensajes válidos en situaciones no soportadas
para saber que una solicitud no fue procesada y actuar en consecuencia
```

#### Valor de negocio

El `Business Message Reject` es la respuesta de A3 cuando un mensaje es correcto a nivel de protocolo pero el negocio no puede procesarlo: una consulta TCR con un bloque `Parties` inválido, un `OrderStatusRequest` para una orden que no existe, o un mensaje no soportado por el perfil. Sin manejarla, el conector envía la solicitud y queda esperando una respuesta que nunca llega.

#### Criterios de aceptación

1. **[Feliz]** Al recibir un `Business Message Reject` (`35=j`) de A3, el conector extrae `RefSeqNum` (45), `RefMsgType` (372), `BusinessRejectRefID` (379), `BusinessRejectReason` (380) y `Text` (58).
2. **[Feliz]** El conector publica el rechazo como evento de error en la cola de errores operativos con MSG-10: "A3 rechazó el mensaje {refMsgType}: {businessRejectReason} — {text}."
3. **[Feliz]** El conector mapea los valores de `BusinessRejectReason` relevantes: 0 = *Other*, 1 = *Unknown ID*, 2 = *Unknown Security*, 3 = *Unknown Message Type*, 4 = *Application not available*, 5 = *Conditionally required field missing*, 6 = *Not authorized*, 18 = *Invalid price increment*.
4. **[Feliz]** El mensaje FIX de rechazo y el mensaje original que lo provocó quedan registrados en formato *raw* conforme a RN-03, correlacionados.
5. **[Feliz]** El evento publicado lleva el `correlation ID` del mensaje original rechazado conforme a RN-04, para que el consumidor pueda correlacionar solicitud y rechazo.
6. **[Alternativo]** Si el rechazo corresponde a una consulta de `FIX-2.05` (TCR) o `FIX-2.06` (estado de órdenes), la consulta pendiente se cierra como **fallida** en el registro interno.
7. **[Error]** Si el `RefSeqNum` no se puede correlacionar con un mensaje enviado, el evento se publica igualmente con la nota de que el mensaje de origen no fue encontrado.
8. **[Validación]** La sesión **no se cierra** ante un `Business Message Reject`: es un rechazo sobre un mensaje de negocio individual.

#### Escenarios BDD

```gherkin
Característica: Procesamiento de rechazos de negocio de A3
  Como sistema consumidor del cliente quiero recibir los rechazos de negocio
  para saber que una solicitud no fue procesada y actuar en consecuencia.

  Escenario: Rechazo de una consulta TCR con bloque Parties incompleto
    Dado que el conector emitió un Trade Capture Report Request con secuencia 932
    Cuando A3 responde con un Business Message Reject con RefSeqNum 932, RefMsgType "AD", BusinessRejectReason 5 y Text "Conditionally required field missing: PartyRole"
    Entonces el conector registra ambos mensajes en auditoría
    Y publica el error MSG-10: "A3 rechazó el mensaje AD: Conditionally required field missing — Conditionally required field missing: PartyRole."
    Y el evento lleva el correlation ID de la solicitud original
    Y la consulta TCR pendiente se marca como fallida

  Escenario: Rechazo por tipo de mensaje no soportado
    Cuando A3 envía un Business Message Reject con BusinessRejectReason 3 y Text "Unknown Message Type"
    Entonces el conector publica el error y no reintenta el mensaje

  Escenario: Rechazo por falta de autorización en el perfil Drop Copy
    Dado que la sesión es de perfil Drop Copy de sólo lectura
    Cuando el conector emite un mensaje no autorizado para ese perfil
    Y A3 responde con Business Message Reject con BusinessRejectReason 6 y Text "Not authorized"
    Entonces el conector publica el error
    Y la sesión permanece activa
```

#### Fuera de alcance

- Reintentos automáticos del mensaje rechazado: un rechazo de negocio indica que la solicitud no es válida en ese contexto, no que hubo un error transitorio.

#### Notas / preguntas abiertas

- **Pendiente (`S-16`):** si el perfil Drop Copy no admite consultas (`35=H`, `35=AF`, `35=AD`), los `Business Message Reject` serán la respuesta de A3. Esta historia es necesaria **independientemente** de la resolución de `S-16`.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.17 — Consumir el estado de la sesión de negociación de A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-03` · ROE A3 v2.0.53, *Trading Session Status* (`35=h`) |
| **Actor** | Sistemas consumidores del cliente · Equipo de operaciones |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |
| **Depende de** | `FIX-2.01` |
| **Habilita** | `FIX-2.04` (interpretación de eventos), `FIX-2.05` (contextualización de TCR) |

#### Historia

```
Como sistema consumidor del cliente
quiero conocer en tiempo real el estado y la fase de cada sesión de negociación de A3
para distinguir la ausencia de eventos por mercado cerrado de la ausencia por un problema de conectividad
```

#### Valor de negocio

Sin el contexto de mercado, los Execution Reports y Trade Capture Reports no se pueden interpretar: no se distingue una ausencia de eventos por mercado cerrado de una por sesión caída. Esta historia convierte el dato de estado del mercado en un evento consumible que habilita la correcta interpretación de toda la información que el conector publica.

#### Criterios de aceptación

1. **[Feliz]** El conector consume los mensajes `Trading Session Status` (`35=h`) de A3 y extrae `TradingSessionID` (336), `TradSesStatus` (340), `TradSesStatusRejReason` (567), `MarketSegmentID` (1300) y `Text` (58).
2. **[Feliz]** El conector mantiene internamente el estado de cada sesión de negociación por segmento de mercado y mapea `TradSesStatus` a las fases: 1 = *Halted*, 2 = *Open* (Trading), 3 = *Closed*, 4 = *Pre-Open* (Pre-Trading), 5 = *Pre-Close* (Post-Trading), 100 = *After Hour*, 101 = *CPX*.
3. **[Feliz]** Cada cambio de fase se publica como evento en la cola de estado de mercado con MSG-26: "Sesión de negociación {tradingSessionId} en fase {tradSesStatus}: {descripción}. MarketSegmentID {segmentId}."
4. **[Feliz]** Cuando la fase cambia, el conector registra adicionalmente MSG-27: "Cambio de fase de negociación: {tradingSessionId} pasó de {faseAnterior} a {faseActual}. {acción}."
5. **[Feliz]** El mensaje FIX queda registrado en formato *raw* conforme a RN-03, con `correlation ID` conforme a RN-04.
6. **[Alternativo]** Si A3 envía un `TradSesStatus` con un valor no mapeado, el conector lo publica con la descripción genérica "Estado no reconocido ({valor})" y alerta.
7. **[Alternativo]** Si la transición a `Closed` o `Halted` ocurre mientras hay consultas TCR o de estado de órdenes pendientes, el conector las marca como condicionadas al contexto: los resultados pueden estar incompletos.
8. **[Validación]** El estado de la sesión de negociación es independiente del estado de la sesión FIX del conector: el mercado puede estar cerrado mientras la sesión FIX sigue conectada, y viceversa.
9. **[Validación]** El conector no deduce estados: publica el estado que A3 informa, conforme a RN-15.

#### Escenarios BDD

```gherkin
Característica: Consumo del estado de la sesión de negociación de A3
  Como sistema consumidor del cliente quiero conocer el estado del mercado
  para distinguir la ausencia de eventos por mercado cerrado de un problema de conectividad.

  Escenario: Apertura de la sesión de negociación
    Dado que la sesión FIX está "Conectada"
    Cuando A3 envía un Trading Session Status con TradSesStatus 2 y TradingSessionID "MERV"
    Entonces el conector actualiza el estado interno del segmento a "Open (Trading)"
    Y publica el evento MSG-26: "Sesión de negociación MERV en fase Open: Trading. MarketSegmentID {segmentId}."
    Y registra MSG-27: "Cambio de fase de negociación: MERV pasó de Pre-Open a Open. Se habilitan las consultas."

  Escenario: Cierre de la sesión de negociación
    Dado que el estado del segmento MERV es "Open"
    Cuando A3 envía un Trading Session Status con TradSesStatus 3
    Entonces el conector actualiza el estado a "Closed"
    Y publica el evento de cierre
    Y marca las consultas pendientes como condicionadas al contexto

  Escenario: Halted por circuito de protección
    Cuando A3 envía un Trading Session Status con TradSesStatus 1 y Text "Market halt: circuit breaker"
    Entonces el conector publica un evento de mercado detenido
    Y alerta al equipo de operaciones

  Escenario: Estado no reconocido
    Cuando A3 envía un Trading Session Status con TradSesStatus 999
    Entonces el conector publica el evento con descripción "Estado no reconocido (999)"
    Y genera una alerta
```

#### Fuera de alcance

- Toma de decisiones automatizadas basadas en el estado del mercado (por ejemplo, no enviar órdenes si el mercado está cerrado): pertenece a la Épica 4.
- Consulta activa del estado del mercado (`Trading Session Status Request`, `35=g`): sólo se consumen los mensajes no solicitados que A3 envía.

#### Notas / preguntas abiertas

- **Verificar con A3:** si el perfil Drop Copy recibe automáticamente los `Trading Session Status` o si hay que suscribirse.
- La lista de fases puede ampliarse si A3 usa extensiones propias: confirmar contra el ambiente reMarkets.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### FIX-2.18 — Mantener el catálogo de cuentas habilitadas para la sesión Drop Copy

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-04` · ROE A3 v2.0.53, *Account List* (`UALT`) y *Account List Incremental* (`UALI`) |
| **Actor** | Conector FIX |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |
| **Depende de** | `FIX-2.01`, `T-05` (alta Drop Copy y mapeo de cuentas) |
| **Habilita** | `FIX-2.05` (composición del bloque `Parties` para consultas TCR), `FIX-2.04` (validación de eventos Drop Copy) |

#### Historia

```
Como conector FIX del cliente
quiero mantener actualizado el catálogo de cuentas habilitadas en la sesión Drop Copy
para validar que los eventos recibidos corresponden a cuentas esperadas y para componer correctamente las consultas TCR por cuenta
```

#### Valor de negocio

Sin el catálogo, el conector no puede componer el bloque `Parties` de las consultas TCR por cuenta (`FIX-2.05`) ni validar que los Execution Reports recibidos por Drop Copy corresponden a cuentas que el cliente espera monitorear. Un evento inesperado de una cuenta no mapeada podría contaminar los sistemas consumidores.

#### Criterios de aceptación

1. **[Feliz]** Tras establecer la sesión, el conector consume el mensaje `Account List` (`UALT`) de A3 que contiene la lista completa de cuentas habilitadas para la sesión Drop Copy, con `Account` (1), `PartyRole` y los roles asociados.
2. **[Feliz]** El conector almacena el catálogo en memoria y registra MSG-28: "Catálogo de cuentas actualizado: {n} cuentas habilitadas para la sesión Drop Copy."
3. **[Feliz]** El conector consume los mensajes `Account List Incremental` (`UALI`) para actualizar el catálogo en tiempo real cuando A3 agrega, modifica o elimina una cuenta durante la jornada.
4. **[Feliz]** El catálogo se usa como fuente para componer el bloque `Parties` de las consultas `Trade Capture Report Request` en `FIX-2.05`.
5. **[Alternativo]** Si el conector recibe un Execution Report para una cuenta que no está en el catálogo habilitado, **lo publica igualmente** —conforme a RN-11, ningún evento se descarta en silencio— pero lo marca con una advertencia y registra MSG-29: "Execution Report recibido para la cuenta {account} que no está en el catálogo habilitado. Evento publicado con marca de advertencia."
6. **[Error]** Si A3 no envía el `Account List` después del `Logon`, el conector opera sin validación de cuenta y alerta al equipo de operaciones.
7. **[Validación]** El catálogo se descarta y se recarga al abrir cada nueva jornada, coherente con RN-19 (reinicio diario).

#### Escenarios BDD

```gherkin
Característica: Mantenimiento del catálogo de cuentas habilitadas
  Como conector FIX del cliente quiero mantener el catálogo de cuentas
  para validar eventos Drop Copy y componer consultas TCR.

  Escenario: Carga inicial del catálogo tras el Logon
    Dado que la sesión FIX acaba de establecerse
    Cuando A3 envía un Account List con 12 cuentas habilitadas
    Entonces el conector almacena las 12 cuentas en memoria
    Y registra MSG-28: "Catálogo de cuentas actualizado: 12 cuentas habilitadas para la sesión Drop Copy."

  Escenario: Actualización incremental durante la jornada
    Dado que el catálogo tiene 12 cuentas
    Cuando A3 envía un Account List Incremental que agrega la cuenta "CLI-NUEVA-01"
    Entonces el catálogo pasa a tener 13 cuentas

  Escenario: Execution Report de una cuenta no catalogada
    Dado que el catálogo contiene las cuentas "CLI-001" a "CLI-012"
    Cuando A3 envía un Execution Report para la cuenta "OTRA-999"
    Entonces el conector lo publica como evento válido con marca de advertencia
    Y registra MSG-29: "Execution Report recibido para la cuenta OTRA-999 que no está en el catálogo habilitado. Evento publicado con marca de advertencia."

  Escenario: A3 no envía el catálogo después del Logon
    Dado que la sesión se estableció hace más de 30 segundos
    Y que A3 no envió un Account List
    Entonces el conector opera sin validación de cuenta
    Y alerta al equipo de operaciones
```

#### Fuera de alcance

- Gestión administrativa de altas y bajas de cuentas en A3: es responsabilidad de `T-05`.
- Validación de que las cuentas tengan permisos específicos por tipo de instrumento.

#### Notas / preguntas abiertas

- **Verificar con A3:** si los mensajes `UALT` y `UALI` están disponibles en el perfil Drop Copy o si son exclusivos de perfiles de trading.
- El formato de estos mensajes es una extensión de A3, no del estándar FIX: confirmar estructura contra la documentación específica del ROE.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ⚠️ Depende de `T-05` (mapeo de cuentas) | ✅ | ⚠️ Sin estimar | ✅ | ✅ |

---

### FIX-2.20 — Gestionar el ciclo diario de la sesión FIX

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-06` · RN-07 (ventana operativa) · RN-19 (reinicio diario) |
| **Actor** | Conector FIX · Equipo de operaciones |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |
| **Depende de** | `FIX-2.01`, `FIX-2.03`, `FIX-2.07`, `FIX-2.09` |

#### Historia

```
Como conector FIX del cliente
quiero gestionar automáticamente la apertura y el cierre de la jornada de negociación alineados a la ventana operativa de A3
para que el ciclo diario se ejecute de forma predecible sin intervención manual y sin generar ruido fuera de horario
```

#### Valor de negocio

El backlog trata la sesión como un estado permanente, pero A3 la opera por ventana diaria (09:30–19:00). Sin esta historia, el conector intenta conectarse fuera de horario y genera alertas falsas, o no inicia la jornada a tiempo y el cliente pierde los primeros eventos del día.

#### Criterios de aceptación

1. **[Feliz]** El conector inicia automáticamente la secuencia de apertura de jornada a las 09:30 (configurable), conforme a RN-07: obtiene credenciales de la API del banco (`FIX-2.01`), reinicia secuencias conforme a RN-19, establece la sesión FIX y dispara la reconciliación de inicio de jornada (`FIX-2.07`).
2. **[Feliz]** Completada la apertura, registra MSG-31: "Apertura de jornada completada: sesión establecida, secuencias reiniciadas, reconciliación iniciada. Jornada {fecha}."
3. **[Feliz]** El conector inicia automáticamente la secuencia de cierre de jornada a las 19:00 (configurable), conforme a RN-07: ejecuta el cierre controlado de la sesión (`FIX-2.03`), archiva los logs del día, genera un resumen diario con contadores de mensajes procesados y errores.
4. **[Feliz]** Completado el cierre, registra MSG-32: "Cierre de jornada completado: sesión cerrada, logs archivados, resumen generado. {totalER} ER procesados, {totalTCR} TCR procesados, {errores} errores."
5. **[Feliz]** Los horarios de apertura, cierre y de la ventana de negociación (10:00–17:30) son configurables por ambiente, conforme a `FIX-2.24`.
6. **[Alternativo]** Si la apertura falla (API de credenciales no responde, A3 no acepta el Logon), el conector reintenta conforme a la política de reintentos configurada **dentro de la ventana de sesión** y alerta.
7. **[Alternativo]** Si A3 cierra la sesión antes de las 19:00 (por ejemplo, por un `Logout` no solicitado), el conector registra el cierre anticipado y no intenta reconectarse si está fuera de la ventana de negociación.
8. **[Error]** Si el cierre de jornada no puede completarse (por ejemplo, el `Logout` no se confirma), el conector fuerza la desconexión, persiste las secuencias y registra el cierre como anormal.
9. **[Validación]** Entre las 19:00 y las 09:30, el conector **no intenta conectarse** ni genera alertas por estar desconectado, conforme a RN-07 y MSG-20.
10. **[Validación]** El resumen diario incluye: fecha, hora de apertura efectiva, hora de cierre efectiva, total de Execution Reports procesados, total de Trade Capture Reports procesados, gaps detectados, gaps recuperados, duplicados descartados y errores publicados.

#### Escenarios BDD

```gherkin
Característica: Gestión del ciclo diario de la sesión FIX
  Como conector FIX del cliente quiero gestionar la apertura y cierre de jornada
  para que el ciclo se ejecute de forma predecible sin intervención manual.

  Escenario: Apertura automática de la jornada
    Dado que son las 09:30 y el conector está en modo cierre de jornada
    Cuando se dispara la apertura automática
    Entonces el conector obtiene las credenciales de la API del banco
    Y reinicia los números de secuencia
    Y establece la sesión FIX con A3
    Y dispara la reconciliación de inicio de jornada
    Y registra MSG-31: "Apertura de jornada completada: sesión establecida, secuencias reiniciadas, reconciliación iniciada. Jornada {fecha}."

  Escenario: Cierre automático de la jornada
    Dado que son las 19:00 y la sesión está "Conectada"
    Cuando se dispara el cierre automático
    Entonces el conector ejecuta el Logout controlado
    Y archiva los logs del día
    Y genera el resumen diario con contadores
    Y registra MSG-32: "Cierre de jornada completado: sesión cerrada, logs archivados, resumen generado. {totalER} ER procesados, {totalTCR} TCR procesados, {errores} errores."

  Escenario: No se intenta conexión fuera de la ventana
    Dado que son las 22:00
    Cuando se evalúa si la sesión debe estar activa
    Entonces el conector no intenta conectarse
    Y no genera alertas por estar desconectado

  Escenario: Fallo en la apertura con reintentos
    Dado que son las 09:30 y la API de credenciales no responde
    Cuando el conector intenta la apertura
    Entonces reintenta conforme a la política configurada
    Y alerta al equipo de operaciones
    Y no intenta conectarse después de las 19:00
```

#### Fuera de alcance

- Reconexión automática intra-jornada: es `FIX-5.03` (Épica 5).
- Gestión de días feriados: se configura externamente, el conector no los conoce de forma autónoma.

#### Notas / preguntas abiertas

- **Definir con el cliente:** si hay días hábiles especiales (medias jornadas, subastas extraordinarias) que requieran horarios diferentes. La solución es que los horarios sean configurables.
- El resumen diario es un insumo natural para el *runbook* operativo de `T-21`.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ⚠️ Orquesta `FIX-2.01`, `FIX-2.03`, `FIX-2.07` | ✅ | ✅ | ⚠️ Sin estimar | ⚠️ Candidata a partir en apertura y cierre | ✅ |

---

### FIX-2.22 — Consumir y publicar los avisos de mercado de A3

| | |
|---|---|
| **Tipo** | HU |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-08` · ROE A3 v2.0.53, *News* (`35=B`) |
| **Actor** | Sistemas consumidores del cliente · Operador de mesa |
| **Prioridad sugerida** | Should |
| **Estimación del input** | Sin estimar (costo marginal) |
| **Depende de** | `FIX-2.01`, `T-03` (contratos MQ) |

#### Historia

```
Como sistema consumidor del cliente
quiero recibir por MQ los avisos de mercado que A3 publica a través del protocolo FIX
para que la mesa de operaciones tenga visibilidad de novedades operativas del mercado sin salir de sus herramientas habituales
```

#### Valor de negocio

A3 usa el mensaje `News` para comunicar novedades operativas por segmento de mercado: suspensiones, extensiones de horario, cambios de condiciones. El costo de implementación es marginal —el conector ya procesa mensajes FIX y publica en MQ— y el valor para la mesa es directo.

#### Criterios de aceptación

1. **[Feliz]** Al recibir un mensaje `News` (`35=B`) de A3, el conector extrae `Headline` (148), `Text` (58), `OrigTime` (42), `Urgency` (61) y `MarketSegmentID` (1300).
2. **[Feliz]** El conector publica el aviso como evento de texto en la cola de estado de mercado, sin procesamiento de contenido adicional, con MSG-33: "Aviso de mercado de A3 publicado: {headline}. OrigTime {origTime}, MarketSegmentID {segmentId}."
3. **[Feliz]** El mensaje FIX queda registrado en formato *raw* conforme a RN-03, con `correlation ID` conforme a RN-04.
4. **[Alternativo]** Si el mensaje contiene múltiples líneas en el bloque `LinesOfText` (33/58), todas se incluyen en el evento publicado.
5. **[Alternativo]** Si `Urgency` = 1 (*Flash*), el evento se marca con prioridad alta.
6. **[Validación]** El conector no interpreta ni filtra el contenido del aviso: lo publica tal cual.
7. **[Validación]** Un aviso duplicado —mismo `OrigTime` y `Headline`— se descarta conforme a RN-05.

#### Escenarios BDD

```gherkin
Característica: Publicación de avisos de mercado de A3
  Como sistema consumidor del cliente quiero recibir los avisos de mercado
  para que la mesa tenga visibilidad de novedades operativas.

  Escenario: Aviso de suspensión de operatoria
    Dado que la sesión FIX está "Conectada"
    Cuando A3 envía un News con Headline "Suspensión temporaria del segmento de Cauciones" y MarketSegmentID "CAUC"
    Entonces el conector publica el aviso en la cola de estado de mercado
    Y registra MSG-33: "Aviso de mercado de A3 publicado: Suspensión temporaria del segmento de Cauciones. OrigTime {origTime}, MarketSegmentID CAUC."

  Escenario: Aviso urgente
    Cuando A3 envía un News con Urgency 1 y Headline "Circuit breaker activado"
    Entonces el evento publicado se marca con prioridad alta

  Escenario: Aviso duplicado
    Dado que ya se publicó un aviso con OrigTime "2026-10-15T14:30:00" y Headline "Extensión de horario"
    Cuando A3 envía el mismo aviso nuevamente
    Entonces el conector no lo publica de nuevo
```

#### Fuera de alcance

- Procesamiento semántico del contenido del aviso (interpretar si afecta a un instrumento específico).
- Mensajes de tipo `Email` (`35=C`): se evalúan en una iteración futura.

#### Chequeo INVEST

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### 6.2 Épica 4 — Order Routing (historias de cabecera)

> Refinadas a nivel de cabecera conforme a SUP-13: objetivo, alcance, dependencias y criterios de alto nivel, suficientes para estimar y priorizar. El detalle completo se elabora al cerrar la Épica 3, incorporando el aprendizaje de la Fase 1.
>
> **Lo que cambia respecto de la Fase 1:** a partir de acá el conector **modifica el estado del mercado**. De ese único cambio de naturaleza se derivan todos los requisitos adicionales de la épica: idempotencia de escritura, máquina de estados de la orden, encadenamiento de identificadores, controles de A3 y, si la operatoria califica como DMA, control de riesgo *pre-trade* homologado.

| Key | Título | US Excel | Est. | Objetivo y alcance | Criterios de aceptación de alto nivel | Dependencias |
|---|---|---:|---|---|---|---|
| **FIX-4.01** | Recibir instrucciones de orden desde MQ | 7 | 5–8 SP | Consumir desde la cola del cliente las instrucciones de alta, cancelación y modificación, validarlas y transformarlas al mensaje FIX correspondiente | Consume de la cola definida · Valida estructura y obligatoriedad · Rechaza y deriva los mensajes inválidos sin descartarlos · **Es idempotente frente a `redelivery` de MQ: una misma instrucción nunca genera dos órdenes** · Registra trazabilidad completa | Contratos MQ de entrada · Duda del Excel: «¿Lo vamos a recibir en la cola o en una API?» → `S-11` |
| **FIX-4.02** | Enviar una nueva orden al mercado | 8 | 3–5 SP | Emitir `NewOrderSingle` (`35=D`) a partir de la instrucción recibida | Genera `ClOrdID` (11) único · Completa `Account`, `Symbol`, `Side`, `OrderQty`, `Price`, `OrdType` (2 = Limit, K = Market with Left Over as Limit) y `TimeInForce` (Day, GTC, IOC, FOK, GTD) · Valida los campos que el mercado fija antes de enviar · Registra auditoría completa · El Execution Report de respuesta se procesa con `FIX-2.04`, **sin cambios en el contrato de salida** | `FIX-4.01` · Duda del Excel: «puede haber alguna verificación respecto de valores en campos fix que estén fijados por el mercado (mensaje bien formado)» |
| **FIX-4.03** | Cancelar una orden vigente | 9 | 3–5 SP | Emitir `OrderCancelRequest` (`35=F`) | Referencia el `OrigClOrdID` correcto de la cadena · Maneja `OrderCancelReject` (`35=9`) · **La cancelación es asincrónica**: el estado sólo cambia al recibir el Execution Report de confirmación | `FIX-4.02` · Observación del Excel: «explicitar que fix es asincrónico» |
| **FIX-4.04** | Modificar una orden vigente | 10 | 3–5 SP | Emitir `OrderCancelReplaceRequest` (`35=G`) | Referencia el `OrigClOrdID` correcto · Genera un nuevo `ClOrdID` para la versión modificada · Maneja `OrderCancelReject` · Asincrónico igual que la cancelación | `FIX-4.02` |
| **FIX-4.05** | Cancelar masivamente las órdenes (*kill switch*) | *No está en el Excel* | Sin estimar | Emitir `OrderMassCancelRequest` (`35=q`) como mecanismo de contingencia | Soporta `MassCancelRequestType` 1 (por instrumento), 4 (por CFICode) y 7 (todas) · Respeta el límite de A3 de 1 cancelación masiva por segundo · Requiere autorización explícita | A3 lo exige como control obligatorio (*Kill Switch*) para el acceso al mercado |
| **FIX-4.06** | Aplicar las reglas de negocio por producto | *Implícita en US 26* | Sin estimar | Validaciones y particularidades de TRD, Renta Fija y Cauciones | A definir con los referentes de negocio del cliente | ⚠️ **Cauciones estará disponible en A3 recién a fines de 2026** |
| **FIX-4.07** | Control de riesgo *pre-trade* | *No está en el Excel* | Sin estimar | Sólo si la operatoria califica como acceso DMA: control de saldo disponible, márgenes al abrir posición, diferencias diarias, límites por segmento e instrumento, cantidad máxima por orden y *kill button*, todos controlables en tiempo real | Exigido por el Manual de Conectividad de A3 para habilitar DMA. **Puede ser un proyecto en sí mismo** | `S-08` — hay que aclararlo ahora aunque el impacto sea en la Épica 4 |

---

### 6.3 Épica 5 — Market Data y Tolerancia a Fallas (historias de cabecera)

| Key | Título | US Excel | Est. | Objetivo y alcance | Criterios de aceptación de alto nivel | Dependencias |
|---|---|---:|---|---|---|---|
| **FIX-5.01** | Suscribirse a Market Data de A3 | 14 | 3–5 SP | Emitir `MarketDataRequest` (`35=V`) y consumir `Snapshot / Full Refresh` (`35=W`) | Genera la suscripción con `MDReqID` único y `SubscriptionRequestType` 0, 1 o 2 · Define `MarketDepth` (0 = Full Book, 1 = Top of Book, N = mejores N niveles) · Recibe y procesa actualizaciones · Maneja `MarketDataRequestReject` (`35=Y`) · Gestiona la reanudación tras reconexión | ⚠️ El gateway **FIX-PTP entrega Full Refresh con profundidad 10 y 1 mensaje cada 500 ms por símbolo**. Mayor frecuencia requiere FIX-PTP-HR, e *incremental refresh* requiere FIX-PTP-LL, **sólo disponible vía colocation** → `S-09` |
| **FIX-5.02** | Publicar Market Data en MQ | 15 | 3–8 SP | Normalizar y distribuir los precios hacia los consumidores internos | Publica según el contrato acordado · Configura colas, tópicos y suscripciones · Soporta el caudal sin degradar el procesamiento de ER y TCR | Observación del Excel: «contemplar la configuración de las colas MQ para publicación (suscripciones, tópicos, etc.)» |
| **FIX-5.03** | Reconexión automática | 18 | 3–5 SP | Restablecer la sesión sin intervención manual | Reintentos configurables con espera creciente · Recupera las secuencias tras reconectar · Dispara la reconciliación de `FIX-2.07` · No reintenta fuera de la ventana operativa de A3 · ⚠️ **El *hard stop* por credenciales rechazadas de RN-18 prevalece sobre toda política de reintento**: ante `Logout` con `Text` de credencial inválida, expirada o usuario bloqueado, no se reintenta nunca automáticamente | `FIX-2.01`, `FIX-2.07`, `FIX-2.11` · RN-18 |
| **FIX-5.04** | Recuperación tras reinicio del proceso | 19 | 1–3 SP | Restaurar el estado operativo tras un reinicio | Recupera las secuencias persistidas · Recupera el estado de las órdenes abiertas mediante consulta a A3 · ❌ **Se elimina del alcance «recupera posiciones locales»**: el conector no mantiene posiciones, conforme a RN-15 | `FIX-2.09`, `FIX-2.07` |
| **FIX-5.05** | Catálogo de instrumentos | *No está en el Excel* | Sin estimar | `SecurityListRequest` / `SecurityList` (`35=x` / `35=y`) y `SecurityStatus` (`35=e` / `35=f`) | Mantiene el catálogo de instrumentos habilitados y su estado | ⚠️ **Puede necesitar adelantarse al MVP** si la normalización de ER y TCR requiere enriquecer más allá del `Symbol` → `S-04` |

---

## 7. Historias técnicas — enablers

> **Adaptación declarada:** la plantilla original de esta sección está pensada para endpoints BFF/BE con tabla de errores HTTP. El producto **no expone endpoints HTTP** en la Fase 1 (SUP-10, SUP-12). Se mantiene la sección para los *enablers* técnicos del conector —capacidades internas sin valor directo para el negocio pero necesarias para que las HU de §6 funcionen— y la tabla de «errores esperados» se reemplaza por **condiciones de error del protocolo FIX y de la integración MQ**.

---

### FIX-2.09 — Persistir los números de secuencia de la sesión

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 4` · Plan de trabajo: «Recoverability — Persistencia de secuencias» |
| **Habilita** | `FIX-2.03`, `FIX-2.10`, `FIX-2.11`, `FIX-5.04` |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 1–3 SP |
| **Depende de** | `S-10` (dónde se persiste) |

#### Objetivo técnico

Almacenar los `MsgSeqNum` entrante y saliente de la sesión FIX de forma que sobrevivan a un reinicio del proceso, para poder continuar la sesión sin pérdida ni duplicación de mensajes.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 4):

```text
Se guarda cada secuencia enviada.
Se guarda cada secuencia recibida.
Los datos sobreviven a reinicios.
```

> Observación literal del Excel (`Obs`, US 4): `Validar con el cliente donde se persiste (storage?)` — ✅ **resuelta el 2026-09-16: persistencia por archivos, deliberadamente para no impactar la base de datos** (`S-10`). **Sybase queda fuera del alcance del MVP.**

#### Criterios de aceptación

1. **[Feliz]** El conector persiste el `MsgSeqNum` de cada mensaje **enviado**, antes de considerarlo emitido.
2. **[Feliz]** El conector persiste el `MsgSeqNum` de cada mensaje **recibido**, antes de procesarlo.
3. **[Feliz]** Tras un reinicio del proceso, el conector recupera los últimos valores persistidos y continúa la numeración desde allí.
4. **[Feliz]** La persistencia se resuelve mediante **almacenamiento en archivos** sobre volumen persistente, conforme a SUP-05. **No se accede a la base de datos**: es una decisión deliberada para no impactar su caudal.
5. **[Feliz]** Al abrir la sesión de cada jornada los números de secuencia **se reinician**, conforme a RN-19. La persistencia tiene por lo tanto alcance **intra-jornada**: su objetivo es sobrevivir a un reinicio del proceso dentro del día, no dar continuidad entre días.
5.1. **[Validación]** Al detectar que la jornada persistida es anterior a la actual, el conector descarta los valores y arranca en 1, en lugar de continuar desde el último número del día previo.
6. **[Error]** Si la escritura de la secuencia falla, el conector no envía el mensaje y genera alerta: es preferible no enviar a enviar con una secuencia que no se puede recuperar.
7. **[Validación]** La persistencia soporta el caudal de mensajes sin convertirse en el cuello de botella del procesamiento.

#### Escenarios BDD

```gherkin
Característica: Persistencia de los números de secuencia de la sesión FIX
  Escenario: Continuidad tras un reinicio del proceso
    Dado que la sesión llegó al MsgSeqNum entrante 1487 y saliente 932
    Y que esos valores quedaron persistidos
    Cuando el proceso del conector se reinicia
    Entonces al restablecer la sesión el conector continúa desde el entrante 1487 y el saliente 932
    Y no se produce ningún gap ni duplicación

  Escenario: Fallo de escritura de la secuencia
    Dado que el almacenamiento de secuencias no está disponible
    Cuando el conector intenta enviar un mensaje
    Entonces el mensaje no se envía
    Y se genera una alerta para el equipo de operaciones
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Almacenamiento no disponible en lectura | La sesión no se inicia; se alerta |
| Almacenamiento no disponible en escritura | No se envía el mensaje; se alerta |
| Valores persistidos corruptos o inconsistentes | La sesión no se inicia automáticamente; requiere intervención manual explícita |

#### Notas / preguntas abiertas

- Si el cliente exige Sybase por política corporativa, hay que re-estimar: el patrón de acceso mediante *Stored Procedures* por cada mensaje puede afectar el caudal. Ver `S-10`.

---

### FIX-2.10 — Detectar gaps en la secuencia entrante

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 6` · Plan de trabajo: «Recoverability — Detección de gaps» |
| **Habilita** | `FIX-2.11`, `FIX-2.07` |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 1–3 SP |
| **Depende de** | `FIX-2.09` |

#### Objetivo técnico

Detectar cualquier discontinuidad en la secuencia de mensajes entrantes para poder disparar la recuperación automática antes de que se procese información incompleta.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 6):

```text
Se detecta cualquier salto.
Se genera ResendRequest.
Se reestablece la sincronización.
```

#### Criterios de aceptación

1. **[Feliz]** El conector compara el `MsgSeqNum` de cada mensaje entrante con el esperado y detecta cualquier salto.
2. **[Feliz]** Al detectar un gap, el conector registra MSG-06: "Gap de secuencia detectado: se esperaba {esperado}, se recibió {recibido}. Se solicita reenvío del rango {desde}-{hasta}." y dispara la recuperación de `FIX-2.11`.
3. **[Feliz]** Los mensajes recibidos durante la recuperación se encolan y se procesan en orden, no antes de completar el rango faltante.
4. **[Alternativo]** Si el `MsgSeqNum` recibido es **menor** al esperado y el mensaje no tiene `PossDupFlag=Y`, el conector trata la situación como inconsistencia grave conforme al protocolo y alerta.
5. **[Validación]** Un mensaje con `PossDupFlag=Y` cuyo `MsgSeqNum` ya fue procesado no se considera gap: se descarta conforme a RN-05 con MSG-12.

#### Escenarios BDD

```gherkin
Característica: Detección de discontinuidades en la secuencia entrante
  Escenario: Salto de secuencia detectado
    Dado que el último MsgSeqNum entrante procesado es 1487
    Cuando A3 envía un mensaje con MsgSeqNum 1492
    Entonces el conector detecta el gap
    Y registra la alerta MSG-06: "Gap de secuencia detectado: se esperaba {esperado}, se recibió {recibido}. Se solicita reenvío del rango {desde}-{hasta}."
    Y solicita el reenvío del rango 1488-1491
    Y encola el mensaje 1492 hasta completar el rango faltante

  Escenario: Mensaje duplicado no se interpreta como gap
    Dado que el último MsgSeqNum entrante procesado es 1487
    Cuando A3 envía un mensaje con MsgSeqNum 1485 y PossDupFlag en Y
    Entonces el conector no lo interpreta como gap
    Y lo descarta registrando MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Secuencia entrante menor a la esperada sin `PossDupFlag` | Inconsistencia grave: alerta y, conforme al protocolo, cierre de la sesión |
| Gap detectado durante una recuperación en curso | Se amplía el rango solicitado; no se inician recuperaciones concurrentes |

---

### FIX-2.11 — Recuperar los mensajes faltantes mediante Resend Request

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 5` · Plan de trabajo: «Recoverability — Resend Requests» |
| **Habilita** | `FIX-2.04`, `FIX-2.05`, `FIX-2.07` |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 1–3 SP |
| **Depende de** | `FIX-2.10` |

#### Objetivo técnico

Reconstruir los mensajes faltantes de la secuencia, en ambas direcciones, conforme al protocolo FIX, para que ningún evento del mercado se pierda.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 5):

```text
Se identifican gaps.
Se responde con los mensajes faltantes.
Se respeta el protocolo FIX.
```

> Observación literal del Excel (`Obs`, US 5): `Se loguean los mensajes en un archivo (enviadp - recibido)`

#### Criterios de aceptación

1. **[Feliz]** Ante un gap detectado, el conector emite un `Resend Request` (`35=2`) con `BeginSeqNo` (7) y `EndSeqNo` (16) correctos, usando `EndSeqNo = 0` cuando solicita todos los mensajes posteriores a uno dado.
2. **[Feliz]** El conector procesa los mensajes retransmitidos por A3 en orden y los entrega al procesamiento de negocio una vez completo el rango.
3. **[Feliz]** El conector atiende los `Resend Request` que **recibe** de A3, retransmitiendo desde su registro los mensajes solicitados conforme al protocolo.
4. **[Feliz]** El conector procesa `Sequence Reset` (`35=4`) en modo **Gap Fill** (`GapFillFlag=Y`) y en modo **Reset** (`GapFillFlag=N`), respetando la regla de que el `NewSeqNo` (36) no puede ser menor al esperado.
5. **[Alternativo]** Completada la recuperación, el conector registra MSG-07: "Secuencia restablecida. Rango {desde}-{hasta} recuperado."
6. **[Error]** Si tras los reintentos configurados el rango no se puede recuperar, el conector registra MSG-08: "No se pudo recuperar el rango {desde}-{hasta} tras {n} intentos. Requiere intervención manual." y alerta.
7. **[Validación]** Los mensajes recuperados se deduplican antes de publicarse, conforme a RN-05: la recuperación no puede generar eventos duplicados en MQ.

#### Escenarios BDD

```gherkin
Característica: Recuperación de mensajes faltantes de la sesión FIX
  Escenario: Recuperación exitosa de un rango
    Dado que el conector detectó un gap en el rango 1488-1491
    Cuando emite un Resend Request con BeginSeqNo 1488 y EndSeqNo 1491
    Y A3 retransmite los cuatro mensajes
    Entonces el conector los procesa en orden
    Y registra el evento MSG-07: "Secuencia restablecida. Rango {desde}-{hasta} recuperado."
    Y ningún evento se publica dos veces en MQ

  Escenario: A3 responde con Sequence Reset en modo Gap Fill
    Dado que el conector solicitó el reenvío del rango 1488-1491
    Cuando A3 responde con un Sequence Reset con GapFillFlag en Y y NewSeqNo 1492
    Entonces el conector avanza la secuencia esperada a 1492
    Y no espera los mensajes administrativos omitidos

  Escenario: A3 solicita un reenvío al conector
    Cuando A3 envía un Resend Request con BeginSeqNo 900 y EndSeqNo 0
    Entonces el conector retransmite desde su registro todos los mensajes a partir del 900

  Escenario: Rango que no se puede recuperar
    Dado que el conector solicitó el reenvío del rango 1488-1491 tres veces
    Cuando A3 no retransmite los mensajes
    Entonces se registra el error MSG-08: "No se pudo recuperar el rango {desde}-{hasta} tras {n} intentos. Requiere intervención manual."
    Y se alerta al equipo de operaciones
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| A3 no responde al `Resend Request` | Reintento configurable; luego MSG-08 y alerta |
| `NewSeqNo` menor al esperado en un `Sequence Reset` | Se rechaza conforme al protocolo y se alerta |
| Mensajes retransmitidos ya procesados | Se descartan conforme a RN-05 con MSG-12 |

---

### FIX-2.12 — Registrar todos los mensajes FIX en formato raw

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Excel `US ID = 17` · Plan de trabajo: «Auditoría — Logging FIX raw, Logging MQ» |
| **Habilita** | Todas las HU de E2 · Requisito de homologación de A3 |
| **Prioridad sugerida** | Must |
| **Estimación del input** | 1–3 SP |

#### Objetivo técnico

Almacenar cada mensaje FIX enviado y recibido en su forma original, de modo que pueda reconstruirse íntegramente la actividad diaria y el ciclo de vida de cualquier operación. A3 puede solicitar estos registros en casos de soporte.

#### Escenarios fuente

> Transcripción literal del Excel (`Acc Crit.`, US 17):

```text
Se almacena mensaje raw.
Se almacena timestamp.
Se almacena sesión asociada.
```

#### Criterios de aceptación

1. **[Feliz]** Cada mensaje FIX enviado y recibido se almacena en formato *raw*, con *timestamp*, dirección (enviado o recibido), `MsgSeqNum`, `MsgType` y sesión asociada, conforme a RN-03.
2. **[Feliz]** Cada mensaje publicado o consumido en MQ se registra con su `correlation ID`, conforme a RN-04.
3. **[Feliz]** El registro permite reconstruir, para cualquier operación, la cadena completa mensaje FIX *raw* → evento normalizado → mensaje MQ.
4. **[Feliz]** El registro cubre la actividad diaria completa y es exportable para entregarlo a A3 si lo solicita.
5. **[Validación]** Los campos `Password` (554) y cualquier otro dato sensible se almacenan **enmascarados**, conforme a RN-06.
6. **[Validación]** El registro se escribe **antes** de procesar o publicar el mensaje, para que un fallo posterior no deje el evento sin rastro.
7. **[Validación]** La política de retención se acuerda con el cliente en `T-04`.

#### Escenarios BDD

```gherkin
Característica: Auditoría de la mensajería FIX y MQ
  Escenario: Registro de un Execution Report recibido
    Cuando A3 envía un Execution Report
    Entonces el mensaje raw queda almacenado con su timestamp, MsgSeqNum, MsgType y sesión
    Y el registro precede a la publicación en MQ
    Y comparte el correlation ID con el evento publicado

  Escenario: Reconstrucción de la cadena de una operación
    Dado que se publicó en MQ el evento con correlation ID "c-88120"
    Cuando se consulta la auditoría por ese correlation ID
    Entonces se obtiene el mensaje FIX raw de origen, el evento normalizado y el mensaje MQ publicado

  Escenario: Enmascaramiento de credenciales
    Cuando el conector registra un Logon enviado
    Entonces el campo Password aparece enmascarado en el registro
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| El almacenamiento de auditoría no está disponible | Alerta inmediata. El comportamiento —detener el procesamiento o continuar degradado— se decide en `T-04`, porque la auditoría es requisito de A3 |
| Registro con credenciales sin enmascarar | Defecto bloqueante de seguridad |

---

### FIX-2.13 — Procesar de forma idempotente los mensajes reenviados

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Propuesta técnica, RAID — riesgo 4: «Tratamiento incorrecto de mensajes duplicados o reenviados en FIX o MQ». **No está en el Excel** |
| **Habilita** | `FIX-2.04`, `FIX-2.05`, `FIX-2.07` |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |

#### Objetivo técnico

Garantizar que ni el mecanismo de recuperación de FIX ni el *redelivery* de MQ produzcan eventos duplicados en los sistemas del cliente. Es la mitigación que la propia propuesta técnica define para uno de sus riesgos principales.

#### Escenarios fuente

> No hay escenarios en el input. Derivado de la mitigación declarada en el RAID: «definir mecanismos de procesamiento idempotente o controles equivalentes para los flujos críticos y validar específicamente los escenarios de reenvío y redelivery».

#### Criterios de aceptación

1. **[Feliz]** El conector mantiene un registro de los identificadores de negocio ya procesados: `ExecID` (17) para Execution Reports y `TradeReportID` (571) para Trade Capture Reports.
2. **[Feliz]** Un mensaje cuyo identificador ya fue procesado no se vuelve a publicar en MQ y se registra MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."
3. **[Feliz]** Un mensaje con `PossDupFlag=Y` se evalúa contra el registro antes de procesarse.
4. **[Feliz]** La deduplicación cubre tanto el reenvío por FIX como la reentrega por MQ.
5. **[Validación]** El registro de identificadores procesados sobrevive a un reinicio del proceso dentro de la jornada.
6. **[Validación]** La ventana de deduplicación es la **jornada de negociación completa**, coherente con el reinicio diario de secuencias de RN-19.

#### Escenarios BDD

```gherkin
Característica: Procesamiento idempotente de los mensajes del mercado
  Escenario: Execution Report reenviado tras una recuperación
    Dado que el Execution Report con ExecID "EX-77120" ya fue publicado
    Cuando A3 lo retransmite en respuesta a un Resend Request
    Entonces no se publica un segundo evento en MQ
    Y se registra MSG-12: "Mensaje FIX duplicado descartado (secuencia {seq}, identificador {id}). No se publica en MQ."

  Escenario: Reentrega del mismo mensaje por MQ
    Dado que el evento con correlation ID "c-88120" ya fue entregado
    Cuando MQ lo reentrega por redelivery
    Entonces el consumidor puede identificarlo como el mismo evento
    Y no se duplica el efecto en los sistemas del cliente

  Escenario: Deduplicación persistente tras reinicio
    Dado que el Execution Report con ExecID "EX-77120" fue publicado antes del reinicio
    Cuando el proceso se reinicia y A3 retransmite ese mensaje
    Entonces el conector lo sigue reconociendo como duplicado
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Registro de deduplicación no disponible | Alerta. No se publica sin poder verificar duplicados: es preferible demorar a duplicar |
| Identificador de negocio ausente en el mensaje | Se cae al criterio de `MsgSeqNum` + `PossDupFlag` y se registra la excepción |

> **Nota de diseño:** en la Fase 1 el costo de un duplicado es un evento informativo repetido. A partir de la Épica 4, el mismo mecanismo evita **órdenes duplicadas en el mercado**. Construirlo ahora, con el costo del error bajo, es una decisión deliberada de secuencia.

---

### FIX-2.14 — Correlacionar de punta a punta la mensajería FIX y MQ

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | Plan de trabajo, etapa MVP: «Auditoría — Correlation IDs». **No está en el Excel** |
| **Habilita** | `FIX-2.04`, `FIX-2.05`, `FIX-2.12`, y el diagnóstico de toda la solución |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |

#### Objetivo técnico

Asignar y propagar un identificador de correlación que atraviese el mensaje FIX, el evento normalizado, el mensaje MQ y el registro de auditoría, de modo que cualquier incidente pueda investigarse sin reconstruir la cadena a mano.

#### Criterios de aceptación

1. **[Feliz]** Todo mensaje FIX de negocio recibido genera un `correlation ID` único que se propaga al evento normalizado, al mensaje MQ y al registro de auditoría, conforme a RN-04.
2. **[Feliz]** Los eventos derivados de un mismo hecho de negocio —por ejemplo, las sucesivas ejecuciones parciales de una orden— comparten además un identificador de agrupación basado en el `ClOrdID` o el `OrderID`.
3. **[Feliz]** El `correlation ID` se incluye en las trazas y en los logs de aplicación, no sólo en la auditoría.
4. **[Validación]** Dado un `correlation ID`, se puede recuperar el mensaje FIX *raw*, el evento publicado y su estado de entrega.
5. **[Validación]** El formato del `correlation ID` se acuerda con arquitectura del cliente en `T-03`, para que sea compatible con las herramientas de trazabilidad corporativas.

#### Escenarios BDD

```gherkin
Característica: Correlación de punta a punta
  Escenario: Trazabilidad de un evento publicado
    Cuando A3 envía un Execution Report y el conector lo publica en MQ
    Entonces el mensaje raw, el evento normalizado y el mensaje MQ comparten el mismo correlation ID

  Escenario: Agrupación de ejecuciones parciales
    Dado que la orden "CLI-000451" recibe tres ejecuciones parciales
    Cuando se publican los tres eventos
    Entonces cada uno tiene su propio correlation ID
    Y los tres comparten el identificador de agrupación de la orden
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Evento publicado sin `correlation ID` | Defecto bloqueante: incumple RN-04 |

---

> Continuación del §7 del documento maestro. Capacidades internas necesarias para que las HU funcionen.

---

### FIX-2.19 — Aplicar control de caudal propio antes de emitir solicitudes

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-05` · RN-08 (límites de caudal de A3) · Manual de Conectividad A3, *Volumen de Mensajes soportados* |
| **Habilita** | `FIX-2.05`, `FIX-2.06`, `FIX-2.07` y toda historia que emita solicitudes hacia A3 |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |
| **Depende de** | `FIX-2.01` |

#### Objetivo técnico

Implementar un mecanismo de control de caudal que garantice que el conector nunca supere los límites de solicitudes de A3, para evitar que A3 desconecte la sesión por envío excesivo de mensajes. El Manual de Conectividad establece que A3 **se reserva el derecho de desconectar** a los participantes que pongan en riesgo la estabilidad de la plataforma.

#### Criterios de aceptación

1. **[Feliz]** El conector mantiene un limitador de caudal que respeta los límites de A3 conforme a RN-08: máximo 1 `Order Mass Status Request` por segundo, máximo 1 `Order Mass Cancel Request` por segundo, máximo 100 `Order Status Request` por segundo.
2. **[Feliz]** Cuando una solicitud excede el límite, el conector la encola internamente y registra MSG-30: "Solicitud {msgType} encolada por control de caudal: {pendientes} solicitudes pendientes. Próximo envío en {ms} ms."
3. **[Feliz]** Las solicitudes encoladas se emiten en orden FIFO cuando se libera el cupo.
4. **[Feliz]** El limitador aplica a cada tipo de solicitud de forma independiente: una solicitud masiva por segundo no bloquea las solicitudes individuales.
5. **[Alternativo]** Si la cola de solicitudes pendientes supera un umbral configurable, el conector emite alerta de saturación y rechaza nuevas solicitudes no críticas.
6. **[Error]** Si pese al control A3 desconecta la sesión por caudal excesivo, el conector registra la desconexión como incidente de caudal y ajusta dinámicamente el umbral.
7. **[Validación]** El control de caudal se aplica **antes** de encolar el mensaje en la capa de sesión FIX, no después.
8. **[Validación]** Los umbrales son configurables por ambiente, para poder ajustarlos si A3 modifica sus límites.

#### Escenarios BDD

```gherkin
Característica: Control de caudal propio antes de emitir solicitudes
  Escenario: Solicitud masiva dentro del límite
    Dado que no se emitió una solicitud masiva en el último segundo
    Cuando el conector necesita emitir un Order Mass Status Request
    Entonces lo emite inmediatamente

  Escenario: Solicitud masiva que excede el límite
    Dado que se emitió un Order Mass Status Request hace 200 ms
    Cuando el conector necesita emitir otro
    Entonces lo encola
    Y registra MSG-30: "Solicitud AF encolada por control de caudal: 1 solicitudes pendientes. Próximo envío en 800 ms."
    Y lo emite automáticamente 800 ms después

  Escenario: Solicitudes independientes por tipo
    Dado que se emitió un Order Mass Status Request hace 200 ms
    Cuando el conector necesita emitir un Order Status Request individual
    Entonces lo emite inmediatamente sin esperar
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Cola de solicitudes pendientes saturada | Alerta de saturación; solicitudes no críticas rechazadas |
| Desconexión por caudal excesivo pese al control | Registro del incidente; ajuste dinámico de umbrales |

---

### FIX-2.21 — Enmascarar credenciales y datos sensibles en la auditoría

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-07` · RN-03 (logging raw) · RN-06 (credenciales nunca persistidas) |
| **Habilita** | `FIX-2.12` (auditoría raw), `FIX-2.01` (Logon) |
| **Prioridad sugerida** | Must |
| **Estimación del input** | Sin estimar |

#### Objetivo técnico

Garantizar que el logging raw exigido por A3 (RN-03) no exponga credenciales ni datos sensibles. El `Logon` (`35=A`) contiene la contraseña en el campo `Password` (554). Registrarlo sin enmascarar es un **incidente de seguridad**. Esta historia implementa el enmascaramiento transversal antes de que el mensaje se escriba en cualquier destino de auditoría.

#### Criterios de aceptación

1. **[Feliz]** Antes de registrar un mensaje FIX en formato *raw*, el conector identifica y enmascara los campos sensibles: `Password` (554), `NewPassword` (925) si existiera, `RawData` (96) cuando contiene credenciales, y cualquier campo que la configuración marque como sensible.
2. **[Feliz]** El enmascaramiento es irreversible: el dato original **no puede recuperarse** desde el registro. Se reemplaza el valor por `"***MASKED***"` o un patrón configurable.
3. **[Feliz]** Cada enmascaramiento queda registrado con MSG-38: "Campo sensible enmascarado en el registro de auditoría: tag {tagId} del mensaje {msgType} con secuencia {seqNum}."
4. **[Feliz]** El enmascaramiento se aplica en **todos los destinos**: log raw, trazas de aplicación, mensajes de error publicados en MQ, y cualquier otro log o salida.
5. **[Validación]** El mensaje FIX que viaja por el protocolo **no se modifica**: el enmascaramiento aplica sólo a la copia que se registra.
6. **[Validación]** Los campos no sensibles del `Logon` (`SenderCompID`, `TargetCompID`, `HeartBtInt`, `DefaultApplVerID`) se registran sin enmascarar.
7. **[Validación]** Conforme a RN-06, las credenciales se mantienen sólo en memoria y **nunca** aparecen en disco, logs, trazas, mensajes de error ni repositorio.
8. **[Error]** Si se detecta un registro de auditoría con un campo sensible sin enmascarar, se trata como **defecto bloqueante de seguridad**.

#### Escenarios BDD

```gherkin
Característica: Enmascaramiento de credenciales en la auditoría
  Escenario: Registro de un Logon con contraseña enmascarada
    Cuando el conector registra un Logon enviado con Password "S3cr3tP4ss"
    Entonces en el log raw el campo 554 aparece como "***MASKED***"
    Y los campos SenderCompID y HeartBtInt aparecen con sus valores originales
    Y se registra MSG-38: "Campo sensible enmascarado en el registro de auditoría: tag 554 del mensaje A con secuencia {seqNum}."

  Escenario: Enmascaramiento en el Logon de respuesta de A3
    Cuando A3 envía su Logon de respuesta
    Entonces el campo Password queda enmascarado en el log raw

  Escenario: Enmascaramiento en trazas y mensajes de error
    Dado que A3 rechaza las credenciales
    Cuando el conector publica el error MSG-02
    Entonces el texto del error no contiene la contraseña utilizada

  Escenario: Detección de credencial sin enmascarar
    Dado que por un defecto la contraseña aparece en un registro
    Cuando un proceso de auditoría revisa los registros
    Entonces se clasifica como defecto bloqueante de seguridad
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Credencial sin enmascarar en cualquier registro | Defecto bloqueante de seguridad |
| Fallo del mecanismo de enmascaramiento | No se registra el mensaje (preferible no registrar a registrar sin enmascarar) |

---

### FIX-2.23 — Exponer un healthcheck del conector

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E2 |
| **Trazabilidad input** | §10 `R-09` · Plan de trabajo: «Monitoreo de sesión» |
| **Habilita** | Operaciones, despliegue corporativo, `FIX-2.08` |
| **Prioridad sugerida** | Should |
| **Estimación del input** | Sin estimar |

#### Objetivo técnico

Exponer un mecanismo de healthcheck que permita al orquestador de contenedores, a los procesos de despliegue corporativos del cliente y al equipo de operaciones verificar que el conector está operativo. Es un requisito habitual de los procesos de despliegue corporativos.

#### Criterios de aceptación

1. **[Feliz]** El conector expone un endpoint HTTP (o mecanismo equivalente definido por arquitectura del cliente) que responde con el estado agregado del conector.
2. **[Feliz]** El healthcheck informa: estado de la sesión FIX (Conectada / Desconectada / Cerrada), estado de la conexión a MQ (Activa / No disponible), *timestamp* del último mensaje recibido de A3, *timestamp* del último mensaje enviado, `MsgSeqNum` entrante y saliente actuales, y tiempo de actividad del proceso.
3. **[Feliz]** La respuesta incluye MSG-34: "Healthcheck: sesión {estadoSesión}, MQ {estadoMQ}, último mensaje A3 hace {segs}s, secuencia entrante {seqIn}, saliente {seqOut}."
4. **[Feliz]** El healthcheck responde `HTTP 200` (o equivalente) cuando todos los componentes están operativos, y `HTTP 503` (o equivalente) cuando algún componente crítico no está disponible.
5. **[Alternativo]** Si un componente no está disponible, la respuesta incluye MSG-35: "Healthcheck degradado: {componente} no disponible. Detalle: {motivo}."
6. **[Validación]** El healthcheck **no expone credenciales ni datos sensibles**, conforme a RN-06.
7. **[Validación]** El endpoint es accesible sin autenticación FIX (es un mecanismo del conector, no del protocolo).
8. **[Validación]** Fuera de la ventana de sesión (19:00–09:30), el healthcheck responde `HTTP 200` con estado de sesión "Fuera de ventana" y no reporta la desconexión como degradación.

#### Escenarios BDD

```gherkin
Característica: Healthcheck del conector FIX
  Escenario: Healthcheck con todos los componentes operativos
    Dado que la sesión FIX está "Conectada" y la conexión MQ está activa
    Cuando se consulta el healthcheck
    Entonces responde con estado 200
    Y reporta MSG-34: "Healthcheck: sesión Conectada, MQ Activa, último mensaje A3 hace {segs}s, secuencia entrante {seqIn}, saliente {seqOut}."

  Escenario: Healthcheck con sesión caída
    Dado que la sesión FIX está "Desconectada" por un fallo
    Cuando se consulta el healthcheck
    Entonces responde con estado 503
    Y reporta MSG-35: "Healthcheck degradado: sesión FIX no disponible. Detalle: Desconexión sin Logout."

  Escenario: Healthcheck fuera de la ventana operativa
    Dado que son las 21:00
    Cuando se consulta el healthcheck
    Entonces responde con estado 200
    Y reporta el estado de la sesión como "Fuera de ventana"
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| El propio healthcheck no responde | El orquestador lo detecta y reinicia el contenedor según su política |

---

### FIX-2.24 — Externalizar la configuración del conector por ambiente

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E1 / E2 |
| **Trazabilidad input** | §10 `R-10` |
| **Habilita** | Todas las historias que usan parámetros configurables |
| **Prioridad sugerida** | Should |
| **Estimación del input** | Sin estimar |

#### Objetivo técnico

Garantizar que todos los parámetros del conector sean configurables por ambiente sin recompilación, para que promover entre reMarkets, ambiente intive, ambiente del cliente y producción no exija recompilar, lo que rompería la trazabilidad del artefacto certificado por A3.

#### Criterios de aceptación

1. **[Feliz]** Todos los parámetros operativos se externalizan en un archivo de configuración, variables de entorno o mecanismo equivalente aprobado por arquitectura del cliente: gateway FIX (*host*, puerto), `SenderCompID`, `TargetCompID`, `OnBehalfOfCompID`, `DeliverToCompID`, `HeartBtInt`, endpoint de la API de credenciales, colas MQ (nombres, *connection factory*), ventana de sesión (inicio, fin), ventana de negociación (inicio, fin), umbrales de alerta, timeouts de conexión y de espera de Logout, y reintentos.
2. **[Feliz]** Al arrancar, el conector valida la configuración y registra MSG-36: "Configuración cargada para el ambiente {ambiente}: gateway {host}:{puerto}, SenderCompID {sender}, colas MQ {colas}."
3. **[Feliz]** Si un parámetro obligatorio falta o tiene un valor inválido, el conector **no arranca** y registra MSG-37: "Configuración inválida: el parámetro {parametro} tiene el valor {valor}, que no cumple la restricción {restriccion}. El conector no arranca."
4. **[Feliz]** La configuración se puede sobreescribir por variable de entorno para facilitar la gestión de contenedores.
5. **[Validación]** Las credenciales **no** se externalizan en la configuración: se obtienen de la API del banco conforme a RN-06.
6. **[Validación]** El mismo artefacto compilado funciona en todos los ambientes sin modificación.
7. **[Validación]** Un cambio de configuración no requiere re-certificación con A3 (sólo un cambio de código la requiere).

#### Escenarios BDD

```gherkin
Característica: Configuración externalizada por ambiente
  Escenario: Arranque con configuración válida
    Dado que el archivo de configuración del ambiente "reMarkets" tiene todos los parámetros obligatorios
    Cuando el conector arranca
    Entonces carga la configuración
    Y registra MSG-36: "Configuración cargada para el ambiente reMarkets: gateway fix.remarkets.primary.com.ar:9876, SenderCompID CLI-FIX, colas MQ {colas}."

  Escenario: Arranque con configuración inválida
    Dado que el parámetro "HeartBtInt" tiene el valor 5
    Cuando el conector intenta arrancar
    Entonces no arranca
    Y registra MSG-37: "Configuración inválida: el parámetro HeartBtInt tiene el valor 5, que no cumple la restricción >= 10 (RN-10). El conector no arranca."

  Escenario: Mismo artefacto en distintos ambientes
    Dado que el artefacto compilado es el mismo
    Cuando se despliega con la configuración del ambiente "producción"
    Entonces usa el gateway fixgw.ptp.primary.com.ar:9876
    Y no requiere recompilación
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Archivo de configuración no encontrado | El conector no arranca; alerta |
| Parámetro obligatorio faltante | MSG-37; el conector no arranca |
| Valor fuera de rango | MSG-37 con detalle de la restricción; el conector no arranca |

---

### FIX-2.25 — Diseñar el contrato MQ con bloque de instrumento opcional y versionado

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | E1 / E2 |
| **Trazabilidad input** | §10 `R-13` · `S-04` (enriquecimiento de instrumento, sin definir) · OBJ-3 del PRD (estabilidad del contrato MQ) |
| **Habilita** | `FIX-2.04`, `FIX-2.05`, `T-03`, y toda evolución futura del contrato MQ |
| **Prioridad sugerida** | Must — **es una decisión de diseño que cuesta poco ahora y mucho después** |
| **Estimación del input** | Sin estimar |
| **Depende de** | `T-03` (definición de contratos MQ) |

#### Objetivo técnico

Diseñar el contrato de los eventos publicados en MQ de forma que incluya un **bloque de instrumento opcional y versionado**, para que incorporar el enriquecimiento con `SecurityList` más adelante sea una extensión aditiva del contrato y no un cambio que rompa a los consumidores. El spike `S-04` —si la normalización necesita más que el `Symbol`— quedó sin definir. Sin esta previsión, definirlo más tarde obliga a versionar el contrato en plena Épica 3, que es lo que OBJ-3 del PRD busca evitar.

#### Criterios de aceptación

1. **[Feliz]** El contrato de los eventos de Execution Report y Trade Capture Report incluye un bloque `instrument` con la estructura: `{ "version": 1, "symbol": "...", "securityExchange": "ROFX" }`.
2. **[Feliz]** El bloque `instrument` se diseña con campos opcionales que pueden agregarse en versiones futuras sin romper el contrato: `currency`, `cfiCode`, `maturityDate`, `contractMultiplier`, `securityType`, `marketSegmentId`.
3. **[Feliz]** Los consumidores existentes que sólo leen `symbol` no se ven afectados cuando se agrega un campo nuevo al bloque `instrument`.
4. **[Feliz]** La versión del bloque se incrementa sólo cuando se agrega un campo nuevo, no cuando se cambia el valor de un campo existente.
5. **[Validación]** En la Fase 1, el bloque `instrument` contiene sólo `version`, `symbol` y `securityExchange`. Los campos opcionales quedan vacíos o ausentes.
6. **[Validación]** El diseño se documenta en `T-03` como parte del contrato MQ y se aprueba por arquitectura del cliente.

#### Escenarios BDD

```gherkin
Característica: Contrato MQ con bloque de instrumento versionado
  Escenario: Evento publicado en la Fase 1 con bloque mínimo
    Cuando el conector publica un evento de Execution Report
    Entonces el evento incluye el bloque instrument con version 1, symbol "DLR/DIC26" y securityExchange "ROFX"
    Y no incluye campos opcionales

  Escenario: Extensión futura con enriquecimiento de SecurityList
    Dado que en una fase futura se incorpora la consulta SecurityList
    Cuando el conector publica un evento enriquecido
    Entonces el bloque instrument tiene version 2 y agrega currency "ARS" y maturityDate "2026-12-15"
    Y los consumidores que sólo leen symbol siguen funcionando sin cambios

  Escenario: Consumidor que ignora campos desconocidos
    Dado que un consumidor implementado en la Fase 1 lee sólo symbol del bloque instrument
    Cuando recibe un evento con version 2 que incluye campos adicionales
    Entonces los campos desconocidos se ignoran sin error
```

#### Condiciones de error

| Condición | Comportamiento esperado |
|---|---|
| Consumidor rompe al recibir campos nuevos | Defecto del consumidor, no del contrato: el diseño prevé compatibilidad hacia atrás |

#### Notas / preguntas abiertas

- **Resuelve `S-04` de forma pragmática**: en lugar de decidir ahora si se necesita enriquecimiento, se diseña el contrato para que la decisión se pueda tomar más tarde sin costo de retrabajo.

---

## 8. Tareas técnicas / habilitadores

> Incluye la **totalidad de las Épicas 1 y 3**, que como se explicó en §6 no producen software sino decisiones, habilitación y validación. Cada tarea lleva Definition of Done concreta y verificable.

### 8.1 Épica 1 — Discovery, Arquitectura y Ambientes

| ID | Key Excel | Tarea | Objetivo | Definition of Done |
|----|-----------|-------|----------|--------------------|
| **T-01** | US 20 | Configuración del ambiente intive | Disponer del ambiente de desarrollo y prueba propio: WebSphere Liberty y colas MQ | El conector arranca en el ambiente, la conexión FIX contra reMarkets se establece y las colas MQ están accesibles. Estimación del input: **8–13 SP** |
| **T-02** | US 21 | Soporte a la configuración del ambiente del cliente | Acompañar al cliente en la preparación de su ambiente (Liberty, MQ, red hacia A3) | El ambiente del cliente está operativo y validado con una conexión de prueba. **Ejecuta el cliente**; el equipo asigna capacidad de soporte. Estimación del input: **13–21 SP** |
| **T-03** | — | Definición de los contratos de mensajería MQ | Acordar el contrato de **salida** que el conector publica: estados de orden, operaciones concertadas, estado de sesión, estado de mercado y errores. **Sólo salida:** el MVP no consume de MQ (SUP-04). Incluye el formato del `correlation ID`, el catálogo §5 y el **bloque de instrumento opcional y versionado** de `R-13` | Contratos versionados y **aprobados por arquitectura del cliente**. No cambian entre el fin de la Épica 1 y el fin de la Épica 3 |
| **T-04** | — | Estrategia de observabilidad, logging y retención | Definir métricas, alertas, canal de alertado, formato de log y política de retención de la auditoría | Documento aprobado; herramientas identificadas; comportamiento ante indisponibilidad de la auditoría decidido |
| **T-05** | — | **Alta de la sesión Drop Copy y mapeo de cuentas con A3** | Solicitar a A3 el usuario FIX con **perfil Drop Copy de sólo lectura** y acordar el conjunto de IDs de cuentas y de operadores del cliente que quedarán asociados a la sesión, para reMarkets y para producción. Incluye coordenadas, CompIDs y credenciales | Usuario Drop Copy creado, mapeo de cuentas confirmado por A3, cuenta de reMarkets creada en `remarkets.primary.ventures` y **conexión de prueba con recepción efectiva de un Execution Report duplicado**. ⚠️ Definir con el negocio el conjunto de cuentas es precondición: determina qué eventos verá el conector. **Bloquea `FIX-2.04`** |
| **T-06** | — | **Integración con la API de credenciales del banco** y procedimiento de actualización | Relevar el contrato de la **API del banco que entrega las credenciales de A3** —endpoint, autenticación del conector contra ella, formato de respuesta, códigos de error, política de caché y comportamiento ante indisponibilidad— e implementar su consumo. Documentar además el procedimiento administrativo de actualización de contraseña, que es fuera de banda conforme a `S-02` | Contrato de la API relevado y consumido: el conector obtiene la credencial al abrir sesión y al reanudar tras *hard stop*, la mantiene sólo en memoria y nunca la persiste. Procedimiento documentado con los dos caminos de actualización: en homologación, tramitación manual del cambio; en producción, gestión a cargo del cliente. Incluye el **runbook de salida del *hard stop*** de RN-18: actualizar credencial en el sistema del banco → acción manual de reanudación → el conector la relee de la API. ⚠️ **Dependencia de disponibilidad en el arranque:** definir el comportamiento si la API no responde a las 09:30. Ver `S-17` |
| **T-07** | — | Relevamiento de códigos CNV y estructura de cuentas del cliente | Obtener los valores del bloque `Parties` que exige A3: agente de negociación, Client ID, agente de compensación, *Executing Trader*, *Desk ID* y *Customer Account* | Códigos documentados y validados contra una consulta TCR real en reMarkets. **Bloquea `FIX-2.05`** |
| **T-08** | — | Definición del framework MQ | Decisión del cliente sobre el framework, librería o componente aprobado, compatible con Java 25 y Liberty | Framework definido, disponible en el repositorio corporativo y probado con un mensaje de ida y vuelta |
| **T-09** | — | Arquitectura de referencia y diseño del FIX Engine | Definir la separación entre capacidades comunes FIX, adaptador A3 e integración el cliente; decidir la librería FIX base | Documento de arquitectura aprobado, con las fronteras de extensibilidad hacia otros mercados explicitadas |
| **T-10** | — | Spike de despliegue Java 25 sobre WebSphere Liberty | Verificar la compatibilidad de la versión de Liberty disponible en el cliente con Java 25 | Aplicación mínima desplegada y ejecutándose en el ambiente objetivo. ✅ **Resuelto el 2026-09-16 (`S-12`): el estándar es IBM WebSphere Liberty**, no Open Liberty. La anotación «Open-Liberty» del Excel queda descartada; corregir `T-01` en consecuencia |
| **T-11** | US 24 (parcial) | Definición de escenarios y casos principales de prueba | Elaborar el catálogo de casos de prueba del MVP, incluyendo escenarios de error y de recuperación | Catálogo revisado con QA y con el cliente, alineado a los criterios de evaluación de A3 |
| **T-12** | — | Backlog refinado, priorización del MVP y plan de releases | Dejar el backlog de la Épica 2 listo para ejecutar | Historias de E2 refinadas, estimadas y priorizadas; plan de releases acordado; spikes bloqueantes resueltos |
| **T-13** | — | Pipeline CI/CD | Construcción y despliegue automatizados en el ambiente intive | El pipeline construye, prueba y despliega de forma reproducible desde la rama principal |

### 8.2 Épica 3 — Homologación A3 y Pruebas de Aceptación del cliente

| ID | Key Excel | Tarea | Objetivo | Definition of Done |
|----|-----------|-------|----------|--------------------|
| **T-14** | US 23 | Gestión del proceso de certificación con A3 | Obtener el paquete de certificación y **formalizar por escrito el alcance parcial ya aceptado** | ✅ **A3 confirmó que acepta la homologación parcial limitada a la integración de TCR y ER, sin envío de órdenes ni market data** (`S-15`, 2026-09-16). Queda por obtener el paquete de certificación, identificar los casos de prueba requeridos y **dejar el acuerdo asentado por escrito**. Estimación del input: **13–21 SP** · Observación del Excel: «Contactar a A3 para validar homologación requerida» |
| **T-15** | US 22 | Prueba de despliegue en el ambiente del cliente | Desplegar el entregable parcial en el ambiente del cliente e integrarlo con el ambiente de pruebas de A3 | Conector desplegado y con sesión FIX establecida desde el ambiente del cliente. Estimación del input: **13–21 SP** |
| **T-16** | US 25 | Pruebas de recuperación, duplicados y colas | Validar los escenarios de riesgo del MVP | Se simulan caídas de sesión, se validan los *resend requests*, se validan los duplicados por FIX y por *redelivery* de MQ, y se validan las recuperaciones. **Cero eventos perdidos y cero duplicados publicados.** Estimación del input: **8–21 SP** |
| **T-17** | US 24 (parcial) | Ejecución de la homologación con A3 | Ejecutar los casos de certificación sobre el alcance acordado | Se validan las sesiones, el manejo de errores y la estabilidad. Evidencias documentadas y entregadas a A3 |
| **T-18** | — | Pruebas de aceptación del cliente | Ejecutar la validación funcional del MVP en el ambiente intive | Casos ejecutados por el cliente, evidencias registradas y **conformidad funcional firmada**. Observación del Excel: «definir prueba de aceptación del producto (DoD)» → `S-13` |
| **T-19** | — | Corrección de defectos de homologación y de aceptación | Cerrar los hallazgos de ambas instancias | Cero defectos bloqueantes abiertos; defectos no bloqueantes con ticket y prioridad |
| **T-20** | — | Definición del ambiente de certificación | Determinar si la certificación se ejecuta sobre el ambiente intive de desarrollo o sobre uno separado | Ambiente definido y disponible. Observación del Excel: «se define un ambiente de certificación separado del de intive que es el de desarrollo» → `S-14` |

---

> Continuación del §8 del documento maestro.

---

### T-21 — Documentar el runbook operativo del conector

| | |
|---|---|
| **Tipo** | TAREA |
| **Épica** | E3 — Homologación A3 y Pruebas de Aceptación del cliente |
| **Trazabilidad input** | §10 `R-11` |
| **Prioridad sugerida** | Should |
| **Depende de** | `FIX-2.01` a `FIX-2.25`, `T-06` |

#### Objetivo

Documentar los procedimientos operativos para los escenarios de contingencia que la Fase 1 entrega. Sin *runbook*, cada incidente escala al equipo de desarrollo.

#### Definition of Done

- [ ] Procedimiento documentado para **hard stop por credenciales rechazadas** (RN-18): actualizar credencial → acción manual de reanudación → verificar sesión.
- [ ] Procedimiento documentado para **gap de secuencia no recuperado** (MSG-08): diagnóstico, intervención manual, re-reconciliación.
- [ ] Procedimiento documentado para **fallo de publicación en MQ** (MSG-13): verificar cola, drenar cola de error, reenviar eventos.
- [ ] Procedimiento documentado para **desconexión fuera de ventana**: verificar si fue cierre normal o fallo.
- [ ] Procedimiento documentado para **apertura fallida de jornada** (API de credenciales no responde, A3 rechaza Logon): escalamiento, alternativas.
- [ ] Contactos de escalamiento definidos para incidentes con A3 Mercados y con la API de credenciales del banco.
- [ ] Revisado y aprobado por el equipo de operaciones y soporte del cliente.

---

### T-22 — Planificar la re-homologación anual con A3

| | |
|---|---|
| **Tipo** | TAREA |
| **Épica** | E3 |
| **Trazabilidad input** | §10 `R-12` |
| **Prioridad sugerida** | Could — decidirlo ahora evita una sorpresa de calendario |

#### Objetivo

La certificación de A3 tiene **vigencia de un año**. Homologar en noviembre o diciembre de 2026 obliga a re-homologar en el mismo período de 2027, y a convivir con vencimientos escalonados si las Épicas 4 y 5 se certifican después. Anticipar la planificación evita que la re-homologación compita con los releases de funcionalidad.

#### Definition of Done

- [ ] Fecha de vencimiento de la certificación de la Fase 1 registrada en el calendario del proyecto.
- [ ] Proceso de re-homologación documentado: qué casos de prueba hay que re-ejecutar, qué evidencia hay que generar, qué contacto en A3 gestiona la renovación.
- [ ] Decisión tomada sobre si conviene alinear la re-homologación de la Fase 1 con la certificación de las Épicas 4 y 5 para unificar el ciclo.
- [ ] Presupuesto de esfuerzo estimado para la re-homologación (debe ser significativamente menor que la primera certificación, dado que los casos ya están diseñados).

---

## 9. Spikes y decisiones pendientes

Consolida la columna `Obs` del Excel, las contradicciones detectadas entre documentos y los vacíos identificados en el análisis del ROE y del Manual de Conectividad de A3.

| ID | Origen | Pregunta abierta | Impacto si no se resuelve | Propuesta del PO | Respuesta *(post HITL)* |
|----|--------|------------------|---------------------------|------------------|-------------------------|
| **S-01** | Análisis del PO | **¿De dónde provienen los Execution Reports si el conector no rutea órdenes?** | Sin tráfico de ER no hay nada que procesar ni que homologar en el corazón del MVP. **Bloquea `FIX-2.04`** | Combinar tres fuentes: solicitar a A3 un **usuario de drop copy** (está en el Manual de Conectividad y entrega órdenes y ejecuciones de forma independiente al ruteo); usar `Order Mass Status Request` como mecanismo de *pull*; y generar el tráfico de prueba cargando órdenes a mano desde eTrader en reMarkets. Confirmar el drop copy con A3 en la primera semana | ✅ **Resuelto (2026-09-16).** La modalidad es **FIX Drop Copy**. A3 configura la sesión del conector con un **perfil de sólo lectura** asociado a determinados IDs de cuentas o de operadores, y el motor de negociación **duplica en tiempo real** hacia esa sesión cada Execution Report de las órdenes que se operan, cancelan o modifican en esas cuentas. El conector es un **oyente pasivo**: los reportes salen de la actividad real o simulada de las cuentas del broker. **En homologación** el tráfico se genera por inyección de órdenes de un tercero sobre **cuentas espejo** mapeadas a la sesión FIX. **En producción** el flujo es el espejo de la actividad de la ALyC: las órdenes las ingresan operadores o clientes desde terminales de sistemas propios o plataformas DMA de terceros. → Impacta RN-17, `FIX-2.04` y `T-05` |
| **S-02** | ROE A3 vs. propuesta técnica | **¿Cuál es el mecanismo real de cambio de contraseña en A3?** El `Logon` sólo define `Username` (553) y `Password` (554); no existe el tag `NewPassword` (925) ni ningún mensaje de cambio de credenciales en la lista de mensajes soportados del ROE v2.0.53 | La estrategia de rotación diaria de la propuesta técnica no es implementable tal como está redactada. **Bloquea `T-06`** y puede afectar la homologación | Consultar formalmente a A3 en la primera semana. Si no existe mecanismo por FIX, acordar con seguridad del cliente una rotación gestionada fuera de banda y simplificar el secret a un único campo con la contraseña vigente | ✅ **Resuelto (2026-09-16).** Confirmado: **no existe mecanismo FIX de cambio de contraseña** en los ROE de A3. La gestión es **puramente administrativa y fuera de banda**: en homologación las contraseñas se tratarán manualmente; en producción las gestiona el cliente. **El conector no debe intentar cambiarlas de forma programática.** Comportamiento a implementar: ante el `Logout` (`35=5`) con que A3 responde a un `Logon` fallido, leer el campo `Text` (58) —donde A3 envía cadenas como `"Invalid username or password"`, `"Password expired"` o `"User locked"`— y aplicar **hard stop**: cortar todo reintento automático para no bloquear el usuario, y disparar alerta crítica. La resolución requiere que un administrador actualice la clave manualmente y la cargue en el secret. → Impacta RN-18, `FIX-2.01`, `FIX-5.03` y `T-06` |
| **S-03** | ROE A3 | **¿Cómo se manejan los números de secuencia entre jornadas?** ¿Se reinician a 1 al abrir la sesión diaria o continúan? `ResetSeqNumFlag` (141) no está documentado en el ROE | Afecta el diseño de la persistencia y de la detección de gaps. **Impacta `FIX-2.09` y `FIX-2.10`** | Consultar a A3 junto con S-02. Mientras tanto, diseñar la persistencia con ambos comportamientos configurables, conforme a SUP-14, para no quedar bloqueados por la respuesta | ✅ **Resuelto (2026-09-16): reinicio DIARIO.** Los números de secuencia se reinician al abrir la sesión de cada jornada. → La persistencia de `FIX-2.09` pasa a tener alcance **intra-jornada**: sirve para sobrevivir a un reinicio del proceso dentro del día, no para dar continuidad entre días. La detección de gaps, el `Resend Request` y la ventana de deduplicación quedan acotados a la jornada. Nueva regla **RN-19**; SUP-14 queda superado |
| **S-04** | Análisis del PO | **¿La normalización de ER y TCR requiere enriquecer con datos del instrumento?** Ambos mensajes traen `Symbol` como string | Si la respuesta es sí, hay que **adelantar `FIX-5.05` (SecurityList) al MVP**. Es sólo lectura, así que no rompe el corte, pero agrega alcance | Definirlo al cerrar los contratos MQ en `T-03`. Recomendación: si los consumidores del cliente necesitan más que el símbolo (moneda, tipo, vencimiento, segmento), adelantar `SecurityList` con carga diaria en memoria | ⏳ **Sin definir (2026-09-16): «no sabemos».** Es una incógnita legítima en esta etapa, pero **no puede quedar abierta hasta la implementación**, porque afecta el contrato MQ, que según OBJ-3 del PRD no debe cambiar entre el fin de la Épica 1 y el fin de la Épica 3. **Propuesta del PO para no quedar bloqueados:** diseñar el evento normalizado con un **bloque de instrumento opcional y versionado**, de modo que incorporar el enriquecimiento con `SecurityList` más adelante sea una **extensión aditiva** del contrato y no un cambio que rompa a los consumidores. Con esa previsión, la decisión se puede postergar sin costo de retrabajo hasta tener los consumidores identificados. Ver `R-13` |
| **S-05** | ROE A3 | **¿Se puede suscribir a Trade Capture Reports en lugar de consultarlos?** El ROE documenta `SubscriptionRequestType` (263) sólo para la variante de *allocations y giveups*, que está fuera de alcance | Define si el flujo de TCR es *pull* periódico o *push*. Cambia el diseño de `FIX-2.05` | Consultar a A3. Asumir *pull* periódico como diseño base, que es lo que el ROE documenta para operaciones regulares | ✅ **Resuelto (2026-09-16): sólo consulta.** No hay suscripción a Trade Capture Reports. El flujo es exclusivamente *pull*, como documenta el ROE para operaciones regulares. → Queda descartado todo diseño de `FIX-2.05` basado en recepción no solicitada de TCR |
| **S-06** | Análisis del PO | **¿Con qué criterio y periodicidad se consultan las operaciones concertadas?** ¿Por cuenta al cierre de jornada, por símbolo bajo demanda, ambas? ¿La reconciliación de `FIX-2.07` alcanza también a las operaciones o sólo a las órdenes? | Sin esto, `FIX-2.05` no tiene definido su disparador | Definir con los referentes de negocio del cliente en la Épica 1. Propuesta base: consulta por cuenta al cierre de jornada más consulta bajo demanda por símbolo | ✅ **Resuelto (2026-09-16): consulta asincrónica a demanda**, sin periodicidad fija. Se descarta la propuesta de consulta programada al cierre de jornada. → En `FIX-2.05` el criterio de disparo deja de ser temporal y pasa a ser **por demanda**; el conector no planifica consultas por horario. Queda por cerrar **quién origina esa demanda**, que es `S-07` |
| **S-07** | SUP-04 | **¿Quién dispara las consultas en la Fase 1?** Con el MVP puramente saliente, no hay cola de entrada | Define si hace falta implementar el consumo MQ en el MVP | Recomendación: el conector dispara sus consultas según su propia planificación configurable. El sentido de entrada se abre recién en la Épica 4, conforme a SUP-04 | ✅ **Resuelto (2026-09-18): las dispara el propio conector, sin cola de entrada.** La opción intermedia de que el cliente las dispare enviando comandos por MQ —evaluada el 16-09— quedó **desestimada del MVP** y se difiere a la Épica 4, donde se analizará junto con el resto del sentido de entrada. **SUP-04 sigue vigente:** el flujo del MVP es A3 → conector → MQ del cliente, en un solo sentido |
| **S-08** | Manual de Conectividad A3 | **¿La operatoria del conector califica como acceso DMA según A3?** | Si califica, la Épica 4 exige un sistema homologado de control de riesgo *pre-trade* (`FIX-4.07`), que puede ser un proyecto en sí mismo | Aclararlo con A3 y con cumplimiento del cliente **durante la Épica 1**, aunque el impacto sea en la Épica 4. Conocerlo temprano cambia la planificación del año | ⏳ **Pendiente (2026-09-16).** El PO mantiene la propuesta y la deja a confirmar con el equipo técnico o con el negocio durante la Épica 1. Registrado como nota en las historias afectadas |
| **S-09** | Manual de Conectividad A3 | **¿Qué gateway de market data necesita el cliente?** FIX-PTP entrega Full Refresh con profundidad 10 cada 500 ms; FIX-PTP-HR llega a 50 ms; FIX-PTP-LL da *incremental refresh* pero **sólo vía colocation** | Aunque Market Data es Épica 5, la elección condiciona la conectividad contratada y posiblemente la certificación | Definirlo en la Épica 1 aunque se implemente en la 5. Si alcanza con FIX-PTP, no hay decisión de infraestructura pendiente | ⏳ **Pendiente (2026-09-16).** El PO mantiene la propuesta y la deja a confirmar con el equipo técnico o con el negocio durante la Épica 1. Registrado como nota en las historias afectadas |
| **S-10** | Excel, `Obs` de US 4 | **¿Dónde se persisten las secuencias?** El Excel pregunta «Validar con el cliente dónde se persiste (storage?)» y anota «se utiliza file storage» | Define si se necesita Sybase en el MVP o alcanza con archivos | Recomendación: archivos sobre volumen persistente, que es el patrón estándar de los motores FIX (SUP-05). Sybase con *Stored Procedures* por cada mensaje puede afectar el caudal. Confirmar con arquitectura | ✅ **Resuelto (2026-09-16): por archivos, deliberadamente para no impactar la base de datos.** → **Sybase queda fuera del alcance del MVP.** Desaparecen la dependencia de Stored Procedures para el flujo de sesión, el riesgo de caudal asociado y una dependencia de equipo del cliente |
| **S-11** | Excel, `Obs` de US 7 | **«¿Lo vamos a recibir en la cola o en una API?»** — cómo llegan las instrucciones de orden desde el cliente | Impacta `FIX-4.01` (Épica 4), no el MVP | La propuesta técnica define **colas MQ** como mecanismo de comunicación con los sistemas internos. Mantener MQ salvo definición contraria de arquitectura del cliente | ⏳ **Pendiente (2026-09-16).** El PO mantiene la propuesta y la deja a confirmar con el equipo técnico o con el negocio durante la Épica 1. Registrado como nota en las historias afectadas |
| **S-12** | Excel vs. propuesta técnica | **¿Open Liberty o IBM WebSphere Application Server Liberty?** El Excel anota «Open-Liberty, MQ revisar MQ dev!» y la propuesta técnica especifica «IBM WebSphere Application Server Liberty». **Son productos distintos** | Afecta licenciamiento, soporte, configuración y el spike de compatibilidad con Java 25. **Impacta `T-01` y `T-10`** | Confirmar con arquitectura del cliente cuál es el estándar corporativo. La propuesta técnica, que es el documento contractual, dice WebSphere Liberty | ✅ **Resuelto (2026-09-16): IBM WebSphere Liberty.** La anotación «Open-Liberty» del Excel queda descartada. → Impacta `T-01` y `T-10` |
| **S-13** | Excel, `Obs` de épica 12 | **«Definir prueba de aceptación del producto (DoD)»** — cuál es el criterio de aceptación formal del cliente | Sin esto, la Épica 3 no tiene criterio de cierre objetivo | Usar como base los criterios de aceptación de fase del PRD §14 y acordarlos con el cliente en la Épica 1, junto con `T-11` | ⏳ **Pendiente (2026-09-16).** El PO mantiene la propuesta y la deja a confirmar con el equipo técnico o con el negocio durante la Épica 1. Registrado como nota en las historias afectadas |
| **S-14** | Excel, `Obs` de US 23 | **¿La certificación se ejecuta sobre un ambiente separado del de desarrollo?** El Excel anota «se define un ambiente de certificación separado del de intive que es el de desarrollo» | Puede agregar un ambiente no contemplado en la estimación | Confirmar con A3 y con el cliente. Si se requiere, agregarlo a `T-01` y re-estimar | ⏳ **Pendiente (2026-09-16).** El PO mantiene la propuesta y la deja a confirmar con el equipo técnico o con el negocio durante la Épica 1. Registrado como nota en las historias afectadas |
| **S-15** | Análisis del PO | **¿A3 acepta homologar un alcance parcial sin envío de órdenes ni market data?** Sus criterios de evaluación incluyen explícitamente ambos | **Es el riesgo número uno del compromiso del 31-dic.** Si A3 exige el conjunto completo, la fecha no se sostiene con este alcance | Iniciar el contacto en el **sprint 0** y obtener el acuerdo por escrito (`T-14`). Si A3 no lo acepta, escalar de inmediato: la decisión de alcance y fecha vuelve al comité | ✅ **Resuelto (2026-09-16): A3 acepta la homologación parcial**, limitada a la integración de TCR y ER, sin envío de órdenes ni market data. **Queda despejado el riesgo número uno del compromiso del 31-dic.** Resta formalizar el acuerdo por escrito y obtener el paquete de certificación en `T-14` |

| **S-17** | Respuesta del PO del 2026-09-16 | **¿Cuál es el contrato de la API del banco que entrega las credenciales de A3?** Endpoint, método de autenticación del conector contra esa API, formato de respuesta, códigos de error y política de caché | **Bloquea `FIX-2.01`**: sin credenciales no hay sesión. Además introduce una **dependencia de disponibilidad en el arranque**: si la API no responde a las 09:30, el conector no abre sesión y la jornada arranca ciega | Relevar el contrato con el equipo dueño de la API en la Épica 1 (`T-06`). Propuesta de diseño: el conector consulta la API **al abrir la sesión de cada jornada y al reanudar tras un *hard stop***, de modo que una rotación de contraseña se propague sin redesplegar; mantiene la credencial sólo en memoria durante la jornada, nunca en disco ni en logs; y ante indisponibilidad de la API aplica reintento acotado y luego alerta, sin degradar a credenciales almacenadas localmente | ✅ **Resuelto parcialmente (2026-09-16): ante indisponibilidad de la API, reintento acotado y alerta crítica, sin abrir sesión y sin degradar a credenciales almacenadas localmente.** Queda pendiente relevar el contrato concreto —endpoint, autenticación, formato de respuesta y códigos de error— en `T-06` |
| **S-16** | Derivado de `S-01` | **¿El perfil Drop Copy de sólo lectura admite emitir `Order Status Request`, `Order Mass Status Request` y `Trade Capture Report Request`?** La confirmación de `S-01` establece que la sesión es de sólo lectura y recibe eventos duplicados, pero no aclara si además habilita consultas salientes | Si A3 **no** las admite sobre Drop Copy, hay que rediseñar `FIX-2.06`, `FIX-2.05` y la reconciliación de `FIX-2.07` sobre el flujo de eventos duplicados exclusivamente. Cambia el alcance de tres historias del MVP | Consultar a A3 junto con la solicitud del usuario Drop Copy en `T-05`. Es una pregunta de una línea que se responde en la misma gestión. Diseño de contingencia: si sólo hay recepción pasiva, la reconciliación se apoya en la persistencia local del último estado conocido por cuenta más el registro de auditoría | ⏳ **Pendiente (2026-09-16).** Detectado al incorporar la respuesta de `S-01`. A confirmar con A3 en la Épica 1 |

> **Pausa obligatoria (skill):** ejecutada el 2026-09-16. Se resolvieron `S-01`, `S-02`, `S-12` y `S-15`; los once restantes quedaron como pendientes a confirmar con el equipo técnico o el negocio, registrados como notas en las historias afectadas. La resolución de `S-01` hizo emerger un nuevo spike, `S-16`.

### 9.1 Impacto de las decisiones tomadas

Las cuatro respuestas no sólo cerraron spikes: **cambiaron el diseño**. Se deja registro de qué se modificó:

| Decisión | Qué cambió |
|---|---|
| **`S-15` — A3 acepta homologación parcial de TCR/ER** | Queda despejado el riesgo principal del compromiso del 31-dic. `T-14` deja de ser una negociación de resultado incierto y pasa a ser una formalización. El corte del MVP definido en el PRD queda **validado por el propio mercado** |
| **`S-01` — Modalidad FIX Drop Copy** | Nueva regla **RN-17**. `FIX-2.04` suma tres criterios: procesar Execution Reports **no solicitados**, tratar el `ClOrdID` como **dato opaco de terceros** y aceptar eventos de órdenes sin historia previa como caso normal, no como error. `T-05` se reformula de «gestión de accesos» a **«alta de la sesión Drop Copy y mapeo de cuentas»**, y pasa a bloquear `FIX-2.04`. Aparece `S-16` |
| **`S-02` — Gestión de contraseñas fuera de banda** | Nueva regla **RN-18** (*hard stop*). `FIX-2.01` suma tres criterios de error y dos escenarios BDD. Nuevo código **MSG-23**. `T-06` incorpora el *runbook* de salida del *hard stop*. `FIX-5.03` queda subordinada a RN-18: ninguna política de reconexión puede pasar por encima del *hard stop* |
| **`S-12` — IBM WebSphere Liberty** | Se descarta la anotación «Open-Liberty» del Excel. `T-01` y `T-10` quedan sin ambigüedad |

**Segunda ronda de definiciones — 2026-09-16 (tarde):**

| Decisión | Qué cambió |
|---|---|
| **Credenciales por API del banco** | **RN-06 reescrita**: el conector ya no lee un secret, sino que **obtiene las credenciales de una API del banco** al abrir sesión y al reanudar tras *hard stop*, y las mantiene sólo en memoria. `T-06` se reformula de «esquema del secret» a **«integración con la API de credenciales»**. **MSG-19** reescrito. Aparece `S-17` y, con él, una **dependencia de disponibilidad en el arranque** que antes no existía: si la API no responde a las 09:30, no hay sesión |
| **`S-03` — Reinicio diario de secuencias** | Nueva regla **RN-19**. **SUP-14 queda superado**: ya no hace falta que el comportamiento sea configurable. `FIX-2.09` pasa a alcance **intra-jornada** y suma un criterio para descartar los valores persistidos de un día anterior. Nuevo código **MSG-25**. La ventana de deduplicación de `FIX-2.13` queda fijada en la jornada |
| **`S-05` y `S-06` — TCR sólo por consulta, asincrónica a demanda** | `FIX-2.05` queda confirmada como flujo exclusivamente *pull*, y su criterio de disparo deja de ser temporal: **no hay consulta programada al cierre de jornada**. Se descarta la propuesta base anterior |
| **`S-07` — «A3»** | ⚠️ Respuesta ambigua. Se aplicó la interpretación de **disparo reactivo a los eventos recibidos**, que preserva SUP-04. **Pendiente de una confirmación de una línea**, porque decide si se construye un planificador, un canal de entrada, o ninguno |
| **`S-10` — Persistencia por archivos** | Confirmado con el motivo explícito de **no impactar la base de datos**. **Sybase sale del alcance del MVP**, y con él una dependencia de equipo y un riesgo de caudal |
| **`S-07` — Disparo de las consultas** | ⚠️ **Definición revisada el 2026-09-18: la cola de entrada queda desestimada del MVP.** La opción de que el cliente dispare las consultas por MQ se difiere a la Épica 4. **SUP-04 vuelve a estar plenamente vigente**: el MVP es puramente saliente. Se eliminaron la historia `FIX-2.15`, la regla RN-20 y los códigos MSG-26 y MSG-27; el componente «Consumidor MQ» vuelve a E4 y `T-03` vuelve a cubrir sólo el contrato de salida |
| **`S-17` — Indisponibilidad de la API de credenciales** | Confirmado: **reintento acotado y alerta crítica, sin abrir sesión y sin degradar a credenciales locales**. Incorporado a RF-02.1 del PRD y a `T-06` |
| **`S-04` — «No sabemos»** | Queda sin definir. Para que la indefinición no bloquee el contrato MQ, se propone `R-13`: **bloque de instrumento opcional y versionado**, de modo que el enriquecimiento futuro sea aditivo |

---

## 10. Recomendaciones del PO — historias faltantes

Todas las historias faltantes identificadas en la v1.0.0 han sido elaboradas como tarjetas completas e incorporadas a las secciones §6, §7 y §8 de este documento. Esta sección queda vacía.

## 11. Observaciones sobre la consistencia del input

Hallazgos del cruce entre el Excel borrador, la propuesta técnica y la documentación de A3. Se listan para que el refinamiento los corrija, no como crítica al trabajo previo: el Excel es una buena base de partida que no tuvo a la vista el ROE de A3.

1. **`US 13 — Procesamiento de TCR` está completamente vacía.** No tiene historia Connextra, ni criterios de aceptación, ni observaciones. Es la **única** fila del backlog en esa condición, y es precisamente la que da nombre al MVP. Elaborada desde cero como `FIX-2.05` a partir del ROE.
2. **`US 13` está clasificada bajo la épica equivocada.** En la hoja *User Stories* figura con `Epic ID = 5` (Market Data A3); en la hoja *Estimation* figura bajo «Procesamiento de Execution Reports», también con ID 5. **TCR es post-trade, no market data**: en el ROE de A3 pertenece al bloque *Post Trade Messages*. Reclasificada a E2.
3. **La numeración de US está desalineada entre hojas.** *User Stories* asigna «Cerrar sesión FIX» a `Epic 1 / US 3`; *US Details* la asigna a `EpicID 2 / US_ID 3`. A partir de ahí los `US_ID` corren una posición entre hojas. Unificar antes de cargar a Jira.
4. **No hay ninguna historia de la Épica 1** salvo las de ambientes. Faltan los entregables comprometidos en el plan de trabajo: definición funcional aprobada, contratos MQ preliminares, mapeo FIX↔MQ, estrategia de observabilidad, estrategia de logging y gestión de contraseñas. Incorporados como `T-03`, `T-04`, `T-06`, `T-09` y `T-12`.
5. **`US 11 — Consultar estado de una orden` está redactada como si hubiera una interfaz de usuario:** «Se muestran estados FIX», «Se exponen timestamps», «Se muestran fills parciales». El conector no tiene UI. La propia observación del Excel lo aclara: «la consulta devuelve el estado de fix, no necesariamente el de la orden (no es un OMS)». Reescrita como `FIX-2.06`; la observación se elevó a **RN-15** porque aplica a todo el conector.
6. **Las épicas de ambientes (9, 10 y 11) suman entre 34 y 63 SP** sobre un total de 118–228 SP: entre el 28% y el 29% del esfuerzo, y **su ejecución depende mayormente del cliente**, no del equipo de desarrollo. Tratadas como `T-01`, `T-02` y `T-15`, con dueño y fecha explícitos.
7. **No se distingue entre recuperabilidad básica y tolerancia a fallas.** Las historias de las épicas 2 y 8 del Excel están todas con `Scope = 1` sin indicación de fase, mientras que el plan de trabajo ubica *Recoverability* en la etapa MVP y *Tolerancia a Fallas* en T0+5. Separadas: `FIX-2.09` a `FIX-2.11` en E2, `FIX-5.03` y `FIX-5.04` en E5.
8. **`US 19 — Recuperación después de reinicio` incluye «Recupera posiciones locales».** El conector no mantiene posiciones ni es un OMS. Criterio eliminado del alcance de `FIX-5.04`, conforme a RN-15.
9. **La hoja *Estimation* tiene las columnas corridas.** Los criterios de aceptación aparecen bajo el encabezado «Activ. Critica», la historia Connextra bajo «Details», y «Phase» contiene el valor 1. No confiar en los encabezados de esa hoja al migrar a Jira.
10. **Contradicción de plataforma: Open Liberty vs. IBM WebSphere Liberty.** El Excel anota «Open-Liberty, MQ revisar MQ dev!» en la épica 9; la propuesta técnica especifica «IBM WebSphere Application Server Liberty». **Son productos distintos**, con distinto licenciamiento, soporte y ciclo de versiones. ✅ Resuelto: **IBM WebSphere Liberty** (`S-12`).
11. **Contradicción de gestión de contraseñas.** La propuesta técnica describe una estrategia de rotación diaria mediante «un mensaje específico de cambio de contraseña» con contraseña actual y nueva. **Ese mensaje no existe en los ROE de A3**: el `Logon` sólo define `Username` (553) y `Password` (554), y no hay tag `NewPassword` (925) ni mensaje de cambio de credenciales en la lista de mensajes soportados. ✅ Resuelto: la gestión es administrativa y fuera de banda (`S-02`), y **el conector obtiene las credenciales desde una API del banco**, no desde un secret (`S-17`).
12. **No hay historias de manejo de errores de protocolo** (`35=3` y `35=j`), pese a que A3 evalúa explícitamente la gestión de errores en la certificación. Incorporadas como `R-01` y `R-02`.
13. **No hay historias de contexto de mercado ni de catálogo de cuentas** (`35=h`, `UALR`/`UALT`/`UALI`), necesarias para interpretar los eventos y para componer las consultas TCR por cuenta. Incorporadas como `R-03` y `R-04`.
14. **El backlog no contempla la ventana operativa diaria de A3** (sesión 09:30–19:00, negociación 10:00–17:30). Incorporada como `R-06` y como RN-07.
15. **La estimación total no cierra con el plan de trabajo.** El mínimo de 118 SP, ajustado a 153 SP por el factor de QA y discovery, contra una velocidad de 15–30 SP por sprint, da entre 5 y 10 sprints. El plan compromete 5 sprints para las épicas 1 a 3. Es consistente **sólo en el extremo optimista**, y además el Excel incluye historias de las épicas 4 y 5. Al recortar al alcance real del MVP la holgura mejora, pero **hay que re-estimar con el backlog refinado**.
16. **La hoja *Roadmap* sólo llega hasta noviembre** (Sp 0 a Sp 6, de septiembre a noviembre) y omite diciembre, que es el mes del compromiso. Extenderla.
17. **`US 12` y `US 13` están estimadas en 3–5 SP cada una**, pero son las dos historias centrales del MVP. `FIX-2.04` debe cubrir las seis variantes de Execution Report del ROE y `FIX-2.05` no tenía criterios cuando se estimó. **Ambas están subestimadas**; re-estimar con las tarjetas elaboradas.
18. **`US 26 — Validación funcional TRD, Renta Fija y Cauciones` no es ejecutable en la Fase 1.** Requiere operatoria real, y además **Cauciones estará disponible en A3 recién a fines de 2026**. Movida a E4/E5.

---

## 12. Matriz de trazabilidad

> **Adaptación declarada:** la plantilla original cruza HU ↔ endpoint ↔ pantalla. El producto no tiene endpoints HTTP ni pantallas, por lo que se cruza **HU ↔ enablers ↔ mensajes FIX ↔ salida MQ**, que es la cadena equivalente en este dominio.

### 12.1 Historias de la Épica 2

| Historia | Enablers que la sostienen | Mensajes FIX involucrados | Salida hacia el cliente | Reglas | US Excel |
|---|---|---|---|---|---:|
| `FIX-2.01` Iniciar sesión | `FIX-2.09`, `FIX-2.12` | `35=A` ↑↓, `35=5` ↓, `35=3` ↓ | Evento de sesión (MSG-01, MSG-02, MSG-19, MSG-23, MSG-24, MSG-25) | RN-06, RN-07, RN-09, RN-10, RN-13, RN-14, RN-18 | 1 |
| `FIX-2.02` Mantener viva la sesión | `FIX-2.12` | `35=0` ↑↓, `35=1` ↑↓ | Alertas (MSG-04, MSG-05) | RN-03, RN-10 | 2 |
| `FIX-2.03` Cerrar sesión | `FIX-2.09`, `FIX-2.11` | `35=5` ↑↓, `35=2` ↓ | Evento de sesión (MSG-03, MSG-04) | RN-07 | 3 |
| `FIX-2.04` Publicar estados de orden | `FIX-2.11`, `FIX-2.12`, `FIX-2.13`, `FIX-2.14` | `35=8` ↓ (seis variantes) | Cola de estados de orden (MSG-11, MSG-12, MSG-13) | RN-01, RN-04, RN-05, RN-11, RN-15, RN-17 | 12 |
| `FIX-2.05` Publicar operaciones concertadas | `FIX-2.12`, `FIX-2.13`, `FIX-2.14` | `35=AD` ↑, `35=AE` ↓, `35=j` ↓ | Cola de operaciones (MSG-17, MSG-21, MSG-22) | RN-02, RN-04, RN-05, RN-08, RN-12 | 13 |
| `FIX-2.06` Consultar estado de órdenes | `FIX-2.14` | `35=H` ↑, `35=AF` ↑, `35=8` ↓ | Cola de estados de orden (MSG-16, MSG-18) | RN-01, RN-08, RN-15 | 11 |
| `FIX-2.07` Reconciliar tras reconectar | `FIX-2.10`, `FIX-2.11`, `FIX-2.13` | `35=AF` ↑, `35=8` ↓ | Eventos de corrección (MSG-14, MSG-15, MSG-16) | RN-05, RN-11 | — |
| `FIX-2.08` Monitorear la sesión | `FIX-2.12`, `FIX-2.14` | — (estado interno) | Métricas y alertas (MSG-04, MSG-05, MSG-08, MSG-13) | RN-06 | 16 |
| `FIX-2.15` Procesar rechazos de sesión | `FIX-2.12`, `FIX-2.21` | `35=3` ↓ | Cola de errores (MSG-09) | RN-03, RN-09 | R-01 |
| `FIX-2.16` Procesar rechazos de negocio | `FIX-2.12`, `FIX-2.14`, `FIX-2.21` | `35=j` ↓ | Cola de errores (MSG-10) | RN-03, RN-04 | R-02 |
| `FIX-2.17` Estado de sesión de negociación | `FIX-2.12`, `FIX-2.14` | `35=h` ↓ | Cola de estado de mercado (MSG-26, MSG-27) | RN-03, RN-04, RN-15 | R-03 |
| `FIX-2.18` Catálogo de cuentas | `FIX-2.12` | `UALT` ↓, `UALI` ↓ | Interno + alertas (MSG-28, MSG-29) | RN-17 | R-04 |
| `FIX-2.20` Ciclo diario | `FIX-2.09`, `FIX-2.12` | `35=A` ↑↓, `35=5` ↑↓ | Eventos de jornada (MSG-31, MSG-32) | RN-07, RN-19 | R-06 |
| `FIX-2.22` Avisos de mercado | `FIX-2.12`, `FIX-2.14` | `35=B` ↓ | Cola de estado de mercado (MSG-33) | RN-03, RN-04, RN-05 | R-08 |


### 12.2 Enablers técnicos

| Enabler | Habilita | Mensajes FIX | US Excel |
|---|---|---|---:|
| `FIX-2.09` Persistir secuencias | `FIX-2.03`, `FIX-2.10`, `FIX-2.11`, `FIX-5.04` | Todos (cabecera) | 4 |
| `FIX-2.10` Detectar gaps | `FIX-2.11`, `FIX-2.07` | Todos (cabecera) | 6 |
| `FIX-2.11` Recuperar mensajes faltantes | `FIX-2.04`, `FIX-2.05`, `FIX-2.07` | `35=2` ↑↓, `35=4` ↓ | 5 |
| `FIX-2.12` Auditoría raw | Todas las HU de E2 · homologación A3 | Todos | 17 |
| `FIX-2.13` Idempotencia | `FIX-2.04`, `FIX-2.05`, `FIX-2.07` | Todos los de negocio | — |
| `FIX-2.14` Correlación de punta a punta | `FIX-2.04`, `FIX-2.05`, `FIX-2.12` | Todos los de negocio | — |
| `FIX-2.19` Control de caudal | `FIX-2.05`, `FIX-2.06`, `FIX-2.07` | RN-08, MSG-30 |
| `FIX-2.21` Enmascaramiento | `FIX-2.12`, `FIX-2.01` | RN-06, MSG-38 |
| `FIX-2.23` Healthcheck | `FIX-2.08`, operaciones | MSG-34, MSG-35 |
| `FIX-2.24` Configuración | Todas | MSG-36, MSG-37 |
| `FIX-2.25` Contrato MQ versionado | `FIX-2.04`, `FIX-2.05`, `T-03` | `S-04` |


### 12.3 Cobertura del catálogo de mensajes

| Código | Historia que lo emite |
|---|---|
| MSG-01, MSG-02, MSG-19, MSG-23, MSG-24 | `FIX-2.01` |
| MSG-03, MSG-04 | `FIX-2.03`, `FIX-2.02`, `FIX-2.08` |
| MSG-05 | `FIX-2.02` |
| MSG-06, MSG-07, MSG-08 | `FIX-2.10`, `FIX-2.11` |
| MSG-09, MSG-10 | `FIX-2.01`, `FIX-2.05`, `R-01`, `R-02` |
| MSG-11, MSG-13 | `FIX-2.04` |
| MSG-12 | `FIX-2.13` |
| MSG-14, MSG-15, MSG-16 | `FIX-2.07`, `FIX-2.06` |
| MSG-17, MSG-21, MSG-22 | `FIX-2.05` |
| MSG-18 | `FIX-2.06` |
| MSG-20, MSG-25 | `FIX-2.01` |

**Sin huérfanos:** los 25 códigos del §5 están referenciados al menos por una historia, y todas las historias de §6 y §7 tienen al menos un código asociado o una justificación de por qué no lo necesitan (`FIX-2.09`, `FIX-2.12` y `FIX-2.14` operan por debajo del nivel de evento publicado).
| MSG-26, MSG-27 | `FIX-2.17` |
| MSG-28, MSG-29 | `FIX-2.18` |
| MSG-30 | `FIX-2.19` |
| MSG-31, MSG-32 | `FIX-2.20` |
| MSG-33 | `FIX-2.22` |
| MSG-34, MSG-35 | `FIX-2.23` |
| MSG-36, MSG-37 | `FIX-2.24` |
| MSG-38 | `FIX-2.21` |

**Sin huérfanos:** los 13 códigos nuevos están referenciados al menos por una historia.

---


### 12.4 Conteo final

| Categoría | Cantidad |
|---|---:|
| Historias de usuario con tarjeta completa (HU, E2) | **14** |
| Historias técnicas con tarjeta completa (HT, E2) | **11** |
| Historias de cabecera (E4/E5) | **12** |
| Tareas técnicas (E1/E3) | **22** |
| Recomendaciones del PO pendientes (§10) | **0** |
| Reglas de negocio transversales (RN) | **19** |
| Códigos de evento y error (MSG) | **38** |
| Spikes y decisiones | **17** |
| **Total de ítems cargables a backlog** | **59** |

## 13. Definition of Ready / Definition of Done

### Definition of Ready (por historia)

- [ ] Objetivo y valor expresados en formato Como / quiero / para.
- [ ] Criterios de aceptación numerados y binarios, con tags de camino, referenciando las reglas de §4 y los códigos de §5.
- [ ] Escenarios BDD en Gherkin español, alineados uno a uno con los criterios de aceptación.
- [ ] Mensajes de evento y error identificados en §5 y **validados con arquitectura del cliente** (`T-03`).
- [ ] Contrato MQ de salida acordado y versionado para los eventos que la historia publica.
- [ ] Mensajes FIX involucrados identificados con su `MsgType` y los tags relevantes del ROE de A3.
- [ ] Dependencias y spikes bloqueantes resueltos o acotados con un plan.
- [ ] Ambiente disponible para probar la historia (reMarkets accesible y sesión Drop Copy operativa).
- [ ] Chequeo INVEST completo, o spike registrado si falla.

### Definition of Done (por historia)

- [ ] Criterios de aceptación cumplidos y demostrables sobre el ambiente intive conectado a reMarkets.
- [ ] Escenarios BDD automatizados, o ejecutados manualmente con evidencia según acuerdo del equipo.
- [ ] Mensajes de evento y error implementados según §5, con el texto acordado.
- [ ] Mensajes FIX registrados en formato *raw* con credenciales enmascaradas (RN-03, RN-06).
- [ ] Eventos publicados con `correlation ID` verificable de punta a punta (RN-04).
- [ ] Comportamiento idempotente verificado ante reenvío FIX y *redelivery* de MQ (RN-05).
- [ ] Contrato MQ documentado y versionado.
- [ ] Pruebas unitarias y de integración en verde en el pipeline.
- [ ] Sin deuda técnica bloqueante conocida sin ticket.

### Definition of Done de la Fase 1

Los criterios de cierre de las épicas 1 a 3 están definidos en el **PRD §14**, e incluyen: sesión estable durante la ventana operativa completa cinco días hábiles consecutivos, cero eventos perdidos y cero duplicados publicados ante un corte deliberado de sesión, auditoría reconstruible de la actividad diaria, homologación parcial de A3 obtenida y conformidad funcional del cliente firmada.

> **Pendiente (`S-13`):** el criterio de aceptación formal del producto por parte del cliente debe acordarse en la Épica 1, tomando el PRD §14 como base. Observación del Excel: «definir prueba de aceptación del producto (DoD)».
