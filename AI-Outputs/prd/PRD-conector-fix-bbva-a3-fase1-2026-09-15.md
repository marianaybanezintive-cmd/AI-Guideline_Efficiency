# PRD — Conector FIX BBVA ↔ A3 Mercados · Fase 1 (Épicas 1 a 3)

> **Versión:** v1.1.0 · **Fecha:** 2026-09-15 · **Actualizado:** 2026-09-16
> **Producto:** Conector FIX BBVA Inversiones ↔ A3 Mercados
> **Alcance de este documento:** Épicas 1 (Discovery, Arquitectura y Ambientes), 2 (MVP TCR/ER y Conectividad FIX) y 3 (Homologación A3 y Pruebas de Aceptación BBVA)
> **Fecha límite comprometida:** 31-dic-2026
> **Autor:** Product Owner
> **Fuentes:**
> - `ImplementacionFixBBVA_PropuestaTecnica_20260908 - DRAFT.docx` (propuesta técnica intive v2.0, 08-sep-2026)
> - `ConectorFix_Backlog&Estimation - BBVA.xlsx` (backlog y estimación preliminar, borrador)
> - `api-trading-fix.pdf` — A3 Mercados, *Rules of Engagement FIX 5.0, gateways FIX-PTP / FIX-PTP-HR*, v2.0.53, abril 2025 (125 pág.)
> - `Manual de Conectividad A3.pdf` — A3 Mercados (28 pág.)

---

## Tabla de contenidos

1. [Resumen ejecutivo — dónde está el corte](#1-resumen-ejecutivo--dónde-está-el-corte)
2. [Contexto y problema](#2-contexto-y-problema)
3. [Objetivos de la Fase 1 y métricas de éxito](#3-objetivos-de-la-fase-1-y-métricas-de-éxito)
4. [Actores y sistemas](#4-actores-y-sistemas)
5. [**El corte del MVP — regla de decisión y matriz de mensajes**](#5-el-corte-del-mvp--regla-de-decisión-y-matriz-de-mensajes)
6. [Alcance por épica](#6-alcance-por-épica)
7. [Alcance diferido — Épicas 4 y 5](#7-alcance-diferido--épicas-4-y-5)
8. [Requerimientos funcionales de la Fase 1](#8-requerimientos-funcionales-de-la-fase-1)
9. [Requerimientos no funcionales y restricciones](#9-requerimientos-no-funcionales-y-restricciones)
10. [Hallazgos de la documentación A3 que condicionan el alcance](#10-hallazgos-de-la-documentación-a3-que-condicionan-el-alcance)
11. [Observaciones sobre el backlog borrador (Excel)](#11-observaciones-sobre-el-backlog-borrador-excel)
12. [Riesgos, dependencias y decisiones abiertas](#12-riesgos-dependencias-y-decisiones-abiertas)
13. [Plan de entrega contra el 31-dic-2026](#13-plan-de-entrega-contra-el-31-dic-2026)
14. [Criterios de aceptación de la Fase 1 (DoD de fase)](#14-criterios-de-aceptación-de-la-fase-1-dod-de-fase)

---

## 1. Resumen ejecutivo — dónde está el corte

El MVP de TCR/ER es, en una frase: **el conector observa el mercado y lo publica hacia BBVA; todavía no actúa sobre él.**

Esa es la línea. No es una división por cantidad de mensajes ni por esfuerzo: es una división por **efecto sobre el estado del mercado**.

| | Épicas 1-3 (Fase 1, hasta 31-dic) | Épica 4 — Order Routing | Épica 5 — Market Data |
|---|---|---|---|
| **Qué hace el conector** | Lee y publica | Crea, modifica y cancela órdenes | Recibe precios en flujo continuo |
| **Efecto sobre el libro de A3** | Ninguno | Altera el libro | Ninguno, pero alto volumen |
| **Riesgo financiero de un bug** | Nulo | Operaciones no deseadas | Decisiones sobre datos erróneos |
| **Mensajes FIX salientes** | Solo sesión y **consultas** (`H`, `AF`, `AD`) | `D`, `F`, `G`, `q` | `V` |
| **Mensajes FIX entrantes** | `8` (Execution Report), `AE` (Trade Capture Report), `h`, `j`, `3` | `9` (Order Cancel Reject) | `W`, `Y` |
| **Habilita** | Homologación parcial y subida a producción del canal de lectura | Operatoria real | Pricing y monitoreo |

**Las tres preguntas que resuelven cualquier caso dudoso:**

1. ¿El mensaje puede modificar el libro de órdenes de A3? → **Épica 4**, sin excepción.
2. ¿El flujo exige sostener el estado del libro o soportar volumen de *streaming*? → **Épica 5**.
3. ¿El valor se entrega leyendo lo que A3 ya decidió y publicándolo a MQ? → **MVP (Épica 2)**.

**Por qué este corte es el correcto y no uno arbitrario:**

- **Riesgo financiero cero.** Ningún mensaje del MVP puede generar, modificar ni cancelar una operación. Eso permite homologar y habilitar producción sin exposición patrimonial ni regulatoria, que es exactamente lo que se necesita para cumplir con el 31-dic.
- **Ejercita el 100% de la infraestructura difícil.** Sesión FIX, números de secuencia, detección de gaps, *resend*, persistencia, reconexión, contratos MQ, correlación, logging *raw*, observabilidad, CI/CD, gestión de secretos. Todo lo compartido y costoso se construye y se prueba primero, con el flujo de menor riesgo.
- **No genera retrabajo.** El contrato MQ de salida del MVP (estados de orden y operaciones ejecutadas) es **el mismo** que consumirá Order Routing. La Épica 4 agrega el sentido de entrada (MQ → FIX), no rehace el de salida.
- **Entrega valor propio, no es un andamio.** Con el MVP BBVA obtiene un *feed* confiable de ejecuciones y operaciones hacia sus sistemas internos aunque las órdenes se sigan originando por eTrader u otro canal. Es un entregable con valor aun si la Épica 4 se demorara.
- **Desacopla el cronograma del bloque regulatorio de DMA.** El Manual de Conectividad de A3 exige, para rutear órdenes, un sistema homologado de control de riesgo *pre-trade* (saldo disponible, márgenes, diferencias diarias, límites por segmento/instrumento, cantidad máxima por orden y *kill button*), más *cancel on disconnect*. Nada de eso aplica a un canal de solo lectura. Sacarlo de la Fase 1 quita del camino crítico una dependencia que no depende del equipo de desarrollo.

> ✅ **Confirmado por A3 el 2026-09-16:** el mercado **acepta la homologación parcial**, limitada a la integración de **TCR y ER**, sin envío de órdenes ni market data. Esto valida el corte propuesto y **despeja el riesgo principal del compromiso del 31-dic**. Los criterios de certificación publicados por A3 (Manual de Conectividad, *Criterios de Evaluación*) sí mencionan «el envío de órdenes» y «la suscripción a datos de mercado», por lo que igualmente corresponde **dejar el acuerdo asentado por escrito** junto con el paquete de certificación. Ver [S-02](#12-riesgos-dependencias-y-decisiones-abiertas).

---

## 1.bis Decisiones confirmadas el 2026-09-16

Cuatro definiciones cerradas que modifican el diseño respecto de la v1.0.0 de este documento.

| Decisión | Definición confirmada | Qué cambia |
|---|---|---|
| **Homologación parcial** | A3 acepta homologar sólo la integración de TCR y ER, sin envío de órdenes ni market data | El corte del MVP queda **validado por el propio mercado**. La gestión con A3 pasa de negociación de resultado incierto a formalización |
| **Origen del tráfico de ER** | **Modalidad FIX Drop Copy.** A3 configura la sesión del conector con un **perfil de sólo lectura** asociado a determinados IDs de cuentas o de operadores, y el motor de negociación **duplica en tiempo real** hacia esa sesión cada Execution Report de las órdenes que se operan, cancelan o modifican en esas cuentas | El conector es un **oyente pasivo**. Los ER llegan **no solicitados**, y el `ClOrdID` que traen fue generado por sistemas de terceros: no pertenece al espacio de identificadores del conector. En homologación, el tráfico se genera por inyección de órdenes de un tercero (soporte de Primary, o el equipo desde el Trader de reMarkets) sobre **cuentas espejo** mapeadas a la sesión. En producción, el flujo espeja la actividad real de la ALyC, cuyas órdenes se originan en terminales de Primary, sistemas propios o plataformas DMA |
| **Gestión de contraseñas** | **Puramente administrativa y fuera de banda.** No existe mecanismo FIX de cambio de contraseña. En reMarkets las asigna y modifica el soporte de Primary; en producción las gestiona la ALyC o el operador del mercado desde las consolas administrativas de Primary | El conector **nunca** intenta cambiar credenciales de forma programática. Ante un `Logout` (`35=5`) cuyo `Text` (58) indique `"Invalid username or password"`, `"Password expired"` o `"User locked"`, aplica **hard stop**: corta todo reintento automático para no bloquear el usuario, y dispara alerta crítica. La resolución exige intervención manual de un administrador |
| **Plataforma de ejecución** | **IBM WebSphere Liberty** | Queda descartada la anotación «Open-Liberty» del backlog borrador. Desaparece la ambigüedad de licenciamiento y soporte |

**Consecuencia sobre la gestión de riesgos:** el riesgo R-1 del §12.2 (los tiempos de A3 no dependen del equipo) se reduce significativamente en su componente de **alcance**, porque la aceptación ya está dada. Persiste en su componente de **calendario**: los tiempos de ejecución de la certificación siguen dependiendo de A3.

**Spike nuevo que emerge de la modalidad Drop Copy:** hay que confirmar con A3 si el perfil de **sólo lectura admite emitir consultas salientes** (`35=H`, `35=AF`, `35=AD`). Si no las admitiera, la consulta de estado, la consulta de operaciones concertadas y la reconciliación deben rediseñarse sobre el flujo de eventos duplicados exclusivamente. Es una pregunta de una línea que se resuelve en la misma gestión del alta del usuario Drop Copy.

---

## 2. Contexto y problema

BBVA Inversiones está construyendo las capacidades para operar por cuenta propia y de terceros en el mercado de capitales argentino bajo la figura de ALyC, con evolución gradual. Esa operatoria requiere integración estandarizada con los mercados, tanto para el ciclo de vida de las órdenes como para la información de mercado.

El proyecto construye un **conector FIX** que actúa como punto de adaptación entre el ecosistema interno de BBVA —que se comunica por **colas MQ**— y la interfaz **FIX 5.0 SP2** del gateway **FIX-PTP** de A3 Mercados. El conector encapsula la gestión de sesión y el procesamiento de mensajes del protocolo, y separa las capacidades comunes de FIX de las particularidades de A3 para habilitar futuras integraciones con otros mercados.

BBVA fijó la prioridad: **login, logout, heartbeat, TCR y ER primero**. El objetivo de negocio de la Fase 1 no es operar: es **habilitar al banco la subida a producción de la integración con A3**, con la homologación aprobada, antes del 31-dic-2026.

### Qué significa TCR y ER en el diccionario de A3

Esto es central para entender el corte, porque los dos mensajes que dan nombre al MVP viven en capas distintas del protocolo:

- **ER — Execution Report (`MsgType=8`).** Es el mensaje que A3 usa para confirmar la recepción de una orden, confirmar cambios sobre una orden existente, **comunicar el estado de una orden**, informar ejecuciones (totales y parciales) y rechazar órdenes. Sus dos campos de control son `OrdStatus` (39, estado actual de la orden) y `ExecType` (150, propósito del mensaje). El ROE define seis variantes: *New*, *Order Canceled Response*, *Order Replaced Response*, *Order Filled/Partially Filled Response*, *Order Status Response* (con y sin órdenes) y *Reject Message Response*.
- **TCR — Trade Capture Report (`MsgType=AE`).** En el ROE de A3 **no** pertenece a *Order Management* sino al bloque **Post Trade Messages**. Reporta **operaciones ya concertadas** y se obtiene como respuesta a un *Trade Capture Report Request* (`MsgType=AD`), que admite consulta **por cuenta** o **por símbolo**.

Es decir: **ER y TCR son flujos de lectura del estado del mercado, no de intervención sobre él.** El corte del MVP no es una concesión de alcance: es fiel a lo que esos mensajes significan en el protocolo.

---

## 3. Objetivos de la Fase 1 y métricas de éxito

### Objetivo de negocio

Habilitar a BBVA a **subir a producción la integración con A3** con homologación aprobada (aunque sea de alcance parcial), antes del 31-dic-2026, sin haber implementado todavía el ruteo de órdenes ni el consumo de *market data*.

### Objetivos de producto

| # | Objetivo | Cómo se verifica |
|---|---|---|
| OBJ-1 | Sesión FIX estable con A3 durante toda la ventana operativa | La sesión se mantiene abierta de 9:30 a 19:00 sin desconexiones no gestionadas durante 5 días hábiles consecutivos en el ambiente de pruebas de A3 |
| OBJ-2 | Ningún evento del mercado se pierde ni se duplica hacia BBVA | Ante corte y reconexión de sesión, el conjunto de ER y TCR publicados en MQ coincide exactamente con el emitido por A3, sin duplicados, verificado por conciliación |
| OBJ-3 | Contrato MQ de salida definido, versionado y estable | Los contratos de los mensajes publicados están aprobados por arquitectura de BBVA y no cambian entre el fin de Épica 1 y el fin de Épica 3 |
| OBJ-4 | Trazabilidad completa de extremo a extremo | Para cualquier operación, se puede reconstruir la cadena mensaje FIX *raw* → evento normalizado → mensaje MQ, correlacionada por un identificador único |
| OBJ-5 | Homologación parcial de A3 obtenida | Certificado de A3 emitido, o acta formal de alcance parcial acordada, con las observaciones cerradas |
| OBJ-6 | Conformidad funcional de BBVA | Pruebas de aceptación ejecutadas por BBVA sobre el ambiente intive, con evidencia y conformidad firmada |

### Métricas

| Métrica | Objetivo Fase 1 |
|---|---|
| Disponibilidad de la sesión FIX dentro de la ventana 9:30–19:00 | ≥ 99% del tiempo, medido sobre días hábiles |
| Eventos FIX entrantes publicados correctamente en MQ | 100% (cero pérdidas) |
| Eventos duplicados publicados en MQ | 0 |
| Tiempo desde recepción del mensaje FIX hasta publicación en MQ | p95 ≤ 500 ms (a validar contra el estándar de BBVA en Épica 1) |
| Tiempo de recuperación tras caída de sesión (reconexión + recuperación de gaps + reconciliación) | ≤ 60 segundos |
| Defectos bloqueantes abiertos al cierre de la Épica 3 | 0 |

### No-objetivos explícitos de la Fase 1

- No se envían órdenes al mercado, ni propias ni de terceros.
- No se consume *market data* en flujo continuo.
- No se implementa control de riesgo *pre-trade*, *kill switch* ni *cancel on disconnect*.
- No se implementan *allocations*, *giveups*, *block trades* ni reporte de posiciones.
- No se implementan reglas de negocio diferenciadas por producto (TRD, Renta Fija, Cauciones) más allá de lo necesario para normalizar y publicar lo recibido.
- No se implementa alta disponibilidad activa/activa ni *failover* automático entre instancias de A3.

---

## 4. Actores y sistemas

### 4.1 Actores

| Actor | Descripción | Rol en Fase 1 |
|---|---|---|
| **Sistemas internos de BBVA** (consumidores) | Aplicaciones que necesitan conocer estados de órdenes y operaciones ejecutadas | Consumen los mensajes que el conector publica en MQ |
| **Conector FIX (el producto)** | Componente Java sobre WebSphere Liberty | Gestiona la sesión FIX, consulta, normaliza y publica |
| **A3 Mercados** | Mercado, gateway FIX-PTP | Emite ER y TCR; homologa la implementación |
| **Operador de mesa BBVA** | Usuario de eTrader | En Fase 1, genera el tráfico de órdenes que produce los ER que el conector observa |
| **Equipo de operaciones / soporte** | Monitoreo de la conectividad | Consume métricas, logs y alertas de sesión |
| **Arquitectura y seguridad BBVA** | Define estándares, MQ, secretos | Aprueba contratos, framework MQ y esquema de rotación de credenciales |
| **A3 Operaciones** (`operaciones@a3mercados.com.ar`) | Alta de usuarios, certificación | Provee credenciales, ambiente de pruebas y el paquete de certificación |

### 4.2 Sistemas y componentes

| Componente | Responsabilidad | Épica |
|---|---|---|
| **FIX Session Layer** | Logon, Logout, Heartbeat, Test Request, Resend Request, Sequence Reset, Reject de sesión | 2 |
| **Adaptador A3** | Particularidades del diccionario de A3 respecto del estándar FIX 5.0 SP2 | 2 |
| **Motor de normalización** | Traduce mensajes FIX al modelo canónico de BBVA | 2 |
| **Integración MQ (salida)** | Publica eventos normalizados hacia las colas de BBVA | 2 |
| **Integración MQ (entrada)** | Consume instrucciones desde BBVA | **4** (en Fase 1 solo se consumen comandos de consulta, si se decide exponerlos) |
| **Persistencia de sesión** | Números de secuencia entrantes y salientes, resistentes a reinicio | 2 |
| **Auditoría** | Log *raw* de todo mensaje FIX enviado y recibido, con *timestamp* y sesión | 2 |
| **Observabilidad** | Métricas, estado de sesión, alertas | 2 |
| **Gestión de secretos** | Lectura del secret de credenciales administrado por seguridad BBVA | 1 y 2 |

---

## 5. El corte del MVP — regla de decisión y matriz de mensajes

### 5.1 La regla

> **Entra en el MVP TCR/ER todo mensaje FIX que no modifica el estado del mercado:** la capa de sesión completa, los flujos de **consulta** (estado de órdenes y operaciones ejecutadas) y la **publicación** de lo recibido hacia MQ.
>
> **Queda fuera de la Fase 1** todo mensaje que **crea, modifica o cancela una orden** (Épica 4 — Order Routing) y todo flujo de **suscripción continua de precios** (Épica 5 — Market Data).

Corolario operativo: el conector del MVP puede desconectarse en cualquier momento sin consecuencias sobre el mercado. A partir de la Épica 4, no.

### 5.2 Matriz de mensajes FIX por épica

Basada en el *Message Summary* del ROE FIX 5.0 v2.0.53 de A3. `↑` = conector → A3, `↓` = A3 → conector.

#### Capa de sesión — **toda dentro del MVP (Épica 2)**

| Mensaje | MsgType | Dir. | Por qué está en el MVP |
|---|---|---|---|
| Logon | `A` | ↑↓ | Apertura y autenticación de la sesión |
| Heartbeat | `0` | ↑↓ | Mantenimiento del enlace; `HeartBtInt` ≥ 10 s |
| Test Request | `1` | ↑↓ | Verificación del enlace y de las secuencias |
| Resend Request | `2` | ↑↓ | Recuperación de mensajes ante gap de secuencia |
| Sequence Reset | `4` | ↑↓ | Modos *Gap Fill* y *Reset* |
| Reject – Session Level | `3` | ↓ | Manejo de errores de protocolo (18 valores de `SessionRejectReason`) |
| Logout | `5` | ↑↓ | Cierre controlado de sesión |

#### Mensajes comunes — **dentro del MVP**

| Mensaje | MsgType | Dir. | Decisión |
|---|---|---|---|
| Business Message Reject | `j` | ↓ | **Incluido.** Es la respuesta de A3 a un mensaje sintácticamente correcto en situación no soportada. Sin esto no hay manejo de errores de negocio |
| News | `B` | ↓ | **Incluido como consumo y publicación pasiva.** Costo marginal; A3 lo usa para avisos de mercado por segmento |
| Trading Session Status | `h` | ↓ | **Incluido.** Informa estado y fase del mercado y de cada segmento (`Pre-Trading`, `Trading`, `Post-Trading`, `Closed`, `CPX`). Sin esto los ER y TCR no se pueden interpretar en contexto |

#### Bloque de órdenes — **el corte pasa por acá**

| Mensaje | MsgType | Dir. | Épica | Criterio |
|---|---|---|---|---|
| **Execution Report** (todas sus variantes) | `8` | ↓ | **2 — MVP** | Es entrante. Consumir, normalizar y publicar en MQ. Incluye *New*, *Canceled*, *Replaced*, *Filled/Partially Filled*, *Order Status Response* y *Reject Message Response* |
| **Order Status Request** | `H` | ↑ | **2 — MVP** | Consulta puntual. No altera el libro |
| **Order Mass Status Request** | `AF` | ↑ | **2 — MVP** | Consulta masiva (`MassStatusReqType=7`, `SecurityStatus=0` para todos los estados). Es el mecanismo de **reconciliación** tras reconexión. No altera el libro |
| New Order – Single | `D` | ↑ | **4** | Crea una orden |
| Order Cancel Request | `F` | ↑ | **4** | Cancela una orden |
| Order Cancel/Replace Request | `G` | ↑ | **4** | Modifica una orden |
| Order Cancel Reject | `9` | ↓ | **4** | Solo tiene sentido si se envían `F` o `G` |
| **Order Mass Cancel Request** | `q` | ↑ | **4** | ⚠️ Aunque se lo piense como *kill switch* operativo, **es un mensaje mutante**: cancela órdenes reales. Va a la Épica 4 sin excepción |

#### Post-trade — **sólo la porción TCR regular entra al MVP**

| Mensaje | MsgType | Dir. | Épica | Criterio |
|---|---|---|---|---|
| **Trade Capture Report Request** — *Regular Trades by Account / by Symbol* | `AD` | ↑ | **2 — MVP** | Consulta de operaciones concertadas, con `TrdType=0` (Regular Trade). Solo lectura |
| **Trade Capture Report** — *Regular Trades* | `AE` | ↓ | **2 — MVP** | Operaciones ejecutadas → normalizar y publicar en MQ |
| Trade Capture Report — *Block Trades* | `AE` (`TrdType=1`) | ↓ | **Fuera del alcance del proyecto** | Implica aceptar/declinar operaciones de bloque: es mutante |
| Trade Capture Report Ack | `AR` | ↑↓ | **Fuera del alcance** | Solo aplica a Block Trades |
| Trade Capture Report Request — *Allocations and giveups* | `AD` (`TrdType=1001/1002`) | ↑ | **Fuera del alcance** | Bloque de asignaciones, no comprometido en la propuesta |
| Allocation Instruction / Ack | `J` / `P` | ↑↓ | **Fuera del alcance** | Ídem |
| Confirmation / Confirmation Ack | `AK` / `AU` | ↓↑ | **Fuera del alcance** | Ídem |
| Request for Positions / Position Report | `AN` / `AP` | ↑↓ | **Fuera del alcance** | El conector no mantiene posiciones |

> **Decisión de alcance explícita y necesaria:** «TCR» en el MVP significa **exclusivamente Trade Capture Report de operaciones regulares (`TrdType=0`)**. El bloque post-trade completo del ROE de A3 (block trades, allocations, giveups, confirmaciones, posiciones) es mucho más grande que eso y no está comprometido en la propuesta técnica. Sin esta acotación escrita, «implementar TCR» se interpreta como todo el capítulo *Post Trade Messages* del ROE —unas 30 páginas— y el MVP se duplica.

#### Market Data e instrumentos — **Épica 5**

| Mensaje | MsgType | Dir. | Épica | Criterio |
|---|---|---|---|---|
| Market Data Request | `V` | ↑ | **5** | Suscripción (`SubscriptionRequestType` 0/1/2) |
| Market Data – Snapshot / Full Refresh | `W` | ↓ | **5** | Volumen y gestión de libro |
| Market Data Request Reject | `Y` | ↓ | **5** | Ídem |
| Security Status Request / Security Status | `e` / `f` | ↑↓ | **5** | Estado del instrumento |
| **Security List Request / Security List** | `x` / `y` | ↑↓ | **5, con excepción a evaluar** | ⚠️ **Zona gris.** Es el catálogo de instrumentos. Los ER y TCR traen `Symbol` como string; si la normalización hacia BBVA necesita enriquecer con datos del instrumento (moneda, tipo, vencimiento, segmento), este mensaje debe adelantarse al MVP. Es solo lectura, así que no viola la regla del corte. Ver [S-04](#12-riesgos-dependencias-y-decisiones-abiertas) |

#### Cuentas — **dentro del MVP**

| Mensaje | MsgType | Dir. | Criterio |
|---|---|---|---|
| Account List Request / Account List / Account List Incremental | `UALR` / `UALT` / `UALI` | ↑↓ | **Incluidos.** Solo lectura, y son necesarios para poblar correctamente el bloque `Parties` y el campo `Account` en las consultas TCR por cuenta |

### 5.3 El corte en la dirección MQ

Igual de importante que el corte de mensajes FIX:

| Flujo MQ | Épica | Detalle |
|---|---|---|
| **Conector → BBVA (publicación)** | **2 — MVP** | Eventos de estado de orden derivados de ER, operaciones ejecutadas derivadas de TCR, estado de sesión, estado de mercado, y errores. **Este contrato se define completo en la Épica 1 y no cambia en la Épica 4** |
| **BBVA → Conector (consumo de comandos de consulta)** | **2 — MVP, opcional** | Solicitudes de reconciliación o de consulta de trades. Es *pull* iniciado por BBVA pero sigue siendo lectura. Su inclusión se decide en la Épica 1 según los casos de uso reales |
| **BBVA → Conector (instrucciones de orden)** | **4** | Alta, cancelación y modificación de órdenes. Es el sentido que abre el riesgo: requiere idempotencia, deduplicación ante *redelivery* de MQ, generación de `ClOrdID` único y máquina de estados |

### 5.4 Capacidades transversales: dónde corta cada una

Este es el punto donde el backlog borrador y la propuesta técnica no coinciden, y hay que decidirlo explícitamente.

| Capacidad | En el MVP (Épica 2) | Diferido a Épica 5 (Tolerancia a fallas) |
|---|---|---|
| **Recuperabilidad** | Persistencia de `MsgSeqNum` entrante y saliente; detección de gaps; emisión y respuesta de `Resend Request`; manejo de `Sequence Reset` en modo *Gap Fill*; **reconciliación básica** vía `AF` al reconectar | Reconexión automática con política de reintentos configurable; recuperación completa del estado operativo tras reinicio del proceso; *failover* a la instancia secundaria de A3 |
| **Idempotencia** | Deduplicación de mensajes FIX reenviados (`PossDupFlag`) antes de publicar en MQ | Idempotencia del lado de la escritura de órdenes (no aplica en Fase 1) |
| **Auditoría** | Log *raw* de todo mensaje FIX enviado y recibido, con *timestamp*, sesión y `correlation ID`; log de los mensajes MQ | Análisis y explotación de la información logueada |
| **Observabilidad** | Estado de sesión (conectado/desconectado, último heartbeat, secuencia actual), métricas y alertas ante ausencia de mensajes | Tableros y análisis avanzado |
| **Alta disponibilidad** | Fuera | Completa |

> El plan de trabajo de la propuesta técnica ya ubica *Recoverability* (persistencia de secuencias, detección de gaps, resend requests, reconciliación básica) **dentro de la etapa MVP TCR/ER**, y *Tolerancia a Fallas* (reconexión automática, recuperación tras reinicio, idempotencia) en la etapa T0+5. El Excel, en cambio, tiene todo con `Scope=1` sin distinción de fase. Esta tabla resuelve la ambigüedad.

---

## 6. Alcance por épica

### Épica 1 — Discovery, Arquitectura y Ambientes

**Objetivo:** reducir la incertidumbre funcional y técnica al punto en que la Épica 2 pueda ejecutarse sin bloqueos.
**Duración prevista:** T0 + 1 mes (2 sprints).

**Dentro de alcance**

1. **Definición funcional aprobada** de los flujos del MVP: ciclo de vida de la orden tal como se observa desde el ER, catálogo de estados (`OrdStatus`) y de tipos de evento (`ExecType`), y estructura de la operación concertada del TCR.
2. **Contratos MQ preliminares** para el sentido conector → BBVA: eventos de orden, operaciones, estado de sesión, estado de mercado y errores. Incluye la política de correlación de identificadores.
3. **Arquitectura de referencia**: separación entre capacidades comunes FIX, adaptador específico de A3 y adaptador de integración BBVA. Diseño del FIX Engine y decisión sobre la librería base.
4. **Estrategia de uso de MQ**: framework aprobado por BBVA, colas, productores y consumidores, tratamiento de errores, *dead letter*, comportamiento ante *redelivery*.
5. **Estrategia de observabilidad y de logging**, alineada a los estándares y herramientas disponibles en BBVA.
6. **Gestión de contraseñas y secretos**: esquema de lectura del secret, y —crítico— **validación con A3 de cuál es el mecanismo real de rotación de credenciales** (ver [S-01](#12-riesgos-dependencias-y-decisiones-abiertas)).
7. **Decisión sobre el origen del tráfico de Execution Reports** en un escenario sin ruteo de órdenes (ver [S-03](#12-riesgos-dependencias-y-decisiones-abiertas)). **Esta es la definición más urgente de toda la Épica 1.**
8. **Acuerdo formal con A3 sobre el alcance de una homologación parcial** (ver [S-02](#12-riesgos-dependencias-y-decisiones-abiertas)).
9. **Backlog refinado y priorizado**, con plan de releases.
10. **Ambientes**: ambiente intive operativo (WebSphere Liberty + MQ), acceso al ambiente de pruebas de A3 (*reMarkets*, `fix.remarkets.primary.com.ar:9876`, alta autogestionada en `remarkets.primary.ventures`) y credenciales gestionadas.
11. **Relevamiento de la estructura de códigos de BBVA** requerida por el bloque `Parties` de A3: código CNV de agente de negociación (`PartyRole=1`), Client ID (`3`), agente de compensación (`4`), *Executing Trader*, *Desk ID* (`76`) y *Customer Account* (`24`).
12. **Definición de escenarios y casos principales de prueba** para la validación del sistema.

**Fuera de alcance:** diseño detallado de Order Routing y de Market Data. Se definen solo las fronteras de extensibilidad necesarias para que las épicas 4 y 5 no obliguen a rehacer la arquitectura.

**Criterio de salida:** contratos MQ aprobados por arquitectura de BBVA, ambientes accesibles con conexión FIX establecida contra reMarkets, spikes bloqueantes S-01 a S-04 resueltos, y backlog de la Épica 2 refinado y estimado.

---

### Épica 2 — MVP TCR/ER y Conectividad FIX

**Objetivo:** construir la base del conector para mercados FIX, con prioridad en TCR y ER, y desplegarla en el ambiente intive.
**Duración prevista:** T0 + 2 meses (2 sprints adicionales).

**Dentro de alcance**

| Bloque | Contenido |
|---|---|
| **Capa de sesión FIX** | Logon con credenciales desde el secret, Logout controlado, Heartbeat según `HeartBtInt`, respuesta a Test Request, emisión de Test Request propio, manejo de Reject de sesión, monitoreo de estado de sesión y ciclo diario alineado a la ventana 9:30–19:00 |
| **Recuperabilidad** | Persistencia de secuencias entrantes y salientes que sobrevive a reinicios, detección de gaps, emisión y atención de Resend Request, manejo de Sequence Reset en modo Gap Fill, reconciliación básica al reconectar mediante Order Mass Status Request |
| **Procesamiento de Execution Report** | Consumo de las seis variantes de `MsgType=8`, interpretación conjunta de `OrdStatus` y `ExecType`, normalización al modelo canónico, deduplicación y publicación en MQ conservando el identificador de correlación |
| **Procesamiento de Trade Capture Report** | Emisión de `AD` por cuenta y por símbolo con `TrdType=0`, consumo de `AE`, manejo del encadenamiento de reportes (`TotNumTradeReports`, `LastRptRequested`), normalización y publicación en MQ |
| **Consulta de estado** | Order Status Request (`H`) y Order Mass Status Request (`AF`), respetando el límite de A3 de **1 solicitud masiva por segundo** |
| **Contexto de mercado** | Consumo de Trading Session Status (`h`) y de News (`B`), y su publicación |
| **Manejo de errores** | Reject de sesión (`3`) con sus 18 razones, Business Message Reject (`j`), y Execution Report de rechazo |
| **Flujo MQ (salida)** | Validaciones, transformaciones y publicación de estados y eventos según el contrato acordado en la Épica 1 |
| **Auditoría** | Logging FIX *raw* (enviado y recibido), logging MQ, correlation IDs de punta a punta |
| **DevOps** | Pipeline CI/CD y despliegue en el ambiente intive |

**Fuera de alcance:** todo mensaje mutante (`D`, `F`, `G`, `q`), toda suscripción de *market data* (`V`, `W`), reconexión automática, recuperación completa tras reinicio del proceso, *failover*, y el bloque post-trade avanzado.

**Criterio de salida:** el conector, desplegado en el ambiente intive y conectado al ambiente de pruebas de A3, mantiene la sesión durante la ventana operativa completa, publica en MQ el 100% de los ER y TCR recibidos sin duplicados, y se recupera de un corte de sesión reconciliando el estado sin pérdida de eventos.

---

### Épica 3 — Homologación A3 y Pruebas de Aceptación BBVA

**Objetivo:** obtener la aprobación de A3 sobre el alcance implementado y la conformidad funcional de BBVA, para habilitar la subida a producción.
**Duración prevista:** mínimo T0 + 2,5 meses (1 sprint); el máximo depende de los tiempos de A3 Mercados.

**Dentro de alcance**

1. **Inicio formal del proceso de homologación** con A3 (`operaciones@a3mercados.com.ar`), recepción del paquete de certificación y de los casos de prueba requeridos.
2. **Ejecución de la certificación** sobre el alcance parcial acordado, cubriendo los criterios de evaluación de A3 que sí aplican: conformidad con la API y los ROE, **gestión de errores** (rechazos y desconexiones) y **rendimiento y estabilidad**.
3. **Pruebas de aceptación de BBVA** sobre el ambiente intive, con evidencia documentada.
4. **Corrección de defectos** surgidos de ambas instancias.
5. **Soporte a BBVA** para la configuración de su ambiente, el despliegue del entregable parcial y su integración con el ambiente de pruebas de A3.

**Fuera de alcance:** certificación de envío de órdenes y de suscripción a *market data*, que son criterios que A3 evalúa pero que corresponden a las épicas 4 y 5 y requerirán una nueva instancia de homologación.

**Criterio de salida:** certificado de A3 emitido (o acta de alcance parcial acordada y firmada), defectos de homologación y de aceptación cerrados, y conformidad funcional de BBVA obtenida.

> **Restricción de planificación:** la certificación de A3 tiene **vigencia de un año**. Homologar en noviembre-diciembre de 2026 implica planificar la re-homologación para el mismo período de 2027, y previsiblemente convivir con ciclos de vencimiento distintos si Order Routing y Market Data se certifican después. Conviene evaluar con A3 si las certificaciones incrementales renuevan la vigencia completa o sólo la del alcance nuevo.

---

## 7. Alcance diferido — Épicas 4 y 5

### Épica 4 — Order Routing (T0 + 3,5 meses)

Lo que la habilita es un único cambio de naturaleza: **el conector pasa a modificar el estado del mercado.** De ahí se derivan todos sus requisitos adicionales.

| Bloque | Contenido |
|---|---|
| Flujo MQ → FIX | Consumo de instrucciones desde las colas de BBVA, validación de estructura y obligatoriedad, rechazo de mensajes inválidos, transformación a FIX |
| Mensajes de orden | `NewOrderSingle` (`D`), `OrderCancelRequest` (`F`), `OrderCancelReplaceRequest` (`G`), manejo de `OrderCancelReject` (`9`) |
| Ciclo de vida | Máquina de estados de la orden, encadenamiento `ClOrdID` / `OrigClOrdID`, generación de `ClOrdID` único, versionado de la orden ante *replace* |
| Idempotencia de escritura | Prevención de alta duplicada de órdenes ante *redelivery* de MQ o reenvío FIX. **Es el riesgo más serio de toda la solución** |
| Reglas por producto | TRD, Renta Fija y Cauciones: validaciones, `OrdType` (`2=Limit`, `K=Market with Left Over as Limit`), `TimeInForce` (Day, GTC, IOC, FOK, GTD), `ExecInst` (`Z`, `G`, `o`) |
| Controles de A3 | *Cancel on disconnect*, `Order Mass Cancel Request` (`q`) como *kill switch*, respeto de los límites de 20 mensajes/segundo de ingreso, cancelación y reemplazo |
| Riesgo *pre-trade* | Si la operatoria califica como acceso DMA: control de saldo disponible, márgenes al abrir posición, diferencias diarias, límites por segmento/instrumento, cantidad máxima por orden y *kill button*, todos controlables en tiempo real por el participante |
| Homologación | Nueva instancia de certificación A3 sobre la funcionalidad nueva, más regresión |

**Dependencias que no existen en la Fase 1:** definición completa de reglas de negocio por producto con los referentes de negocio de BBVA, y —si aplica DMA— un sistema homologado de control de riesgo *pre-trade*.

### Épica 5 — Market Data y Tolerancia a Fallas (T0 + 5 meses)

| Bloque | Contenido |
|---|---|
| Market Data | `MarketDataRequest` (`V`) con `SubscriptionRequestType` 0/1/2, `MarketDepth` (Full Book, Top of Book, N niveles), consumo de `Snapshot/Full Refresh` (`W`), manejo de `MarketDataRequestReject` (`Y`) |
| Definición de instrumentos | `SecurityListRequest` / `SecurityList` (`x` / `y`), `SecurityStatusRequest` / `SecurityStatus` (`e` / `f`) |
| Publicación MQ | Normalización y *fan-out* de precios hacia los consumidores, con configuración de tópicos y suscripciones |
| Tolerancia a fallas | Reconexión automática, recuperación tras reinicio, idempotencia, *failover* |
| Testing | *Failover*, *recovery*, duplicados, *redelivery* MQ |
| Homologación | Nueva instancia de certificación A3, más regresión completa sobre TRD, Renta Fija y Cauciones |

**Consideración de gateway:** el gateway **FIX-PTP** (el del MVP) entrega *market data* en modalidad **Full Refresh** con profundidad máxima 10 y frecuencia de 1 mensaje cada 500 ms por símbolo, apto para terminal humana u OMS. Si BBVA necesitara mayor frecuencia (FIX-PTP-HR, 1 msg/50 ms) o *incremental refresh* de baja latencia (FIX-PTP-LL, sólo disponible vía *colocation*), eso implica **otro gateway, otra solicitud a A3 y posiblemente otra certificación**. Conviene definirlo en la Épica 1 aunque se implemente en la 5, porque condiciona la conectividad contratada.

---

## 8. Requerimientos funcionales de la Fase 1

Numerados para trazabilidad con las historias de usuario.

### 8.1 Gestión de sesión

| ID | Requerimiento |
|---|---|
| RF-01 | El conector establece una sesión FIX 5.0 SP2 con el gateway FIX-PTP de A3 mediante `Logon` (`35=A`), con `EncryptMethod=0`, `HeartBtInt` ≥ 10 y `DefaultApplVerID=9` |
| RF-02 | Las credenciales (`Username`, `Password`) se obtienen del secret administrado por seguridad de BBVA, con acceso de sólo lectura, y nunca se registran en logs |
| RF-03 | El conector completa correctamente `SenderCompID`, `TargetCompID`, `OnBehalfOfCompID` y `DeliverToCompID` según lo definido por A3, y no abre más de una sesión con la misma combinación |
| RF-04 | El conector intercambia `Heartbeat` (`35=0`) según el intervalo negociado y responde a `Test Request` (`35=1`) devolviendo el `TestReqID` recibido |
| RF-05 | El conector emite `Test Request` ante ausencia de mensajes durante el intervalo esperado |
| RF-06 | El conector ejecuta `Logout` (`35=5`) controlado al cierre de la ventana operativa y libera recursos, dejando la sesión marcada como cerrada |
| RF-07 | El conector interpreta una desconexión sin `Logout` como condición anormal y la registra y alerta como tal |
| RF-08 | El conector opera dentro de la ventana de sesión FIX de A3 (9:30 a 19:00), diferenciándola de la ventana de negociación (10:00 a 17:30) |

### 8.2 Recuperabilidad y consistencia

| ID | Requerimiento |
|---|---|
| RF-09 | El conector persiste los `MsgSeqNum` entrantes y salientes de forma que sobrevivan a un reinicio del proceso |
| RF-10 | El conector detecta discontinuidades en la secuencia entrante y emite `Resend Request` (`35=2`) con el rango faltante |
| RF-11 | El conector atiende los `Resend Request` recibidos de A3 retransmitiendo los mensajes solicitados conforme al protocolo |
| RF-12 | El conector procesa `Sequence Reset` (`35=4`) en modo *Gap Fill* y en modo *Reset* |
| RF-13 | El conector identifica los mensajes reenviados (`PossDupFlag`) y no los vuelve a publicar en MQ |
| RF-14 | Tras restablecer una sesión interrumpida, el conector ejecuta una reconciliación mediante `Order Mass Status Request` (`35=AF`) y publica las diferencias detectadas |

### 8.3 Procesamiento de Execution Report

| ID | Requerimiento |
|---|---|
| RF-15 | El conector consume `Execution Report` (`35=8`) e interpreta el evento a partir de la combinación de `ExecType` (150) y `OrdStatus` (39) |
| RF-16 | El conector procesa las variantes *New*, *Order Canceled Response*, *Order Replaced Response*, *Order Filled/Partially Filled Response*, *Order Status Response* y *Reject Message Response* |
| RF-17 | El conector normaliza cada ER al modelo canónico acordado, preservando `ClOrdID`, `OrigClOrdID`, `OrderID`, `ExecID`, `Account`, `Symbol`, `Side`, cantidades (`OrderQty`, `CumQty`, `LeavesQty`, `LastQty`), precios (`Price`, `AvgPx`, `LastPx`) y `TransactTime` |
| RF-18 | El conector publica cada evento normalizado en la cola MQ correspondiente, conservando un identificador de correlación que permite vincularlo con el mensaje FIX de origen |
| RF-19 | El conector publica los rechazos de orden informados por A3 como eventos de error diferenciados, incluyendo el motivo |

### 8.4 Procesamiento de Trade Capture Report

| ID | Requerimiento |
|---|---|
| RF-20 | El conector emite `Trade Capture Report Request` (`35=AD`) con `TradeRequestType=1` y `TrdType=0` (Regular Trade), en modalidad por cuenta y por símbolo |
| RF-21 | El conector compone correctamente el bloque `Parties` con los roles requeridos por A3 (Executing Firm, Client ID, Clearing Firm, Executing Trader, Desk ID, Customer Account) |
| RF-22 | El conector consume `Trade Capture Report` (`35=AE`) y maneja el encadenamiento de reportes usando `TotNumTradeReports` (748) y `LastRptRequested` (912) |
| RF-23 | El conector normaliza cada operación concertada preservando `TradeReportID`, `TrdMatchID`, `LastPx`, `LastQty`, `Side`, `Account`, `Symbol`, `TradeDate` y `TransactTime`, y la publica en MQ |
| RF-24 | El conector descarta o deriva a un flujo diferenciado los TCR con `TrdType` distinto de 0, dejando constancia en el log |

### 8.5 Consulta de estado

| ID | Requerimiento |
|---|---|
| RF-25 | El conector emite `Order Status Request` (`35=H`) para consultar una orden puntual |
| RF-26 | El conector emite `Order Mass Status Request` (`35=AF`) con `MassStatusReqType=7`, pudiendo filtrar por `SecurityStatus` (0 = todos los estados, 1 = sólo activas) |
| RF-27 | El conector respeta el límite de A3 de **1 solicitud masiva de estado por segundo** y de **100 solicitudes de estado de orden por segundo**, aplicando control de caudal propio |

### 8.6 Contexto de mercado y errores

| ID | Requerimiento |
|---|---|
| RF-28 | El conector consume `Trading Session Status` (`35=h`) y mantiene y publica el estado y la fase de cada segmento de mercado |
| RF-29 | El conector consume `News` (`35=B`) y lo publica hacia BBVA asociado a su `MarketSegmentID` |
| RF-30 | El conector procesa `Reject – Session Level` (`35=3`) registrando `RefSeqNum`, `RefTagID`, `RefMsgType` y `SessionRejectReason`, y genera alerta |
| RF-31 | El conector procesa `Business Message Reject` (`35=j`) registrando `RefMsgType`, `BusinessRejectReason` y `Text`, y lo publica como evento de error |
| RF-32 | El conector consume `Account List` (`UALT`) e `Account List Incremental` (`UALI`) y mantiene el catálogo de cuentas habilitadas |

### 8.7 Auditoría y observabilidad

| ID | Requerimiento |
|---|---|
| RF-33 | El conector almacena cada mensaje FIX enviado y recibido en formato *raw*, con *timestamp* y sesión asociada, permitiendo reconstruir la actividad diaria completa |
| RF-34 | El conector registra el estado de la sesión: conectado/desconectado, último heartbeat, secuencia entrante y saliente actual |
| RF-35 | El conector emite alertas ante ausencia prolongada de mensajes, desconexión no controlada, gap de secuencia no recuperado y fallo de publicación en MQ |
| RF-36 | Todo mensaje publicado en MQ y todo mensaje FIX registrado comparten un `correlation ID` que permite la trazabilidad de punta a punta |

> A3 puede solicitar acceso a los registros de actividad diaria en casos de soporte, por lo que RF-33 no es opcional.

---

## 9. Requerimientos no funcionales y restricciones

### 9.1 Tecnología (impuesta por BBVA)

| Aspecto | Definición |
|---|---|
| Lenguaje | Java 25 o superior |
| Servidor de aplicaciones | **IBM WebSphere Liberty** ✅ confirmado el 2026-09-16; queda descartada la anotación «Open-Liberty» del backlog borrador |
| Persistencia (si se requiere) | Sybase 15.7/16, con acceso mediante Stored Procedures |
| Mensajería interna | Colas MQ; el framework/librería concreto lo define BBVA en la Épica 1 |
| Gestión de credenciales | Secrets administrados por el área de seguridad de BBVA, acceso de sólo lectura para el conector |

> ⚠️ Verificar en la Épica 1 que la versión de WebSphere Liberty disponible en BBVA soporte Java 25. Es una combinación que conviene validar con un *spike* de despliegue temprano antes de comprometer código.

### 9.2 Protocolo y conectividad (impuesto por A3)

| Aspecto | Definición |
|---|---|
| Versión FIX | 5.0 SP2 (`DefaultApplVerID=9`), sobre transporte FIXT |
| Gateway | FIX-PTP |
| Ambiente de pruebas | reMarkets — `fix.remarkets.primary.com.ar`, puerto 9876, accesible por Internet, con alta autogestionada en `remarkets.primary.ventures` |
| Ambiente productivo | `fixgw.ptp.primary.com.ar`, puerto 9876 |
| Ventana de sesión FIX | 9:30 a 19:00 |
| Ventana de negociación | 10:00 a 17:30 |
| Intervalo de heartbeat | ≥ 10 segundos |
| Identificación de instrumentos | Por `Symbol`, único en cada mercado; `SecurityExchange = ROFX` |
| Conectividad recomendada | Línea punto a punto dedicada. Internet está habilitado pero A3 lo considera no confiable en alta volatilidad |
| Límites de caudal relevantes en Fase 1 | Solicitud de estado de orden: 100/s · Solicitud masiva de estado: **1/s** · Cancelación masiva: 1/s |

### 9.3 Requerimientos no funcionales del producto

| ID | Requerimiento |
|---|---|
| RNF-01 | El conector no pierde eventos: todo mensaje FIX de negocio recibido debe resultar en un mensaje MQ publicado o en un error registrado y alertado |
| RNF-02 | El conector no duplica eventos: el procesamiento es idempotente frente a reenvíos FIX y a *redelivery* de MQ |
| RNF-03 | La arquitectura separa las capacidades comunes de FIX, el adaptador específico de A3 y la integración con BBVA, de modo que incorporar otro mercado FIX no requiera modificar el núcleo |
| RNF-04 | Las credenciales nunca aparecen en logs, trazas, mensajes de error ni en el repositorio |
| RNF-05 | El conector soporta el reinicio del proceso sin pérdida de las secuencias de sesión |
| RNF-06 | El logging *raw* cumple el requisito de A3 de poder reconstruir la actividad diaria completa |
| RNF-07 | La configuración (endpoints, CompIDs, intervalos, colas, cuentas) es externalizable por ambiente, sin recompilación |

---

## 10. Hallazgos de la documentación A3 que condicionan el alcance

Estos son hallazgos del análisis del ROE v2.0.53 y del Manual de Conectividad que **cambian o acotan** lo que la propuesta técnica y el backlog borrador asumen. Cada uno tiene su decisión asociada en la sección 12.

| # | Hallazgo | Impacto |
|---|---|---|
| **H-1** | **No existe mensaje de cambio de contraseña en el ROE de A3.** El `Logon` (`35=A`) define únicamente `EncryptMethod` (98), `HeartBtInt` (108), `Username` (553), `Password` (554) y `DefaultApplVerID` (1137). No aparece el tag `NewPassword` (925) ni ningún mensaje de cambio de credenciales en el *Message Summary* de mensajes soportados | La estrategia de rotación diaria descripta en la propuesta técnica —secret con `<contraseña actual>` y `<nueva contraseña>`, poblando «una vez al día el mensaje de cambio de contraseña»— **no es implementable tal como está redactada** con este ROE. ✅ **Resuelto el 2026-09-16:** la gestión de contraseñas es administrativa y fuera de banda, y el conector aplica *hard stop* ante rechazo de credenciales. Ver §1.bis y **S-01** |
| **H-2** | **Los criterios de certificación de A3 incluyen envío de órdenes y suscripción a market data.** El Manual de Conectividad establece que los participantes deben completar «la conexión exitosa, la suscripción a datos de mercado, el envío de órdenes, y el manejo de errores» | La homologación de la Épica 3 es necesariamente **parcial**. ✅ **Resuelto el 2026-09-16: A3 acepta la homologación parcial de TCR/ER.** Queda despejado el riesgo número uno del compromiso del 31-dic; resta formalizar el acuerdo por escrito. Ver §1.bis y **S-02** |
| **H-3** | **`ResetSeqNumFlag` (141) no está documentado en el ROE** | La estrategia de manejo de secuencias al inicio de cada jornada (¿se reinician a 1 o continúan?) no está definida en la documentación disponible y debe confirmarse con A3. Afecta directamente el diseño de la persistencia de secuencias. → **S-05** |
| **H-4** | **El servicio de *drop copy* existe pero no está especificado en este ROE.** El Manual de Conectividad describe un usuario configurado que entrega, de forma independiente de la conexión de ruteo, la información de órdenes ingresadas y sus ejecuciones. El ROE FIX-PTP no lo documenta como tal | ✅ **Confirmado el 2026-09-16 como la modalidad del MVP.** A3 asocia la sesión a IDs de cuentas o de operadores y duplica en tiempo real los Execution Reports de esas cuentas. Ver §1.bis y **S-03**. Queda por confirmar si el perfil de sólo lectura admite consultas salientes |
| **H-5** | **El bloque `Parties` de los TCR por cuenta exige códigos CNV específicos de BBVA**: agente de negociación (`PartyRole=1`), Client ID (`3`), agente de compensación y liquidación (`4`), Executing Trader, Desk ID (`76`) y Customer Account (`24`) | Sin esos códigos no se puede emitir un `AD` por cuenta. Es una dependencia dura de BBVA para el MVP, y no figura en el backlog borrador |
| **H-6** | **La certificación de A3 tiene vigencia de un año** | Homologar en noviembre/diciembre de 2026 obliga a re-homologar en el mismo período de 2027, y a convivir con vencimientos escalonados si las épicas 4 y 5 se certifican después |
| **H-7** | **El gateway FIX-PTP entrega market data en Full Refresh, profundidad 10, 1 mensaje cada 500 ms por símbolo**, orientado a terminal humana u OMS. Mayor frecuencia o *incremental refresh* requieren los gateways FIX-PTP-HR o FIX-PTP-LL, este último **sólo disponible vía colocation** | Aunque Market Data es Épica 5, la elección de gateway condiciona la conectividad contratada y posiblemente la certificación. Debe decidirse en la Épica 1 |
| **H-8** | **A3 ofrece también una API REST/WebSocket** como alternativa a FIX, con integración más rápida pero menor performance | No cambia la decisión tomada (FIX), pero conviene dejar registrado por qué se descartó, para cerrar la discusión de forma permanente |
| **H-9** | **La ventana de sesión FIX (9:30–19:00) es más amplia que la de negociación (10:00–17:30)** | Implica un ciclo diario de sesión y define la franja donde ubicar tareas como la rotación de credenciales y la reconciliación de inicio de jornada. No está contemplado en el backlog borrador |
| **H-10** | **Cauciones estará disponible para operar recién a fines de 2026** | La validación funcional de Cauciones no puede cerrarse en la Fase 1. No afecta al MVP TCR/ER, pero sí a la planificación de la Épica 4 |
| **H-11** | **El acceso DMA exige control de riesgo *pre-trade* homologado** (saldo, márgenes, diferencias diarias, límites por segmento/instrumento, cantidad máxima y *kill button*), controlable en tiempo real por el participante | Sólo aplica si la operatoria del conector califica como DMA. Es una dependencia mayor de la Épica 4 que conviene aclarar ahora, porque puede requerir un proyecto en sí misma. → **S-06** |

---

## 11. Observaciones sobre el backlog borrador (Excel)

El Excel `ConectorFix_Backlog&Estimation - BBVA.xlsx` es una buena base de partida, pero tiene inconsistencias que hay que resolver antes de convertirlo en backlog ejecutable. Se listan para que el refinamiento las corrija, no como crítica al trabajo previo.

| # | Observación | Acción propuesta |
|---|---|---|
| **O-1** | **«Procesamiento de TCR» (US 13) está sin ningún detalle**: no tiene historia Connextra, ni criterios de aceptación, ni observaciones. Es la única historia del backlog en esa condición, y es precisamente la que da nombre al MVP | Elaborarla completa; es la historia de mayor prioridad del refinamiento |
| **O-2** | **«Procesamiento de TCR» está clasificada bajo la épica equivocada.** En la hoja *User Stories* aparece con `Epic ID = 5` (Market Data A3); en la hoja *Estimation* aparece bajo la épica «Procesamiento de Execution Reports», también con ID 5. TCR es **post-trade**, no market data | Reclasificar bajo la épica de procesamiento post-trade del MVP |
| **O-3** | **Numeración de US desalineada entre hojas.** La hoja *User Stories* asigna «Cerrar sesión FIX» a `Epic 1 / US 3`; la hoja *US Details* la asigna a `EpicID 2 / US_ID 3`. A partir de ahí, los `US_ID` corren una posición entre hojas | Unificar la numeración antes de cargar a Jira |
| **O-4** | **No hay ninguna historia de la Épica 1 (Discovery y Arquitectura)** salvo las de ambientes (épicas 9, 10 y 11). Faltan las que corresponden a entregables comprometidos: definición funcional aprobada, contratos MQ, mapeo FIX↔MQ, estrategia de observabilidad, estrategia de logging y gestión de contraseñas | Incorporarlas en el refinamiento de la Épica 1 |
| **O-5** | **«Consultar estado de una orden» (US 11) está redactada como si hubiera una interfaz de usuario**: «Se muestran estados FIX», «Se exponen timestamps», «Se muestran fills parciales». El conector no tiene UI. La propia observación del Excel lo aclara: «la consulta devuelve el estado de fix, no necesariamente el de la orden (no es un OMS)» | Reescribirla como consulta FIX (`H` / `AF`) con publicación del resultado en MQ, y separar la API REST asincrónica como capacidad deseable aparte |
| **O-6** | **Las épicas de ambientes (9, 10 y 11) suman entre 34 y 63 SP**, sobre un total de 118–228 SP. Es entre el 28% y el 29% del esfuerzo, y **depende de BBVA, no del equipo de desarrollo** | Tratarlas como dependencias con dueño y fecha explícitos, no como backlog del equipo. Son el principal riesgo de cronograma |
| **O-7** | **No se distingue entre recuperabilidad básica (MVP) y tolerancia a fallas (Épica 5).** Todas las historias de las épicas 2 (Recuperación y Consistencia) y 8 (Alta Disponibilidad) están con `Scope=1` sin indicación de fase, mientras que la propuesta técnica las separa en etapas distintas | Aplicar la separación de la [sección 5.4](#54-capacidades-transversales-dónde-corta-cada-una) |
| **O-8** | **«Recuperación después de reinicio» (US 19) incluye «Recupera posiciones locales»** | El conector no mantiene posiciones. Quitar ese criterio o reemplazarlo por recuperación del estado de sesión |
| **O-9** | **La hoja *Estimation* tiene las columnas corridas**: los criterios de aceptación aparecen bajo el encabezado «Activ. Critica» y la historia Connextra bajo «Details», mientras «Phase» contiene el valor 1 | Remapear al migrar a Jira; no confiar en los encabezados de esa hoja |
| **O-10** | **No hay historias de manejo de errores de protocolo**: `Reject` de sesión (`35=3`) con sus 18 razones, ni `Business Message Reject` (`35=j`). A3 evalúa explícitamente la gestión de errores en la certificación | Incorporarlas al MVP; son requisito de homologación |
| **O-11** | **No hay historias de Trading Session Status (`35=h`) ni de Account List (`UALR`/`UALT`/`UALI`)**, que son necesarias para interpretar los eventos y para componer las consultas TCR por cuenta | Incorporarlas al MVP |
| **O-12** | **La estimación mínima total (118 SP, ajustada a 153 SP) contra una velocidad de 15–30 SP/sprint** da entre 5 y 10 sprints para el alcance completo de la Fase 1 del Excel. El plan de trabajo compromete 5 sprints para las épicas 1 a 3 | Es consistente **sólo** en el extremo optimista, y el Excel incluye historias de las épicas 4 y 5. Al recortar al alcance real del MVP la holgura mejora, pero conviene re-estimar con el backlog refinado |
| **O-13** | **La hoja *Roadmap* sólo llega hasta noviembre** (Sp 0 a Sp 6, septiembre a noviembre) y omite diciembre | Extender el roadmap hasta el 31-dic para reflejar el compromiso real |

---

## 12. Riesgos, dependencias y decisiones abiertas

### 12.1 Decisiones abiertas — a resolver en la Épica 1

| ID | Pregunta | Impacto si no se resuelve | Propuesta del PO |
|---|---|---|---|
| **S-01** ✅ **RESUELTO 16-09** | **¿Cuál es el mecanismo real de cambio de contraseña en A3?** El ROE no define `NewPassword` (925) ni ningún mensaje de cambio de credenciales | La estrategia de rotación diaria de secrets descripta en la propuesta no es implementable. Bloquea la definición de seguridad y puede afectar la homologación | Consultar formalmente a A3 en la primera semana. Si no existe mecanismo por FIX, proponer a seguridad de BBVA una rotación gestionada fuera de banda (portal o solicitud a A3) con frecuencia acordada, y ajustar el contrato del secret a un único campo de contraseña vigente |
| **S-02** ✅ **RESUELTO 16-09** | **¿A3 acepta una homologación parcial limitada a sesión, consulta de estado y post-trade regular, sin envío de órdenes ni market data?** | Es el riesgo número uno del compromiso del 31-dic. Si A3 exige certificar el conjunto completo, la fecha no se sostiene con el alcance actual | Iniciar el contacto con `operaciones@a3mercados.com.ar` **en el sprint 0**, pidiendo el paquete de certificación y el acuerdo escrito del alcance parcial. Es la actividad de mayor prioridad del proyecto y no depende de ninguna otra |
| **S-03** ✅ **RESUELTO 16-09** | **¿De dónde provienen los Execution Reports si el conector no rutea órdenes?** | Sin tráfico de ER no hay nada que probar ni que homologar en el corazón del MVP | Combinar tres fuentes: (a) solicitar a A3 un **usuario de drop copy**, que entrega órdenes y ejecuciones de forma independiente al ruteo; (b) usar `Order Mass Status Request` (`AF`) como mecanismo de *pull* y reconciliación; (c) en reMarkets, generar el tráfico cargando órdenes manualmente desde eTrader. Confirmar (a) con A3 en la Épica 1 |
| **S-04** | **¿La normalización de ER y TCR hacia el modelo canónico de BBVA requiere enriquecimiento con datos del instrumento?** Los ER y TCR traen `Symbol` como string | Si la respuesta es sí, hay que adelantar `SecurityList` (`x`/`y`) al MVP. Es solo lectura, así que no rompe el corte, pero sí agrega alcance | Definirlo al cerrar el contrato MQ en la Épica 1. Recomendación: si los consumidores de BBVA necesitan más que el símbolo, adelantar `SecurityList` con carga diaria en memoria |
| **S-05** | **¿Cómo se manejan los números de secuencia entre jornadas?** ¿Se reinician a 1 al abrir la sesión diaria o continúan? `ResetSeqNumFlag` (141) no está documentado en el ROE | Afecta directamente el diseño de la persistencia y la lógica de detección de gaps | Consultar a A3 junto con S-01. Diseñar la persistencia de modo que ambos comportamientos sean configurables, para no depender de la respuesta |
| **S-06** | **¿La operatoria del conector califica como acceso DMA según A3?** | Si califica, la Épica 4 requiere un sistema homologado de control de riesgo *pre-trade*, que puede ser un proyecto en sí mismo | Aclararlo con A3 y con cumplimiento de BBVA durante la Épica 1, aunque el impacto sea en la Épica 4. Conocerlo temprano cambia la planificación del año |
| **S-07** | **¿Dónde se persisten las secuencias?** El Excel pregunta «validar con BBVA dónde se persiste (storage?)» y anota «se utiliza file storage» | Define si se necesita Sybase en el MVP o alcanza con almacenamiento en archivos | Recomendación del PO: archivos en almacenamiento persistente para el MVP, que es el patrón estándar de los motores FIX, y evaluar Sybase sólo si BBVA lo exige por política. Confirmar con arquitectura en la Épica 1 |
| **S-08** | **¿Qué framework MQ aprueba BBVA?** | Bloquea toda la implementación de publicación del MVP | Definición de BBVA, comprometida en la propuesta para las primeras etapas. Debe cerrarse antes del fin del sprint 1 |
| **S-09** | **¿Se incluye el sentido MQ → conector para comandos de consulta en el MVP?** (por ejemplo, que BBVA solicite una reconciliación o una consulta de trades) | Define si el MVP tiene una cola de entrada o es puramente saliente | Recomendación: incluirlo sólo si hay un caso de uso real de BBVA. Si no lo hay, el MVP publica de forma autónoma según su propia planificación y el sentido de entrada se abre recién en la Épica 4 |
| **S-10** | **¿La API REST asincrónica de consulta de estado entra en el alcance?** Está identificada como capacidad deseable, no mandatoria | Si entra, agrega alcance al MVP; si no, hay que sacarla del backlog | Recomendación: **no incluirla en la Fase 1**. Es deseable, no obligatoria, y su valor depende de decisiones de modelo de información que recién se toman en la Épica 1. Reevaluar al cierre de la Épica 3 |

### 12.2 Riesgos

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R-1** | **Los tiempos de A3 no dependen del equipo.** El plan indica que el máximo de la etapa de homologación «depende de tiempos de A3 Mercados» | Alto — pone en riesgo el 31-dic | Iniciar el contacto con A3 en el sprint 0, antes de tener código. Tratar la obtención del paquete de certificación y el acuerdo de alcance parcial como el primer entregable del proyecto |
| **R-2** | **Disponibilidad de los ambientes de BBVA** (Liberty y colas MQ) es precondición explícita de las etapas iniciales | Alto — las épicas de ambiente son ~29% del esfuerzo estimado y no las ejecuta el equipo de desarrollo | Asignar dueño y fecha por ambiente desde el sprint 0. Usar reMarkets, que es accesible por Internet con alta autogestionada, para no bloquear el desarrollo del conector mientras el ambiente BBVA se prepara |
| **R-3** | **Definición tardía del framework y de los contratos MQ** | Alto — bloquea toda la publicación del MVP | Es un entregable comprometido de la Épica 1. Escalar si no está cerrado al fin del sprint 1 |
| **R-4** | **Tratamiento incorrecto de mensajes duplicados o reenviados**, tanto por el mecanismo de recuperación de FIX como por el *redelivery* de MQ | Medio en Fase 1 (duplicación de eventos informativos), **crítico a partir de la Épica 4** (duplicación de órdenes) | Diseñar el procesamiento idempotente desde el MVP, aunque el costo del error todavía sea bajo. Probar explícitamente reenvío y *redelivery* |
| **R-5** | **Complejidad de la recuperación y sincronización de sesiones FIX** | Medio-alto | Definir los escenarios de recuperación explícitamente en la Épica 1 y validarlos con pruebas específicas en la Épica 2, incluyendo la reconciliación vía `AF` |
| **R-6** | **Java 25 sobre WebSphere Liberty** puede no estar soportado en la versión disponible en BBVA | Medio | Spike de despliegue «hola mundo» en la Épica 1, antes de comprometer código |
| **R-7** | **Disponibilidad de referentes de negocio y técnicos de BBVA** para resolver definiciones | Medio | Designar interlocutores desde el inicio y mantener una instancia regular de resolución de dudas |
| **R-8** | **Interpretación amplia de «TCR»** que arrastre todo el bloque post-trade del ROE | Medio — duplicaría el MVP | La acotación de la [sección 5.2](#52-matriz-de-mensajes-fix-por-épica) a `TrdType=0` debe quedar escrita en la definición de alcance y en cada historia |

### 12.3 Dependencias de BBVA

| Dependencia | Requerida para | Fecha límite sugerida |
|---|---|---|
| Framework/librería MQ aprobada | Épica 2 completa | Fin sprint 1 |
| Contratos de mensajes MQ validados | Épica 2 completa | Fin Épica 1 |
| Ambiente intive: Liberty + MQ operativos | Épica 2 | Fin sprint 1 |
| Ambiente BBVA: Liberty + MQ | Épica 3 (despliegue del entregable parcial) | Fin Épica 2 |
| Credenciales y coordenadas de A3 (reMarkets y producción) | Épica 2 | Sprint 0 / sprint 1 |
| Secret de credenciales con acceso de lectura | Épica 2 | Fin sprint 2 |
| Estructura de códigos CNV y cuentas para el bloque `Parties` | RF-21 (TCR por cuenta) | Fin Épica 1 |
| Referentes de negocio designados | Épica 1 | Sprint 0 |
| Conectividad de red hacia A3 (reglas de firewall, línea PaP o Internet) | Épica 2 | Fin sprint 1 |

---

## 13. Plan de entrega contra el 31-dic-2026

Tomando T0 = mediados de septiembre de 2026 y sprints de dos semanas:

| Etapa | Duración | Ventana estimada | Entregable de cierre |
|---|---|---|---|
| **Épica 1** — Discovery, Arquitectura y Ambientes | 2 sprints | sep → mediados de oct | Definición funcional, contratos MQ, arquitectura, ambientes, backlog refinado, S-01 a S-04 resueltos |
| **Épica 2** — MVP TCR/ER y Conectividad FIX | 2 sprints | mediados de oct → mediados de nov | Conector desplegado en ambiente intive, conectado a reMarkets, publicando en MQ |
| **Épica 3** — Homologación A3 y Aceptación BBVA | ≥ 1 sprint | mediados de nov → ¿? | Certificado A3 (parcial) y conformidad BBVA |
| **Holgura hasta el 31-dic** | ~4 semanas | dic | Absorbe demoras de A3 y corrección de defectos |

**Lectura del PO sobre la fecha (actualizada al 2026-09-16):** el camino crítico da aproximadamente 5 sprints —unas 10 semanas— y deja cerca de un mes de holgura. Con la aceptación de la homologación parcial ya confirmada por A3, **el riesgo de alcance quedó despejado** y la holgura pasa a cubrir riesgos de ejecución en lugar de una renegociación de alcance. Persiste el riesgo de **calendario**: los tiempos de ejecución de la certificación siguen dependiendo de A3.

En consecuencia, las prioridades del sprint 0 se reordenan:

1. **Solicitar a A3 el alta del usuario Drop Copy y acordar el mapeo de cuentas y operadores**, junto con el paquete de certificación y la confirmación de si el perfil de sólo lectura admite consultas salientes. Es ahora la gestión más urgente, porque **bloquea la historia central del MVP**: sin la sesión Drop Copy configurada no hay Execution Reports que procesar.
2. **Definir con el negocio qué cuentas y operadores de BBVA quedan asociados a la sesión.** Determina qué eventos verá el conector, y es precondición de la gestión anterior.
3. **Asignar dueño y fecha a los ambientes de BBVA** (R-2). Representan cerca del 29% del esfuerzo estimado y no los ejecuta el equipo de desarrollo.
4. **Formalizar por escrito el acuerdo de homologación parcial** ya aceptado verbalmente, junto con el paquete de certificación.

---

## 14. Criterios de aceptación de la Fase 1 (DoD de fase)

La Fase 1 se considera completa cuando:

- [ ] El conector establece y sostiene una sesión FIX con el ambiente de pruebas de A3 durante la ventana operativa completa (9:30–19:00), durante 5 días hábiles consecutivos, sin desconexiones no gestionadas.
- [ ] El conector consume los Execution Reports de A3 en sus seis variantes, los normaliza y los publica en MQ conforme al contrato acordado, con `correlation ID` verificable de punta a punta.
- [ ] El conector emite Trade Capture Report Requests por cuenta y por símbolo con `TrdType=0`, consume las respuestas encadenadas y las publica en MQ.
- [ ] El conector ejecuta consultas de estado puntuales y masivas respetando los límites de caudal de A3.
- [ ] Ante un corte de sesión, el conector reconecta, recupera los mensajes faltantes mediante Resend Request y reconcilia el estado vía Order Mass Status Request, **sin pérdida ni duplicación de eventos publicados** (verificado con una prueba de corte deliberado).
- [ ] Todo mensaje FIX enviado y recibido queda registrado en formato *raw* con *timestamp* y sesión, permitiendo reconstruir la actividad diaria completa.
- [ ] Los errores de protocolo (Reject de sesión y Business Message Reject) se procesan, registran, alertan y publican como eventos de error diferenciados.
- [ ] El pipeline de CI/CD despliega el conector en el ambiente intive de forma reproducible.
- [ ] Las credenciales se obtienen del secret de BBVA y no aparecen en ningún log ni traza.
- [ ] A3 emitió el certificado de homologación sobre el alcance acordado, o existe un acta formal de alcance parcial con las observaciones cerradas.
- [ ] BBVA ejecutó sus pruebas de aceptación sobre el ambiente intive y dejó constancia de conformidad funcional.
- [ ] No quedan defectos bloqueantes abiertos.
- [ ] El backlog de las Épicas 4 y 5 está refinado con el aprendizaje de la Fase 1 incorporado.

---

*Documento generado como insumo para el refinamiento de historias de usuario con el agente `po-expert-user-stories`.*
