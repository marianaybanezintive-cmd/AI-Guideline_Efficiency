# Flexxus — Discovery de modernización · Entregable parcial Semana 1 (track de Producto)

> **Alcance:** solo **Venta** y **Stock**. Compras, Fondos, Contabilidad, RMA, Producción, Calidad y RR.HH. no se relevan.
> **Fecha:** 2026-10-07 · **Versión:** v0.1 preliminar, para revisión con los referentes de Flexxus
> **Autor:** Líder de Producto (intive)
> **Documento asociado:** [PRD Venta y Stock](../prd/PRD-flexxus-venta-stock-2026-10-07.md) (corte del MVP, requerimientos, hallazgos H-n y decisiones abiertas S-nn)

Este documento resume los cuatro puntos pedidos para el entregable parcial de la Semana 1. Las decisiones y los riesgos no se repiten acá: viven en el PRD y se citan por su ID.

---

## Resumen

| Punto | Estado | Lo principal |
|---|---|---|
| 1. Situación actual preliminar | 🟡 Preliminar | Venta y Stock existen en **tres implementaciones**: el ERP Delphi, el ERP Web / POS y Flexxus Order (beta). Conviven dos bases de datos (Firebird y MariaDB) |
| 2. Inventario de módulos y capabilities | 🟡 Preliminar | **24 capabilities de Venta** y **12 de Stock**, sobre 94 opciones de menú de Venta y 34 de Stock del Delphi |
| 3. Inventario de documentación | 🟡 Parcial | 19 fuentes catalogadas. **No hay documentación funcional vigente del Delphi**; la mejor documentación de reglas es la del carrito web, y tiene reglas que el código no implementa |
| 4. Foco Venta y Stock | ✅ Definido | Corte del MVP propuesto: el ciclo de un comprobante de venta y su efecto en stock. Pendiente de acuerdo con Flexxus (S-01) |
| Estado de accesos | 🔴 Bloqueante parcial | Las fuentes del ERP general están **incompletas** (1.728 archivos sin descargar, incluida la lógica de Venta y Stock) |

---

## 1. Situación actual preliminar

### 1.1 El producto

Flexxus es un ERP con más de veinte años de producto y más de 2.200 clientes activos. Es una aplicación Delphi cliente-servidor sobre Firebird, con **una versión única** para toda la base instalada, que se adapta a cada cliente por parametrización y está cerrada a la extensión.

### 1.2 Cómo se implementan hoy Venta y Stock

| Implementación | Qué es | Usuarios | Estado | Venta | Stock |
|---|---|---|---|---|---|
| **ERP Delphi** (`Erp_04-12_Provisorio`, rama `develop`) | Core transaccional de escritorio | Toda la base instalada | En producción | Completa (94 opciones de menú) | Completa (34 opciones + maestros) |
| **Flexxus Corralón** (`Corralon_0336`, rama `master`) | Variante vertical del ERP para corralones, con Print Server y servidor de depósitos | Clientes del vertical | En producción ⏳ a confirmar | Variante | Variante |
| **ERP Web / POS** (`flexxuserpweb` v1.164.0) | Facturador web y app mobile para vendedores y viajantes, sobre la API v4 | Mostrador y calle | En producción desde 2021 | Carrito (FC, NP, PR, NC), cobros con pasarelas, cuenta corriente, pedidos, hoja de ruta | Consulta de stock por depósito, toma de inventario |
| **Flexxus Order** (1.0 beta) | Nueva generación web (React 19, Node.js, MariaDB) que reemplaza a Flexxus web V2 | ⏳ a confirmar qué clientes | Beta; migración de base módulo por módulo | Carrito nuevo, cobro unificado, NC, ND, pedidos, presupuestos, remitos, factura electrónica, libro IVA | Depósitos en árbol de 2 niveles, ajustes con motivo, remitos entre depósitos |
| **Flexxus Web API v6** (2.8.337.0) | API REST versionada (/v1 a /v6), única capa de acceso a la base para terceros | Ecommerce, integradores y apps de Flexxus | En producción; migrando a Firebird 5 | Comprobantes, clientes, cobros, pedidos | Existencias por depósito, tomas de inventario |

### 1.3 Modelo de datos

| Base | Usada por | Lo que se sabe |
|---|---|---|
| **Firebird** (2.5 → 5) | ERP Delphi, API v6, ERP Web / POS | Lógica en procedimientos almacenados. No se recibió el esquema de la base del ERP general; solo la descripción de tablas del Corralón (44 tablas maestras, 29 de movimientos) |
| **MariaDB `order-v6`** | Flexxus Order | Dump del 06/10/2026: 386 tablas y 658 procedimientos. Tablas centrales de Venta y Stock: `CABEZACOMPROBANTES` / `CUERPOCOMPROBANTES`, `CABEZAPEDIDOS` / `CUERPOPEDIDOS`, `CABEZAPRESUPUESTOS`, `VINCULOREMITOS`, `STOCK`, `DEPOSITOS`, `CORRECCIONESSTOCKMANUALES`, `MOTIVOSAJUSTESSTOCK`, `LISTASPRECIO`, `ARTICULOS_LISTASPRECIO` |

### 1.4 Modelo de parametrización (primer relevamiento)

| Nivel | Dónde vive | Volumen observado | Ejemplos en Venta y Stock |
|---|---|---|---|
| Parámetros generales | `PARAMETROSGENERALES` | 345 parámetros | 4 (precios con IVA), 43 (cantidad de listas), 55 (solo artículos con stock), 58 (contado por defecto), 82 (facturar sin descontar stock), 109 (validación de stock), 154 (remito con factura de contado) |
| Parámetros por punto de venta | `PARAMETROSPUNTOSDEVENTA` | 5.137 filas en la base de test | Numeración, tipo de salida (controlador fiscal, impresora o manual) |
| Parámetros propios del POS web | Configuración › Parámetros del POS | ⏳ a contar | Orden del listado, fotos, artículos sin cargo |
| Permisos | Par (menú, permiso) por perfil | 1.058 permisos especiales; 566 ítems de menú | 402 / 404 / 405: validar cuenta corriente en NP / FC / NC |
| Configuración por instalación | `Flexxus.ini`, `PuntosDeVenta.ini` | Uno por instalación | Servidor y ruta de base, motor y dialecto |

El carrito web lee 28 parámetros; el 109 es una política con rangos, no un sí/no, y el 82 se interpreta de tres formas distintas en el código web (PRD H-7). La implantación de un cliente nuevo se basa en un **cuestionario de pre-parametrización** (v1.02, 2008) que cubre depósitos, puntos de venta, cajas, monedas, generalidades de ventas y clientes, sucursales e impresiones.

**Diferencias entre instalaciones:** todavía no medidas. Hay al menos dos fuentes de variación: los **valores de parámetros** y la **variante vertical** del producto (Corralón vs ERP general). Se propone medirlas sobre 5 instalaciones representativas (PRD S-05).

### 1.5 Esquema de despliegue (lo que se sabe, insumo del track de Tecnología)

- La API corre **en el servidor de cada cliente**, en Docker Desktop sobre Windows con un reverse proxy, o por consola con PM2 en entornos legacy que no soportan Docker.
- Los servicios centrales de Flexxus corren en un clúster Docker Swarm administrado con Portainer, en la infraestructura de su proveedor.
- Flexxus Order se despliega con Docker y Bitbucket Pipelines; el ERP Web / POS como PWA y builds Android/iOS.
- El ERP Delphi se conecta a la base por la configuración de `Flexxus.ini` (servidor y ruta de la base Firebird).

Topología por cliente, versionado, seguridad y costo: a relevar por el track de Tecnología.

### 1.6 Fricción del usuario (hipótesis a validar en sesión)

Las fricciones confirmadas requieren las sesiones con referentes de negocio. Hipótesis tomadas de las fuentes:

- **Navegación por menú extenso:** el Delphi expone 574 acciones en 12 solapas; solo Venta tiene 94 opciones repartidas en 14 grupos. Es el límite de productividad que declara Flexxus.
- **Varias formas de cerrar una venta:** el cobro difiere por comprobante en el Delphi; Flexxus Order lo unificó porque «el cajero aprende una sola forma de cerrar una venta».
- **Configuración que el usuario no ve:** el mismo comprobante se comporta distinto según 28 o más parámetros y según permisos que pueden denegarse en silencio (PRD H-8).
- **Bloqueos de cuenta corriente inconsistentes:** la venta a un cliente con facturas vencidas no se bloquea en la implementación web contra la base real (PRD H-5).

---

## 2. Inventario de módulos y capabilities (Venta y Stock)

### 2.1 Módulos del ERP Delphi

El menú principal (`frmPrincipal.dfm`) tiene 12 solapas: Inicio, Archivos, **Ventas**, Compras, Fondos, Contabilidad, RMA, **Stock**, Producción, Calidad, RR.HH. e Informes. El código tiene 978 formularios (sin contar residuos de merge): unos 209 de Venta, 156 de Stock y artículos, y 22 compartidos, según su nombre.

| Solapa | Grupo de menú | Opciones | Ejemplos |
|---|---|---|---|
| Ventas | Comprobantes › Facturación | 17 | Factura, factura manual, facturación de pedidos y de remitos, NC, ND, solicitud de NC, débito interno, liquidación de granos |
| Ventas | Comprobantes › Impresora fiscal | 5 | Cierre X, cierre Z, control de numeración |
| Ventas | Comprobantes › Facturación electrónica | 1 | Facturación electrónica |
| Ventas | Comprobantes › Facturación masiva | 2 | Facturación masiva, lotes |
| Ventas | Comprobantes › Notas de pedido | 8 | Pedido, planilla, pendientes por cliente y por pedido, salida, anulación, autorización |
| Ventas | Comprobantes › Presupuestos | 3 | Presupuesto, planilla, anulación |
| Ventas | Comprobantes › Remitos | 10 | Remito, remito manual, por devolución, internos, expedición, remito electrónico ARBA |
| Ventas | Comprobantes › Otros | 12 | Carta de porte, guía de reparto, ticket, garantías, contrarreembolso, cierres Z |
| Ventas | Comprobantes › Consulta | 5 | Consulta, numeración, anulación, anulación por numeración |
| Ventas | Cuentas corrientes | 11 | Cuenta corriente, movimientos, cobros, intereses, cobranza masiva |
| Ventas | Precios y bonificaciones | 9 | Precios, consulta por forma de pago, lista editable, bonificaciones, promociones |
| Ventas | Vendedores | 5 | Comisiones, períodos, premios |
| Ventas | Fidelización de clientes | 4 | Premios, puntos, coeficientes |
| Ventas | Ventas no realizadas | 2 | Nueva VNR, costo de oportunidad |
| **Ventas** | **Total** | **94** | |
| Stock | Correcciones de stock | 3 | Nuevo ajuste, planilla, despachos de aduana |
| Stock | Consulta de movimientos | 7 | Listado general y por depósito, histórico, series, distribuciones |
| Stock | Transferencias entre depósitos | 9 | Remito de salida, de entrada, manual, automático, movimientos internos, consumo interno |
| Stock | Inventarios | 8 | Toma, actualización, carga de cantidades, carga desde archivo |
| Stock | Análisis de stock | 3 | Rotación, optimización mínimo/máximo, diferencias |
| Stock | Transformaciones | 3 | Estructura de producto, movimiento de producción |
| Stock | Reparto | 1 | Confirmación de entrega |
| **Stock** | **Total** | **34** | |
| Archivos | Artículos / Depósitos | 17 / 5 | Maestros que consumen Venta y Stock |

Además hay unas 20 acciones de Venta y Stock fuera de categoría: picking, packing, preparación de mercadería, hojas de ruta, cierres de stock, antigüedad de stock, motivos de ajuste, acopios, reglas de precio, políticas de redondeo y promociones.

### 2.2 Capabilities y su presencia por implementación

Leyenda: ✅ presente · 🟡 parcial o con brechas documentadas · ❌ no presente · ⏳ a verificar. Épica: 1 = MVP, 2 = operación de stock, 3 = capacidades nuevas, — = fuera de la etapa.

**Venta**

| ID | Capability | Delphi | ERP Web / POS | Flexxus Order | API v6 | Épica |
|---|---|---|---|---|---|---|
| CV-01 | Consulta de artículos, precios y stock al vender | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-02 | Talles, lotes y códigos de barra en la venta | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-03 | Presupuesto | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-04 | Nota de pedido (con anticipo y fecha de entrega) | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-05 | Factura y factura electrónica (CAE) | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-06 | Nota de crédito vinculada a factura | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-07 | Nota de débito | ✅ | ⏳ | ✅ | ⏳ | 1 |
| CV-08 | Remito de venta y de devolución | ✅ | ⏳ | ✅ | ✅ | 1 |
| CV-09 | Facturación de pedidos y de remitos pendientes | ✅ | ⏳ | ✅ | ⏳ | 1 |
| CV-10 | Consulta, reimpresión, envío y anulación de comprobantes | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-11 | Cobro en el checkout (efectivo, tarjeta, cheque, retenciones, CC) | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-12 | Validación de cuenta corriente y límite de crédito al vender | ✅ | 🟡 | 🟡 | ✅ | 1 |
| CV-13 | Precios por lista, multiplazo, pactados, ofertas y descuentos | ✅ | ✅ | 🟡 | ✅ | 1 |
| CV-14 | Percepciones y retenciones en la venta | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-15 | Acopios (venta con entrega diferida) | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-16 | Libro IVA ventas e informes de ventas | ✅ | 🟡 | ✅ | ⏳ | — |
| CV-17 | Impresora fiscal (cierres X/Z) | ✅ | ❌ | ❌ | ❌ | ⏳ S-11 |
| CV-18 | Cobro con QR y terminales (MP, Payway/Prisma, Clover, MODO, Go) | ⏳ | ✅ | ⏳ | ✅ | ⏳ S-09 |
| CV-19 | Facturación masiva y por lote | ✅ | ❌ | ❌ | ⏳ | 3 |
| CV-20 | Comprobantes de verticales (granos, carta de porte, garantías, contrarreembolso) | ✅ | ❌ | ❌ | ⏳ | 3 |
| CV-21 | Picking, packing, preparación y hoja de ruta | ✅ | ✅ | ⏳ | ✅ | 3 |
| CV-22 | Vendedores, comisiones y premios | ✅ | 🟡 | ❌ | ⏳ | 3 |
| CV-23 | Fidelización y ventas no realizadas | ✅ | ❌ | ❌ | ❌ | 3 |
| CV-24 | Gestión de cuenta corriente fuera de la venta (intereses, cobranza masiva) | ✅ | 🟡 | ✅ | ✅ | — |

**Stock**

| ID | Capability | Delphi | ERP Web / POS | Flexxus Order | API v6 | Épica |
|---|---|---|---|---|---|---|
| CS-01 | Descuento, reserva y reingreso de stock por comprobante de venta | ✅ | ✅ | ✅ | ✅ | 1 |
| CS-02 | Validación de stock al vender (parámetro 109) | ✅ | ✅ | ✅ | ⏳ | 1 |
| CS-03 | Consulta de stock por depósito y por sucursal | ✅ | ✅ | ⏳ | ✅ | 1 |
| CS-04 | Ajustes de stock con motivo | ✅ | ❌ | ✅ | ⏳ | 2 |
| CS-05 | Transferencias entre depósitos y movimientos internos | ✅ | ❌ | ✅ | ⏳ | 2 |
| CS-06 | Toma de inventario | ✅ | ✅ (conteo) | ⏳ | ✅ | 2 |
| CS-07 | Consulta de movimientos, histórico, series y lotes | ✅ | ❌ | ⏳ | ⏳ | 2 |
| CS-08 | Maestro de depósitos (subdepósitos, casilleros, externos, centros de distribución) | ✅ | ❌ | 🟡 (árbol de 2 niveles) | ⏳ | 2 |
| CS-09 | Maestro de artículos y listas de precio | ✅ | ✅ | ✅ | ✅ | 2 |
| CS-10 | Cierres de stock y despachos de aduana | ✅ | ❌ | ❌ | ⏳ | 2 |
| CS-11 | Análisis de rotación, optimización y antigüedad | ✅ | ❌ | ❌ | ❌ | 3 |
| CS-12 | Transformaciones de artículos | ✅ | ❌ | ❌ | ❌ | 3 |

Conteo: 15 capabilities de Venta y 3 de Stock en el MVP (Épica 1); 7 en la Épica 2; 7 en la Épica 3; 2 fuera de la etapa y 2 a decidir.

La presencia ✅ de Flexxus Order sale de su nota de release; la de ERP Web / POS, de su nota de release y su documento funcional; la de API v6, de su nota de release. Los ⏳ se verifican contra el código en la Semana 2.

---

## 3. Inventario de documentación disponible

Confiabilidad: **Alta** = verificada contra el código por su autor · **Media** = descriptiva, sin verificación · **Baja** = antigua o de otra variante del producto.

| # | Documento | Tipo | Versión / fecha | Cubre Venta | Cubre Stock | Confiabilidad | Uso en la etapa |
|---|---|---|---|---|---|---|---|
| D-01 | `Flexxus - Propuesta Tecnica v1.0.docx` | Propuesta de Discovery | v1.0, sep 2026 | — | — | Alta | Alcance, plan y entregables |
| D-02 | Documento funcional Punto de Venta (`flexxuserpweb`) | Funcional | v3.2, 78 págs. | ✅ | 🟡 | Media | Flujo de venta web, parámetros (págs. 68–71) y permisos (72–74) |
| D-03 | Nota de release Flexxus Order | Release | 1.0 beta, 06/10/2026 | ✅ | ✅ | Media | Capabilities y stack de Flexxus Order |
| D-04 | Nota de release ERP Web / POS | Release | 1.164.0, 06/10/2026 | ✅ | 🟡 | Media | Capabilities del POS y sus integraciones |
| D-05 | Nota de release Web API v6 | Release | 2.8.337.0, 06/10/2026 | ✅ | ✅ | Media | Cobertura de la API y despliegue |
| D-06 | Propuesta Arquitectura Multi-Tenant | Propuesta técnica | mayo 2026 | 🟡 | ✅ | Media | Stock por sucursal, multiempresa (Épica 3) |
| D-07 | `spec/carrito/` de `flexxus-order` (README, factura, pedido, presupuesto, NC) | Especificación funcional | viva, al 06/10/2026 | ✅ | 🟡 | **Alta**, con correcciones registradas | Reglas del ciclo de venta, con las que el código no cumple |
| D-08 | `spec/carrito/erp-parameters.md`, `erp-permissions.md` | Inventario de parámetros y permisos | viva | ✅ | ✅ | Alta | 28 parámetros del carrito y modelo de permisos |
| D-09 | `spec/carrito/database-gaps.md`, `backend-contract-identifiers.md` | Brechas de base y de endpoints | viva | ✅ | 🟡 | Alta | Brechas entre implementaciones |
| D-10 | `openspec/specs/*` de `flexxus-order` (37 especificaciones) | Especificaciones de capabilities | viva | ✅ | ✅ (`deposito-crud`) | Alta | Comportamiento implementado en Flexxus Order |
| D-11 | `openspec/changes/archive` de `flexxus-order` (180 cambios) | Historial de cambios | mar–sep 2026 | ✅ | ✅ | Alta | Trazabilidad de qué se migró |
| D-12 | `specs/` de `flxwebapi-v6` (37 archivos) e `install.docx` | Especificaciones de la API e instalación | viva | 🟡 | 🟡 | Alta | Endpoints y migración a Firebird 5 |
| D-13 | Dump MariaDB `flexxusorder` | Modelo de datos | 06/10/2026 | ✅ | ✅ | Alta | Tablas, procedimientos y valores de parámetros de test |
| D-14 | Cuestionario de Pre-Parametrización (Flexxus Corralón) | Guía de implantación | v1.02, 2008 | ✅ | ✅ | Baja | Base para relevar el modelo de parametrización |
| D-15 | Descripción de tablas Corralón (2 planillas) | Modelo de datos | sin fecha | ✅ | ✅ | Baja | Estructura de comprobantes y stock del Delphi |
| D-16 | Plantillas de migración (Corralón Express, NE) | Layout de migración | sin fecha | 🟡 | ✅ | Baja | Campos maestros de artículos y stock |
| D-17 | `Flexxus Corralón.doc` | Lista de funcionalidades | sin fecha | 🟡 | 🟡 | Baja | Alcance del vertical |
| D-18 | Ayudas `.chm` del ERP (errores BDE, migración de datos) | Ayuda | sin fecha | — | — | Baja | Sin uso para Venta y Stock |
| D-19 | Skills y agentes de los repositorios (`erp-functional-analyst`, `delphi-reading-guide`) | Guía de análisis del código | viva | — | — | Media | Insumo para configurar los agentes de análisis |

**No hay:** documentación funcional vigente del ERP Delphi para Venta y Stock, esquema de la base Firebird del ERP general, ni backlog Jira accesible. Las notas de release y las especificaciones son del **06/10/2026**, un día antes de este relevamiento.

---

## 4. Foco Venta y Stock: qué entra y qué se ignora

- **Se analiza:** todo lo que nace de un comprobante de venta al cliente y su efecto en stock (MVP), más el inventario de la operación de stock y de las capacidades nuevas (Épicas 2 y 3) a nivel de catálogo.
- **Se ignora:** Compras, Fondos (salvo el cobro en el checkout), Contabilidad, RMA, Producción, Calidad, RR.HH. y la gestión de cuenta corriente fuera de la venta.
- **Corte propuesto para el MVP:** «entra lo que ocurre entre la búsqueda del artículo y la confirmación del comprobante de venta, incluido su efecto inmediato en el stock; queda afuera lo que mueve stock o maestros sin venta, y lo que exige una capacidad que el core no tiene». Detalle y matriz en el PRD §5.
- **Pendiente de acordar con Flexxus:** el brief propone Pagos a Proveedores como módulo de referencia (PRD S-01), y no está definida la sigla «MVP TCR/ER» (PRD S-08).

---

## Estado de cada acceso

| Acceso | Estado | Detalle | Acción |
|---|---|---|---|
| Fuentes del ERP Delphi general (`Erp_04-12_Provisorio`) | 🔴 Parcial | OneDrive no descargó 1.728 archivos: `03-ERP/unit` (115 unidades de lógica, entre ellas `UStock`, `UArticulos`, `FuncionesComprobantes`, `FuncionesRemitos`), `04-PS`, `05-Datos Externos`, `06-Librerias`, `03-ERP/sueldos`. Falta el `.dpr` del ERP | Pedir el repositorio git o volver a sincronizar la carpeta (PRD S-04), antes del 09-10 |
| Fuentes de Flexxus Corralón (`Corralon_0336`) | ✅ Disponible | 2.650 archivos, sin faltantes en el registro de OneDrive | — |
| Repositorios `flexxus-order`, `flexxuserpweb`, `flxwebapi-v6` | 🟡 Snapshot | Comprimidos del 06/10/2026; sin acceso al repositorio remoto | Pedir acceso de lectura si se necesita historial |
| Modelo de datos MariaDB (`order-v6`) | 🟡 Dump | Dump completo; sin acceso a una base en vivo | Pedir acceso de solo lectura a la base de test |
| Modelo de datos Firebird del ERP | 🔴 Pendiente | Solo la descripción de tablas del Corralón | Pedir esquema o base de referencia |
| Entorno de referencia con datos de prueba | 🔴 Pendiente | No recibido | Confirmar con el administrador de accesos |
| Jira FO y FLEXV2 | 🔴 Pendiente | Solo hay referencias en las especificaciones | Pedir acceso de lectura |
| Documentos legacy `.doc` / `.xls` | ✅ Disponible | Convertidos a texto para el análisis | — |

---

*Siguiente paso: validar este documento con los referentes de Flexxus en la sesión de cierre de la Semana 1 y resolver S-01, S-04 y S-05 del PRD.*
