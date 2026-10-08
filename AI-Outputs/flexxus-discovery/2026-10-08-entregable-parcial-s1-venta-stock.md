# Flexxus — Discovery de modernización · Entregable parcial Semana 1 (track de Producto)

> **Alcance:** solo **Venta** y **Stock**. Compras, Fondos, Contabilidad, RMA, Producción, Calidad y RR.HH. no se relevan.
> **Fecha:** 2026-10-08 · **Versión:** v0.2 preliminar, para revisión con los referentes de Flexxus. Reemplaza a la [v0.1 del 07-10](2026-10-07-entregable-parcial-s1-venta-stock.md)
> **Autor:** Líder de Producto (intive)
> **Documento asociado:** [PRD Venta y Stock v2.0.0](../prd/PRD-flexxus-venta-stock-2026-10-08.md) (corte del MVP, requerimientos, hallazgos H-n y decisiones abiertas S-nn)

Este documento resume los cuatro puntos pedidos para el entregable parcial de la Semana 1. Las decisiones y los riesgos no se repiten acá: viven en el PRD y se citan por su ID.

**Qué cambió respecto de la v0.1:** el 08-10 llegaron las fuentes completas del ERP y tres colecciones de notas de release del Delphi. Con ellas se verificó en el código la lógica de Venta y Stock que antes faltaba. El resultado cambia el inventario (varias capabilities que se creían nuevas ya existen en el core) y corrige un supuesto: el Delphi ya opera varias empresas por instalación.

---

## Resumen

| Punto | Estado | Lo principal |
|---|---|---|
| 1. Situación actual preliminar | 🟡 Preliminar, con reglas verificadas en el código | Venta y Stock existen en **tres implementaciones** (ERP Delphi, ERP Web / POS y Flexxus Order beta) sobre dos bases (Firebird y MariaDB). Las reglas de stock del Delphi ya están leídas en el código: fórmula de stock remanente, las diez variantes del parámetro 109, descuento por casillero y control de negativos en la base |
| 2. Inventario de módulos y capabilities | 🟡 Preliminar | **26 capabilities de Venta** y **13 de Stock**, sobre 94 opciones de menú de Venta y 34 de Stock que abren 58 y 27 formularios. **20 en el MVP**, 14 en la Épica 2, 1 en la Épica 3 |
| 3. Inventario de documentación | 🟡 Mejorado | 24 fuentes catalogadas. La documentación funcional del Delphi son **3.028 notas de release** (1.399 de Venta o Stock); no hay manual funcional ni esquema de la base Firebird |
| 4. Foco Venta y Stock | ✅ Definido, corte revisado | MVP: el ciclo de un comprobante de venta, con lo que el core aplica dentro de él (promociones, cupones, puntos) y su efecto en stock, en la empresa del usuario. Pendiente de acuerdo con Flexxus (S-01) |
| Estado de accesos | 🟡 Fuentes OK, quedan pendientes | Fuentes del ERP completas. Siguen pendientes: versión de referencia del código (S-14), base Firebird de referencia, entorno de prueba y Jira |

---

## 1. Situación actual preliminar

### 1.1 El producto

Flexxus es un ERP con más de veinte años de producto y más de 2.200 clientes activos. Es una aplicación Delphi cliente-servidor sobre Firebird, con **una versión única** para toda la base instalada, que se adapta a cada cliente por parametrización y está cerrada a la extensión. Las notas de release muestran una evolución continua: versiones Enterprise 03.09 a 04.12 y Corralón 03.01 a 03.37.

### 1.2 Cómo se implementan hoy Venta y Stock

| Implementación | Qué es | Usuarios | Estado | Venta | Stock |
|---|---|---|---|---|---|
| **ERP Delphi** (`Erp_04-12_Provisorio`, rama `develop`) | Core transaccional de escritorio | Toda la base instalada | En producción | Completa (94 opciones de menú, 58 formularios), con motor de promociones, multiempresa y terminales POSNET/VISA | Completa (34 opciones, 27 formularios, más maestros) |
| **Flexxus Corralón** (`Corralon_0336`, rama `master`) | Variante vertical del ERP para corralones, con Print Server y servidor de depósitos | Clientes del vertical | En producción (notas de release hasta la Cln 03.37) | Variante | Variante |
| **ERP Web / POS** (`flexxuserpweb` v1.164.0) | Facturador web y app mobile para vendedores y viajantes, sobre la API v4 | Mostrador y calle | En producción desde 2021 | Carrito (FC, NP, PR, NC), cobros con pasarelas, cuenta corriente, pedidos, hoja de ruta | Consulta de stock por depósito, toma de inventario |
| **Flexxus Order** (1.0 beta) | Nueva generación web (React 19, Node.js, MariaDB) que reemplaza a Flexxus web V2 | ⏳ a confirmar qué clientes | Beta; migración de base módulo por módulo | Carrito nuevo, cobro unificado, NC, ND, pedidos, presupuestos, remitos, factura electrónica, libro IVA | Depósitos en árbol de 2 niveles, ajustes con motivo, remitos entre depósitos |
| **Flexxus Web API v6** (2.8.337.0) | API REST versionada (/v1 a /v6), única capa de acceso a la base para terceros | Ecommerce, integradores y apps de Flexxus | En producción; migrando a Firebird 5 | Comprobantes, clientes, cobros, pedidos | Existencias por depósito, tomas de inventario |

### 1.3 Modelo de datos

| Base | Usada por | Lo que se sabe |
|---|---|---|
| **Firebird** (2.5 → 5) | ERP Delphi, API v6, ERP Web / POS | El stock vive en dos niveles: `CASILLEROS` (artículo × depósito × lote × empresa, con `StockActual`) y `STOCK` (total por artículo y lote, recalculado después de cada movimiento). El control de stock negativo lo hacen objetos de la base (excepción `ERROR_STOCK_NEGATIVO`). Todo filtra por `IDEMPRESA`. No se recibió el esquema completo ni los triggers y procedimientos (PRD S-14) |
| **MariaDB `order-v6`** | Flexxus Order | Dump del 06/10/2026: 386 tablas y 658 procedimientos. Tablas centrales de Venta y Stock: `CABEZACOMPROBANTES` / `CUERPOCOMPROBANTES`, `CABEZAPEDIDOS` / `CUERPOPEDIDOS`, `CABEZAPRESUPUESTOS`, `VINCULOREMITOS`, `STOCK`, `DEPOSITOS`, `CORRECCIONESSTOCKMANUALES`, `MOTIVOSAJUSTESSTOCK`, `LISTASPRECIO`, `ARTICULOS_LISTASPRECIO` |

### 1.4 Modelo de parametrización

| Nivel | Dónde vive | Volumen observado | Ejemplos en Venta y Stock |
|---|---|---|---|
| Parámetros generales | `PARAMETROSGENERALES`; constantes en `uParametrosGenerales.pas` | **399 constantes en el código** (345 filas en la base de test); las pantallas de Venta del menú leen 163 y las de Stock 79; 12 declaradas sin uso | 4, 43, 52, 55, 58, 82, 109, 116, 154, 287 (ver tabla siguiente) |
| Parámetros por punto de venta | `PARAMETROSPUNTOSDEVENTA` | 5.137 filas en la base de test | Numeración, tipo de salida (controlador fiscal, impresora o manual) |
| Parámetros propios del POS web | Configuración › Parámetros del POS | ⏳ a contar | Orden del listado, fotos, artículos sin cargo |
| Permisos | Par (menú, permiso) por perfil, más permisos especiales por pantalla | 1.058 permisos especiales; 566 ítems de menú; **77 permisos especiales distintos** solo en las 7 pantallas de comprobante | 402 / 404 / 405: validar cuenta corriente en NP / FC / NC; 963: destildar la validación de cuenta corriente |
| Configuración por instalación | `Flexxus.ini`, `PuntosDeVenta.ini` | Uno por instalación | Servidor y ruta de base, motor y dialecto |

**Parámetros clave con su efecto verificado en el código:**

| Parámetro | Qué decide | Valores y efecto |
|---|---|---|
| **109** Validación de stock | Contra qué stock se valida, si avisa o bloquea, y si valida la NP | Real: 1, 4, 6, 9 · Remanente: 0, 2, 5, 7 · Remanente + órdenes de compra: 3, 8. Avisa con 0, 4, 5, 9; bloquea con 1, 2, 3, 6, 7, 8. La NP se valida solo de 5 a 9. Solo aplica a artículos que verifican stock; la NC nunca valida |
| **82** Facturar sin descontar stock | Qué comprobante mueve stock | Activo: la FC no descuenta y el remito sí; lo facturado sin remitir resta del remanente |
| **52 / 154** Remito al facturar (cuenta corriente / contado) | Si la FC genera el remito | 1 tildado y editable · 2 tildado y fijo · 3 no disponible · 4 a elección; no aplica con entrega pactada o reparto propio |
| **116** NP de otras empresas | Ver y facturar NP de otra empresa | 0 ve todas, factura solo las propias · 1 ve y factura todas · 2 ve y factura solo las propias · 3 ve solo las propias y factura de otras (NR 04.11) |
| **287** Validar siempre cuenta corriente | Si el vendedor puede saltear la validación | Activo: la validación queda tildada y solo la destilda el permiso especial 963 |
| **537** Control de stock negativo | Por stock general de la empresa o por depósito | Creado en la NR 04.12; **no está en la copia del código recibida** (PRD H-15, S-14) |

El stock remanente se calcula así: stock real − stock comprometido en NP − facturado sin remitir − reservado en órdenes de reparación (este último solo con su parámetro activo).

**Diferencias entre instalaciones:** todavía no medidas. Las fuentes de variación son tres: **valores de parámetros** (solo el 109 tiene diez variantes), **variante vertical** (Corralón vs ERP general) y **cantidad de empresas por instalación**. Se propone medirlas sobre 5 instalaciones representativas (PRD S-05, S-12, S-13).

### 1.5 Esquema de despliegue (lo que se sabe, insumo del track de Tecnología)

- La API corre **en el servidor de cada cliente**, en Docker Desktop sobre Windows con un reverse proxy, o por consola con PM2 en entornos legacy que no soportan Docker.
- Los servicios centrales de Flexxus corren en un clúster Docker Swarm administrado con Portainer, en la infraestructura de su proveedor.
- Flexxus Order se despliega con Docker y Bitbucket Pipelines; el ERP Web / POS como PWA y builds Android/iOS.
- El ERP Delphi se conecta a la base por la configuración de `Flexxus.ini`; el proyecto principal es `03-ERP/prj/ERP.dpr`, con Print Server (`04-PS`) y librerías propias de menús, alertas y terminales de cobro (`06-Librerias`).

Topología por cliente, versionado, seguridad y costo: a relevar por el track de Tecnología.

### 1.6 Cómo está construida la lógica de Venta (insumo del track de Tecnología)

- **La lógica vive en los formularios.** `frmFacturacion` tiene 19.153 líneas, `frmPedidos` 16.817, `frmRemitoInterno` 15.654 y `frmNotaCreditoVenta` 13.306. Las 7 pantallas de comprobante suman 748 sentencias SQL embebidas. Cada formulario abre y revierte su propia transacción.
- **Un mismo formulario sirve a muchos casos.** `frmRemitoInterno` atiende remito de venta, remito manual, remito por devolución, remito interno y remitos de transferencia entre depósitos; `frmFacturacion` atiende factura y factura manual.
- **El movimiento de stock está centralizado, pero se invoca desde 43 archivos.** `ModificarStock` actualiza casillero y total; los formularios deciden cuándo llamarlo.
- **Hay residuos de merge:** 231 archivos de conflicto o respaldo, entre ellos cuatro copias de `frmFacturacion`.

### 1.7 Fricción del usuario (hipótesis a validar en sesión)

Las fricciones confirmadas requieren las sesiones con referentes de negocio. Hipótesis tomadas de las fuentes:

- **Navegación por menú extenso:** el Delphi expone 574 acciones en 12 solapas; solo Venta tiene 94 opciones repartidas en 14 grupos. Es el límite de productividad que declara Flexxus.
- **Varias formas de cerrar una venta:** el cobro difiere por comprobante en el Delphi; Flexxus Order lo unificó porque «el cajero aprende una sola forma de cerrar una venta».
- **Configuración que el usuario no ve:** el mismo comprobante se comporta distinto según 163 parámetros leídos en las pantallas de Venta y según permisos que pueden denegarse en silencio (PRD H-8, H-20).
- **Mensajes de stock que no dicen contra qué se validó:** según el valor del 109, el mismo faltante se informa como «stock real» o «stock remanente», y como aviso o como bloqueo (PRD H-14).
- **Bloqueos de cuenta corriente inconsistentes:** la venta a un cliente con facturas vencidas no se bloquea en la implementación web contra la base real (PRD H-5).

---

## 2. Inventario de módulos y capabilities (Venta y Stock)

### 2.1 Módulos del ERP Delphi

El menú principal (`frmPrincipal.dfm`) tiene 12 solapas: Inicio, Archivos, **Ventas**, Compras, Fondos, Contabilidad, RMA, **Stock**, Producción, Calidad, RR.HH. e Informes. El código tiene 978 formularios (sin contar residuos de merge) y 115 unidades de lógica. Las 94 opciones de Venta abren 58 formularios distintos y las 34 de Stock, 27; las demás abren diálogos o planillas genéricas. El mapa completo opción → formulario está en el [Anexo A](#anexo-a--mapa-de-opciones-de-menú-a-formularios).

**Resumen por grupo de menú**

| Solapa | Grupo de menú | Opciones | Épica |
|---|---|---|---|
| Ventas | Comprobantes › Facturación | 17 | 1 (granos y líquido producto: 2) |
| Ventas | Comprobantes › Facturación › Impresora fiscal | 5 | ⏳ S-11 |
| Ventas | Comprobantes › Facturación electrónica | 1 | 1 |
| Ventas | Comprobantes › Facturación masiva | 2 | 2 |
| Ventas | Comprobantes › Notas de pedido | 8 | 1 (salida de pedidos: 2) |
| Ventas | Comprobantes › Presupuestos | 3 | 1 |
| Ventas | Comprobantes › Remitos | 10 | 1 (internos, expedición y ARBA: 2) |
| Ventas | Comprobantes › Otros | 12 | Ticket: 1; resto: 2 |
| Ventas | Comprobantes › Consulta | 5 | 1 |
| Ventas | Cuentas corrientes | 11 | Validación al vender: 1; gestión: fuera de la etapa |
| Ventas | Precios y bonificaciones | 9 | Consultas: 1; administración: 2 |
| Ventas | Vendedores | 5 | 2 |
| Ventas | Fidelización de clientes | 4 | 2 (los puntos se calculan en el comprobante: 1) |
| Ventas | Ventas no realizadas | 2 | 2 |
| **Ventas** | **Total** | **94** | |
| Stock | Correcciones de stock | 3 | 2 |
| Stock | Consulta de movimientos | 7 | Listados de stock: 1; resto: 2 |
| Stock | Transferencias entre depósitos | 9 | 2 |
| Stock | Inventarios | 8 | 2 |
| Stock | Análisis de stock | 3 | 2 |
| Stock | Transformaciones | 3 | 2 |
| Stock | Reparto | 1 | 2 |
| **Stock** | **Total** | **34** | |
| Archivos | Artículos / Depósitos | 17 / 5 | 2 (maestros que lee el MVP) |

**Detalle de opciones.** La descripción funcional se deduce del nombre de la opción, del formulario que abre (Anexo A), del código y de las notas de release. Las marcadas con ⏳ son interpretaciones a confirmar con el referente de negocio.

#### Solapa Ventas (94 opciones)

| Grupo | Opción | Para qué se usa principalmente |
|---|---|---|
| Comprobantes › Facturación | Factura | Emitir la factura de venta (contado o cuenta corriente) con cobro, efecto en stock y remito automático según los parámetros 52 y 154 |
| Comprobantes › Facturación | Factura Manual | Registrar una factura emitida fuera del sistema (talonario manual) cargando su numeración |
| Comprobantes › Facturación | Facturación de Pedidos | Seleccionar notas de pedido pendientes y facturarlas, total o parcialmente |
| Comprobantes › Facturación | Facturación de Remitos | Facturar en forma automática remitos de venta ya entregados y pendientes de facturar |
| Comprobantes › Facturación | Solicitud Nota de Crédito | Pedir una NC (devolución o bonificación) para que la apruebe un usuario autorizado antes de emitirla |
| Comprobantes › Facturación | Planilla Solicitud Nota de Créditos | Consultar y aprobar o rechazar las solicitudes de NC pendientes |
| Comprobantes › Facturación | ABM Motivos | Mantener los motivos que justifican una NC, una ND o una solicitud |
| Comprobantes › Facturación | Nota de Crédito | Emitir la NC vinculada a una o más facturas, con reingreso de stock si corresponde |
| Comprobantes › Facturación | Nota de Crédito Manual | Registrar una NC emitida fuera del sistema |
| Comprobantes › Facturación | Planilla de Notas de Crédito | Consultar las NC emitidas, filtrar, reimprimir y exportar |
| Comprobantes › Facturación | Nota de Débito | Emitir una ND al cliente (intereses, diferencias de precio o de cambio, gastos) |
| Comprobantes › Facturación | Nota de Débito Manual | Registrar una ND emitida fuera del sistema |
| Comprobantes › Facturación | Planilla de Notas de Débito | Consultar las ND emitidas |
| Comprobantes › Facturación | Débito Interno | Cargar un débito en la cuenta corriente del cliente sin comprobante fiscal ⏳ |
| Comprobantes › Facturación | Líquido Producto | Emitir la liquidación al comitente en la venta por cuenta y orden de terceros (consignación) ⏳ |
| Comprobantes › Facturación | Estados de Comprobantes | Mantener los estados que puede tomar un comprobante en su circuito (por ejemplo, pendiente, autorizado, entregado) |
| Comprobantes › Facturación | Liquidación Primaria de Granos | Emitir la liquidación primaria de granos del vertical agro |
| Comprobantes › Facturación › Impresora fiscal | Cierre X (Cajero) | Emitir el informe parcial del controlador fiscal por cajero o turno, sin cerrar la jornada |
| Comprobantes › Facturación › Impresora fiscal | Cierre Z (Diario) | Cerrar la jornada fiscal del controlador, con su informe diario obligatorio |
| Comprobantes › Facturación › Impresora fiscal | Controlar Numeración del Controlador Fiscal | Comparar la numeración del controlador con la del sistema y detectar saltos |
| Comprobantes › Facturación › Impresora fiscal | Abrir Cajón | Abrir el cajón de dinero conectado al controlador fiscal |
| Comprobantes › Facturación › Impresora fiscal | Reimpresión Cierre Z | Volver a imprimir un cierre Z ya emitido |
| Comprobantes › Facturación electrónica | Facturación Electrónica | Gestionar los comprobantes electrónicos ante AFIP/ARCA: solicitud y reintento de CAE y estado de cada comprobante ⏳ |
| Comprobantes › Facturación masiva | Facturación Masiva | Generar en un solo proceso las facturas de un lote de clientes (abonos, cuotas, servicios periódicos) |
| Comprobantes › Facturación masiva | Lotes de Facturación | Armar y mantener los lotes de clientes y conceptos que usa la facturación masiva |
| Comprobantes › Notas de pedido | Pedido | Cargar la nota de pedido del cliente: compromete stock, fija fecha de entrega y admite anticipo |
| Comprobantes › Notas de pedido | Planilla de Notas de Pedido | Consultar los pedidos y su estado (pendiente, parcial, facturado) y operar sobre ellos |
| Comprobantes › Notas de pedido | Artículos Pendientes Por Cliente | Ver qué artículos pedidos falta entregar o facturar, agrupados por cliente |
| Comprobantes › Notas de pedido | Artículos Pendientes Por Pedidos | Ver los artículos pendientes de cada pedido |
| Comprobantes › Notas de pedido | ABM Operaciones | Mantener los tipos de operación que clasifican los pedidos ⏳ |
| Comprobantes › Notas de pedido | Salida de Pedidos | Registrar la preparación y salida de mercadería de los pedidos desde el depósito |
| Comprobantes › Notas de pedido | Anulación de Pedidos | Anular una nota de pedido y liberar el stock que comprometía |
| Comprobantes › Notas de pedido | Planilla Autorización Pedidos | Autorizar los pedidos retenidos (por ejemplo, por crédito o por precio) antes de que se preparen o facturen |
| Comprobantes › Presupuestos | Presupuesto | Emitir una cotización al cliente, sin efecto fiscal ni de stock, con vencimiento |
| Comprobantes › Presupuestos | Planilla de Presupuestos | Consultar los presupuestos y convertirlos en pedido o factura |
| Comprobantes › Presupuestos | Anulación de Presupuestos | Anular presupuestos vencidos o rechazados |
| Comprobantes › Remitos | Remito | Emitir el remito de entrega de la venta, que descuenta stock cuando la factura no lo hace (parámetro 82) |
| Comprobantes › Remitos | Remito Manual | Registrar un remito emitido fuera del sistema |
| Comprobantes › Remitos | Remito por Devolución de Mercaderías | Registrar la mercadería que devuelve el cliente y reingresarla al stock |
| Comprobantes › Remitos | Planilla de Remitos | Consultar los remitos emitidos y su estado de facturación |
| Comprobantes › Remitos | Planilla de Expedición | Organizar los remitos a despachar y su salida física |
| Comprobantes › Remitos | Remito Interno | Mover mercadería sin venta (préstamo, muestra, envío a sucursal) con efecto en stock |
| Comprobantes › Remitos | Remito Interno Manual | Registrar un remito interno emitido fuera del sistema |
| Comprobantes › Remitos | Remito Interno por Devolución de Mercaderías | Reingresar la mercadería que vuelve de un remito interno |
| Comprobantes › Remitos | Planilla de Remitos Internos | Consultar los remitos internos |
| Comprobantes › Remitos | Remito Electrónico (ARBA) | Generar el COT de ARBA para el traslado de mercadería en la provincia de Buenos Aires |
| Comprobantes › Otros | Carta de Porte | Emitir la carta de porte para el transporte de granos |
| Comprobantes › Otros | Planilla de Cartas de Porte | Consultar las cartas de porte emitidas |
| Comprobantes › Otros | Guía de Reparto | Armar el recorrido del reparto propio con los comprobantes a entregar |
| Comprobantes › Otros | Planilla de Guías de Reparto | Consultar las guías de reparto y su estado |
| Comprobantes › Otros | Ticket | Emitir un ticket de venta rápida de mostrador (controlador fiscal o consumidor final) |
| Comprobantes › Otros | Planilla de Tickets | Consultar los tickets emitidos |
| Comprobantes › Otros | Garantía de Artículos | Registrar la garantía de un artículo vendido (número de serie, plazo) |
| Comprobantes › Otros | Planilla de Garantías de Artículos | Consultar las garantías vigentes y vencidas |
| Comprobantes › Otros | ABM Estado ContraReembolso | Mantener los estados de las ventas con cobro contra entrega |
| Comprobantes › Otros | Planilla ContraReembolsos | Seguir las ventas contra reembolso hasta su cobro |
| Comprobantes › Otros | Gestión Cierres Z | Registrar y consultar los cierres Z de cada controlador fiscal |
| Comprobantes › Otros | Planilla de Tickets de Cambio | Consultar los tickets de cambio que habilitan cambiar un producto en otro momento ⏳ |
| Comprobantes › Consulta | Consulta | Buscar cualquier comprobante de venta del cliente, verlo, reimprimirlo y enviarlo |
| Comprobantes › Consulta | Numeración de Comprobantes | Configurar la numeración por tipo de comprobante y punto de venta |
| Comprobantes › Consulta | Modificación Masiva de Numeración | Corregir en bloque la numeración de comprobantes |
| Comprobantes › Consulta | Anulación | Anular un comprobante de venta y revertir sus efectos en stock y cuenta corriente |
| Comprobantes › Consulta | Anulación Por Numeración | Anular un rango de números de comprobante (por ejemplo, formularios inutilizados) |
| Cuentas corrientes | Cuenta Corriente | Consultar la cuenta corriente del cliente y registrar cobros imputados a sus comprobantes |
| Cuentas corrientes | Movimientos | Listar los movimientos de cuenta corriente de uno o varios clientes |
| Cuentas corrientes | Saldos al Inicio | Cargar los saldos iniciales de los clientes en la implantación |
| Cuentas corrientes | Planilla de Cobros | Consultar los recibos de cobro emitidos |
| Cuentas corrientes | Modificación de Imputaciones | Cambiar a qué comprobantes se aplicó un cobro |
| Cuentas corrientes | Deudas Totales | Ver la deuda total y vencida por cliente |
| Cuentas corrientes | Generación de Intereses | Calcular los intereses por mora y generar sus notas de débito |
| Cuentas corrientes | Importación de Cobros | Importar cobros desde un archivo (bancos, empresas de cobranza) |
| Cuentas corrientes | Cobranza Masiva de Documentos | Cobrar en bloque documentos de financiación propia |
| Cuentas corrientes | ABM Variables | Definir las variables (consultas) que usan las fórmulas de límite de crédito |
| Cuentas corrientes | ABM Fórmulas Predefinidas | Definir las fórmulas que calculan el límite de crédito de los clientes |
| Precios y bonificaciones | Precios | Consultar el precio de los artículos por lista, con stock y precio con o sin IVA |
| Precios y bonificaciones | Consultas de Precio por Forma de Pago | Ver el precio final según la forma de pago y el plan de cuotas de tarjeta |
| Precios y bonificaciones | Planilla de Artículos sin Cambios de Precio | Detectar los artículos con el precio desactualizado |
| Precios y bonificaciones | Planilla de Últimos Precios de Venta | Ver a qué precio se vendió por última vez cada artículo, por cliente |
| Precios y bonificaciones | Lista de Precios Editable | Modificar en bloque los precios y márgenes de las listas |
| Precios y bonificaciones | Impresión de Códigos de Barra | Imprimir etiquetas con código de barras y precio |
| Precios y bonificaciones | Bonificaciones | Consultar y mantener las bonificaciones por cliente y artículo |
| Precios y bonificaciones | Modificación Masiva de Bonificaciones | Cambiar en bloque las bonificaciones de varios clientes o artículos |
| Precios y bonificaciones | Lista de Precios de Artículos en Promoción | Listar los artículos con una promoción vigente y su precio promocional |
| Vendedores | Comisiones | Liquidar las comisiones de los vendedores de un período |
| Vendedores | Períodos de Liquidación | Definir los períodos en los que se liquidan las comisiones |
| Vendedores | Planilla de Premios por Artículos | Consultar los premios o comisiones asignados por artículo |
| Vendedores | Premios | Consultar los premios o comisiones por vendedor |
| Vendedores | Planilla Comisiones | Consultar las comisiones ya liquidadas y pagadas |
| Fidelización de clientes | Asignación de Premios | Canjear los puntos acumulados de un cliente por premios |
| Fidelización de clientes | Premios | Mantener el catálogo de premios canjeables |
| Fidelización de clientes | Puntos | Modificar en bloque los puntos que otorga cada artículo |
| Fidelización de clientes | Configuración de Coeficientes | Definir los coeficientes que convierten el importe de la compra en puntos |
| Ventas no realizadas | Nueva VNR | Registrar una venta perdida (falta de stock, precio, plazo) para medir la demanda insatisfecha |
| Ventas no realizadas | Análisis Costo Oportunidad | Analizar las ventas no realizadas y su impacto económico |

#### Solapa Stock (34 opciones)

| Grupo | Opción | Para qué se usa principalmente |
|---|---|---|
| Correcciones de stock | Despachos de Aduana | Asignar o corregir el despacho de importación asociado al stock de un artículo |
| Correcciones de stock | Planilla de Ajustes | Consultar los ajustes manuales de stock realizados |
| Correcciones de stock | Nuevo Ajuste | Registrar un ajuste de stock positivo o negativo con su motivo |
| Consulta de movimientos | Seguimiento de Números de Serie | Rastrear un número de serie: ingreso, venta, devolución y depósito actual |
| Consulta de movimientos | Listado General | Listar el stock real y remanente de los artículos de toda la empresa |
| Consulta de movimientos | Listado por Depósito | Listar el stock por depósito y casillero, con su remanente |
| Consulta de movimientos | Histórico de Artículos | Ver todos los movimientos históricos de un artículo con su comprobante de origen |
| Consulta de movimientos | Seguimiento de Stock por Depósito | Seguir los movimientos de stock de un depósito en un período |
| Consulta de movimientos | Planilla de Distribuciones | Consultar las distribuciones de mercadería entre sucursales o depósitos |
| Consulta de movimientos | Capacidad Centro de Distribución | Definir y controlar la capacidad de los centros de distribución |
| Transferencias entre depósitos | Remito de Salida | Emitir el remito que saca mercadería de un depósito hacia otro |
| Transferencias entre depósitos | Remito de Transferencia Manual | Registrar una transferencia emitida fuera del sistema |
| Transferencias entre depósitos | Generación Automática de Remito de Transferencia | Generar las transferencias necesarias para reponer depósitos a partir de un criterio (por ejemplo, stock mínimo) ⏳ |
| Transferencias entre depósitos | Remito de Entrada | Recibir en el depósito de destino la mercadería de un remito de salida |
| Transferencias entre depósitos | Movimiento Interno | Mover stock entre casilleros de un mismo depósito |
| Transferencias entre depósitos | Planilla de Movimientos Internos | Consultar los movimientos entre casilleros |
| Transferencias entre depósitos | Anulación de Movimientos Internos | Anular un movimiento interno y revertir su efecto |
| Transferencias entre depósitos | Distribución de Mercadería | Repartir mercadería de un depósito central entre varias sucursales |
| Transferencias entre depósitos | Consumo Interno de Materiales | Dar de baja stock consumido por la propia empresa |
| Inventarios | Inventario | Emitir el inventario valorizado del stock a una fecha ⏳ |
| Inventarios | Toma de Inventarios | Generar una toma de inventario (artículos y depósitos a contar) |
| Inventarios | Actualización de Toma de Inventarios | Aplicar al stock las diferencias de una toma ya contada |
| Inventarios | Cargar Cantidades | Cargar las cantidades contadas de una toma |
| Inventarios | Planilla de Inventarios | Consultar las tomas de inventario y su estado |
| Inventarios | Carga de Inventario desde Archivo | Importar el conteo desde un archivo o un colector de datos |
| Inventarios | Bienes de Uso | Consultar el inventario de bienes de uso de la empresa |
| Inventarios | Carga Toma de Inventarios | Cargar el conteo de una toma por otra vía (por ejemplo, escáner) ⏳ |
| Análisis de stock | Análisis de Diferencias | Analizar las diferencias de stock detectadas en las tomas |
| Análisis de stock | Análisis de Rotación | Medir la rotación de los artículos para detectar los de baja salida |
| Análisis de stock | Optimización de Stock | Calcular stock mínimo, máximo y óptimo por artículo y depósito |
| Transformaciones | Estructura de Producto | Definir qué componentes forman un artículo compuesto o elaborado |
| Transformaciones | Movimiento de Producción | Registrar la transformación: consume componentes y da de alta el producto |
| Transformaciones | Planilla de Movimientos | Consultar los movimientos de producción o transformación |
| Reparto | Confirmación de Entrega | Confirmar que el cliente recibió la mercadería de un remito o una guía de reparto |

#### Solapa Archivos — maestros que consume Venta y Stock (22 opciones)

| Grupo | Opción | Para qué se usa principalmente |
|---|---|---|
| Artículos | Artículos | Alta, baja y modificación del artículo: códigos, precios, impuestos, control de stock, talles, lotes y series |
| Artículos | Rubros | Mantener los rubros que clasifican los artículos |
| Artículos | Marcas | Mantener las marcas de los artículos |
| Artículos | Familias | Mantener las familias de artículos (usadas en precios, promociones y comisiones) |
| Artículos | Bultos | Definir los bultos o presentaciones en que se mueve un artículo |
| Artículos | Bienes de Uso | Mantener los bienes de uso de la empresa |
| Artículos | Piezas Alternativas | Definir grupos de artículos equivalentes que se ofrecen cuando falta uno |
| Artículos | Unidades de Medida | Mantener las unidades de medida |
| Artículos | Posiciones Arancelarias | Mantener las posiciones arancelarias de importación y exportación |
| Artículos | Grupos de Talles | Definir las curvas de talles y colores |
| Artículos | Planilla Descripciones Adicionales | Mantener descripciones extendidas de los artículos |
| Artículos | Modificación Masiva de Artículos | Cambiar datos de muchos artículos a la vez |
| Artículos | Empaques | Definir los empaques de venta de un artículo (por ejemplo, caja por 12) |
| Artículos | Conversión de Unidades | Definir equivalencias entre unidades de medida de un artículo |
| Artículos | ABM Artículos Transformación | Definir los artículos que intervienen en las transformaciones |
| Artículos | Grupos de Familias | Agrupar familias para reportes y reglas |
| Artículos | Características | Definir atributos adicionales de los artículos |
| Depósitos | Casilleros | Mantener las ubicaciones (casilleros) dentro de cada depósito, donde se guarda el stock |
| Depósitos | Depósitos | Alta y configuración de los depósitos de la empresa |
| Depósitos | Sub Depósitos | Dividir un depósito en sectores |
| Depósitos | Depósitos Externos | Registrar depósitos de terceros (consignación, logística tercerizada) |
| Depósitos | Centros de distribución | Definir los centros de distribución que abastecen a las sucursales |

Además hay unas 20 acciones de Venta y Stock fuera de categoría: picking, packing, preparación de mercadería, hojas de ruta, cierres de stock, antigüedad de stock, motivos de ajuste, acopios, reglas de precio, políticas de redondeo y promociones.

### 2.2 Capabilities y su presencia por implementación

Leyenda: ✅ presente · 🟡 parcial o con brechas documentadas · ❌ no presente · ⏳ a verificar. Épica: 1 = MVP, 2 = operación de stock, maestros y procesos fuera del comprobante, 3 = capacidades nuevas, — = fuera de la etapa. **Negrita en Épica** = reclasificada en la v0.2.

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
| CV-08 | Remito de venta y de devolución, con remito automático al facturar (parámetros 52 y 154) | ✅ | ⏳ | ✅ | ✅ | 1 |
| CV-09 | Facturación de pedidos y de remitos pendientes | ✅ | ⏳ | ✅ | ⏳ | 1 |
| CV-10 | Consulta, reimpresión, envío y anulación de comprobantes | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-11 | Cobro en el checkout (efectivo, tarjeta, cheque, retenciones, CC) | ✅ | ✅ | ✅ | ✅ | 1 |
| CV-12 | Validación de cuenta corriente y límite de crédito al vender (fórmula de límite configurable) | ✅ | 🟡 | 🟡 | ✅ | 1 |
| CV-13 | Precios por lista, multiplazo, pactados, ofertas y descuentos | ✅ | ✅ | 🟡 | ✅ | 1 |
| CV-14 | Percepciones y retenciones en la venta | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-15 | Acopios (venta con entrega diferida) | ✅ | ✅ | ✅ | ⏳ | 1 |
| CV-16 | Libro IVA ventas e informes de ventas | ✅ | 🟡 | ✅ | ⏳ | — |
| CV-17 | Impresora fiscal (cierres X/Z) | ✅ | ❌ | ❌ | ❌ | ⏳ S-11 |
| CV-18 | Cobro con terminales (POSNET/VISA en el Delphi) y con QR de pasarelas (MP, Payway/Prisma, Clover, MODO, Go) | 🟡 terminales | ✅ | ⏳ | ✅ | ⏳ S-09 (terminales 1, QR 3) |
| CV-19 | Facturación masiva y por lote | ✅ | ❌ | ❌ | ⏳ | **2** |
| CV-20 | Comprobantes de verticales (granos, carta de porte, garantías, contrarreembolso) | ✅ | ❌ | ❌ | ⏳ | **2** |
| CV-21 | Picking, packing, salida de pedidos, expedición, guía de reparto | ✅ | ✅ | ⏳ | ✅ | **2** |
| CV-22 | Vendedores, comisiones y premios | ✅ | 🟡 | ❌ | ⏳ | **2** |
| CV-23 | Administración de fidelización (premios, coeficientes) y ventas no realizadas | ✅ | ❌ | ❌ | ❌ | **2** |
| CV-24 | Gestión de cuenta corriente fuera de la venta (intereses, cobranza masiva) | ✅ | 🟡 | ✅ | ✅ | — |
| CV-25 | Promociones, cupones de descuento, reglas de precio y puntos aplicados al comprobante (`GestorPromociones`) | ✅ | ⏳ | ⏳ | ⏳ | **1** (nueva) |
| CV-26 | Facturación de NP de otra empresa de la instalación (parámetro 116) | ✅ | ⏳ | ⏳ | ⏳ | **1** ⏳ S-13 (nueva) |

**Stock**

| ID | Capability | Delphi | ERP Web / POS | Flexxus Order | API v6 | Épica |
|---|---|---|---|---|---|---|
| CS-01 | Descuento, reserva y reingreso de stock por comprobante de venta | ✅ | ✅ | ✅ | ✅ | 1 |
| CS-02 | Validación de stock al vender (parámetro 109, diez variantes) y control de negativos | ✅ | ✅ | ✅ | ⏳ | 1 |
| CS-03 | Consulta de stock real y remanente por depósito, sucursal y empresa | ✅ | ✅ | ⏳ | ✅ | 1 |
| CS-04 | Ajustes de stock con motivo | ✅ | ❌ | ✅ | ⏳ | 2 |
| CS-05 | Transferencias entre depósitos y movimientos internos | ✅ | ❌ | ✅ | ⏳ | 2 |
| CS-06 | Toma de inventario | ✅ | ✅ (conteo) | ⏳ | ✅ | 2 |
| CS-07 | Consulta de movimientos, histórico, series y lotes | ✅ | ❌ | ⏳ | ⏳ | 2 |
| CS-08 | Maestro de depósitos (subdepósitos, casilleros, externos, centros de distribución) | ✅ | ❌ | 🟡 (árbol de 2 niveles) | ⏳ | 2 |
| CS-09 | Maestro de artículos y listas de precio | ✅ | ✅ | ✅ | ✅ | 2 |
| CS-10 | Cierres de stock y despachos de aduana | ✅ | ❌ | ❌ | ⏳ | 2 |
| CS-11 | Análisis de rotación, optimización y diferencias | ✅ | ❌ | ❌ | ❌ | **2** |
| CS-12 | Transformaciones de artículos | ✅ | ❌ | ❌ | ❌ | **2** |
| CS-13 | Stock de la sucursal con visibilidad cruzada entre compañías de un grupo (Multi-Tenant) | 🟡 (empresas por instalación, sin grupo) | ❌ | ❌ | ❌ | 3 (nueva) |

Conteo: **20 capabilities en el MVP** (17 de Venta y 3 de Stock); 14 en la Épica 2; 1 en la Épica 3; 2 fuera de la etapa y 2 a decidir (39 en total).

La presencia ✅ del Delphi se verificó el 08-10 contra el menú y el código; la de Flexxus Order sale de su nota de release; la de ERP Web / POS, de su nota de release y su documento funcional; la de API v6, de su nota de release. Los ⏳ se verifican en la Semana 2.

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
| D-06 | Propuesta Arquitectura Multi-Tenant | Propuesta técnica | mayo 2026 | 🟡 | ✅ | Media; su premisa de empresa única no coincide con el código (PRD H-17) | Stock por sucursal, multiempresa (Épica 3) |
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
| D-20 | Notas de release Flexxus Enterprise (`NR_Flexxus Enterprise.rar`) | Release por funcionalidad | 03.09 a 04.07 (41 versiones) | ✅ (803 notas) | ✅ (252) | Media | Evidencia funcional de cada regla; se indexa por capability en la Semana 2 |
| D-21 | Notas de release Flexxus 4 (`NR_Flexxus 4.rar`) | Release por funcionalidad | 04.00 a 04.12 | ✅ (105 notas únicas) | ✅ (42) | Media | Cambios recientes: parámetro 116 entre empresas (04.11), parámetro 537 de stock negativo (04.12) |
| D-22 | Notas de release Corralón (`Corralon Enterprise.rar`) | Release por funcionalidad | Cln 03.01 a 03.37 | ✅ (240 notas) | ✅ (96) | Media | Diferencias del vertical Corralón (PRD S-05) |
| D-23 | Fuentes completas del ERP (`Erp_04-12_Provisorio.zip`) | Código fuente | rama `develop`, octubre 2026 | ✅ | ✅ | **Alta** (es el comportamiento), con versión a confirmar (PRD S-14) | Extracción de reglas: `uParametrosGenerales`, `Funciones`, `FuncionesComprobantes`, `ModificacionesBaseDatos`, `GestorPromociones` |
| D-24 | Planillas de `05-Datos Externos` | Formatos de importación | sin fecha | 🟡 | ✅ | Baja | Formatos de importación de pedidos, precios, toma de inventario y números de serie |

En las notas de release, una nota cuenta para Venta y para Stock cuando trata ambos temas; las cifras salen de clasificar los títulos y la carpeta de módulo de los 3.028 documentos únicos, a revisar en la indexación de la Semana 2.

**No hay:** manual funcional del ERP Delphi para Venta y Stock (las notas describen cambios, no el comportamiento completo), esquema y objetos de la base Firebird del ERP general, ni backlog Jira accesible. Las notas de release no indican el sistema de tickets de origen (PRD O-7).

---

## 4. Foco Venta y Stock: qué entra y qué se ignora

- **Se analiza:** todo lo que nace de un comprobante de venta al cliente, lo que el core aplica dentro de él y su efecto en stock (MVP), más el inventario de la operación de stock, maestros y procesos comerciales, y de las capacidades nuevas (Épicas 2 y 3) a nivel de catálogo.
- **Se ignora:** Compras, Fondos (salvo el cobro en el checkout), Contabilidad, RMA, Producción, Calidad, RR.HH. y la gestión de cuenta corriente fuera de la venta.
- **Corte propuesto para el MVP (revisado el 08-10):** «entra lo que ocurre entre la búsqueda del artículo y la confirmación del comprobante de venta, incluidos las promociones, cupones y puntos que el core aplica y su efecto inmediato en el stock, en la empresa del usuario; queda afuera lo que ocurre fuera de ese ciclo aunque el core ya lo haga (Épica 2) y lo que exige una capacidad que el core no tiene (Épica 3)». Detalle y matriz en el PRD §5.
- **Qué se movió:** promociones, cupones y puntos pasan al MVP; picking, packing, reparto, comisiones, VNR, análisis de stock y verticales pasan de la Épica 3 a la Épica 2. La Épica 3 queda con el modelo Multi-Tenant y los cobros QR.
- **Pendiente de acordar con Flexxus:** el brief propone Pagos a Proveedores como módulo de referencia (PRD S-01), y no está definida la sigla «MVP TCR/ER» (PRD S-08).

---

## Estado de cada acceso

| Acceso | Estado | Detalle | Acción |
|---|---|---|---|
| Fuentes del ERP Delphi general (`Erp_04-12_Provisorio`) | ✅ Disponible (08-10) | Copia completa: `03-ERP/unit` (115 unidades), `ERP.dpr`, `04-PS`, `05-Datos Externos`, `06-Librerias`. Rama `develop`; no incluye el parámetro 537 de la versión 04.12 publicada | Confirmar la etiqueta o el commit de la 04.12 con el referente técnico (PRD S-14) |
| Notas de release del Delphi | ✅ Disponible (08-10) | 3 colecciones, 3.028 documentos únicos | Pedir el sistema de tickets de origen (PRD O-7) |
| Fuentes de Flexxus Corralón (`Corralon_0336`) | ✅ Disponible | 2.650 archivos | — |
| Repositorios `flexxus-order`, `flexxuserpweb`, `flxwebapi-v6` | 🟡 Snapshot | Comprimidos del 06/10/2026; sin acceso al repositorio remoto | Pedir acceso de lectura si se necesita historial |
| Modelo de datos MariaDB (`order-v6`) | 🟡 Dump | Dump completo; sin acceso a una base en vivo | Pedir acceso de solo lectura a la base de test |
| Modelo de datos Firebird del ERP | 🔴 Pendiente | Las tablas de stock se conocen por el código; faltan el esquema y los triggers y procedimientos de stock negativo | Pedir esquema o base de referencia con sus objetos (PRD S-14) |
| Entorno de referencia con datos de prueba | 🔴 Pendiente | No recibido | Confirmar con el administrador de accesos |
| Jira FO y FLEXV2 | 🔴 Pendiente | Solo hay referencias en las especificaciones | Pedir acceso de lectura |
| Documentos legacy `.doc` / `.xls` | ✅ Disponible | Convertidos a texto para el análisis | — |

---

## Anexo A — Mapa de opciones de menú a formularios

Extraído de `frmPrincipal.pas` y `frmPrincipal.dfm`: para cada opción de Venta y Stock, el formulario que crea su manejador. «Por otra vía» son opciones que abren un diálogo, una planilla genérica o una acción sin formulario propio.

| Solapa | Grupo | Opciones | Formularios que abre |
|---|---|---|---|
| Ventas | Comprobantes - Facturación | 17 | `frmABMEstadosComprobantes`, `frmABMMotivos`, `frmDebitoInterno`, `frmFacturacion`, `frmFacturacionAutomatica`, `frmFacturacionPendientes`, `frmLiquidacionPrimariadeGranos`, `frmLiquidoProducto`, `frmNotaCreditoVenta`, `frmNotaDebitoVenta`, `frmPlanillaNotaCredito` · 1 por otra vía |
| Ventas | Comprobantes - Facturación - Impresora Fiscal | 5 | 5 por otra vía |
| Ventas | Comprobantes - Facturación Electrónica | 1 | 1 por otra vía |
| Ventas | Comprobantes - Facturación Masiva | 2 | `frmABMLotesFacturacion`, `frmFacturacionMasivaXLote` |
| Ventas | Comprobantes - Notas de Pedido | 8 | `frmABMOperaciones`, `frmArticulosPendientePorCliente`, `frmArticulosPendientePorPedidos`, `frmPedidos`, `frmPedidosPendientes`, `frmPlanillaAutorizacionPedido`, `frmSalidaPedidos` · 1 por otra vía |
| Ventas | Comprobantes - Presupuestos | 3 | `frmPresupuesto`, `frmPresupuestosPendientes` · 1 por otra vía |
| Ventas | Comprobantes - Remitos | 10 | `frmARBARemitoElectronico`, `frmPlanillaExpedicion`, `frmPlanillaRemitosInternos`, `frmRemitoInterno` · 1 por otra vía |
| Ventas | Comprobantes - Otros | 12 | `frmABMEstadoContraReembolso`, `frmCartasDePorte`, `frmGarantia`, `frmGestionCierresZ`, `frmGuiaDeReparto`, `frmPlanillaCartasPorte`, `frmPlanillaContraReembolsos`, `frmPlanillaGarantiasArt`, `frmPlanillaGuiasReparto`, `frmPlanillaTickets`, `frmPlanillaTicketsCambio`, `frmTicket` |
| Ventas | Comprobantes - Consulta | 5 | `frmModificacionNumeracionVentas`, `frmPARFacturacion` · 3 por otra vía |
| Ventas | Cuentas Corrientes | 11 | `fIngresoCobroDesdeArchivo`, `frmABMVariables`, `frmCobranzaMasivaDocumentos`, `frmGeneracionInteresesClientes`, `frmMovimientoClientes`, `frmPagoCuentasCorrientes`, `frmPlanillaDeudaCLientes`, `frmPlanillaPagos`, `frmSaldoInicioVentas` · 2 por otra vía |
| Ventas | Precios y Bonificaciones | 9 | `frmConsultaFormasPago`, `frmImpresionCodigosBarra`, `frmPlanillaArticulosEnPromocion` · 6 por otra vía |
| Ventas | Vendedores | 5 | `frmListadoLiquidacionVendedores`, `frmPlanillaComisionesPagas`, `frmabmperiodoscomisiones2` · 2 por otra vía |
| Ventas | Fidelización de Clientes | 4 | `frmConfiguracionCoeficientes`, `frmPlanillaPremios` · 2 por otra vía |
| Ventas | Ventas No Realizadas | 2 | `frmPlanillaVentasNoRealizadas` · 1 por otra vía |
| Stock | Correcciones de Stock | 3 | `frmABMStockXDespacho`, `frmCorrecionStockManual`, `frmPlanillaMovimientosStockManuales` |
| Stock | Consulta de Movimientos | 7 | `frmABMCapacidadCentroDistribucion`, `frmPlanillaDistribuciones`, `frmPlanillaMovimientoStockPorCasillero`, `frmPlanillaStock`, `frmPlanillaStockPorCasillero`, `frmSeguimientoNumerosSerie`, `frmhistoricoArticulos` |
| Stock | Transferencias entre Depósitos | 9 | `frmConsumoInternoMateriales`, `frmDistribucionMercaderia`, `frmMovimientosEntreCasilleros`, `frmRemitoInterno`, `frmRemitoTransferencia` · 3 por otra vía |
| Stock | Inventarios | 8 | `frmActualizacionTomaInventarios`, `frmCargaInventarioDesdeArchivo`, `frmCargaStockTomaInventario`, `frmGeneracionTomaInventario`, `frmPlanillaBienesdeUso`, `frmPlanillaTomaInventarios` · 2 por otra vía |
| Stock | Análisis de Stock | 3 | `frmAnalisisRotacion`, `frmPlanillaDiferenciaStock` · 1 por otra vía |
| Stock | Transformaciones | 3 | `frmEstructuraProductos`, `frmListadoProduccion`, `frmMovimientoProduccion` |
| Stock | Reparto | 1 | `frmConfirmacionRemitos` |

---

*Siguiente paso: validar este documento con los referentes de Flexxus en la sesión de cierre de la Semana 1 y resolver S-01, S-05 y S-14 del PRD.*
