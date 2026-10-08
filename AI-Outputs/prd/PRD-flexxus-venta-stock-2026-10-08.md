# PRD - Flexxus ERP — Discovery de modernización: Venta y Stock, situación actual y corte del MVP (Épicas 1 a 3)

> **Versión:** v2.0.0 · **Fecha:** 2026-10-07 · **Actualizado:** 2026-10-08 — fuentes completas del ERP y notas de release analizadas: cambia el corte (promociones, cupones y puntos entran al MVP; la Épica 2 absorbe lo que el core ya hace fuera del comprobante; la Épica 3 queda solo con capacidades que el core no tiene) y se corrige el supuesto de empresa única
> **Producto:** Flexxus ERP (core Delphi cliente-servidor) y sus frentes web: Flexxus ERP Web / POS, Flexxus Order y Flexxus Web API v6
> **Alcance de este documento:** únicamente las funcionalidades de **Venta** y **Stock**. Épica 1 — Ciclo de venta con efecto en stock (MVP); Épica 2 — Operación de stock, maestros y procesos comerciales fuera del comprobante; Épica 3 — Capacidades nuevas sobre el core. Compras, Fondos, Contabilidad, RMA, Producción, Calidad y RR.HH. quedan excluidos
> **Fecha límite comprometida:** sin fecha comprometida para la construcción. La etapa de Discovery cierra al final de la Semana 4 (estimado 2026-10-30, ⏳ a validar contra la fecha real de inicio)
> **Autor:** Product Owner
> **Fuentes:**
> - `Flexxus - Propuesta Tecnica v1.0.docx` (propuesta de Discovery de intive, v1.0, septiembre 2026; alcance, plan de 4 semanas, 13 entregables, riesgos R1–R7)
> - `flexxus_id-flexxuserpweb - documento funcional V1 3.2 1.pdf` (documento funcional del Punto de Venta, v3.2, 78 págs.; parámetros y permisos en págs. 68–74)
> - `flexxus_id-flexxus-order - Nota de release.pdf` (Flexxus Order 1.0 beta, 06/10/2026, 8 págs.)
> - `flexxus_id-flexxuserpweb_nota_de_release.pdf` (Flexxus ERP Web / POS v1.164.0, 06/10/2026, 3 págs.)
> - `flexxus_id-flxwebapi-v6-nota-de-release.pdf` (Flexxus Web API v6 2.8.337.0, 06/10/2026, 5 págs.)
> - `flexxus_id-flexxus-order - multi-tenant.pdf` (propuesta técnica Arquitectura Multi-Tenant, mayo 2026, 10 págs.)
> - `flexxus_id-flexxus-order - dump20261006.sql` (dump MariaDB `flexxusorder`, 386 tablas, 658 procedimientos)
> - Repositorios comprimidos `flexxus-order` (9.702 archivos), `flexxuserpweb` (3.369) y `flxwebapi-v6` (6.434); en particular `spec/carrito/*.md` y `openspec/specs/*` de `flexxus-order`
> - Fuentes Delphi `Erp_04-12_Provisorio.zip` (rama `develop`, **completas** desde el 08/10/2026: `03-ERP/unit` con 115 unidades, `ERP.dpr`, `04-PS`, `06-Librerias`) y `Corralon_0336.zip` (rama `master`); menú principal relevado de `03-ERP/frm/frmPrincipal.dfm`; unidades analizadas: `uParametrosGenerales`, `Funciones`, `FuncionesComprobantes`, `ModificacionesBaseDatos`, `UStock`, `FuncionesRemitos`, `GestorPromociones`, `frmFacturacion`, `frmRemitoInterno`
> - Notas de release del Delphi: `NR_Flexxus Enterprise.rar` (versiones 03.09 a 04.07), `NR_Flexxus 4.rar` (04.00 a 04.12) y `Corralon Enterprise.rar` (Cln 03.01 a 03.37): 3.028 documentos únicos, 1.399 de Venta o Stock
> - `Corralon_0336/06-Documentos` (Cuestionario de Pre-Parametrización v1.02 de 2008, descripción de tablas y plantillas de migración)
> - Detalle de inventarios: [Entregable parcial S1 v0.2 — Venta y Stock](../flexxus-discovery/2026-10-08-entregable-parcial-s1-venta-stock.md)

---

## Tabla de contenidos

1. [Resumen ejecutivo — dónde está el corte](#1-resumen-ejecutivo--dónde-está-el-corte)
2. [Contexto y problema](#2-contexto-y-problema)
3. [Objetivos de la etapa Venta y Stock y métricas de éxito](#3-objetivos-de-la-etapa-venta-y-stock-y-métricas-de-éxito)
4. [Actores y sistemas](#4-actores-y-sistemas)
5. [**El corte del MVP — regla de decisión y matriz de capacidades**](#5-el-corte-del-mvp--regla-de-decisión-y-matriz-de-capacidades)
6. [Alcance por épica](#6-alcance-por-épica)
7. [Alcance diferido — Épicas 2 y 3](#7-alcance-diferido--épicas-2-y-3)
8. [Requerimientos funcionales de la etapa Venta y Stock](#8-requerimientos-funcionales-de-la-etapa-venta-y-stock)
9. [Requerimientos no funcionales y restricciones](#9-requerimientos-no-funcionales-y-restricciones)
10. [Hallazgos de la documentación y el código de Flexxus que condicionan el alcance](#10-hallazgos-de-la-documentación-y-el-código-de-flexxus-que-condicionan-el-alcance)
11. [Observaciones sobre el backlog borrador (OpenSpec y especificaciones de flexxus-order)](#11-observaciones-sobre-el-backlog-borrador-openspec-y-especificaciones-de-flexxus-order)
12. [Riesgos, dependencias y decisiones abiertas](#12-riesgos-dependencias-y-decisiones-abiertas)
13. [Plan de entrega contra el cierre del Discovery](#13-plan-de-entrega-contra-el-cierre-del-discovery)
14. [Criterios de aceptación de la etapa Venta y Stock (DoD de fase)](#14-criterios-de-aceptación-de-la-etapa-venta-y-stock-dod-de-fase)

---

## 1. Resumen ejecutivo — dónde está el corte

**El MVP de Venta y Stock es el ciclo completo de una venta: buscar el artículo, ver su precio y su stock, emitir el comprobante (presupuesto, pedido, factura o nota de crédito) con las promociones, cupones y puntos que el core aplica dentro de él, cobrarlo y reflejar su efecto en el stock del depósito, en la empresa del usuario; todavía no mueve stock sin una venta asociada ni incorpora capacidades que el core no tiene hoy.**

El corte no es por cantidad de pantallas ni por esfuerzo: es por **qué hecho de negocio dispara la operación**. Entra lo que nace de un comprobante de venta al cliente, incluido todo lo que el core resuelve automáticamente dentro de él; queda afuera lo que ocurre por otro motivo y lo que exige una capacidad nueva. La v2.0.0 aplica la regla sobre el código: lo que la v1.0.0 había ubicado en la Épica 3 por falta de fuentes (promociones, fidelización, picking, reparto) ya existe en el core (H-18).

| | Épica 1 — Ciclo de venta con efecto en stock (MVP) | Épica 2 — Operación de stock, maestros y procesos comerciales fuera del comprobante | Épica 3 — Capacidades nuevas sobre el core |
|---|---|---|---|
| **Qué hace el producto** | Consulta de artículo, precio y stock; PR, NP, FC, NC, ND y remito de venta; promociones, cupones y puntos aplicados en el comprobante; cobro en el checkout; efecto en stock | Ajustes, transferencias, inventario, picking, packing, expedición y reparto; ABM de artículos, depósitos, listas, promociones y premios; comisiones, VNR, análisis de stock; comprobantes por lote y de verticales | Modelo Multi-Tenant (Grupo › Compañía › Sucursal, stock de la sucursal, visibilidad cruzada configurable); cobros QR de pasarelas |
| **Efecto sobre el estado del sistema** | Crea comprobantes fiscales y descuenta, reserva o reingresa stock por cada venta | Modifica existencias y maestros, o procesa ventas ya emitidas, sin un comprobante nuevo al cliente en el mostrador | Agrega entidades y flujos que el core no tiene (grupo, compañía como tenant, transferencia trazable entre compañías) |
| **Riesgo de un defecto** | Alto — fiscal (CAE ante AFIP/ARCA) y diferencia de stock o de importe visible al cliente | Medio — diferencia de inventario o de liquidación detectable en el cierre siguiente | Medio — no afecta la operación vigente si no se habilita |
| **Interfaces salientes** | Solicitud de CAE; impresión y envío del comprobante; terminales POSNET/VISA ya integradas en el core | Remito electrónico ARBA (transferencias) | Pasarelas QR (Mercado Pago, MODO), mapas, notificaciones |
| **Interfaces entrantes** | Padrón ARCA del cliente; confirmación de pagos externos | Carga de inventario desde archivo o escáner | Registro de grupos y compañías (landing multi-tenant) |
| **Habilita** | Definir la experiencia objetivo y las capacidades del core que expone el primer módulo | Reemplazar la operación de depósito y la administración comercial del Delphi | Diferenciación SaaS y nuevos dominios alrededor del core |

**Las tres preguntas que resuelven cualquier caso dudoso:**

1. ¿Requiere una capacidad, integración o estructura de datos que el core actual no tiene, **verificado en el código** (modelo Multi-Tenant, pasarelas QR)? → **Épica 3**.
2. ¿Ocurre fuera del ciclo de un comprobante de venta al cliente (operación de depósito, administración de maestros, procesos posteriores o por lote)? → **Épica 2**, sin excepción.
3. ¿Ocurre entre la búsqueda del artículo y la confirmación del comprobante de venta, incluidos lo que el core aplica automáticamente y su efecto inmediato en stock? → **MVP (Épica 1)**.

**Por qué este corte es el correcto y no uno arbitrario:**

- **Concentra el riesgo donde está el valor.** La venta es la operación de mayor volumen y la única con efecto fiscal directo; es también donde Flexxus ya invirtió dos reconstrucciones web (ERP Web / POS y Flexxus Order), así que la fricción y las reglas están mejor documentadas que en el resto del producto.
- **Ejercita primero el acoplamiento más difícil.** Un comprobante de venta toca artículos, precios, clientes, cuenta corriente, depósitos, parámetros y permisos a la vez. Si el core permite exponer este flujo, el resto de Stock es un subconjunto.
- **No genera retrabajo.** Las Épicas 2 y 3 reutilizan las capacidades que expone la Épica 1 (consulta de artículo y stock, modelo de depósito, parametrización) sin redefinirlas.

> ⚠️ El brief de Flexxus propone **Pagos a Proveedores** como módulo de referencia (Propuesta técnica, «Cuestiones abiertas al momento de esta propuesta»). El foco en Venta y Stock es una decisión del track de Producto de intive que **debe acordarse con el decisor de Flexxus** antes del cierre de la Semana 1. Ver [S-01](#121-decisiones-abiertas--a-resolver-en-la-épica-1).

---

## 1.bis Decisiones confirmadas el 2026-10-07 y el 2026-10-08

Definiciones cerradas de alcance interno del track de Producto o resueltas por Flexxus; las abiertas viven en §12.1.

### Ronda del 2026-10-07

| Decisión | Definición confirmada | Qué cambia |
|---|---|---|
| **Alcance funcional del relevamiento** | El Líder de Producto de intive acota el análisis de la etapa a **Venta y Stock**; el resto de los módulos se ignora (07-10) | Los inventarios de capabilities y documentación de la Semana 1 cubren solo esos dominios; el resto queda como «no relevado» en el inventario general |

### Ronda del 2026-10-08

| Decisión | Definición confirmada | Qué cambia |
|---|---|---|
| **Fuentes completas del ERP (S-04)** | Flexxus entregó la copia completa de `Erp_04-12_Provisorio` y tres colecciones de notas de release del Delphi (08-10) | H-4 queda resuelto; RF-03, RF-13 y RF-14 pasan a tener evidencia en el código; R-1 queda mitigado |
| **Reclasificación del corte sobre evidencia del código** | La pregunta «¿el core no lo tiene?» se responde con el código y no con la documentación web. Promociones, cupones y puntos se aplican dentro de FC, NP, PR y remito (`GestorPromociones`) → **Épica 1**. Picking, packing, expedición, reparto, comisiones, VNR, análisis de stock y comprobantes de verticales existen en el core y ocurren fuera del comprobante de mostrador → **Épica 2**. La Épica 3 queda solo para el modelo Multi-Tenant y los cobros QR de pasarelas | Cambia la matriz de §5.2 y el alcance de §6 y §7; se agregan RF-25 a RF-27 |
| **Empresa del usuario como contexto del MVP** | El Delphi ya opera varias empresas por instalación (`IDEMPRESA`, empresa principal 1, modo compilador, H-17). El MVP opera en la empresa del usuario logueado y no asume empresa única | §5.4 y RF-27; S-07 se reformula y se abre S-13 |

---

## 2. Contexto y problema

Flexxus es un ERP argentino con más de veinte años de producto y más de 2.200 clientes activos, construido en Delphi con arquitectura cliente-servidor, con una versión única, parametrizable y cerrada a la extensión (Propuesta técnica, «Situación actual»). Flexxus quiere modernizarlo para ganar **productividad** (que el sistema reúna contexto y recomiende en lugar de exigir que el usuario arme su recorrido por el menú) e **innovación** (dominios nuevos alrededor del core sin tocar la lógica transaccional).

intive ejecuta una etapa de Discovery de cuatro semanas, de análisis y planificación, sin desarrollo ni prototipos. El track de Producto releva la operación real, la parametrización y la fricción del usuario, y define la experiencia objetivo sobre un módulo de referencia. Este PRD consolida la Semana 1 para **Venta y Stock** y propone dónde cortar el primer módulo a modernizar.

El relevamiento muestra que Venta y Stock no parten de cero: además del core Delphi (menú con 94 opciones de Venta y 34 de Stock), existen el **ERP Web / POS** (v1.164.0, en uso por vendedores y viajantes) y **Flexxus Order** (1.0 beta, que reconstruye ventas, stock y maestros sobre MariaDB). El problema de la etapa no es solo entender el Delphi: es decidir **cuál de las tres implementaciones es la referencia de comportamiento** y cuál la base de la experiencia objetivo.

### Qué significa comprobante, stock y parametrización en el diccionario de Flexxus

- **Comprobante de venta** — documento con tipo y numeración por punto de venta: Presupuesto (PR, sin efecto fiscal ni stock), Nota de Pedido (NP, compromete entrega y admite anticipo), Factura (FC, efecto fiscal y de stock), Nota de Crédito/Débito (NC/ND) y Remito. Es el disparador del corte: lo que nace de un comprobante de venta es MVP.
- **Stock real y remanente** — el **stock real** es la suma de `CASILLEROS.StockActual` por artículo, lote, depósito y empresa; la tabla `STOCK` lo consolida por artículo y lote después de cada movimiento (`ModificarStock`). El **stock remanente** es el real menos lo comprometido en notas de pedido, lo facturado sin remitir y, si está activo, lo reservado en órdenes de reparación (`CalculaStockRemanente`). El parámetro 109 «Validación de Stock» (valores 0 a 9) define contra qué compara, si avisa o bloquea y si valida la nota de pedido (H-14). El parámetro 82 «Facturar sin descontar stock» traslada el descuento al remito.
- **Depósito y empresa** — en el Delphi conviven Depósitos, Sub Depósitos, Casilleros, Depósitos Externos y Centros de distribución; Flexxus Order lo reemplaza por un árbol de dos niveles (spec `deposito-crud`). Todo depósito y todo movimiento pertenecen a una **empresa** (`IDEMPRESA`), una razón social dentro de la misma instalación: la empresa 1 es la principal y el «modo compilador» consolida el stock de varias (H-17). No es el «tenant» de la propuesta Multi-Tenant.
- **Parametrización** — 399 constantes de parámetros generales en el código (`uParametrosGenerales.pas`; 345 filas en la base de test) y parámetros por punto de venta (5.137 filas) que cambian el comportamiento de la venta sin cambiar el código; el carrito web lee 28 (spec `erp-parameters.md`) y las pantallas de Venta del Delphi leen 163 (H-20).

**El corte no es una concesión de alcance: sigue lo que el propio producto define como unidad de operación, el comprobante de venta y su efecto en el depósito.**

---

## 3. Objetivos de la etapa Venta y Stock y métricas de éxito

### Objetivo de negocio

Que Flexxus decida, al cierre del Discovery (estimado 2026-10-30), el alcance y la base del primer módulo a modernizar con información verificada sobre el comportamiento real de Venta y Stock, sus variantes por parametrización y su fricción para el usuario.

### Objetivos de producto

| # | Objetivo | Cómo se verifica |
|---|---|---|
| OBJ-1 | Inventario de capabilities de Venta y Stock con su presencia en cada implementación (Delphi, ERP Web / POS, Flexxus Order, API v6) | Cada capability tiene fuente citada y estado por implementación; revisado por el referente técnico |
| OBJ-2 | Mapa de la parametrización que modifica Venta y Stock y de sus diferencias entre instalaciones | Lista de parámetros con código, efecto y valores observados en al menos 5 instalaciones (⏳ a validar la muestra) |
| OBJ-3 | Flujo as-is del ciclo de venta con las fricciones efectivas del usuario | Flujo validado en sesión con el referente de negocio; cada fricción con evidencia (sesión, pantalla o dato) |
| OBJ-4 | Corte del MVP y módulo de referencia acordados con Flexxus | Acta firmada por el decisor; S-01 y S-02 resueltas |
| OBJ-5 | Estado de cada acceso y de la documentación disponible, con bloqueos visibles | Tabla de accesos con estado OK / parcial / pendiente y responsable, entregada al cierre de la Semana 1 |
| OBJ-6 | Requerimientos del MVP con equivalencia funcional al comportamiento vigente | Cada RF de §8 trazado a una pantalla del Delphi o a una regla del ERP Web, y a un parámetro o permiso cuando aplique |

### Métricas

| Métrica | Objetivo de la etapa |
|---|---|
| Capabilities de Venta y Stock con fuente verificada | ≥ 90 % (⏳ a validar) |
| Parámetros de Venta y Stock clasificados (efecto + valores observados) | 100 % de los 28 que lee el carrito más los de stock y remito (52, 55, 77, 82, 109, 116, 154, 237); efecto en el código ya relevado para 52, 82, 109, 116, 154 y 287 (H-14); resto a relevar en Semana 2 |
| Sesiones de relevamiento con referentes de negocio | ≥ 2 en la Semana 1 y ≥ 2 en la Semana 2 (⏳ a validar agenda) |
| Fricciones documentadas con evidencia | ≥ 10 en el ciclo de venta (⏳ a validar) |
| Accesos en estado OK al cierre de la Semana 1 | 100 % (fuentes del ERP OK desde el 08-10; siguen pendientes Jira, base Firebird de referencia y entorno de prueba) |

### No-objetivos explícitos de la etapa Venta y Stock

- No se desarrolla, prototipa ni prueba ningún componente (Propuesta técnica, «Fuera de alcance»).
- No se relevan Compras, Fondos, Contabilidad, RMA, Producción, Calidad ni RR.HH.; la gestión de cuenta corriente fuera del cobro en el checkout tampoco.
- No se diseña la migración de datos ni de clientes.
- No se miden performance ni costo de operación reales.
- No se define la arquitectura destino: es del track de Tecnología; acá solo se declaran las capacidades que la experiencia requiere.

---

## 4. Actores y sistemas

### 4.1 Actores

| Actor | Descripción | Rol en la etapa |
|---|---|---|
| **Vendedor de mostrador / cajero** | Arma la venta, emite el comprobante y cobra (Delphi o facturador web) | Fuente principal de fricción; observado en sesión |
| **Vendedor viajante** | Toma pedidos y cobra desde la app mobile, con hoja de ruta | Fuente de fricción mobile; su logística es Épica 3 |
| **Encargado de depósito** | Prepara pedidos, transfiere y ajusta stock, hace tomas de inventario | Fuente para Épica 2; valida el efecto en stock de la venta |
| **Administrador / implementador** | Parametriza la instalación, define permisos y perfiles | Fuente del modelo de parametrización y sus diferencias |
| **Referente de negocio y producto (Flexxus)** | Conoce la operación de los clientes y la dirección del producto | Valida flujo, fricción, corte y prioridades |
| **Referente técnico (Flexxus)** | Conoce el código, su historia y las decisiones de diseño | Valida capabilities, reglas y dependencias |
| **Decisor del proyecto (Flexxus)** | Aprueba alcance e inversión | Resuelve S-01, S-02 y S-07 |
| **Líder de Producto (intive)** | Conduce el track de Producto | Autor de este PRD y de los entregables parciales |
| **Arquitecto de Solución (intive)** | Conduce el track de Tecnología | Consume las capacidades y datos que requiere la experiencia |

### 4.2 Sistemas y componentes

| Componente | Responsabilidad | Épica |
|---|---|---|
| **Flexxus ERP Delphi** (`Erp_04-12_Provisorio`, rama `develop`) | Core transaccional: 12 solapas de menú, 574 acciones, 978 formularios, 115 unidades de lógica; Venta y Stock completos, multiempresa por `IDEMPRESA`, motor de promociones, terminales POSNET/VISA (`06-Librerias`) | 1, 2 (referencia de comportamiento) |
| **Flexxus Corralón** (`Corralon_0336`, rama `master`) | Variante vertical del ERP para corralones, con Print Server y servidor de depósitos | Variante a contrastar (S-05) |
| **Base Firebird del ERP** | Datos y procedimientos del core; migración de Firebird 2.5 a 5 en curso | 1, 2 |
| **Flexxus Web API v6** (`flxwebapi`, 2.8.337.0) | API REST versionada (/v1 a /v6) sobre Firebird, única capa de acceso para terceros; ventas, stock, pedidos, artículos | 1, 2 |
| **Flexxus ERP Web / POS** (`flexxuserpweb`, v1.164.0) | Facturador web y app mobile (React, Ionic, Capacitor) sobre la API v4 | 1 (experiencia vigente) |
| **Flexxus Order** (1.0 beta) | Nueva generación web: React 19 + Node.js + MariaDB `order-v6`; carrito, cobro unificado, depósitos en árbol, precios por lista | 1, 2 (candidato a base del MVP, S-02) |
| **AFIP / ARCA** | CAE de factura electrónica, padrones y catálogos | 1 |
| **ARBA** | Remito electrónico (COT) | 2 |
| **Pasarelas de cobro** (Mercado Pago, Payway/Prisma, Clover, MODO, Go Cuotas) | Cobro con QR o terminal; el Delphi integra terminales POSNET y VISA | 1 (terminales, ⏳ S-09) / 3 (QR) |

---

## 5. El corte del MVP — regla de decisión y matriz de capacidades

### 5.1 La regla

> **Entra en el MVP todo lo que ocurre dentro del ciclo de un comprobante de venta al cliente:** consulta de artículo, precio y stock; armado y emisión de PR, NP, FC, NC, ND y remito de venta; lo que el core aplica automáticamente al armarlo (promociones, cupones, puntos, validaciones de stock y de cuenta corriente); cobro en el checkout; y el efecto inmediato del comprobante sobre el stock del depósito (descuento, reserva, reingreso), siempre en la empresa del usuario.

> **Queda fuera de la etapa** todo lo que ocurre fuera de ese ciclo aunque el core ya lo haga (Épica 2) y todo lo que requiere una capacidad que el core actual no tiene, verificado en el código (Épica 3).

Corolario: el MVP **lee** maestros (artículos, listas de precio, reglas de promoción, clientes, depósitos, parámetros) pero no los **administra**.

### 5.2 Matriz de capacidades por épica

El detalle por opción de menú, pantalla y fuente vive en el [entregable parcial S1 v0.2](../flexxus-discovery/2026-10-08-entregable-parcial-s1-venta-stock.md) §2; acá se resume por bloque. En la columna Criterio, «Pregunta n» remite a las tres preguntas de §1.

#### Consulta de artículo, precio y stock — **dentro del MVP (Épica 1)**

| Capacidad | Origen en el Delphi | Por qué está en el MVP | Épica | Criterio |
|---|---|---|---|---|
| Búsqueda de artículos (código, descripción, código de barras, pesables) | Selección de artículos de comprobantes; parámetros 32, 44, 150 | Primer paso de toda venta | 1 | Pregunta 3 |
| Precio por lista, multiplazo, precio pactado y oferta | Ventas › Precios y Bonificaciones › Precios; parámetros 4, 21, 43, 49, 50 | Determina el importe del comprobante | 1 | Pregunta 3 |
| Promociones, cupones de descuento, reglas de precio y puntos aplicados al comprobante | `GestorPromociones` (motor usado por FC, NP, PR y remito); `prCalcularPuntos`; parámetros 99, 311 | El core los aplica al armar el comprobante: sin ellos el importe no es equivalente (RNF-01) | 1 | Pregunta 3 (reclasificado desde Épica 3, H-18) |
| Stock por depósito, talles y lotes al vender | Listado de stock por depósito; parámetros 20, 55, 83, 109, 237 | Condiciona si la venta se puede hacer | 1 | Pregunta 3 |

#### Comprobantes de venta — **dentro del MVP (Épica 1); el corte pasa por acá**

| Capacidad | Origen en el Delphi | Por qué | Épica | Criterio |
|---|---|---|---|---|
| Presupuesto, planilla y anulación | Ventas › Comprobantes › Presupuestos (3 opciones) | Inicio del ciclo comercial | 1 | Pregunta 3 |
| Nota de pedido, planilla, pendientes, anulación, autorización | Ventas › Comprobantes › Notas de Pedido (8) | Compromete stock y entrega | 1 | Pregunta 3 |
| Factura, NC, ND (electrónicas), facturación de pedidos y de remitos | Ventas › Comprobantes › Facturación (17) y Facturación Electrónica (1) | Núcleo fiscal de la venta | 1 | Pregunta 3 |
| Remito de venta y remito por devolución | Ventas › Comprobantes › Remitos (10) | Efecto físico de la venta | 1 | Pregunta 3 |
| Consulta, reimpresión y anulación de comprobantes | Ventas › Comprobantes › Consulta (5) | Corrección dentro del ciclo | 1 | Pregunta 3 |
| Facturación de NP de otra empresa de la instalación | Parámetro 116 (valores 0 a 3, NR 04.11) | Ocurre dentro del comprobante, pero solo en instalaciones multiempresa | 1 ⏳ | Pregunta 3 ⏳ S-13 |
| *Facturación masiva y lotes de facturación* | Facturación Masiva (2) | Existe en el core; procesa por lote, no nace de una venta en mostrador | 2 | Pregunta 2 ⏳ S-10 |
| *Liquidación primaria de granos, carta de porte* | Facturación (1), Otros (1) | Comprobantes de verticales que ya existen en el core | 2 | Pregunta 2 ⏳ S-10 |
| *Impresora fiscal: cierres X/Z, control de numeración* | Facturación › Impresora Fiscal (5) | Vigencia a confirmar | ⏳ | S-11 |
| *Remito interno de venta* | Remitos (4 de 10) | Mueve stock sin venta al cliente | 2 | Pregunta 2 |

#### Cobro dentro del ciclo de venta — **dentro del MVP (Épica 1)**

| Capacidad | Origen | Por qué | Épica | Criterio |
|---|---|---|---|---|
| Cobro en el checkout: efectivo, tarjeta, cheque, retenciones, cuenta corriente | Formas de pago del comprobante; Flexxus Order «cobro unificado» | Sin cobro la factura de contado no se cierra | 1 | Pregunta 3 |
| Validación de cuenta corriente y límite de crédito al vender | Permisos 402/404/405; parámetros 58, 287 | Condiciona la emisión | 1 | Pregunta 3 |
| *Gestión de cuenta corriente: intereses, cobranza masiva, importación de cobros, saldos al inicio* | Ventas › Cuentas Corrientes (11) | Ocurre fuera del comprobante de venta; dominio Fondos | Fuera de la etapa | Alcance 1.bis |

#### Efecto de la venta en el stock — **dentro del MVP (Épica 1)**

| Capacidad | Origen | Por qué | Épica | Criterio |
|---|---|---|---|---|
| Descuento de stock al facturar o remitir | `ModificarStock` sobre `CASILLEROS` y `STOCK`; parámetros 52, 82, 154 | Es el efecto inmediato del comprobante | 1 | Pregunta 3 |
| Reserva / stock remanente por pedido | `CalculaStockRemanente`; parámetro 109 (valores 0 a 9, H-14) | Evita vender lo comprometido | 1 | Pregunta 3 |
| Reingreso por NC o remito de devolución | Parámetros 184, 206 | Cierra el ciclo de devolución | 1 | Pregunta 3 |
| Acopios (venta con entrega diferida) | ABM y Planilla de Acopios | Ligados al comprobante de venta | 1 | Pregunta 3 |

#### Operación de stock, maestros y procesos comerciales fuera del comprobante — **Épica 2**

| Capacidad | Origen en el Delphi | Épica | Criterio |
|---|---|---|---|
| Ajustes de stock y motivos | Stock › Correcciones de Stock (3) | 2 | Pregunta 2 |
| Transferencias entre depósitos, movimientos internos, distribución, consumo interno | Stock › Transferencias entre Depósitos (9) | 2 | Pregunta 2 |
| Toma de inventario y carga desde archivo | Stock › Inventarios (8) | 2 | Pregunta 2 |
| Consulta de movimientos, histórico, series, cierres de stock | Stock › Consulta de Movimientos (7) | 2 | Pregunta 2 |
| ABM de artículos, depósitos, listas de precio, reglas de promoción y premios; modificación masiva de precios y bonificaciones | Archivos › Artículos (17), Depósitos (5); Precios y Bonificaciones; Fidelización (4) | 2 | Pregunta 2 |
| Picking, packing, salida de pedidos, expedición, guía de reparto y confirmación de entrega | `frmSelPickingPendientes`, `frmPacking`, Planilla de Expedición, Guía de Reparto, Stock › Reparto (reclasificado desde Épica 3, H-18) | 2 | Pregunta 2 |
| Comisiones de vendedores, premios y ventas no realizadas | Ventas › Vendedores (5), VNR (2) (reclasificado desde Épica 3) | 2 | Pregunta 2 |
| Análisis de rotación, optimización de stock mínimo/máximo, diferencias | Stock › Análisis de Stock (3) (reclasificado desde Épica 3) | 2 | Pregunta 2 |

#### Capacidades nuevas — **Épica 3**

| Capacidad | Origen | Épica | Criterio |
|---|---|---|---|
| Modelo Multi-Tenant: Grupo › Compañía › Sucursal, stock de la sucursal física, catálogos compartidos, visibilidad cruzada configurable, transferencias trazables entre compañías | Propuesta Multi-Tenant (mayo 2026); el Delphi tiene empresas por instalación pero no esta jerarquía (H-17) | 3 | Pregunta 1 |
| Cobros QR de pasarelas (Mercado Pago, MODO, Go Cuotas) | ERP Web / POS; sin equivalente en el Delphi (⏳ verificar en Semana 2) | 3 | Pregunta 1 ⏳ S-09 |

> **Decisión de alcance explícita y necesaria:** «Stock» en el MVP significa **el efecto de la venta sobre la existencia de un depósito de la empresa del usuario**, no la gestión de depósito. Sin esta acotación, Stock arrastra 34 opciones de menú más los maestros y vuelve inviable el análisis en profundidad dentro de cuatro semanas (cf. R-5).

### 5.3 El corte en la dirección venta → stock

El flujo principal recorre comprobantes encadenados; cada tramo cae de un lado del corte según qué lo dispara.

| Flujo de integración | Épica | Detalle |
|---|---|---|
| **Artículo → Carrito** | **1** | Búsqueda, precio, stock disponible según parámetro 109 y depósito del usuario |
| **PR → NP → Remito → FC** | **1** | Conversión de presupuesto, facturación de pedidos y de remitos; copia de contenido según parámetros del cuestionario de pre-parametrización |
| **FC con remito automático** | **1** | Parámetro 52 (FC en cuenta corriente) y 154 (FC de contado): el remito se genera tildado y editable (1), tildado y fijo (2), no disponible (3) o a elección (4), salvo entrega pactada o reparto propio |
| **NP de otra empresa → FC** | **1** ⏳ | Parámetro 116: la planilla muestra NP de todas las empresas o solo de la propia, y permite o no facturarlas ([S-13](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| **FC / NC → AFIP/ARCA** | **1** | Solicitud de CAE; monitor de transacciones |
| **NC / Remito de devolución → Stock** | **1** | Reingreso al depósito; parámetros 184 y 206 |
| **Depósito A → Depósito B** | **2** | Remito de transferencia y remito electrónico ARBA |
| **Toma de inventario → Ajuste** | **2** | Diferencias de stock y corrección manual |
| **NP → Picking → Packing → Expedición** | **2** | Preparación posterior al pedido; existe en el core |
| **Compañía A → Compañía B** | **3** | Transferencia trazable de stock entre compañías del grupo (Multi-Tenant) |

### 5.4 Capacidades transversales: dónde corta cada una

La documentación web y el Delphi no coinciden en varias capacidades; se decide por capacidad.

| Capacidad | En el MVP (Épica 1) | Diferido a Épica 2 o 3 (Operación de stock / Capacidades nuevas) |
|---|---|---|
| **Parametrización** | Los 28 parámetros que lee el carrito más los de stock y remito 52, 55, 77, 82, 109, 116, 154 y 237, con sus variantes reales | El resto de los 163 parámetros que leen las pantallas de Venta del Delphi, según aparezcan en el análisis (H-20) |
| **Permisos** | Permisos del ciclo de venta (precio, descuento, depósito, lista, validación de CC por comprobante) y los permisos especiales de las 7 pantallas de comprobante (77 códigos distintos, H-16) | Perfiles completos y auditoría de usuarios |
| **Fiscal** | CAE de FC, NC y ND electrónicas | Remito electrónico ARBA (2); impresora fiscal ⏳ S-11 |
| **Cobros externos** | Efectivo, tarjeta, cheque, retenciones, cuenta corriente y terminales POSNET/VISA que ya integra el core | QR de pasarelas (3) ⏳ S-09 |
| **Multi-sucursal / multiempresa** | La empresa del usuario logueado (`IDEMPRESA`) y sus N depósitos; facturación de NP de otra empresa según el parámetro 116 ⏳ S-13 | Modelo Multi-Tenant y visibilidad cruzada configurable (3) |
| **Control de stock negativo** | El vigente en la instalación: por artículo y, desde la 04.12, por stock general o por depósito (parámetro 537) ⏳ S-14 | Migración entre modalidades y su auditoría (2) |
| **Auditoría** | Trazabilidad usuario-fecha-comprobante-movimiento de stock | Auditoría de maestros y de parámetros (2) |

> La propuesta Multi-Tenant (pág. 2) dice que «el sistema maneja actualmente una sola empresa por instalación». El código lo contradice: el Delphi filtra por `IDEMPRESA` en 724 de sus 1.401 unidades y tiene parámetros específicos para operar entre empresas (H-17). El MVP preserva ese comportamiento; lo nuevo de la Épica 3 es la jerarquía Grupo › Compañía › Sucursal, no la existencia de varias empresas.

---

## 6. Alcance por épica

### Épica 1 — Ciclo de venta con efecto en stock (MVP)

**Objetivo:** dejar definido, al cierre del Discovery, el primer módulo a modernizar: flujo as-is verificado, experiencia objetivo, capacidades del core que expone, requerimientos con criterio de aceptación y su dimensionamiento.
**Duración prevista:** análisis en el Discovery (Semanas 1 a 4, ver §13); construcción a estimar en el roadmap de la Semana 4.

**Dentro de alcance**

| Bloque | Contenido |
|---|---|
| Relevamiento (S1) | Inventario de capabilities de Venta y Stock por implementación; parametrización que afecta la venta; estado de accesos y documentación ([entregable parcial S1 v0.2](../flexxus-discovery/2026-10-08-entregable-parcial-s1-venta-stock.md)) |
| Reglas del core (S1–S2) | Extracción de reglas del Delphi para el ciclo de venta: validación y descuento de stock, remito automático, promociones, cuenta corriente, empresa; cada regla con unidad, parámetro y nota de release |
| Operación real (S1–S2) | Sesiones con referentes de negocio sobre mostrador, facturador web y mobile; fricciones con evidencia (OBJ-3) |
| Variantes (S1–S2) | Diferencias efectivas entre instalaciones: valores de parámetros, vertical Corralón vs ERP general ([S-05](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| Experiencia objetivo (S2–S3) | Pasos del flujo de venta y la información que el sistema debe reunir en cada uno, sobre el módulo de referencia ([S-01](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| Capacidades del core (S2–S3) | Qué capacidades de negocio (artículo, precio, stock, cliente, comprobante, cobro) requiere la experiencia y con qué profundidad |
| Requerimientos (S4) | RF y RNF del primer módulo con criterio de aceptación (§8 y §9 como base) |

**Fuera de alcance:** la operación de stock sin venta (Épica 2), las capacidades nuevas (Épica 3) y todo módulo distinto de Venta y Stock.

**Criterio de salida:** S-01 y S-02 resueltas por el decisor; flujo as-is validado por el referente de negocio; cada RF trazado a su origen (OBJ-6); capabilities del MVP con su dependencia del core identificada por el track de Tecnología.

> **Restricción de planificación:** las fuentes ya están completas ([S-04](#121-decisiones-abiertas--a-resolver-en-la-épica-1) resuelta), pero la lógica de Venta vive en formularios de 10.000 a 19.000 líneas con SQL embebido (H-16). La extracción de reglas se acota a las pantallas de comprobante del MVP y a las unidades `Funciones`, `FuncionesComprobantes`, `ModificacionesBaseDatos` y `GestorPromociones`.

---

## 7. Alcance diferido — Épicas 2 y 3

### Épica 2 — Operación de stock, maestros y procesos comerciales fuera del comprobante (a planificar en el roadmap)

La habilita el cambio de disparador: la operación ya no nace de un comprobante al cliente en el mostrador, sino de una necesidad del depósito o de la administración, o de un proceso sobre ventas ya emitidas. Todo su contenido existe hoy en el core. Sus requisitos se derivan del modelo de depósito que fije la Épica 1 ([S-06](#121-decisiones-abiertas--a-resolver-en-la-épica-1)).

| Bloque | Contenido |
|---|---|
| Movimientos | Ajustes con motivo, transferencias entre depósitos, movimientos internos entre casilleros, distribución, consumo interno |
| Inventario | Toma, carga desde archivo y escáner, actualización, diferencias y cierres de stock |
| Consulta | Movimientos por depósito, histórico de artículos, seguimiento de series y lotes |
| Maestros | ABM de artículos, depósitos, listas de precio, rubros, marcas, reglas de promoción, cupones y premios; modificación masiva de precios y bonificaciones |
| Logística | Picking, packing, salida de pedidos, expedición, guía de reparto, confirmación de entrega |
| Comercial | Comisiones de vendedores, premios, ventas no realizadas |
| Verticales y lotes | Facturación masiva y por lote, liquidación primaria de granos, carta de porte ([S-10](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| Analítica | Rotación, optimización de stock mínimo/máximo, diferencias |
| Fiscal | Remito electrónico ARBA |

**Dependencias que no existen en la etapa:** modelo de depósito objetivo acordado; inventario de casilleros y depósitos externos en uso por clientes reales; uso real de logística y verticales en la base instalada.

### Épica 3 — Capacidades nuevas sobre el core (a planificar en el roadmap)

La habilita la arquitectura destino: requiere exponer capacidades del core de forma estable (Business APIs y Events, principios de Flexxus) y una jerarquía Grupo › Compañía › Sucursal que el Delphi no tiene. Sus empresas por instalación (`IDEMPRESA`) son el punto de partida, no la solución (H-17).

| Bloque | Contenido |
|---|---|
| Multi-Tenant | Grupo › Compañía › Sucursal; stock de la sucursal física; catálogos compartidos entre compañías; stock cruzado (sin acceso / solo ver / ver + incorporar); transferencias trazables entre compañías |
| Cobros QR | Pasarelas QR (Mercado Pago, MODO, Go Cuotas) que hoy solo ofrece el ERP Web / POS |

**Dependencias que no existen en la etapa:** arquitectura destino (Semana 3), decisión de multiempresa ([S-07](#121-decisiones-abiertas--a-resolver-en-la-épica-1)), mapa entre las empresas actuales y las compañías del modelo nuevo.

**Consideración de modelo de stock:** si la Épica 1 adopta el árbol de dos niveles de Flexxus Order, el stock por sucursal de la propuesta Multi-Tenant se apoya en él sin rediseño; si adopta el modelo Delphi (subdepósitos y casilleros), la Épica 3 hereda una migración de modelo.

---

## 8. Requerimientos funcionales de la etapa Venta y Stock

Los RF describen lo que el primer módulo modernizado debe hacer, derivado del comportamiento vigente. Todos trazan a OBJ-6. Desde la v2.0.0, los RF con regla extraída del Delphi citan su unidad entre paréntesis; el resto se traza en el análisis de la Semana 2.

### 8.1 Consulta de artículo, precio y stock

| ID | Requerimiento |
|---|---|
| RF-01 | El sistema permite buscar artículos por código, descripción y código de barras, incluidos los códigos configurables con peso, precio o cantidad (parámetros 32 y 150) |
| RF-02 | El sistema resuelve el precio según lista de precios, multiplazo, precio pactado por cliente y precio de oferta vigente (parámetros 4, 43, 99) |
| RF-03 | El sistema muestra el stock del artículo por depósito, lote y empresa según la política del parámetro 109: real, remanente (real menos NP pendientes, facturado sin remitir y, con su parámetro activo, órdenes de reparación) o remanente más órdenes de compra (`Funciones.CalculaStockRemanente`) |
| RF-04 | El sistema ofrece solo artículos con stock cuando el parámetro 55 está activo, considerando talles y lotes (parámetros 20 y 83) |
| RF-05 | El sistema muestra los precios con o sin IVA y en moneda base según los parámetros 21, 49 y 50, sin alterar el importe facturado |

### 8.2 Comprobantes de venta

| ID | Requerimiento |
|---|---|
| RF-06 | El sistema emite Presupuesto, Nota de Pedido, Factura, Nota de Crédito y Nota de Débito desde un mismo flujo, con el tipo elegido condicionando pasos y validaciones |
| RF-07 | El sistema convierte un presupuesto en pedido o factura, y factura pedidos y remitos pendientes copiando su contenido según la parametrización |
| RF-08 | El sistema solicita el CAE para FC, NC y ND electrónicas y no da por emitido un comprobante sin CAE |
| RF-09 | La nota de crédito se vincula a una o más facturas de origen, buscadas por número o por rango de fechas según el parámetro 119 |
| RF-10 | El sistema bloquea la venta a clientes no facturables en FC y NP, y la permite en PR |
| RF-11 | El sistema valida el CUIT del cliente cuando el importe supera el umbral de la sucursal (`montovalidacioncuit`) |
| RF-12 | El sistema permite consultar, reimprimir, enviar por mail y anular comprobantes de venta |

### 8.3 Efecto en stock y validaciones

| ID | Requerimiento |
|---|---|
| RF-13 | Al confirmar una FC o un remito de venta, el sistema descuenta el stock del casillero (depósito × lote) y recalcula el total del artículo, salvo que el parámetro 82 indique facturar sin descontar stock; si el artículo no admite stock negativo, la operación completa se revierte (`ModificacionesBaseDatos.ModificarStock`) |
| RF-14 | Para artículos que verifican stock, el sistema avisa (parámetro 109 en 0, 4, 5 o 9) o impide (1, 2, 3, 6, 7 u 8) confirmar un comprobante que supera el stock disponible; la NP solo se valida con valores de 5 a 9, la NC nunca se valida y la FC no se valida si viene de un remito o si el 82 traslada el descuento al remito (`Funciones.fxTieneQueVerificarStock`) |
| RF-15 | Una NC o un remito de devolución reingresa el stock al depósito correspondiente (parámetros 184 y 206) |
| RF-16 | El sistema verifica que el artículo esté asociado al depósito elegido, o lo asocia automáticamente si el parámetro 77 lo indica |
| RF-17 | El sistema registra acopios (venta con entrega diferida) y su saldo pendiente de entrega |

### 8.4 Cobro dentro del ciclo de venta

| ID | Requerimiento |
|---|---|
| RF-18 | El checkout admite combinar efectivo, tarjeta, cheque, retenciones y cuenta corriente en una misma operación |
| RF-19 | El sistema propone la factura como contado aunque el cliente tenga cuenta corriente cuando el parámetro 58 está activo, y propone o fuerza el remito automático según los parámetros 52 (cuenta corriente) y 154 (contado) (`frmFacturacion`) |
| RF-20 | El sistema valida la cuenta corriente del cliente (saldo, límite y comprobantes vencidos) según el permiso de cada tipo de comprobante y el parámetro 287 |

### 8.5 Parametrización, permisos y auditoría

| ID | Requerimiento |
|---|---|
| RF-21 | Todo comportamiento de §8.1 a §8.4 que dependa de un parámetro lo lee de la configuración de la instalación; ningún valor queda fijo en el código |
| RF-22 | El sistema aplica los permisos por usuario sobre editar precio, descuento, lista de precios y depósito en el comprobante |
| RF-23 | Cada comprobante y cada movimiento de stock que genera quedan registrados con usuario, fecha, sucursal, depósito y comprobante de origen |
| RF-24 | El sistema bloquea las opciones del comprobante mientras se registra y muestra un resultado único de éxito o error |

### 8.6 Reglas que el core aplica dentro del comprobante (agregadas en v2.0.0)

| ID | Requerimiento |
|---|---|
| RF-25 | Al armar PR, NP, FC o remito, el sistema aplica las promociones, reglas de precio y cupones de descuento vigentes con el mismo resultado que el motor del ERP, incluida la regla de descuento general o por línea (parámetro 311) y de descuento sobre oferta (parámetro 99) (`GestorPromociones`) |
| RF-26 | El sistema calcula los puntos de fidelización del cliente por comprobante y su vencimiento, y un cupón se consume entero, vigente, del mismo cliente y sin atraso en sus pagos (`FuncionesComprobantes.prCalcularPuntos` y `prVencerPuntosComprobante`; NR 03.15 «Consumo de cupones de descuento») |
| RF-27 | El sistema opera en la empresa del usuario logueado: stock, depósitos, comprobantes y numeración se filtran por `IDEMPRESA`, y la facturación de NP de otra empresa respeta el parámetro 116 (`Funciones.fxCondicionEmpresas`) |

---

## 9. Requerimientos no funcionales y restricciones

### 9.1 Tecnología (impuesta por Flexxus)

| Aspecto | Definición |
|---|---|
| Principios no negociables | Core protegido, sin DB directa, Business APIs, Events, aislamiento y eficiencia en costos (Propuesta técnica, «Criterios de trabajo») |
| Core vigente | Delphi cliente-servidor sobre Firebird (migración 2.5 → 5); versión única para toda la base instalada |
| Frentes web vigentes | ERP Web / POS: React 18 + Ionic 8 + Capacitor 7 sobre API v4. Flexxus Order: React 19 + Node.js/Express + MariaDB 10.6 con Sequelize |
| API | flxWebAPI v6: REST JSON, JWT, rutas /v1 a /v6 conviviendo; única capa que accede a la base |
| Proceso | Especificación previa con OpenSpec vinculada a Jira; pruebas Vitest, Jest y Playwright |

> ⚠️ Verificar en la Semana 2, con el track de Tecnología, cuál de los dos frentes web y cuál de las dos bases (Firebird o MariaDB) es la referencia del MVP (S-02, S-03).

### 9.2 Integración y datos (impuesto por AFIP/ARCA y por el core)

| Aspecto | Definición |
|---|---|
| Factura electrónica | Solicitud de CAE por web services de AFIP/ARCA; catálogo oficial de tipos de comprobante; moneda extranjera |
| Padrones | Datos del cliente según ARCA; padrón de percepciones y retenciones |
| Remito electrónico | ARBA (Épica 2) |
| Acceso a datos | Ningún componente externo lee tablas internas del core; todo pasa por API (principio «sin DB directa») |
| Despliegue | API en el servidor de cada cliente (Docker Desktop sobre Windows o PM2 en entornos legacy) y servicios centrales en Docker Swarm del proveedor de Flexxus |

### 9.3 Requerimientos no funcionales del producto

| ID | Requerimiento |
|---|---|
| RNF-01 | Equivalencia funcional: el 100 % de los casos de prueba de equivalencia de los flujos del MVP da el mismo resultado que el ERP vigente (comprobante, importes, stock) |
| RNF-02 | Atomicidad: el comprobante, su efecto en stock y su cobro se graban completos o no se graban; 0 comprobantes parciales en las pruebas de falla |
| RNF-03 | La búsqueda de artículos responde en p95 ≤ 1 s con 100.000 artículos (⏳ a validar volumen real con Flexxus) |
| RNF-04 | Los listados de comprobantes y artículos se paginan y ordenan en el servidor, sin degradación con ≥ 1 millón de comprobantes (⏳ a validar) |
| RNF-05 | El costo incremental por instalación de exponer el MVP se mide y se compara por alternativa de topología (Semana 3, track de Tecnología) |
| RNF-06 | El 100 % de los parámetros de §5.4 se respeta con todos sus valores posibles, verificado por pruebas parametrizadas |
| RNF-07 | Disponibilidad del punto de venta durante el horario comercial del cliente ≥ 99,5 % (⏳ a validar contra el SLA vigente) |

---

## 10. Hallazgos de la documentación y el código de Flexxus que condicionan el alcance

Hallazgos de la Semana 1 que cambian o acotan lo que asume la propuesta técnica; cada uno tiene su decisión en §12.

| # | Hallazgo | Impacto |
|---|---|---|
| **H-1** | **El brief de Flexxus propone Pagos a Proveedores como módulo de referencia.** La propuesta técnica lo registra como cuestión abierta a acordar en la sesión de inicio | El foco en Venta y Stock debe acordarse con el decisor → [S-01](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-2** | **Venta y Stock ya tienen dos reconstrucciones web.** ERP Web / POS v1.164.0 (desde 2021, 12.861 commits) y Flexxus Order 1.0 beta (mar 2024 – oct 2026, 180 cambios especificados, «6 áreas funcionales: ventas, cuenta corriente, compras, fondos, stock y maestros») | El as-is tiene tres implementaciones; hay que decidir cuál es la referencia de comportamiento y cuál la base de la experiencia → [S-02](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-3** | **Conviven dos modelos de datos.** Firebird (ERP Delphi y API v6, migrando a Firebird 5) y MariaDB `order-v6` (386 tablas, 658 procedimientos), que «reemplaza progresivamente» a Firebird «módulo por módulo» (nota de release de Flexxus Order) | La coexistencia ya empezó, sin una fuente de verdad única para stock y comprobantes → [S-03](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-4** | ✅ **Resuelto el 08-10.** La copia del 07-10 estaba incompleta (1.728 archivos sin descargar, entre ellos las 115 unidades de `03-ERP/unit`). La entrega del 08-10 trae `03-ERP/unit` completa, `ERP.dpr`, `04-PS`, `05-Datos Externos` y `06-Librerias` | Las reglas de stock y comprobantes ya se leen en el Delphi (H-14 a H-20) → [S-04](#121-decisiones-abiertas--a-resolver-en-la-épica-1) resuelta, R-1 mitigado |
| **H-5** | **La documentación del carrito describe reglas que el código no implementa.** Según `spec/carrito/README.md` §0.4b, el saldo de cuenta corriente no bloquea ninguna venta, y un cliente con facturas vencidas no se bloquea contra la base real porque el procedimiento `FMA_SALDOSCTACTECLIENTES_V6` no existe en `order-v6`; siete endpoints del carrito no devuelven datos | La documentación no alcanza como fuente de reglas; cada regla del MVP se valida contra el código y contra el referente → R-3 |
| **H-6** | **Un tipo de dato divergente invierte una regla de bloqueo.** `CLIENTES.facturable` es `boolean` en `order-v6` y `string` en el origen (`database-gaps.md` §2.1) | Riesgo de que la venta a un cliente no facturable se permita o se bloquee al revés según la implementación → validación en S2 |
| **H-7** | **La parametrización es masiva y no binaria.** 345 parámetros generales y 5.137 filas de parámetros por punto de venta en la base de test; el carrito lee 28 y el backend lee otros dentro de procedimientos; el 109 es una política con rangos y el 82 se compara de tres formas distintas (`erp-parameters.md` §2 y §4.1) | Una «venta» tiene N variantes según la instalación; el MVP debe definir qué variantes soporta → [S-05](#121-decisiones-abiertas--a-resolver-en-la-épica-1), R-7 |
| **H-8** | **El front web solo carga los permisos del menú 78.** El modelo es un par (menú, permiso) y varias combinaciones comprobante × acción quedan denegadas en silencio, incluida la bonificación por ítem en NC (`erp-permissions.md` §1) | Los permisos del MVP se relevan sobre el Delphi, no sobre el front web |
| **H-9** | **Flexxus Order cambió el modelo de depósitos.** Reemplaza subdepósitos por un árbol de dos niveles; el Delphi tiene Depósitos, Sub Depósitos, Casilleros, Depósitos Externos y Centros de distribución | El efecto de la venta en stock depende del modelo elegido → [S-06](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-10** | **La propuesta Multi-Tenant cambia la pertenencia del stock.** El stock pasa a pertenecer a la sucursal física, con visibilidad cruzada configurable entre compañías. Su premisa de «una sola empresa por instalación» no coincide con el código (H-17) | El modelo Multi-Tenant sigue fuera del MVP; las empresas actuales, no → [S-07](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-11** | **Hay dos variantes del producto en las fuentes.** `Corralon_0336` (vertical Corralón, con Print Server y servidor de depósitos, documentación de 2007-2010) y `Erp_04-12_Provisorio` (ERP general, rama `develop`) | Las diferencias entre instalaciones pueden ser de vertical y no solo de parámetros → [S-05](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-12** | **El Delphi no tiene un manual funcional de Venta ni de Stock** (actualizado 08-10). Su documentación funcional son las notas de release por versión (H-19), más el cuestionario de pre-parametrización (v1.02, 2008), descripciones de tablas del Corralón y ayudas `.chm` de errores y migración | El riesgo R4 de la propuesta se atenúa pero no desaparece: las notas describen cambios, no el comportamiento completo → R-3 |
| **H-13** | **El código tiene residuos que confunden el análisis.** La copia completa del 08-10 trae 231 archivos de conflicto de merge o respaldo (`_BACKUP_`, `_BASE_`, `_LOCAL_`, `_REMOTE_`, `.orig`); `frmFacturacion` tiene cuatro copias de conflicto | Los agentes de análisis deben excluirlos para no duplicar reglas → acción del track de Tecnología |
| **H-14** | **El parámetro 109 combina tres dimensiones en un solo valor de 0 a 9:** contra qué compara (real en 1, 4, 6 y 9; remanente en 0, 2, 5 y 7; remanente más órdenes de compra en 3 y 8), si avisa (0, 4, 5, 9) o bloquea (1, 2, 3, 6, 7, 8) y si valida la NP (solo de 5 a 9). Solo aplica a artículos con `VerificaStock = 1`; la NC nunca valida stock (`Funciones.fxValidarStockArticulos`, `fxTieneQueVerificarStock`) | RF-03 y RF-14 quedan definidos; la experiencia objetivo tiene que mostrar al usuario contra qué stock se validó → [S-12](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-15** | **El stock se guarda en dos niveles y el control de negativos vive en la base.** Cada movimiento actualiza `CASILLEROS` (depósito × lote × empresa) y recalcula `STOCK`; el negativo lo rechaza la base con la excepción `ERROR_STOCK_NEGATIVO` según el artículo. La NR 04.12 crea el parámetro 537 (control por stock general o por depósito) para evitar «intervenciones técnicas manuales» en la base, pero **la constante 537 no existe en esta copia del código** (salta de 536 a 539) | La regla de negativos depende de objetos de la base que no se recibieron; la copia de `develop` no coincide con la 04.12 publicada → [S-14](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-16** | **La lógica de Venta vive en los formularios.** `frmFacturacion` tiene 19.153 líneas, `frmPedidos` 16.817 y `frmRemitoInterno` 15.654; las 7 pantallas de comprobante suman 748 sentencias SQL embebidas y 77 permisos especiales distintos; `ModificarStock` se invoca desde 43 archivos y cada formulario maneja su propia transacción (`prAnularTodasTransacciones`) | Exponer «emitir comprobante» como capacidad del core exige extraer reglas de la UI; el dimensionamiento de la Semana 4 tiene que reflejarlo → R-8 |
| **H-17** | **El Delphi ya es multiempresa dentro de una instalación.** 724 de las 1.401 unidades de `03-ERP` filtran por `IDEMPRESA`; la empresa 1 es la principal, el «modo compilador» suma stock de varias empresas (parámetro 540) y el 116 regula ver y facturar NP de otra empresa (NR 04.11, valores 0 a 3). El parámetro 535 «validar stock por empresa» está declarado pero nadie lo usa | Contradice la premisa de la propuesta Multi-Tenant; el MVP no puede asumir empresa única → RF-27, [S-07](#121-decisiones-abiertas--a-resolver-en-la-épica-1), [S-13](#121-decisiones-abiertas--a-resolver-en-la-épica-1) |
| **H-18** | **Varias «capacidades nuevas» de la v1.0.0 ya existen en el core.** El motor de promociones y cupones (`GestorPromociones`, 144.436 caracteres) lo usan FC, NP, PR y remito; también existen fidelización por puntos, picking, packing, guía de reparto, expedición, optimización de stock y terminales POSNET/VISA (`06-Librerias`) | Se reclasifican: promociones, cupones y puntos a la Épica 1; el resto a la Épica 2 (§1.bis, ronda 08-10) |
| **H-19** | **Las notas de release son la documentación funcional del Delphi.** 3.028 documentos únicos de las versiones 03.01 a 04.12 (Enterprise, Flexxus 4 y Corralón); 1.399 tratan Venta o Stock. Están ordenadas por versión y por ticket, no por capability, con duplicados `.docx`/`.pdf` y archivos temporales | Fuente de evidencia funcional para cada regla del MVP; hay que indexarlas por capability → [O-7](#11-observaciones-sobre-el-backlog-borrador-openspec-y-especificaciones-de-flexxus-order) |
| **H-20** | **La parametrización real es mayor que la del carrito y tiene peso muerto.** El código declara 399 constantes (345 filas en la base de test); las pantallas de Venta del menú leen 163 y las de Stock 79; 12 están declaradas sin uso (entre ellas 200 «depósito de reserva» y 535) y el parámetro 1 «multidepósitos», marcado como descartado, sigue con 132 referencias | El alcance de parametrización del MVP (§5.4) es un subconjunto explícito; el resto se clasifica en la Semana 2 → R-7 |

---

## 11. Observaciones sobre el backlog borrador (OpenSpec y especificaciones de flexxus-order)

No se recibió un backlog Jira para este Discovery. Los repositorios traen especificaciones OpenSpec y las trazas de los tableros Jira FO y FLEXV2; se listan las observaciones para el análisis, no como crítica.

| # | Observación | Acción propuesta |
|---|---|---|
| **O-1** | **No hay backlog del Discovery ni acceso a Jira FO / FLEXV2.** Solo se ven las historias citadas en las especificaciones (FO-225, FO-236, FO-247, FO-300, entre otras) | Pedir acceso de lectura a ambos tableros para cruzar el estado real de Venta y Stock |
| **O-2** | **La especificación del carrito es transitoria.** `spec/carrito/` se vacía a medida que avanzan las 24 subtareas de FO-225; el documento mobile está pendiente | Tomarla como foto al 06/10/2026 y citar la versión del repositorio en cada regla |
| **O-3** | **El carrito documentado es el de `flexxuserpweb`, no el de `flexxus-order`.** El propio README lo aclara (§0.1) | Distinguir en el inventario qué regla vale para cada implementación |
| **O-4** | **Un criterio de aceptación de FO-300 (depósitos) no se cumple.** El selector de artículos responde 500 (spec `deposito-crud`) | Registrarlo como deuda conocida del frente que podría ser base del MVP |
| **O-5** | **La cobertura web vs Delphi no está medida.** El Delphi tiene 94 opciones de Venta y 34 de Stock; las notas de release web describen áreas, no opciones | Construir la matriz de cobertura por opción en la Semana 2 ([entregable parcial S1 v0.2](../flexxus-discovery/2026-10-08-entregable-parcial-s1-venta-stock.md) §2 como base) |
| **O-6** | **El nombre «MVP TCR/ER» no aparece en ninguna fuente.** | Confirmar alcance y significado de la sigla ([S-08](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| **O-7** | **Las notas de release traen número de ticket pero no el tablero de origen.** Por ejemplo, «74606» en la NR 04.12 del parámetro 537 o «441135» en la 04.11 del parámetro 116; los nombres tienen variantes («Enterprice», «Entreprise») y archivos temporales `~$` | Pedir a Flexxus el sistema de tickets de origen para enlazar cada nota con su historia, e indexar las 1.399 notas de Venta y Stock por capability del inventario en la Semana 2 |

---

## 12. Riesgos, dependencias y decisiones abiertas

### 12.1 Decisiones abiertas — a resolver en la Épica 1

| ID | Pregunta | Impacto si no se resuelve | Propuesta del PO |
|---|---|---|---|
| **S-01** ⏳ **SIN DEFINIR** | **¿El módulo de referencia es Venta y Stock o Pagos a Proveedores (brief de Flexxus)?** | La experiencia objetivo se define sobre un módulo que Flexxus no prioriza (R5 de la propuesta) | Presentar Venta y Stock al decisor con el argumento de §1; dejar Pagos a Proveedores como segundo tramo del roadmap |
| **S-02** ⏳ **SIN DEFINIR** | **¿El MVP toma como base Flexxus Order, el ERP Web / POS o se define independiente de ambos?** | Se duplica trabajo ya hecho o se hereda deuda no medida | Tomar el comportamiento del Delphi como referencia y Flexxus Order como base de experiencia; decidir la base técnica en la Semana 3 con el track de Tecnología |
| **S-03** ⏳ **SIN DEFINIR** | **¿Cuál es la fuente de verdad de stock y comprobantes durante la coexistencia: Firebird o MariaDB?** | Diferencias de stock entre implementaciones en clientes que usan ambas | Relevar qué clientes operan Flexxus Order hoy y con qué base; llevarlo como insumo del camino de coexistencia |
| **S-04** ✅ **RESUELTO 08-10** | **¿Puede Flexxus entregar las fuentes completas del ERP (repositorio git o carpeta sincronizada)?** | — | Resuelto: Flexxus entregó `Erp_04-12_Provisorio.zip` completo y las notas de release del Delphi el 08-10 (§1.bis). Queda abierta la correspondencia con la versión publicada ([S-14](#121-decisiones-abiertas--a-resolver-en-la-épica-1)) |
| **S-05** ⏳ **SIN DEFINIR** | **¿Cuántas variantes del producto (verticales) hay en la base instalada y qué parámetros de Venta y Stock varían entre clientes?** | El MVP se diseña para una configuración que no es la mayoritaria | Elegir con el referente de negocio 5 instalaciones representativas y extraer sus valores de `PARAMETROSGENERALES` y `PARAMETROSPUNTOSDEVENTA` |
| **S-06** ⏳ **SIN DEFINIR** | **¿El modelo de depósitos objetivo es el árbol de dos niveles de Flexxus Order o el modelo Delphi?** | El efecto de la venta en stock se especifica dos veces | Relevar cuántos clientes usan subdepósitos, casilleros y depósitos externos; proponer el árbol si el uso es marginal |
| **S-07** ⏳ **SIN DEFINIR** | **¿El modelo Multi-Tenant (Grupo › Compañía › Sucursal) entra en el primer módulo?** (reformulada 08-10: las empresas por instalación ya existen, H-17) | El MVP crece con una jerarquía que el core no tiene, o se diseña sin prever cómo las empresas actuales pasan a compañías | Mantener el modelo Multi-Tenant en la Épica 3; el MVP opera por `IDEMPRESA` (RF-27) y el track de Tecnología define cómo se mapea a compañía |
| **S-08** ⏳ **SIN DEFINIR** | **¿Qué abarca la sigla «MVP TCR/ER»?** | Alcance del MVP interpretado distinto por cada parte | Confirmarlo con el Líder de Producto y registrarlo en §2 |
| **S-09** ⏳ **SIN DEFINIR** | **¿Los cobros por QR y terminales (Mercado Pago, Payway/Prisma, Clover, MODO, Go Cuotas) entran en el MVP?** | Integraciones externas en el camino crítico | Incluir efectivo, tarjeta, cheque, retenciones y cuenta corriente; evaluar las pasarelas por uso real |
| **S-10** ⏳ **SIN DEFINIR** | **¿La facturación masiva y los comprobantes de verticales (granos, carta de porte) quedan fuera del MVP?** | Alcance del MVP sobredimensionado | Dejarlos en la Épica 3 salvo evidencia de uso mayoritario |
| **S-11** ⏳ **SIN DEFINIR** | **¿Sigue vigente la impresora fiscal (cierres X/Z) en la base instalada?** | Se especifica una capacidad en desuso o se omite una obligatoria | Consultar al referente de negocio el porcentaje de clientes con controlador fiscal |
| **S-12** ⏳ **SIN DEFINIR** | **¿Qué valores del parámetro 109 (0 a 9, H-14) y del 82 usa la mayoría de los clientes?** | RF-03 y RF-14 se diseñan para las diez variantes por igual | Extraerlo de la muestra de S-05 y soportar en el MVP solo los valores con uso real |
| **S-13** | **¿El MVP soporta la facturación de NP de otra empresa (parámetro 116 en 1 o 3) y el modo compilador?** | Se omite un caso que usan instalaciones multiempresa, o se carga el MVP con un caso marginal | Medir en la muestra de S-05 cuántas instalaciones tienen más de una empresa y qué valor de 116 usan; incluirlo solo si hay uso real |
| **S-14** | **¿Qué versión del código es la referencia de comportamiento: la rama `develop` recibida o la 04.12 publicada?** La copia no tiene el parámetro 537 de la NR 04.12 (H-15) | Las reglas extraídas no coinciden con lo que corre en los clientes | Pedir al referente técnico la etiqueta o el commit de la 04.12 y los objetos de base (triggers y procedimientos de stock) antes del 14-10 |

### 12.2 Riesgos

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R-1** | **El acceso a las fuentes del Delphi sigue incompleto en la Semana 2** — **mitigado 08-10** (S-04 resuelta). Queda el riesgo residual de que la copia no sea la versión publicada (S-14) | Bajo — reglas extraídas de una versión distinta de la productiva | Confirmar la etiqueta 04.12 con el referente técnico (S-14) |
| **R-2** | **Tres implementaciones con reglas distintas para la misma venta** | Alto — se especifica una regla que no es la vigente | Matriz regla × implementación; el referente técnico decide la canónica |
| **R-3** | **La documentación disponible describe comportamiento no implementado** (H-5, H-12) | Medio — requerimientos falsos en el MVP | Toda regla del MVP con doble evidencia: código y referente |
| **R-4** | **Disponibilidad de los referentes de negocio menor a la prevista** | Medio — fricción no relevada | Agenda cerrada en la Semana 1; sesiones grabadas para validación diferida |
| **R-5** | **Venta y Stock es demasiado amplio para analizar en profundidad en cuatro semanas** (128 opciones de menú) | Alto — análisis superficial; la v2.0.0 suma al MVP el motor de promociones (H-18) | Profundidad solo sobre la Épica 1; las Épicas 2 y 3 a nivel de inventario; del motor de promociones se relevan sus resultados en el comprobante, no su administración |
| **R-6** | **Expectativa de prototipo de la experiencia dentro de la etapa** | Medio — diferencia entre lo esperado y lo entregado | Recordar el «Fuera de alcance» de la propuesta en cada revisión semanal |
| **R-7** | **La parametrización multiplica las variantes del ciclo de venta** (H-7, H-14, H-20) | Alto — el dimensionamiento subestima la construcción | Fijar en S-05 las variantes soportadas y dimensionar por variante |
| **R-8** | **Las reglas de Venta están dispersas en formularios con SQL embebido** (H-16) | Alto — reglas omitidas al exponer el comprobante como capacidad del core, o extracción más lenta que lo planificado | Extraer reglas solo de las pantallas del MVP con agentes de análisis, excluyendo residuos (H-13); validar cada regla con el referente técnico y con su nota de release (H-19) |

### 12.3 Dependencias del cliente Flexxus

| Dependencia | Requerida para | Fecha límite sugerida |
|---|---|---|
| ~~Fuentes completas del ERP Delphi~~ | ✅ Entregadas el 2026-10-08 (S-04) | — |
| Etiqueta o commit de la versión 04.12 y objetos de base de stock (triggers y procedimientos de `CASILLEROS` y `STOCK`) | Épica 1, RF-13, RF-14, S-14 | 2026-10-14 |
| Sistema de tickets de origen de las notas de release | O-7, H-19 | 2026-10-14 |
| Sesión de contextualización de visión de producto y alcance de la modernización | S-01, S-02 | 2026-10-09 |
| Sesiones con referentes de negocio sobre mostrador, facturador web y mobile | OBJ-3, Épica 1 | 2026-10-14 |
| Muestra de 5 instalaciones representativas con sus valores de parámetros | S-05, S-12, RF-21 | 2026-10-14 |
| Acceso de lectura a Jira FO y FLEXV2 | O-1, O-5 | 2026-10-12 |
| Base de referencia Firebird con datos de prueba y acceso de solo lectura a `order-v6` | S-03, S-06 | 2026-10-12 |

---

## 13. Plan de entrega contra el cierre del Discovery

Supuestos: T0 = lunes 2026-10-05 (⏳ a validar), etapa de plazo fijo de cuatro semanas, sin sprints; cada semana cierra con un entregable parcial (Propuesta técnica, «Plan de trabajo»).

| Etapa | Duración | Ventana estimada | Entregable de cierre |
|---|---|---|---|
| **Semana 1** — Relevamiento | 1 semana | 05-10 al 09-10 | Situación actual preliminar de Venta y Stock, inventarios y estado de accesos (este PRD + entregable parcial S1) |
| **Semana 2** — Análisis | 1 semana | 12-10 al 16-10 | Experiencia objetivo preliminar sobre el módulo de referencia; capacidades del core que requiere; candidatos a punto de entrada |
| **Semana 3** — Definición | 1 semana | 19-10 al 23-10 | Funcionalidad objetivo contra lo que la arquitectura habilita; alcance del primer módulo; secuencia posterior |
| **Épica 1** — requerimientos del primer módulo | Semana 4 | 26-10 al 30-10 | RF y RNF con criterio de aceptación; secuencia de las Épicas 2 y 3 |
| **Holgura hasta el cierre del Discovery** | 0 días | — | Ninguna: una sesión que se reprograma sin reemplazo afecta el resultado |

**Lectura del PO sobre la fecha (actualizada al 2026-10-08):** con S-04 resuelta, el camino crítico pasa a ser S-01 → extracción de reglas de las pantallas de comprobante en la Semana 2 (H-16, R-8) → alcance del primer módulo en la Semana 3. Sigue sin haber holgura: la reclasificación del corte suma el motor de promociones al MVP, y la muestra de instalaciones (S-05) define cuántas de las variantes de los parámetros 109, 82 y 116 se soportan.

En consecuencia, las prioridades de lo que resta de la Semana 1 son:

1. **Acordar el módulo de referencia y el corte v2.0.0 con el decisor (S-01)** — sin él la Semana 2 no tiene destino.
2. **Pedir la muestra de instalaciones (S-05)** — define S-12 y S-13 y acota las variantes de parametrización del MVP.
3. **Confirmar la versión de referencia del código y los objetos de base de stock (S-14)** — evita extraer reglas de una versión que no corre en los clientes.
4. **Agendar las sesiones con referentes de negocio** — mostrador, facturador web y mobile.
5. **Confirmar la sigla «MVP TCR/ER» (S-08)** — evita una lectura distinta del alcance.

---

## 14. Criterios de aceptación de la etapa Venta y Stock (DoD de fase)

La etapa Venta y Stock se considera completa cuando:

- [ ] El inventario de capabilities de Venta y Stock tiene ≥ 90 % de capabilities con fuente citada y estado por implementación, revisado por el referente técnico (OBJ-1)
- [ ] Los parámetros de §5.4 tienen efecto y valores observados en la muestra de instalaciones de S-05 (OBJ-2)
- [ ] El flujo as-is del ciclo de venta está validado en sesión con el referente de negocio, con ≥ 10 fricciones con evidencia (OBJ-3)
- [ ] El decisor de Flexxus aprobó por escrito el módulo de referencia y el corte del MVP (S-01, S-02 resueltas) (OBJ-4)
- [ ] La tabla de estado de accesos y el inventario de documentación se entregaron al cierre de la Semana 1, con responsable por cada pendiente (OBJ-5)
- [ ] Cada RF de §8 tiene origen trazado (pantalla del Delphi o regla web) y criterio de aceptación (OBJ-6)
- [ ] Ninguna S-nn del alcance de la Épica 1 queda sin definir al cierre de la Semana 4

---

*Documento generado como insumo para el refinamiento de historias de usuario con el agente `po-expert-user-stories`.*
