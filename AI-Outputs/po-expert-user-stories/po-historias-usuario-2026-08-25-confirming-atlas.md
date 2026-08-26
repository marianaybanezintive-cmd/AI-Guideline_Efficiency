# Historias de Usuario — Portal Confirming (Atlas)

> **Versión:** v1.0.0 · **Fecha:** 2026-08-25
> **Fuente única de requerimientos:** `Confirming.xlsx` (hoja CONFIRMING) · POC https://marianaintive.github.io/atlas-confirming-poc/ (v2.11.4)
> **Autor:** PO (elaboración de historias) · **Producto:** Portal Confirming — Banco Atlas
> **POC / referencia de diseño:** https://marianaintive.github.io/atlas-confirming-poc/
> **Generado con:** skill `po-expert-user-stories`
> **Nota:** No se reutilizó ningún MD/documento generado previamente. Keys duplicados del Excel: 2ª FAC-05 → **FAC-06**; 2ª CON-03 (Eliminar FE) → **CON-12**.

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

Primera versión elaborada **solo** desde `Confirming.xlsx` + POC Confirming. Criterios de forma: tarjetas Connextra, AC numerados con tags, Gherkin en español, MSG inline, separación FE/HT según columna STACK del Excel, HITL de supuestos y spikes.

---

## 1. Criterio de elaboración y alcance

| Criterio | Decisión aplicada |
|----------|-------------------|
| **Filas tachadas** (Excel) | Ninguna tachada; todas candidatas |
| **Filas puntuadas / detalladas** | Elaboradas como tarjeta completa |
| **Escenarios del input** | Transcritos en *Escenarios fuente*; expandidos a AC + Gherkin |
| **Historias faltantes** | Solo en §10 (Login, ABM, Reportes, Dashboard de la POC) |
| **Identificadores** | Conservar issue_key; duplicados → FAC-06, CON-12 |
| **Idioma y formato** | Español; Gherkin ES |
| **OCR / escaneo** | **FUERA** (S-01) |
| **HITL** | SUP-01…10 confirmados; S-01 fuera; S-02…08 confirmados |

| Tipo | Significado |
|------|-------------|
| `HU-FE` | Historia con impacto principal en Front End |
| `HU-BE` | Historia de valor vía backend/notificación (si aplica) |
| `HT` | Historia técnica (endpoint BFF/BE) |
| `TAREA` | Habilitador de infraestructura o configuración |

---

## 2. Matriz de inclusión / desestimación

| Fila | Key | Summary | Tipo | Estado | Motivo |
|-----:|-----|---------|------|--------|--------|
| 3 | FAC-01 | Botonera Cargar Factura individual | HU-FE | ✅ Incluida | Excel + modal POC |
| 4 | FAC-02 | Carga masiva template/archivo | HU-FE | ✅ Incluida | OCR excluido (S-01) |
| 5 | FAC-03 | GET obtenerInfoEnte | HT | ✅ Incluida | Reuso MAGIA |
| 6 | FAC-04 | Multimoneda USD/PYG | HU-FE | ✅ Incluida | Excel + POC |
| 7 | FAC-05 | POST cargarFactura | HT | ✅ Incluida | Excel |
| 8 | FAC-06 | POST notificaciónNuevaFactura | HT | ✅ Incluida | Key propuesto (era FAC-05 dup.) |
| 9 | CON-01 | Filtros / Grilla / FV-FNV-FNO | HU-FE | ✅ Incluida | Excel + POC |
| 10 | CON-03 | GET grillafacturas | HT | ✅ Incluida | Excel |
| 11 | CON-02 | Grilla acciones | HU-FE | ✅ Incluida | Excel + POC |
| 12 | CON-12 | Acción Eliminar | HU-FE | ✅ Incluida | Key propuesto (era CON-03 dup.) |
| 13 | CON-04 | Editar fecha de pago | HU-FE | ✅ Incluida | Excel + POC |
| 14 | CON-05 | Aprobar EGP (factura) | HU-FE | ✅ Incluida | Distinto de SIM-05 |
| 15 | CON-06 | PATCH actualizarfactura | HT | ✅ Incluida | Excel |
| 16 | CON-07 | Información crediticia | HU-FE | ✅ Incluida | Excel |
| 17 | CON-08 | GET info ente financiera | HT | ✅ Incluida | Reuso MAGIA |
| 18 | CON-09 | Máquina de estados | HT | ✅ Incluida | BE fuente de verdad |
| 19 | CON-10 | GET estados | HT | ✅ Incluida | Excel |
| 20 | CON-11 | Habilitar / Bloquear | HU-FE | ✅ Incluida | Excel |
| 21 | SIM-01 | Simular individual/múltiple | HU-FE | ✅ Incluida | Excel + POC |
| 22 | SIM-02 | GET simularAdelanto | HT | ✅ Incluida | Excel |
| 23 | SIM-03 | POST generarAdelanto | HT | ✅ Incluida | Excel |
| 24 | SIM-04 | POST notificaciónAdelanto | HT | ✅ Incluida | Excel |
| 25 | SIM-05 | Aprobar/Rechazar adelanto | HU-FE | ✅ Incluida | Excel |

**Resumen:** 23 filas Excel → **12 HU-FE** + **11 HT** incluidas · **0** desestimadas · OCR como capacidad **fuera** (no genera tarjeta).

---

## 3. Contexto de solución, actores y supuestos

### 3.1 Perfiles de usuario (actores / dominios)

| Dominio | Roles / perfiles (POC) | Operación típica en Confirming |
|---------|------------------------|--------------------------------|
| BANCO | Admin / operador AD | Visión amplia, soporte, ABM (fuera de este Excel) |
| EGP | Cargador / Aprobador | Carga, habilitar/bloquear, aprobar factura y adelanto, info crediticia |
| PROVEEDOR | Cliente Atlas / No cliente | Carga, simular/solicitar adelanto, seguimiento desembolso |

### 3.2 Componentes involucrados

- FE Portal Confirming (pantalla Confirming, modales carga/edición/simulación)
- BFF Confirming (orquestación, agregación, notificaciones)
- BE Confirming (dominio factura, máquina de estados, freeze de límite)
- MAGIA-120 / MAGIA-122 (info ente) — existente
- CORE bancario (cuenta préstamo / desembolso)
- Canal de notificaciones (email / in-app según configuración ABM — fuera de Excel)

### 3.3 Supuestos (a confirmar con el equipo técnico)

| # | Supuesto | Confirmación *(post HITL)* |
|---|----------|---------------------------|
| SUP-01 | Alcance de esta entrega = Confirming del Excel; Login/ABM/Reportes/Dashboard POC → §10 | confirmado — sin cambios |
| SUP-02 | FAC-03 y CON-08 = reuso MAGIA-120/122 (cableado, no reescritura) | confirmado — sin cambios |
| SUP-03 | Escaneo OCR = Could + spike; luego S-01 lo dejó **FUERA** | confirmado — sin cambios; S-01 → fuera |
| SUP-04 | Eliminar = baja lógica | confirmado — sin cambios |
| SUP-05 | Reglas 30 días Vencida / NO ELEGIBLE según CON-09 | confirmado — sin cambios |
| SUP-06 | Monedas solo PYG y USD | confirmado — sin cambios |
| SUP-07 | Confirmación de simulación freeza límite (API − freezado) | confirmado — sin cambios |
| SUP-08 | Solicitante ≠ cargador; cutoff 17:00 PY; revert freeze si CORE falla | confirmado — sin cambios |
| SUP-09 | Pestañas FV / FNV / FNO según estados listados | confirmado — sin cambios |
| SUP-10 | Renombrar duplicados FAC-06 y CON-12 | confirmado — sin cambios |

---

## 4. Reglas de negocio transversales (RN)

| ID | Regla | Fuente |
|----|-------|--------|
| **RN-01** | Solo se persisten facturas cuyo EGP y Proveedor existen y están **activos** | FAC-01, FAC-02, FAC-05 |
| **RN-02** | Toda factura nace en estado **Pendiente** | CON-09, FAC-05 |
| **RN-03** | Si vencimiento documental &lt; 30 días → **Vencida** (auto). Si fecha de pago &lt; 30 días → **NO ELEGIBLE**; EGP puede corregir fecha de pago y rehabilitar según máquina | CON-09, CON-04, SUP-05 |
| **RN-04** | Si Fecha Pago se omite en carga, se usa Fecha de vencimiento | POC modal carga |
| **RN-05** | Monedas operables: **PYG** y **USD** | FAC-04, SUP-06 |
| **RN-06** | Eliminación de factura = **baja lógica** | CON-12, CON-06, SUP-04 |
| **RN-07** | Límite a mostrar / disponible = límite API − límite freezado; al confirmar simulación se freeza | CON-07, SIM-01, SUP-07 |
| **RN-08** | Simulación múltiple exige mismo EGP + mismo Proveedor + misma moneda | SIM-01 |
| **RN-09** | Quien solicita adelanto no puede ser quien cargó la factura; solo antes de las 17:00 (hora Paraguay) | SIM-03, SUP-08 |
| **RN-10** | Notificaciones de alta/adelanto solo se envían en flujos **OK** | FAC-06, SIM-04, S-05 |
| **RN-11** | Máquina de estados: **BE** es fuente de verdad; BFF orquesta | CON-09, S-02 |
| **RN-12** | Ventana de n días (default **5 días hábiles**, configurable) entre aprobación EGP y solicitud de adelanto | SIM-02, S-03 |

---

## 5. Catálogo de mensajes de UI

| Código | Contexto | Mensaje |
|--------|----------|---------|
| MSG-01 | Validación entes | "El EGP o Proveedor indicado no existe o no está activo. Verificá los datos e intentá nuevamente." |
| MSG-02 | Carga OK | "Factura cargada correctamente." |
| MSG-03 | Carga error | "No pudimos cargar la factura. Intentá nuevamente." |
| MSG-04 | Archivo inválido | "El archivo no tiene el formato esperado. Descargá el template e intentá nuevamente." |
| MSG-05 | Resultado masivo | "Carga masiva finalizada: {ok} correctas, {error} con error." |
| MSG-06 | Moneda requerida | "Seleccioná la moneda de la factura." |
| MSG-07 | Grilla vacía | "No hay facturas para los filtros seleccionados." |
| MSG-08 | Desembolso | "Desembolso en curso..." |
| MSG-09 | Sin permiso | "No tenés permiso para esta acción." |
| MSG-10 | Eliminar OK | "Factura eliminada correctamente." |
| MSG-11 | Eliminar error | "No pudimos eliminar la factura. Intentá nuevamente." |
| MSG-12 | Warning 30 días | "Atención: con esta fecha de pago la factura quedará NO ELEGIBLE (quedan menos de 30 días)." |
| MSG-13 | Fecha pago OK | "Fecha de pago actualizada." |
| MSG-14 | Aprobación EGP factura | "Factura aprobada por el EGP." |
| MSG-15 | Rechazo EGP factura | "Factura rechazada por el EGP." |
| MSG-16 | Error decisión EGP | "No pudimos registrar la decisión del EGP. Intentá nuevamente." |
| MSG-17 | Info crediticia | "No pudimos obtener la información crediticia. Reintentá más tarde." |
| MSG-18 | Habilitar OK | "{n} factura(s) habilitada(s)." |
| MSG-19 | Bloquear OK | "{n} factura(s) bloqueada(s)." |
| MSG-20 | Transición parcial | "Algunas facturas no admiten esta transición y fueron omitidas." |
| MSG-21 | Error estado | "No pudimos actualizar el estado. Intentá nuevamente." |
| MSG-22 | Simulación mezcla | "Para simular múltiples facturas deben ser del mismo EGP, Proveedor y moneda." |
| MSG-23 | Disclaimer simulación | "Los valores simulados son estimativos y pueden variar al confirmar la operación." |
| MSG-24 | Límite excedido | "El monto supera el límite de crédito disponible del EGP." |
| MSG-25 | Freeze OK | "Simulación confirmada. El límite crediticio fue reservado." |
| MSG-26 | Adelanto aprobado | "Adelanto aprobado. Se inicia el proceso de desembolso." |
| MSG-27 | Adelanto rechazado | "Adelanto rechazado." |

---
## 6. Historias de usuario funcionales (tarjetas de backlog)
### FAC-01 — Cargar factura individual desde botonera Confirming
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | FAC — Carga de facturas |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | FAC-03, FAC-05 |
| **Habilita** | FAC-06 |
| **Pantalla POC** | Confirming → Cargar Nueva Factura |

#### Historia
```
Como usuario del Portal Confirming (EGP / Proveedor / Banco según permiso)
quiero cargar una factura de forma individual desde la botonera global
para registrar el documento y dejarlo disponible en la grilla en estado Pendiente
```

#### Valor de negocio
 Habilita el ingreso unitario de facturas al flujo de confirming con validación de entes activos.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario Cargar facturas individual
-Escenario de VALIDACION que el EGP y PROVEEDOR asociados a la factura a guardar exista y esté activo

```

#### Criterios de aceptación

1. [Feliz] Desde Confirming, al pulsar "Cargar Factura" se abre el modal "Cargar Nueva Factura" con sección de carga individual y campos: Nro. Factura*, Empresa (EGP)*, Proveedor*, Fecha emisión*, Fecha vencimiento*, Moneda*, Monto*, Fecha Pago (opcional), Timbrado*, Estado Inicial (Pendiente).
2. [Feliz] Si omito Fecha Pago, el sistema usa la fecha de vencimiento (RN-04).
3. [Validación] Si EGP o Proveedor no existen o no están activos, no se guarda y veo MSG-01: "El EGP o Proveedor indicado no existe o no está activo. Verificá los datos e intentá nuevamente."
4. [Feliz] Con datos válidos y POST OK, la factura aparece en FV/Pendiente y veo MSG-02: "Factura cargada correctamente."
5. [Error] Si falla el guardado, veo MSG-03: "No pudimos cargar la factura. Intentá nuevamente." y no se crea el registro.


#### Escenarios BDD
```gherkin
Característica: Carga individual de factura
  Escenario: Carga exitosa con entes activos
    Dado que estoy en la pantalla Confirming con permiso de carga
    Y existen un EGP y un Proveedor activos
    Cuando abro "Cargar Factura" y completo los campos obligatorios
    Y confirmo el alta
    Entonces veo el mensaje MSG-02: "Factura cargada correctamente."
    Y la factura figura en Facturas Vigentes con estado Pendiente

  Escenario: Validación de ente inexistente o inactivo
    Dado que el Proveedor asociado no está activo
    Cuando intento guardar la factura
    Entonces veo el mensaje MSG-01: "El EGP o Proveedor indicado no existe o no está activo. Verificá los datos e intentá nuevamente."
    Y no se crea la factura

```

#### Fuera de alcance

- Carga masiva y escaneo OCR (FAC-02 / S-01 fuera)
- Notificación al EGP (FAC-06)


#### Notas / preguntas abiertas

- Depende de FAC-03/FAC-05 para validación y persistencia.


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### FAC-02 — Carga masiva de facturas (template + archivo)
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | FAC — Carga de facturas |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | FAC-03, FAC-05 |
| **Habilita** | FAC-06 |
| **Pantalla POC** | Confirming → Carga masiva |

#### Historia
```
Como usuario del Portal Confirming con permiso de carga
quiero descargar un template y cargar múltiples facturas desde archivo
para agilizar el alta masiva sin carga manual una a una
```

#### Valor de negocio
 Reduce tiempo operativo de onboarding de facturas al confirming.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario Cargar facturas masivo: descargar template
-Escenario Cargar facturas masico: cargar desde archivo
-Escenario scanear facturas? → FUERA (S-01)
-Escenario de VALIDACION que el EGP y PROVEEDOR asociados a la factura a guardar exista y esté activo

```

#### Criterios de aceptación

1. [Feliz] En el modal de carga, la sección masiva permite descargar template (.xls/.xlsx/.csv) con columnas: Nro. Factura, Empresa (EGP), Proveedor, Fecha emisión, Fecha vencimiento, Moneda, Monto, Fecha Pago, Timbrado.
2. [Feliz] Puedo subir un archivo válido; el sistema procesa fila a fila y muestra "Resultado de carga masiva" con OK / error por fila.
3. [Validación] Filas con EGP/Proveedor inexistente o inactivo se rechazan con detalle; las válidas se persisten (RN-01).
4. [Error] Archivo con formato inválido → MSG-04: "El archivo no tiene el formato esperado. Descargá el template e intentá nuevamente."
5. [Feliz] Al finalizar, veo MSG-05: "Carga masiva finalizada: {ok} correctas, {error} con error."


#### Escenarios BDD
```gherkin
Característica: Carga masiva de facturas
  Escenario: Descarga de template
    Dado que abro Cargar Factura
    Cuando solicito descargar el template
    Entonces obtengo un archivo con las columnas definidas en la POC

  Escenario: Carga parcial con validación de entes
    Dado un archivo con 2 filas válidas y 1 con proveedor inactivo
    Cuando proceso la carga masiva
    Entonces se crean solo las 2 facturas válidas
    Y el resultado detalla el error de la fila inválida
    Y veo el mensaje MSG-05: "Carga masiva finalizada: {ok} correctas, {error} con error."

```

#### Fuera de alcance

- Escaneo / OCR de facturas (S-01 confirmado FUERA)
- Edición inline de filas fallidas (re-subir archivo)


#### Notas / preguntas abiertas

- Escenarios de OCR no se implementan en esta entrega.


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S⚠️ T✅

---

### FAC-04 — Selector de moneda USD / PYG al cargar factura
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | FAC — Carga de facturas |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | FAC-01 |
| **Habilita** | SIM-01 |
| **Pantalla POC** | Confirming → Cargar (Moneda) |

#### Historia
```
Como usuario que carga facturas
quiero elegir la moneda USD o PYG
para registrar el monto en la divisa correcta del confirming
```

#### Valor de negocio
 Soporta operaciones multimoneda alineadas a línea de crédito del EGP.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario selector de moneda USD / PYG

```

#### Criterios de aceptación

1. [Feliz] En carga individual (y template masivo) el campo Moneda ofrece solo PYG y USD (RN-05).
2. [Validación] Sin moneda seleccionada no se habilita guardar; veo MSG-06: "Seleccioná la moneda de la factura."
3. [Feliz] La moneda queda visible en grilla y condiciona simulación múltiple (mismo EGP-Proveedor-moneda).


#### Escenarios BDD
```gherkin
Característica: Multimoneda en carga
  Escenario: Selección PYG
    Dado el modal de carga individual
    Cuando selecciono moneda PYG y completo el resto de campos
    Entonces la factura se guarda en PYG y se muestra así en la grilla

```

#### Fuera de alcance

- Otras monedas distintas de PYG/USD


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-01 — Pantalla Confirming: filtros, grilla y pestañas FV / FNV / FNO
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-03 |
| **Habilita** | CON-02, CON-11, SIM-01 |
| **Pantalla POC** | Confirming (grilla) |

#### Historia
```
Como usuario del Portal Confirming
quiero ver facturas filtradas en pestañas por vigencia/operabilidad
para operar solo sobre el conjunto relevante a cada estado
```

#### Valor de negocio
 Organiza el trabajo diario de EGP/Proveedor/Banco sobre el ciclo de vida de facturas.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario de Filtros de Busqueda
-Escenario de campos a Mostrar en la Grilla
-Escenario de pestañas FV/FNV/FNO de la grilla según estado de la facturas

```

#### Criterios de aceptación

1. [Feliz] Existe pantalla Confirming con pestañas: Facturas Vigentes (Pendiente, Habilitada, Bloqueada, Pendiente aprobación EGP, Pendiente de desembolso), Facturas No Vigentes (Financiada, Vencida), Facturas No Operables (NO ELEGIBLE) — RN-02.
2. [Feliz] Filtros: Buscar, Fecha de Vencimiento, Fecha de Pago, Estado (lista alineada a máquina de estados).
3. [Feliz] Columnas grilla: Nro. Factura, Empresa (EGP), Proveedor, Fecha emisión, Fecha vencimiento, Moneda, Monto, Fecha Pago, Timbrado, Estado, Eliminar, Acciones (según POC).
4. [Feliz] Botonera global visible según selección/permisos: Habilitar, Bloquear, Simular, Cargar Factura.
5. [Alternativo] Sin resultados → MSG-07: "No hay facturas para los filtros seleccionados."


#### Escenarios BDD
```gherkin
Característica: Grilla Confirming
  Escenario: Pestaña FV muestra solo estados vigentes
    Dado facturas en Pendiente y Financiada
    Cuando abro la pestaña Facturas Vigentes
    Entonces veo la Pendiente y no veo la Financiada

  Escenario: Filtro por estado
    Dado varias facturas Habilitadas y Bloqueadas
    Cuando filtro Estado = Habilitada
    Entonces la grilla lista solo Habilitadas

```

#### Fuera de alcance

- Acciones de fila (CON-02+)
- ABM de entes


#### Notas / preguntas abiertas

- Depende de CON-03 (GET grilla).


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S⚠️ T✅

---

### CON-02 — Botonera de acciones por factura en la grilla
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-01 |
| **Habilita** | CON-12, CON-04, CON-05 |
| **Pantalla POC** | Confirming → Acciones |

#### Historia
```
Como usuario en la grilla Confirming
quiero ver las acciones disponibles por factura según estado
para iniciar eliminar, editar fecha de pago, aprobar EGP o ver desembolso en curso
```

#### Valor de negocio
 Expone el punto de entrada UX a cada flujo operativo sin ejecutar aún la lógica completa (flujos en otras HUs).


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario de boton Eliminar Factura, siempre visible y activo
-Escenario de botón Editar Fecha de Pago, siempre visible y activo
-Escenario de botón Aprobar EGP, solo se muestra para facturas en estado Pendiente de Aprobación EGP
-Escenario de Mensaje de Espera en desembolso: "Desembolso en curso..." con ruedita animada, solo para Pendiente de Desembolso

```

#### Criterios de aceptación

1. [Feliz] Columna Acciones muestra Eliminar y Editar Fecha de Pago siempre visibles/activos (sujeto a permiso de rol).
2. [Feliz] Botón Aprobar EGP solo si estado = Pendiente de Aprobación EGP.
3. [Feliz] Si estado = Pendiente de Desembolso, en acciones se muestra MSG-08: "Desembolso en curso..." con indicador animado (sin botones conflictivos) — S-07 polling 15–30s.
4. [Alternativo] Sin permiso: acciones no disponibles o deshabilitadas con MSG-09: "No tenés permiso para esta acción."


#### Escenarios BDD
```gherkin
Característica: Acciones por fila
  Escenario: Aprobar EGP visible solo en estado correcto
    Dado una factura Pendiente de Aprobación EGP y otra Habilitada
    Cuando visualizo la grilla
    Entonces solo la primera muestra el botón Aprobar EGP

  Escenario: Desembolso en curso
    Dado una factura Pendiente de Desembolso
    Cuando miro la columna Acciones
    Entonces veo el mensaje MSG-08: "Desembolso en curso..."
    Y un indicador animado

```

#### Fuera de alcance

- Implementación de modales (CON-12, CON-04, CON-05)


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-12 — Eliminar factura con modal de confirmación
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Usuario Confirming |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-02, CON-06 |
| **Habilita** | — |
| **Pantalla POC** | Confirming → Eliminar |

#### Historia
```
Como usuario con permiso
quiero eliminar una factura desde la grilla con confirmación
para retirar del operable documentos cargados por error (baja lógica)
```

#### Valor de negocio
 Corrige errores de carga sin borrar físicamente el historial (SUP-04 / RN-06).


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario modal de confirmación del boton Eliminar Factura, con los datos de la factura y boton de confirmar

```

#### Criterios de aceptación

1. [Feliz] Al pulsar Eliminar se abre modal con datos clave de la factura y acciones Confirmar / Cancelar.
2. [Feliz] Al confirmar, se aplica baja lógica (RN-06); la factura deja de operarse en grillas vigentes según regla de proyección; veo MSG-10: "Factura eliminada correctamente."
3. [Alternativo] Cancelar cierra el modal sin cambios.
4. [Error] Falla de API → MSG-11: "No pudimos eliminar la factura. Intentá nuevamente."


#### Escenarios BDD
```gherkin
Característica: Eliminar factura
  Escenario: Confirmación de baja lógica
    Dado una factura Pendiente en la grilla
    Cuando pulso Eliminar y confirmo en el modal
    Entonces veo el mensaje MSG-10: "Factura eliminada correctamente."
    Y la factura ya no aparece como operable en FV

```

#### Fuera de alcance

- Borrado físico en base
- Restaurar factura eliminada


#### Notas / preguntas abiertas

- Key propuesto (Excel tenía CON-03 duplicado) → CON-12 (SUP-10).


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-04 — Editar fecha de pago con warning de NO ELEGIBLE
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | EGP / autorizado |
| **Dominios** | EGP/todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-02, CON-06, CON-09 |
| **Habilita** | — |
| **Pantalla POC** | Confirming → Editar fecha de pago |

#### Historia
```
Como usuario EGP / operador autorizado
quiero editar la fecha de pago de una factura
para evitar o corregir el estado NO ELEGIBLE cuando quedan menos de 30 días
```

#### Valor de negocio
 Recupera facturas operables ajustando la fecha de pago (RN-03).


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario modal de confirmación del boton Editar Fecha de Pago de Factura, con los datos de la factura y boton de confirmar (con warning de cantidad de dias para que pase a NO Elegible)

```

#### Criterios de aceptación

1. [Feliz] Modal "Editar fecha de pago" muestra factura y campo Fecha de Pago.
2. [Validación] Si la nueva fecha deja menos de 30 días, muestro MSG-12: "Atención: con esta fecha de pago la factura quedará NO ELEGIBLE (quedan menos de 30 días)."
3. [Feliz] Al confirmar, se actualiza vía PATCH; si la fecha vuelve a ≥30 días desde hoy, el estado puede pasar a Habilitada según máquina de estados (RN-03); MSG-13: "Fecha de pago actualizada."
4. [Alternativo] Cancelar no persiste cambios.


#### Escenarios BDD
```gherkin
Característica: Editar fecha de pago
  Escenario: Warning por proximidad a 30 días
    Dado una factura con fecha de pago a 25 días
    Cuando abro Editar Fecha de Pago
    Entonces veo el mensaje MSG-12: "Atención: con esta fecha de pago la factura quedará NO ELEGIBLE (quedan menos de 30 días)."

  Escenario: Corrección que rehabilita
    Dado una factura NO ELEGIBLE
    Cuando el EGP setea una fecha de pago con ≥30 días y confirma
    Entonces la factura deja FNO y pasa a estado operable según RN-03
    Y veo el mensaje MSG-13: "Fecha de pago actualizada."

```

#### Fuera de alcance

- Edición de otros campos de la factura


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-05 — Aprobar o rechazar factura pendiente de aprobación EGP
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Aprobador EGP |
| **Dominios** | EGP |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-02, CON-06 |
| **Habilita** | SIM-01 |
| **Pantalla POC** | Confirming → Aprobar EGP |

#### Historia
```
Como aprobador EGP
quiero aprobar o rechazar (con o sin motivo) una factura en Pendiente de Aprobación EGP
para autorizar que continúe el flujo hacia el adelanto/desembolso
```

#### Valor de negocio
 Control crediticio del EGP antes de avanzar operaciones (paso 1 de S-04).


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario modal de confirmación del boton Aprobar EGP, con los datos de la factura y boton de confirmar (misma información que el modal de Simulación, con datos bloqueados) y opciones Aprobar, Rechazar (con o sin motivo)

```

#### Criterios de aceptación

1. [Feliz] Modal muestra información tipo simulación en solo lectura + acciones Aprobar / Rechazar.
2. [Feliz] Aprobar cambia estado según máquina (avanza flujo); MSG-14: "Factura aprobada por el EGP."
3. [Feliz] Rechazar permite motivo opcional (S-08); MSG-15: "Factura rechazada por el EGP."
4. [Validación] Solo disponible en Pendiente de Aprobación EGP (CON-02).
5. [Error] Fallo API → MSG-16: "No pudimos registrar la decisión del EGP. Intentá nuevamente."


#### Escenarios BDD
```gherkin
Característica: Aprobación EGP de factura
  Escenario: Aprobar
    Dado una factura Pendiente de Aprobación EGP
    Cuando abro Aprobar EGP y confirmo Aprobar
    Entonces veo el mensaje MSG-14: "Factura aprobada por el EGP."
    Y el estado deja de ser Pendiente de Aprobación EGP

  Escenario: Rechazar sin motivo
    Dado el modal de Aprobar EGP
    Cuando elijo Rechazar sin completar motivo
    Entonces la operación se acepta
    Y veo el mensaje MSG-15: "Factura rechazada por el EGP."

```

#### Fuera de alcance

- Aprobación/rechazo de la simulación de adelanto (SIM-05 — flujo distinto, S-04)


#### Notas / preguntas abiertas

- Distinto de SIM-05 (confirmado S-04).


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-07 — Cabecera de información crediticia EGP y Proveedor
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Aprobador EGP |
| **Dominios** | EGP |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-08 |
| **Habilita** | CON-05, SIM-05 |
| **Pantalla POC** | Confirming → Info crediticia |

#### Historia
```
Como aprobador EGP
quiero ver información crediticia del EGP y del Proveedor
para decidir con contexto límites, tasas y morosidad al aprobar adelantos
```

#### Valor de negocio
 Reduce riesgo de aprobación a ciegas; límite mostrado = límite API − freezado (RN-07).


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario cabecera de información financiera del EGP: RUC, Razón Social, Limites, Tasas
-Escenario cabecera de información financiera del Proveedor: RUC, Razón Social, creditos activos, estado de morosidad
-Escenario Calculo de Limite de credito a mostrar = limite de credito obtenido desde la API - Limite freezado

```

#### Criterios de aceptación

1. [Feliz] Cabecera/panel EGP: RUC, Razón Social, Límites, Tasas; límite disponible = API − freezado (RN-07).
2. [Feliz] Cabecera Proveedor: RUC, Razón Social, créditos activos, estado de morosidad.
3. [Error] Si falla info ente → MSG-17: "No pudimos obtener la información crediticia. Reintentá más tarde."
4. [Feliz] Visible en contexto de aprobación/simulación para dominio EGP.


#### Escenarios BDD
```gherkin
Característica: Info crediticia
  Escenario: Cálculo de límite disponible
    Dado límite API 1000 y freezado 200
    Cuando consulto la cabecera EGP
    Entonces el límite a mostrar es 800

```

#### Fuera de alcance

- Edición de límites (ABM/core)


#### Notas / preguntas abiertas

- Consume CON-08 / MAGIA-120-122.


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### CON-11 — Habilitar y bloquear facturas en lote desde botonera
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | CON — Grilla Confirming |
| **Actor** | Usuario autorizado |
| **Dominios** | todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-01, CON-06, CON-09 |
| **Habilita** | SIM-01 |
| **Pantalla POC** | Confirming → Habilitar/Bloquear |

#### Historia
```
Como usuario autorizado
quiero habilitar o bloquear una o varias facturas desde la botonera global
para controlar qué documentos pueden avanzar a simulación/adelanto
```

#### Valor de negocio
 Gestión masiva del estado operable antes del adelanto.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario Habilitar Factura: cambio de estado de multiples facturas en estados válidos (pendiente/bloqueado)
-Escenario Bloquear Factura: cambio de estado de multiples facturas en estados válidos (pendiente/habilitado/pendiente de aprobacion de EGP)

```

#### Criterios de aceptación

1. [Feliz] Selecciono N facturas y Habilitar: solo transicionan desde Pendiente o Bloqueada → Habilitada; MSG-18: "{n} factura(s) habilitada(s)."
2. [Feliz] Bloquear: desde Pendiente, Habilitada o Pendiente de Aprobación EGP → Bloqueada; MSG-19: "{n} factura(s) bloqueada(s)."
3. [Validación] Si alguna selección no admite la transición, no se aplica a esa fila y veo MSG-20: "Algunas facturas no admiten esta transición y fueron omitidas."
4. [Error] Fallo total → MSG-21: "No pudimos actualizar el estado. Intentá nuevamente."


#### Escenarios BDD
```gherkin
Característica: Habilitar / Bloquear
  Escenario: Habilitar múltiples desde Pendiente
    Dado 3 facturas Pendiente seleccionadas
    Cuando pulso Habilitar
    Entonces pasan a Habilitada
    Y veo el mensaje MSG-18: "{n} factura(s) habilitada(s)."

```

#### Fuera de alcance

- Transiciones automáticas por fecha (CON-09)


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

### SIM-01 — Simular adelanto individual y múltiple
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | SIM — Simulación y adelanto |
| **Actor** | Proveedor / autorizado |
| **Dominios** | PROVEEDOR/todos |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-11, SIM-02 |
| **Habilita** | SIM-03, SIM-05 |
| **Pantalla POC** | Confirming → Simulación de Adelanto |

#### Historia
```
Como usuario Proveedor / operador autorizado
quiero simular el adelanto de una o varias facturas Habilitadas
para conocer montos estimados y confirmar una solicitud de préstamo
```

#### Valor de negocio
 Transparencia financiera antes de comprometer límite y generar solicitud al CORE.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Simular múltiples misma fecha de pago → 1 cuota si mismo EGP-Proveedor-moneda
-Simular múltiples fechas distintas → n cuotas si mismo EGP-Proveedor-moneda
-Simular individual → 1 cuota
-Validación límite crédito (grisar las que exceden)
-Confirmación freeza límite
-Disclaimer valores estimativos

```

#### Criterios de aceptación

1. [Feliz] Solo facturas Habilitadas seleccionables para Simular; si mezcla EGP/Proveedor/moneda distinta → MSG-22: "Para simular múltiples facturas deben ser del mismo EGP, Proveedor y moneda."
2. [Feliz] Modal "Simulación de Adelanto" con cálculos; siempre MSG-23: "Los valores simulados son estimativos y pueden variar al confirmar la operación."
3. [Validación] Facturas que exceden límite disponible se grisán/bloquean (RN-07); MSG-24: "El monto supera el límite de crédito disponible del EGP."
4. [Feliz] Misma fecha de pago → préstamo 1 cuota; fechas distintas → n cuotas (S-06).
5. [Feliz] Al confirmar simulación se freeza el límite (SUP-07) y se avanza a generación (SIM-03); MSG-25: "Simulación confirmada. El límite crediticio fue reservado."
6. [Alternativo] Cancelar no freeza ni genera solicitud.


#### Escenarios BDD
```gherkin
Característica: Simulación de adelanto
  Escenario: Múltiple misma moneda y EGP-Proveedor
    Dado 2 facturas Habilitadas mismo EGP-Proveedor-moneda y distinta fecha de pago
    Cuando pulso Simular
    Entonces el modal muestra cálculo unificado en n cuotas
    Y veo el mensaje MSG-23: "Los valores simulados son estimativos y pueden variar al confirmar la operación."

  Escenario: Exceso de límite
    Dado facturas cuyo monto supera el disponible
    Cuando intento incluirlas en la simulación
    Entonces quedan bloqueadas/grisadas
    Y veo el mensaje MSG-24: "El monto supera el límite de crédito disponible del EGP."

```

#### Fuera de alcance

- Aprobación EGP posterior (SIM-05)
- Escaneo


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S⚠️ T✅

---

### SIM-05 — Aprobar o rechazar simulación de adelanto (EGP)
| | |
|---|---|
| **Tipo** | HU-FE |
| **Épica** | SIM — Simulación y adelanto |
| **Actor** | Aprobador EGP |
| **Dominios** | EGP |
| **Prioridad sugerida** | Must |
| **Depende de** | SIM-03 |
| **Habilita** | SIM-04 |
| **Pantalla POC** | Confirming → Decisión adelanto |

#### Historia
```
Como aprobador EGP
quiero aprobar o rechazar la solicitud de adelanto generada tras la simulación del Proveedor
para autorizar el desembolso o devolver la operación
```

#### Valor de negocio
 Segundo control EGP sobre el crédito solicitado (paso 2 de S-04), distinto de CON-05.


#### Escenarios fuente
> Transcripción literal del input:

```text
-Escenario de Aprobación del adelanto por parte del EGP para avanzar con el desembolso solicitado por el usuario Proveedor
-Escenario de Rechazo del adelanto por parte del EGP, con o sin motivo

```

#### Criterios de aceptación

1. [Feliz] El EGP ve la solicitud pendiente con datos de simulación bloqueados.
2. [Feliz] Aprobar → avanza a Pendiente de Desembolso / integración CORE según flujo; MSG-26: "Adelanto aprobado. Se inicia el proceso de desembolso."
3. [Feliz] Rechazar con motivo opcional (S-08) → libera freeze de límite; MSG-27: "Adelanto rechazado."
4. [Error] Fallo → MSG-16: "No pudimos registrar la decisión del EGP. Intentá nuevamente."


#### Escenarios BDD
```gherkin
Característica: Decisión EGP sobre adelanto
  Escenario: Aprobación de adelanto
    Dado un adelanto pendiente de decisión EGP
    Cuando el aprobador confirma Aprobar
    Entonces veo el mensaje MSG-26: "Adelanto aprobado. Se inicia el proceso de desembolso."
    Y la factura pasa a Pendiente de Desembolso

  Escenario: Rechazo libera freeze
    Dado un adelanto con límite freezado
    Cuando el EGP rechaza
    Entonces el freeze se libera
    Y veo el mensaje MSG-27: "Adelanto rechazado."

```

#### Fuera de alcance

- CON-05 (aprobación de factura, no del adelanto)


#### Notas / preguntas abiertas

—


#### Chequeo INVEST
 I✅ N✅ V✅ E✅ S✅ T✅

---

## 7. Historias técnicas — Endpoints BFF / BE (enablers)

### FAC-03 — HT · GET obtenerInfoEnte (reuso MAGIA-120/122) para validar entes

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | FAC — Carga |
| **Habilita** | FAC-01, FAC-02 |
| **Contrato** | `GET /v1/entes/{id}` → MAGIA |
| **Prioridad sugerida** | Must |
| **Depende de** | MAGIA-120/122 |

#### Objetivo técnico
 Consumir API existente MAGIA-120/122 para validar existencia y estado activo de EGP/Proveedor en carga de facturas (no reimplementar).


#### Criterios de aceptación

1. BFF/BE expone o reutiliza GET info ente usado por FAC-01/FAC-02.
2. Respuesta incluye existencia y estado activo/inactivo.
3. Errores de dependencia se mapean a 502/503 sin inventar ente.


#### Escenarios BDD
```gherkin
Característica: obtenerInfoEnte para carga
  Escenario: Ente activo
    Dado un RUC de EGP activo en MAGIA
    Cuando consulto obtenerInfoEnte
    Entonces recibo 200 con estado activo

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 404 | ENTE_NOT_FOUND | Ente inexistente |
| 409 | ENTE_INACTIVE | Ente inactivo |
| 502 | UPSTREAM_ERROR | Falla MAGIA |


#### Notas / preguntas abiertas

- Ya desarrollado (Excel); cablear consumo Confirming.

---

### FAC-05 — HT · POST cargarFactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | FAC — Carga |
| **Habilita** | FAC-01, FAC-02, FAC-06 |
| **Contrato** | `POST /v1/facturas` → BE |
| **Prioridad sugerida** | Must |
| **Depende de** | FAC-03 |

#### Objetivo técnico
 Persistencia de factura(s) con validaciones de negocio y estado inicial Pendiente.


#### Criterios de aceptación

1. POST crea factura con campos de carga; estado inicial Pendiente (RN-02).
2. Valida entes activos antes de persistir.
3. 201/200 OK; 400 validación; 409 conflicto (duplicado nro+timbrado según regla).
4. Emite evento/hook para FAC-06 solo en OK (S-05).


#### Escenarios BDD
```gherkin
Característica: POST cargarFactura
  Escenario: Alta OK
    Dado un payload válido con entes activos
    Cuando invoco POST /cargarFactura
    Entonces respondo éxito y la factura queda Pendiente

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 400 | VALIDATION_ERROR | Campos inválidos |
| 409 | ENTE_INACTIVE | Ente no activo |
| 500 | UNEXPECTED | Error interno |


#### Notas / preguntas abiertas

—

---

### FAC-06 — HT · POST notificaciónNuevaFactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | FAC — Carga |
| **Habilita** | — |
| **Contrato** | `POST /v1/notificaciones/factura-nueva` → BFF |
| **Prioridad sugerida** | Must |
| **Depende de** | FAC-05 |

#### Objetivo técnico
 Notificar al EGP el pedido/alta de carga de factura solo cuando FAC-05 fue OK (S-05). Key propuesto (Excel duplicaba FAC-05).


#### Criterios de aceptación

1. Si carga OK → envía notificación al EGP.
2. Si carga ERROR → no envía notificación.
3. Fallo de notificación no revierte la factura ya creada; se registra para reintento (definir política en DoD).


#### Escenarios BDD
```gherkin
Característica: Notificación nueva factura
  Escenario: Notifica solo en éxito
    Dado POST cargarFactura OK
    Cuando corre el flujo de notificación
    Entonces se envía aviso al EGP

  Escenario: No notifica en error
    Dado POST cargarFactura con error
    Cuando termina el flujo
    Entonces no se envía notificación

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 502 | NOTIFY_FAILED | Canal de notificación caído |


#### Notas / preguntas abiertas

- Renombrado de 2ª fila FAC-05 → FAC-06 (SUP-10).

---

### CON-03 — HT · GET grillafacturas

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | CON — Grilla |
| **Habilita** | CON-01 |
| **Contrato** | `GET /v1/facturas` → BE |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-09 |

#### Objetivo técnico
 Proveer a FE el listado de facturas del EGP/Proveedor (o visión Banco) con filtros y proyección por pestaña.


#### Criterios de aceptación

1. GET retorna facturas según ente/rol y filtros (buscar, fechas, estado).
2. Incluye campos de columnas de grilla POC.
3. No retorna facturas en baja lógica como operables (RN-06).


#### Escenarios BDD
```gherkin
Característica: GET grillafacturas
  Escenario: Listado por EGP
    Dado un usuario EGP autenticado
    Cuando consulto GET /grillafacturas
    Entonces recibo solo facturas de su dominio

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 401 | UNAUTHORIZED | Sin sesión |
| 403 | FORBIDDEN | Sin permiso |


#### Notas / preguntas abiertas

—

---

### CON-06 — HT · PATCH actualizarfactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | CON — Grilla |
| **Habilita** | CON-12, CON-04, CON-11, CON-05 |
| **Contrato** | `PATCH /v1/facturas/{id}` → BE |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-09 |

#### Objetivo técnico
 Actualizar factura (baja lógica, fecha de pago, cambios de estado manuales orquestados).


#### Criterios de aceptación

1. PATCH soporta: baja lógica, fecha de pago, transición de estado validada por máquina (CON-09 en BE).
2. Rechaza transiciones inválidas con 409.
3. Usado por CON-12, CON-04, CON-11, CON-05.


#### Escenarios BDD
```gherkin
Característica: PATCH actualizarfactura
  Escenario: Actualizar fecha de pago
    Dado una factura existente
    Cuando envío PATCH con nueva fechaPago
    Entonces persiste y recalcula elegibilidad si aplica

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 409 | INVALID_TRANSITION | Estado no permite el cambio |
| 404 | NOT_FOUND | Factura inexistente |


#### Notas / preguntas abiertas

- Baja = lógica (SUP-04).

---

### CON-08 — HT · GET obtenerInfoEnte (info crediticia) reuso MAGIA

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | CON — Grilla |
| **Habilita** | CON-07 |
| **Contrato** | `GET /v1/entes/{id}/credito` → MAGIA |
| **Prioridad sugerida** | Must |
| **Depende de** | MAGIA-120/122 |

#### Objetivo técnico
 Obtener datos financieros para cabecera CON-07 (límites, tasas, morosidad) vía MAGIA-120/122.


#### Criterios de aceptación

1. Expone datos necesarios para EGP y Proveedor.
2. BFF calcula o recibe límite disponible = límite − freezado (RN-07) de forma consistente con SIM.


#### Escenarios BDD
```gherkin
Característica: Info crediticia ente
  Escenario: Respuesta OK
    Cuando consulto info financiera del EGP
    Entonces recibo RUC, razón social, límites y tasas

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 502 | UPSTREAM_ERROR | MAGIA no disponible |


#### Notas / preguntas abiertas

- Ya desarrollado; integrar freeze local Confirming.

---

### CON-09 — HT · Máquina de estados de facturas (BE fuente de verdad)

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | CON — Grilla |
| **Habilita** | CON-06, CON-10, CON-11 |
| **Contrato** | BE dominio estados |
| **Prioridad sugerida** | Must |
| **Depende de** | — |

#### Objetivo técnico
 Implementar transiciones manuales y automáticas de estado en BE (S-02).


#### Criterios de aceptación

1. Nacimiento: Pendiente (automático al alta).
2. Manual: Habilitar / Bloquear (CON-11).
3. Auto: si vencimiento documental < 30 días → Vencida (no operable) (RN-03).
4. Auto/regla: si fecha pago < 30 días → NO ELEGIBLE; EGP puede corregir fecha → vuelve operable/Habilitada según reglas.
5. BFF no redefine transiciones; solo invoca BE (S-02).


#### Escenarios BDD
```gherkin
Característica: Máquina de estados
  Escenario: Paso a Vencida por fecha documental
    Dado una factura con vencimiento documental a menos de 30 días
    Cuando corre la evaluación automática
    Entonces el estado es Vencida

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 409 | INVALID_TRANSITION | Transición no permitida |


#### Notas / preguntas abiertas

—

---

### CON-10 — HT · GET estados de facturas / reglas de transición

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | CON — Grilla |
| **Habilita** | CON-01, CON-02 |
| **Contrato** | `GET /v1/facturas/estados` → BE |
| **Prioridad sugerida** | Should |
| **Depende de** | CON-09 |

#### Objetivo técnico
 Exponer estados y/o matriz de transiciones para que FE habilite acciones y validaciones.


#### Criterios de aceptación

1. GET lista estados canónicos alineados a pestañas FV/FNV/FNO.
2. Opcionalmente retorna transiciones permitidas por estado origen.
3. Consistente con CON-09.


#### Escenarios BDD
```gherkin
Característica: GET estados
  Escenario: Catálogo de estados
    Cuando consulto GET estados
    Entonces recibo el set: Pendiente, Habilitada, Bloqueada, Pendiente aprobación EGP, Pendiente de desembolso, Financiada, Vencida, NO ELEGIBLE

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 500 | UNEXPECTED | Error interno |


#### Notas / preguntas abiertas

—

---

### SIM-02 — HT · GET simularAdelantoFactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | SIM — Adelanto |
| **Habilita** | SIM-01 |
| **Contrato** | `GET /v1/adelantos/simulacion` → BE |
| **Prioridad sugerida** | Must |
| **Depende de** | CON-08, CON-09 |

#### Objetivo técnico
 Calcular montos estimados y límites actualizados para el modal de simulación; validar expiración n días post aprobación EGP (S-03 default 5 días hábiles configurable).


#### Criterios de aceptación

1. 200 con breakdown de cálculo + límite disponible.
2. Error de cálculo → 422/500 mapeado a FE.
3. Si excedió n días desde aprobación EGP → bloquear adelanto con código de negocio EXPIRADO.


#### Escenarios BDD
```gherkin
Característica: GET simularAdelantoFactura
  Escenario: Cálculo OK
    Dado facturas Habilitadas elegibles
    Cuando consulto simulación
    Entonces recibo montos estimados y límite actualizado

  Escenario: Expiración n días
    Dado aprobación EGP hace más de n días configurados
    Cuando solicito simulación/adelanto
    Entonces respondo error de expiración

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 422 | CALC_ERROR | No se pudo calcular |
| 409 | ADVANCE_EXPIRED | Superó n días |
| 409 | LIMIT_EXCEEDED | Supera límite |


#### Notas / preguntas abiertas

- n configurable; default 5 días hábiles (S-03).

---

### SIM-03 — HT · POST generarAdelantoFactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | SIM — Adelanto |
| **Habilita** | SIM-01, SIM-04, SIM-05 |
| **Contrato** | `POST /v1/adelantos` → BE/CORE |
| **Prioridad sugerida** | Must |
| **Depende de** | SIM-02 |

#### Objetivo técnico
 Crear solicitud de adelanto hacia CORE, freeze de límite, validaciones de usuario y horario, reversión ante error.


#### Criterios de aceptación

1. OK → envía a CORE relación cuenta préstamo–facturas (nro factura en core); 1 cuota o n cuotas (S-06).
2. ERROR → no envía a CORE; revierte freeze (SUP-08).
3. Validar solicitante ≠ quien cargó la factura.
4. Validar horario antes de 17:00 (hora Paraguay).
5. Recalcular límite freezado.


#### Escenarios BDD
```gherkin
Característica: POST generarAdelantoFactura
  Escenario: Generación OK
    Dado simulación válida antes de las 17:00 y usuario distinto al cargador
    Cuando confirmo generarAdelanto
    Entonces se crea solicitud en CORE y se freeza límite

  Escenario: Mismo usuario cargador
    Dado que el solicitante cargó la factura
    Cuando intenta generar adelanto
    Entonces se rechaza la operación

  Escenario: Error CORE con reversión
    Dado respuesta de error del CORE
    Cuando termina el flujo
    Entonces no queda freeze huérfano

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 403 | SAME_USER_FORBIDDEN | Mismo usuario cargador |
| 403 | AFTER_CUTOFF | Después de 17:00 |
| 502 | CORE_ERROR | Fallo CORE (con revert) |


#### Notas / preguntas abiertas

—

---

### SIM-04 — HT · POST notificaciónAdelantoFactura

| | |
|---|---|
| **Tipo** | HT (enabler) |
| **Épica** | SIM — Adelanto |
| **Habilita** | — |
| **Contrato** | `POST /v1/notificaciones/adelanto` → BFF |
| **Prioridad sugerida** | Must |
| **Depende de** | SIM-03 |

#### Objetivo técnico
 Notificar EGP (pedido de adelanto) y Proveedor (crédito generado) solo en flujos OK.


#### Criterios de aceptación

1. Adelanto OK → notificación a EGP del pedido de adelanto.
2. Adelanto ERROR → no notifica a EGP.
3. Crédito/generación OK → notificación a Proveedor del crédito generado.
4. Error → no notifica al Proveedor.


#### Escenarios BDD
```gherkin
Característica: Notificaciones de adelanto
  Escenario: Doble notificación en éxito
    Dado adelanto OK
    Cuando corre notificación
    Entonces EGP recibe aviso de pedido y Proveedor de crédito generado

```

#### Errores esperados

| Código HTTP | Código negocio | Cuándo |
| 502 | NOTIFY_FAILED | Fallo canal |


#### Notas / preguntas abiertas

—

---

## 8. Tareas técnicas / habilitadores

| ID | Key Excel | Tarea | Objetivo | Definition of Done |
|----|-----------|-------|----------|--------------------|
| **T-01** | CON-09 | Job/evaluación automática de fechas (30 días) | Pasar a Vencida / NO ELEGIBLE sin intervención manual | Job documentado, corrida en ambiente test, logs de transición |
| **T-02** | SIM-02 | Parámetro `n` días hábiles post-aprobación EGP | Expirar adelantos vencidos (default 5) | Config en BE, leído por SIM-02, sin hardcode FE |
| **T-03** | SIM-03 | Reloj de cutoff 17:00 America/Asuncion | Rechazar generación fuera de horario | Test unitario TZ + mensaje FE |
| **T-04** | CON-02 | Refresh periódico grilla (15–30 s) en Pendiente de desembolso | Actualizar MSG-08 sin websocket MVP | Documentado en FE; cancelable al salir de pantalla |
| **T-05** | FAC-03 / CON-08 | Cableado cliente MAGIA-120/122 | Reusar APIs existentes | Contrato verificado en integración |

---

## 9. Spikes y decisiones pendientes (columna DUDAS)

| ID | Origen | Pregunta abierta | Impacto si no se resuelve | Propuesta del PO | Respuesta *(post HITL)* |
|----|--------|------------------|---------------------------|------------------|-------------------------|
| **S-01** | FAC-02 / POC | ¿Escaneo OCR en MVP? | Infla FAC-02 | Fuera + spike aparte | **FUERA** — no forma parte del alcance |
| **S-02** | CON-09 | ¿Estados en BE o BFF? | Dueño de verdad | BE fuente de verdad; BFF orquesta | confirmado — sin cambios |
| **S-03** | SIM-02 | Valor de n días post-aprobación EGP | Regla expiración | Default 5 días hábiles configurable | confirmado — sin cambios |
| **S-04** | CON-05 vs SIM-05 | ¿Mismo flujo o dos? | Duplicación UX | Dos pasos distintos | confirmado — sin cambios |
| **S-05** | FAC-05/06 | ¿Notificar solo si carga OK? | Notifs erróneas | Solo si POST OK | confirmado — sin cambios |
| **S-06** | SIM-01/03 | ¿1 préstamo n cuotas en CORE? | Contrato CORE | 1 solicitud, n cuotas, N facturas | confirmado — sin cambios |
| **S-07** | CON-02 | ¿Polling vs push desembolso? | Complejidad FE | Mensaje + spinner + refresh 15–30s | confirmado — sin cambios |
| **S-08** | CON-05 / SIM-05 | ¿Motivo de rechazo obligatorio? | Validación modal | Motivo opcional; si hay, se persiste | confirmado — sin cambios |

---

## 10. Recomendaciones del PO — historias faltantes

> Capacidades visibles en la POC **no** presentes en `Confirming.xlsx`. No mezclar con §6/§7.

### 10.1 Imprescindibles antes de salir a producción

| ID | Historia propuesta | Por qué falta / riesgo | Prioridad |
|----|--------------------|------------------------|-----------|
| **R-01** | Épica Login (LO-*) completa: primer login, 2FA AD/OTP, password temporal, bloqueo, olvido, inactividad | Sin autenticación no hay operación real | Must |
| **R-02** | Autorización por dominio/rol sobre botonera Confirming | Excel dice “recurso: todos” pero POC diferencia roles | Must |
| **R-03** | Liberación/auditoría de freeze de límite ante timeouts y rechazos | Riesgo de límite congelado huérfano | Must |
| **R-04** | Idempotencia y reintento de notificaciones (FAC-06 / SIM-04) | Fallos de canal dejan EGP/Proveedor desinformados | Must |

### 10.2 Recomendadas para completar la experiencia

| ID | Historia propuesta | Por qué falta / riesgo | Prioridad |
|----|--------------------|------------------------|-----------|
| **R-05** | Dashboard métricas (Adelantos, Transacciones, Mora, Rentabilidad) | Presente en POC, ausente en Excel | Could |
| **R-06** | ABM EGP / Proveedor / Usuarios / Roles / Notificaciones | Presente en POC Gestión (ABM) | Should |
| **R-07** | Reportes por rol (Banco / EGP / Proveedor) | Presente en POC Reportes | Should |
| **R-08** | Mi Perfil (solo lectura + derivación Home Banking) | Presente en POC | Could |
| **R-09** | Escaneo OCR de facturas | Explícitamente fuera (S-01); retomar como épica futura | Won't (ahora) |

---

## 11. Observaciones sobre la consistencia del input

1. **Keys duplicados:** `FAC-05` (filas 7–8) y `CON-03` (filas 10 y 12). Resuelto con **FAC-06** y **CON-12** (SUP-10).
2. **STACK vacío** en CON-07: tratado como HU-FE por contenido de pantalla.
3. **CON-09** marcado `BE/BFF?` en Excel → resuelto S-02 (BE).
4. **CON-06** escenarios Excel hablaban de “consulta grilla” (copy-paste); interpretado como actualización (PATCH) según Summary/Objetivo.
5. **SIM-04** objetivo decía “Notificación de creación de factura” (copy-paste); escenarios hablan de adelanto → se elaboró como notificaciones de adelanto.
6. **FAC-02** duda de escaneo → S-01 **FUERA**.
7. POC incluye Login/ABM/Reportes no cubiertos por el Excel → §10.
8. POC muestra “Escaneando documento…” pese a exclusión OCR → no generar AC de OCR.

---

## 12. Matriz de trazabilidad HU ↔ endpoint ↔ pantalla

| HU | Historias técnicas | Endpoints BFF (propuestos) | Pantalla / paso POC |
|----|--------------------|----------------------------|---------------------|
| FAC-01 | FAC-03, FAC-05, FAC-06 | GET entes · POST facturas · POST notif. factura | Cargar Nueva Factura (individual) |
| FAC-02 | FAC-03, FAC-05, FAC-06 | idem + procesamiento batch | Carga masiva / Resultado carga masiva |
| FAC-04 | FAC-05 | POST facturas (campo moneda) | Selector Moneda en carga |
| CON-01 | CON-03, CON-10 | GET facturas · GET estados | Confirming grilla + pestañas |
| CON-02 | — | — (UI) | Columna Acciones |
| CON-12 | CON-06 | PATCH facturas | Modal Eliminar / Confirmar |
| CON-04 | CON-06, CON-09 | PATCH facturas | Editar fecha de pago |
| CON-05 | CON-06 | PATCH facturas / decisión EGP | Modal Aprobar EGP |
| CON-07 | CON-08 | GET entes/crédito | Cabecera info crediticia |
| CON-11 | CON-06, CON-09 | PATCH facturas (batch) | Botones Habilitar / Bloquear |
| SIM-01 | SIM-02, SIM-03 | GET simulación · POST adelanto | Modal Simulación de Adelanto |
| SIM-05 | SIM-03, SIM-04 | PATCH/POST decisión adelanto · notif. | Aprobación/Rechazo adelanto |

---

## 13. Definition of Ready / Definition of Done

**Definition of Ready (por historia)**

- [ ] Objetivo y valor en formato Como / quiero / para
- [ ] Criterios de aceptación numerados (binarios) con tags, referenciando MSG/RN
- [ ] Escenarios BDD en Gherkin (español), alineados a los AC
- [ ] Mensajes de UI identificados (§5) y validados con UX
- [ ] Contrato de endpoints identificado (§7) y acordado con el equipo técnico
- [ ] Dependencias y spikes bloqueantes resueltos o acotados (S-01 fuera; resto confirmados)
- [ ] Diseño o pantalla de referencia disponible (POC)
- [ ] Chequeo INVEST completo (o spike marcado si falla)

**Definition of Done (por historia)**

- [ ] Criterios de aceptación cumplidos y demostrables
- [ ] Escenarios BDD automatizados o ejecutados manualmente según acuerdo del equipo
- [ ] Mensajes UI implementados según §5
- [ ] Documentación de API actualizada (si HT)
- [ ] Sin deuda técnica bloqueante conocida sin ticket
