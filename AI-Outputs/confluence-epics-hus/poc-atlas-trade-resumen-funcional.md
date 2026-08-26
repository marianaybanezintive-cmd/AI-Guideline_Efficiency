# POC Atlas Trade — Resumen funcional de la propuesta

**POC entregada al cliente:** [https://marianaintive.github.io/atlas-confirming-poc/](https://marianaintive.github.io/atlas-confirming-poc/)  
**Versión de la POC:** v2.11.4  
**Producto:** Atlas Trade — Portal de Confirming (Banco Atlas)  
**Fecha de este resumen:** 26/08/2026  
**Audiencia:** Producto, negocio, UX y stakeholders del banco

Este documento resume **las propuestas y funcionalidades que se pueden recorrer en la POC**, acotadas a las pantallas del proyecto: **Login, Mi perfil, ABM y Confirming**. Es el puente entre el prototipo ejecutable y la [Documentación Funcional](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625686029/Documentaci+n+Funcional) de las épicas MAGIA.

> La POC es un **prototipo navegable en el front**, sin backend real. Sirve para validar flujos, reglas, mensajes y permisos con el cliente. Lo que acá se describe como “propuesta” es el comportamiento acordado para el producto; lo marcado como “simulado / pendiente” no debe tomarse como comportamiento productivo.

---

## 1. Para qué existe esta POC

Atlas Trade propone digitalizar el **Confirming**: el banco adelanta al Proveedor el importe de una factura aceptada por una **Empresa Gran Pagador (EGP)**, con cargo a la línea de crédito de esa EGP.

La POC demuestra, de punta a punta, que un usuario habilitado puede:

1. **Ingresar** de forma segura según su dominio (Banco, EGP o Proveedor).
2. **Ver y gestionar su perfil** y el detalle del ente con el que opera.
3. **Administrar** EGP, Proveedores, usuarios, roles y notificaciones (ABM).
4. **Operar facturas** en Confirming: cargar, habilitar/bloquear, simular adelanto, aprobar/rechazar y desembolsar.

### 1.1 Valor por segmento

| Segmento | Job | Dolor que ataca | Qué propone la POC |
|---|---|---|---|
| **Banco Atlas** | Gobernar el producto, autorizar entes/usuarios y supervisar operaciones | Procesos dispersos, poco control de accesos | Login corporativo, ABM con autorización, Confirming sobre cualquier ente |
| **EGP** | Habilitar facturas de sus proveedores y aprobar adelantos dentro de su línea | Demora en el pago a proveedores y gestión manual | Carga y habilitación de facturas, simulación, aprobación/rechazo del adelanto |
| **Proveedor** | Cobrar antes del vencimiento, con costos transparentes | Espera hasta la fecha de pago de la EGP | Consulta de facturas, simulación de adelanto, visibilidad del neto a acreditar |

### 1.2 Pantallas en alcance de este resumen

| Pantalla | Qué cubre | Épica MAGIA |
|---|---|---|
| **Login** | Primer ingreso, acceso recurrente, 2FA, recupero, bloqueo e inactividad | [MAGIA-155 — Login](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687640/Login) |
| **Mi perfil** | Datos del usuario (solo lectura) + detalle del ente + cambio de contraseña vía Home Banking | Complemento de Login / ABM (el detalle de ente se movió desde el ABM) |
| **ABM** | EGP, Proveedores, Usuarios, Roles y Notificaciones | [MAGIA-5 — Gestión de ABM](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625686041/Gesti+n+de+ABM) |
| **Confirming** | Grilla, carga, máquina de estados, simulación y desembolso | [MAGIA-346 Confirming](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687845/Confirming) · [MAGIA-347 Gestión de Facturas](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687859/Gesti+n+de+Facturas) · [MAGIA-348 Simulación](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687873/Simulaci+n+de+Adelantos) · [MAGIA-349 Desembolso](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687887/Desembolso) |

**Fuera de este recorte (existen en la POC como maqueta):** Dashboard de métricas y Reportes por rol. No forman parte del alcance funcional del proyecto que se documenta acá.

### 1.3 Cómo entrar a la POC

- Botón **Ingresar sin credenciales (modo demo)** — entra directo a la plataforma (chip *Modo demo sin login*).
- Panel **Escenarios de login** — permite elegir perfil, estado de la credencial y saltar a cada pantalla del flujo.

| Perfil | Usuario | Contraseña temporal | Contraseña definitiva |
|---|---|---|---|
| BANCO | `admin` | `Temporal2026` | `admin` |
| EGP | `ana` | `Temporal2026` | `Atlas2026!` |
| Proveedor cliente | `laura` | `Temporal2026` | `Atlas2026!` |
| Proveedor no cliente | `supervisor` | `Temporal2026` | `Atlas2026!` |

Cualquier otra contraseña dispara intentos fallidos; al tercero se bloquea el usuario.

---

## 2. Actores, dominios y permisos

Tres **dominios** operan la misma plataforma, con roles y permisos distintos.

| Dominio | Roles en la POC | Origen de la credencial | 2FA | Cambio de contraseña |
|---|---|---|---|---|
| **Banco** | ADMIN, SUPERVISOR, OPERADOR, APROBADOR, GERENTE, EJECUTIVO DE CUENTAS | Active Directory | Lo resuelve el AD (fuera del portal) | AD / Mesa de Ayuda |
| **EGP** | ADMIN, OPERADOR | Contraseña temporal → propia en la plataforma | OTP por mail | Home Banking o contraseña propia |
| **Proveedor cliente** | ADMIN, SUPERVISOR, OPERADOR | Igual que EGP | OTP por mail | Home Banking o contraseña propia |
| **Proveedor no cliente** | ADMIN, SUPERVISOR, OPERADOR | Igual que EGP | OTP por mail | Solo contraseña propia (no tiene Home Banking) |

La POC **simula visibilidad por permiso** (grillas, botones y acciones se ocultan o deshabilitan). El usuario demo `ana` opera como administrador con acceso total para poder recorrer todo.

Figma de referencia:

- Login: [LOGIN — borrador](https://www.figma.com/design/hg0oh2EuaupC0RxOTuvOBV/LOGIN---borrador?node-id=0-1)
- ABM: [Gestión ABM](https://www.figma.com/design/RjUHuOcHrXAXHwi3pKnjAi/Gesti%C3%B3n-ABM?node-id=1-2)

---

## 3. Login — acceso seguro al portal

**Objetivo de negocio:** que un usuario Banco, EGP o Proveedor ingrese de forma segura, complete su primer acceso, recupere credenciales cuando corresponda y mantenga una sesión protegida.

### 3.1 Propuesta de flujos

La POC implementa un **asistente de 3 pasos** (Contraseña → Verificación → Listo) con pantallas distintas según el perfil.

#### A. Primer ingreso BANCO

1. Usuario y contraseña de AD.
2. Pantalla de **doble factor del AD** (en la POC: *Simular aprobación* / *Simular rechazo*).
3. Si el AD aprueba → entra al portal **sin crear contraseña** en Atlas Trade.
4. Si el AD rechaza → vuelve al login con mensaje de reintento.

#### B. Primer ingreso EGP / Proveedor

1. Ingresa con **usuario + contraseña temporal** recibida por mail de bienvenida (el alta se dispara desde el ABM).
2. La temporal es de **un solo uso**: no puede entrar al portal sin cambiarla.
3. Elige canal de actualización:
   - **Home Banking** (solo si es cliente Atlas) — derivación informativa.
   - **Crear contraseña nueva acá** — siempre disponible.
4. El Proveedor **no cliente** no ve la opción Home Banking; el portal no expone en la UI si es o no cliente: el canal lo decide el backend.
5. Define la contraseña definitiva (política en vivo).
6. Configura **2FA por mail** (OTP de 6 dígitos).
7. Entra al portal.

#### C. Acceso recurrente

1. Usuario + contraseña definitiva.
2. Se pide **OTP de 2FA** después de cada cierre de sesión.
3. Opción **Recordar este dispositivo como seguro** (propuesta; en producto queda sujeta a política de Seguridad).

#### D. Recupero / desbloqueo

| Perfil | Qué propone la POC |
|---|---|
| Banco | Informa que la contraseña se gestiona en el AD / Mesa de Ayuda (interno 1500 · mesadeayuda@bancoatlas.com.py) |
| EGP / Proveedor cliente | Elige Home Banking o cambio en el portal (OTP + nueva contraseña) |
| Proveedor no cliente | Solo cambio en el portal (OTP + nueva contraseña) |
| Usuario bloqueado | El desbloqueo ocurre al cambiar la contraseña o vía Mesa de Ayuda |

### 3.2 Pantallas del flujo (todas recorribles)

| Pantalla | Para qué |
|---|---|
| Login | Usuario, contraseña, *¿Olvidaste tu contraseña?*, ingreso demo |
| 2FA del AD | Segundo factor corporativo (solo Banco) |
| Contraseña temporal | Aviso de un solo uso y obligación de cambio |
| Canal de actualización | Home Banking vs contraseña propia |
| Derivación Home Banking | Mensaje informativo (integración pendiente) |
| Nueva contraseña | Checklist de política + confirmación |
| Correo del código | Confirma o cambia el mail que recibe el OTP |
| Código OTP | 6 dígitos, reenvío, *recordar dispositivo* |
| 2FA configurado | Cierre del onboarding |
| Olvidé mi contraseña | Ingreso de usuario (respuesta genérica, exista o no) |
| Aviso AD | Cambio de contraseña Banco fuera del portal |
| Usuario bloqueado | 3 intentos fallidos |
| Contraseña actualizada | Confirmación y vuelta al login |

### 3.3 Reglas de negocio propuestas (Login)

| ID | Regla |
|---|---|
| RN-01 | La contraseña temporal es de un solo uso y obliga al cambio antes de entrar. |
| RN-02 | Política de contraseña: mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número, 1 especial; distinta de la anterior. (A validar con Seguridad.) |
| RN-03 | OTP: 6 dígitos, vigencia 5 minutos, un solo uso, máximo 3 intentos, reenvío con cooldown 60 s y máximo 3 reenvíos. |
| RN-04 | A los **3 intentos fallidos** se bloquea el acceso. |
| RN-05 | Sesión: cierra a los **5 minutos** de inactividad; **1 minuto antes** avisa con opción de continuar. |
| RN-06 | El 2FA se pide siempre luego de un cierre de sesión. En Banco lo resuelve el AD. |
| RN-07 | El error de credenciales es **genérico** (no se revela si el usuario existe). |
| RN-09 | El FE no decide el canal de contraseña: lo determina el dominio / política del backend. |

### 3.4 Qué queda simulado / pendiente de producto

- No hay Keycloak, AD ni envío real de mails: el OTP se muestra como ayuda de demo.
- La derivación a Home Banking es **informativa** (spike de integración).
- El 2FA del AD es un stub de aprobación/rechazo (spike de federación).
- Auditoría de intentos y persistencia de dispositivo confiable: propuestas, no persistidas.

---

## 4. Mi perfil

**Objetivo de negocio:** que el usuario vea **quién es** y **con qué ente opera**, sin editar datos maestros desde esta pantalla. El detalle de EGP/Proveedor que antes estaba en el ABM (*Ver detalle*) se consulta acá para no mezclar administración con operación.

### 4.1 Bloque Datos del usuario (solo lectura)

| Campo | Contenido |
|---|---|
| Usuario de login | Usuario con el que ingresó |
| Documento | Cédula |
| Nombre / Apellido | Datos personales |
| Email / Teléfono | Contacto |
| Dominio | Banco, EGP o Proveedor |
| Rol | Rol asignado en el ABM |
| Ente asociado | Razón social del EGP o Proveedor vinculado |

Nada de este bloque es editable. La fuente de verdad de esos datos es el ABM.

### 4.2 Seguridad de acceso

- Botón **Actualizar contraseña en Home Banking**.
- Confirma la redirección; en la POC no cambia la contraseña (la integración queda pendiente).
- Alineado al flujo de Login LO-31 para EGP / Proveedor cliente.

### 4.3 Detalle del ente

Comportamiento según dominio:

| Quién está logueado | Qué ve |
|---|---|
| **EGP o Proveedor** | El detalle de **su** ente asociado (misma ficha que el antiguo *Ver detalle* del ABM) |
| **Banco** | El detalle del EGP o Proveedor elegido en el selector global **Estás operando para el ente**. Si está en *Todos los entes*, pide seleccionar uno |

La ficha incluye, según el tipo de ente:

- Tipo, RUC, razón social, estado de autorización, email, teléfono, adjuntos.
- Cliente Atlas (sí/no).
- **Si es EGP:** monedas, TNA, comisión, IVA, desembolsos automáticos.
- **Si es Proveedor no cliente:** datos bancarios (cuenta crédito, banco, moneda, documento y titular).
- Relaciones EGP–Proveedor del RUC.

---

## 5. ABM — administración del padrón

**Objetivo de negocio:** que Banco (y, con permisos, EGP/Proveedor) administren el ecosistema Confirming **sin procesos fuera de la plataforma**: alta, consulta, edición, autorización, bloqueo y baja de entes, usuarios, roles y notificaciones.

Pantalla: **Administración (ABM)**. Alta rápida con el botón **+** → Nuevo EGP / Nuevo Proveedor / Nuevo Usuario.

Las grillas tienen **paginado de 25**, filtros y acciones condicionadas por permiso. Si el perfil no tiene permiso de ver, se informa y no se listan datos.

### 5.1 Empresas Gran Pagador (EGP)

**Grilla:** RUC, Razón social, Email, Monedas, Línea de crédito, Cliente Atlas, Estado, Acciones.

**Filtros:** buscar por RUC / razón social, Cliente Atlas (Ambos / Sí / No), Estado (Pendiente de Autorización / Autorizado / Activo / Bloqueado).

**Alta / edición — datos que propone el formulario:**

- Datos generales: tipo EGP, RUC, razón social, email, teléfono.
- Monedas habilitadas (GS/PYG y/o USD; al menos una).
- Línea de crédito.
- Condiciones financieras: % interés (TNA), % comisión, % IVA, condiciones especiales.
- Flags: Cliente Atlas, Desembolsos automáticos.
- Adjuntos (en la POC, preview en sesión).

**Estados del ente:**

| Estado | Significado |
|---|---|
| Pendiente de Autorización | Alta cargada; aún no opera |
| Autorizado / Activo | Puede operar en Confirming |
| Bloqueado | No opera; se puede desbloquear |
| Rechazado | Autorización denegada, con motivo |

**Acciones por fila (según permiso):** Gestionar (autorizar/rechazar si está pendiente), Editar, Bloquear/Desbloquear, Eliminar.

**Propuesta de autorización:** un segundo usuario con permiso *Autorización* confirma o rechaza el alta. El rechazo pide motivo. Hasta estar autorizado, el ente no debería operar facturas.

### 5.2 Proveedores

**Grilla:** RUC, Razón social, EGP asociado, Email, Cliente Atlas, Estado, Acciones.

Mismos estados y ciclo de autorización que EGP, con estas diferencias de negocio:

- Debe vincularse a un **EGP padre**.
- Si **no es cliente Atlas**, el formulario pide **datos bancarios y titular** (cuenta crédito, banco, moneda, tipo y nro. de documento, nombre y apellido) para poder acreditar el adelanto.
- El mismo RUC puede aparecer como EGP en un vínculo y como Proveedor de otro EGP (caso Retail S.A. en la demo).

### 5.3 Usuarios del portal

**Grilla:** Nombre, Apellido, Cédula, Email, Teléfono, Ente asociado, Rol, Estado, Acciones.

**Filtros:** ente (RUC / razón), cédula, apellido, estado.

**Alta / edición:** nombre, apellido, cédula, email, teléfono, ente asociado, rol (catálogo según dominio del ente).

**Estados:** Pendiente de Autorización → Autorizado / Rechazado; más Bloqueado (acceso).

**Reglas propuestas:**

- El alta de un usuario EGP/Proveedor **dispara el mail de bienvenida** con usuario y contraseña temporal (enganche con Login).
- Usuario Banco **no recibe temporal**: entra con AD.
- Cambiar **ente asociado** o **rol** de un usuario ya autorizado lo vuelve a **Pendiente de autorización**.
- Bloqueo de usuario por reintentos de login (Keycloak) se refleja en este padrón y notifica.

**Acciones:** ver detalle, gestionar autorización, editar, bloquear, eliminar — todas sujetas a permiso.

### 5.4 Roles y permisos

La POC propone un **catálogo granular** (no un rol monolítico). Se configura por **dominio + nombre de rol**.

**Permisos ABM (extracto):** ver pantalla, CRUD de entes, bloqueo de EGP, CRUD de usuarios, autorización y bloqueo de usuarios, configuración de roles, CRUD de notificaciones (las de sistema no se borran), filtros.

**Permisos Confirming (extracto):** ver pantalla y filtros; pestañas vigentes / no vigentes / no operables; carga manual y masiva; editar datos o solo fecha de pago; habilitar / bloquear; simular adelanto; aprobar desembolso EGP; aprobar desembolso Banco; revertir (1.ª y 2.ª aprobación); ver información sensible; ver/descargar documentos; descargar grilla.

Roles precargados (propuesta de gobierno):

| Dominio | Rol | Intención |
|---|---|---|
| Banco | ADMIN | Acceso total ABM + Confirming |
| Banco | SUPERVISOR | Ve, autoriza, bloquea, opera Confirming, reversión |
| Banco | OPERADOR | Opera Confirming (carga, habilita, simula); no ABM |
| Banco | APROBADOR | Aprueba desembolso Banco y reversión |
| Banco | GERENTE | Consulta ABM y Confirming + info sensible |
| Banco | EJECUTIVO DE CUENTAS | Consulta Confirming y documentos |
| EGP | ADMIN | ABM + Confirming de su universo |
| EGP | OPERADOR | Carga, habilita, bloquea y simula; sin ABM |
| Proveedor | ADMIN | Ve Confirming, simula, documentos |
| Proveedor | OPERADOR | Solo consulta facturas vigentes |

### 5.5 Notificaciones

Tablero de **plantillas** disparadas por eventos de negocio. No es un buzón in-app: es la configuración de *qué se avisa, a quién y por qué canal*.

**Columnas:** Agrupador, Nombre, Evento/estado disparador, Tipo, Dominio, Rol, Emails, Mensaje, Activa, Acciones.

**Tipos de envío:** Dominio y Rol, Email, o ambos.

**Agrupadores y propuestas cargadas en la POC:**

| Agrupador | Eventos que cubre |
|---|---|
| **ABM** | Alta de ente; alta de usuario Banco/EGP/Proveedor pendiente de autorización; cambio de ente o rol de un usuario ya autorizado; bloqueo por reintentos de login |
| **LOGIN** | Bienvenida primer login Banco (en producto se desestimó el mail con temporal para Banco); bienvenida EGP/Proveedor con temporal |
| **Simulación** | Solicitud de aprobación al EGP; aprobación automática al banco (pendiente de desembolso); aviso a EGP y Proveedor cuando queda Financiada; rechazo de adelanto |
| **Gestión de facturas** | Nueva factura pendiente de habilitar; alerta 15 días a vencimiento; alerta crítica 5 días; fecha de pago próxima (30–31 días); alcanzó fecha de pago (NO ELEGIBLE); alcanzó vencimiento (Vencida, inactiva en el seed) |

Las notificaciones **de sistema** no se pueden borrar; las de usuario sí, si hay permiso.

### 5.6 Auditoría ABM (propuesta)

La POC registra en consola un log de altas/cambios de entes y usuarios (quién, qué, cuándo). En producto debe persistirse.

---

## 6. Confirming — operación de facturas y adelantos

**Objetivo de negocio:** que EGP, Proveedor y Banco operen el ciclo de vida de la factura hasta el adelanto, con costos transparentes y control de la línea de crédito de la EGP.

### 6.1 Contexto de operación

En la topbar, **Estás operando para el ente**:

- Filtra la grilla (facturas del EGP o del Proveedor elegido).
- Muestra el **panel financiero** de ese ente: RUC, línea de crédito, TNA, comisión, IVA, monedas.
- Si está en *Todos los entes* (típico Banco), el panel se oculta y se ven todas las facturas.

### 6.2 Consulta: filtros, pestañas y grilla

**Filtros:** buscar (nro. factura / EGP / proveedor), fecha de vencimiento, fecha de pago, estado.

**Pestañas (una factura vive en una sola):**

| Pestaña | Estados |
|---|---|
| **Vigentes** | Pendiente, Habilitada, Bloqueada, Pendiente aprobación EGP, Pendiente de desembolso |
| **No vigentes** | Financiada, Vencida |
| **No operables** | NO ELEGIBLE |

**Grilla:** Nro. factura, EGP, Proveedor, emisión, vencimiento, moneda, monto, fecha de pago, timbrado, estado, eliminar, acciones.

Fechas en pantalla: `dd-mm-yyyy`. Monedas: **GS** (guaraníes / PYG) y **USD**.

**Botonera global:** Habilitar · Bloquear · Simular · Cargar Factura. Se habilitan o muestran tooltip según la selección.

### 6.3 Carga de facturas

Tres caminos propuestos:

1. **Individual** — modal con nro., EGP, proveedor, emisión, vencimiento, fecha de pago, moneda, monto, timbrado. Si no se indica fecha de pago, se toma el vencimiento.
2. **Masiva** — Excel/CSV con template descargable. Procesamiento **parcial**: las filas inválidas se informan agrupadas por motivo; las válidas se cargan. Obligatorio: nro., EGP, proveedor, emisión, vencimiento, moneda, monto > 0.
3. **Escaneo / QR** — en la POC es simulado (timeout); en producto es fase posterior.

**Alta:** la factura nace en **Pendiente**, salvo que se pida Habilitada/Bloqueada, o que la fecha de pago esté a **menos de 30 días** → **NO ELEGIBLE**.

### 6.4 Acciones sobre facturas

| Acción | Desde qué estado | Resultado |
|---|---|---|
| **Habilitar** (individual o masivo) | Pendiente o Bloqueada | Habilitada |
| **Bloquear** (individual o masivo) | Pendiente o Habilitada | Bloqueada |
| **Editar fecha de pago** | NO ELEGIBLE, Pendiente, Habilitada, Bloqueada | Si queda ≥ 30 días → Habilitada; si no → NO ELEGIBLE (con confirmación) |
| **Eliminar** | Operable | Confirmación; irreversible en UI |
| **Simular** (individual) | Habilitada | Modal de ticket de adelanto |
| **Simular** (múltiple, cabecera) | ≥ 2 Habilitadas, mismo EGP + Proveedor + moneda | Un solo ticket; 1 cuota si misma fecha de pago, N cuotas si fechas distintas |
| **Ejecutar adelanto** | Desde la simulación | Pasa a Pendiente aprobación EGP |
| **Aprobar EGP** | Pendiente aprobación EGP | Pendiente de desembolso (aprobación banco **automática** en la POC) |
| **Rechazar con motivo** | Pendiente aprobación EGP | Pide nueva fecha de pago → Habilitada o NO ELEGIBLE |
| **Rechazar sin motivo** | Pendiente aprobación EGP | Bloqueada |

La primera factura tildada **ancla** la combinatoria (EGP + Proveedor + moneda); las que no coinciden no se pueden tildar.

### 6.5 Cálculo del adelanto (propuesta transparente al usuario)

```
interés    = monto × TNA × días a adelantar / 365
comisión   = monto × % comisión
IVA        = (interés + comisión) × % IVA
neto       = monto − interés − comisión − IVA
```

- Las tasas salen de la **configuración del EGP**.
- `días a adelantar` no puede ser negativo.
- El monto a adelantar no puede superar el de la factura (en múltiple, el monto es la suma y es de solo lectura).
- Tras ejecutar, CORE BANKING se simula con ~2,5 s: **éxito → Financiada**; **error (~15 % en demo) → vuelve a Pendiente aprobación EGP** para reintentar.

### 6.6 Máquina de estados (resumen)

```
Alta ──► Pendiente ──habilitar──► Habilitada ──simular/ejecutar──► Pendiente aprobación EGP
              │                      │                                      │
              └──bloquear──► Bloqueada                              aprueba ──► Pendiente desembolso ──CORE OK──► Financiada
                                                                     │                              └──CORE error──► Pendiente aprobación EGP
                                                                     ├──rechazo con motivo──► Habilitada / NO ELEGIBLE
                                                                     └──rechazo sin motivo──► Bloqueada

Fecha de pago < 30 días ──► NO ELEGIBLE ──corregir fecha ≥ 30──► Habilitada
Vencimiento documental (propuesta Excel, no en POC) ──► Vencida
```

**Estados terminales:** Financiada y Vencida. NO ELEGIBLE es el único no operable con salida (corregir fecha de pago).

### 6.7 Reglas que la POC ya demuestra

- Fecha de pago mínima: **30 días calendario** (parámetro `PAYMENT_DATE_MIN_DAYS`).
- Habilitar solo desde Pendiente/Bloqueada; bloquear solo desde Pendiente/Habilitada; simular solo desde Habilitada.
- Simulación múltiple con misma combinatoria.
- Monedas GS/USD y alias en carga masiva (PYG → GS, DÓLAR → USD).
- Formato de fechas `dd-mm-yyyy`.

### 6.8 Propuestas de producto **aún no simuladas** en la POC

Estas reglas están en las épicas MAGIA-346/347/348 y deben construirse en el desarrollo; la POC no las ejecuta:

| Propuesta | Impacto |
|---|---|
| Freeze del límite de crédito al confirmar la simulación (disponible = límite − freeze) | El panel hoy muestra el límite estático |
| Quien **solicita** el adelanto no puede ser quien **cargó** la factura | Segregación de funciones |
| Corte horario: generar adelanto **solo antes de las 17:00** (hora PY) | Control operativo tesorería |
| Ventana de n días entre aprobación EGP y solicitud de adelanto | Evita adelantos vencidos |
| EGP y Proveedor deben existir y estar **activos** al guardar la factura | Integridad con ABM |
| Leyenda *valores simulados son estimativos* en el modal | Transparencia |
| Transición automática a **Vencida** por vencimiento documental | Cierre de ciclo |
| Bloquear también desde Pendiente aprobación EGP (Excel vs POC) | Alinear con negocio |
| Aprobación bancaria **manual** (hoy la POC la da por automática) | Si el banco la exige, reaparecen Banco Aprueba / Rechaza |
| Reversión de adelanto (épica Reversiones) | Stubs / residuales en la POC |

Morosidad (MAGIA-350) y Reversiones (MAGIA-547) tienen documentación propia bajo Documentación Funcional; no se detallan acá porque no son el núcleo navegable de estas cuatro pantallas.

---

## 7. Recorridos sugeridos para validar con el cliente

### Login — onboarding EGP

`Perfil EGP + Primer login` → `ana` / `Temporal2026` → cambiar contraseña → OTP → entrar al portal.

### Login — Banco

`Perfil BANCO` → `admin` / `Temporal2026` → simular aprobación AD → portal.

### ABM — alta y autorización

ABM → Nuevo EGP o Proveedor → queda Pendiente de Autorización → **Gestionar** (autorizar o rechazar con motivo) → Nuevo Usuario asociado → autorización → (en producto) mail de bienvenida.

### Mi perfil

Entrar como EGP/Proveedor y abrir **Mi perfil**: datos en solo lectura + ficha del ente. Como Banco, elegir un ente en *Estás operando para el ente* y ver su detalle.

### Confirming — camino feliz

1. Tab **Vigentes**, factura **Pendiente** → **Habilitar**.
2. **Simular** → revisar ticket → **Ejecutar adelanto**.
3. **Aprobar EGP** → espera CORE → **Financiada**.

### Confirming — no elegible

Alta con fecha de pago a menos de 30 días → tab **No operables** → editar fecha ≥ 30 días → vuelve a **Habilitada**.

### Confirming — masivo

Seleccionar ≥ 2 facturas **Habilitada** del mismo EGP+Proveedor+moneda → **Simular** en cabecera. Cargar Excel desde el modal (descargar template primero).

---

## 8. Mapa POC ↔ Documentación Funcional

| En la POC | Página de épica |
|---|---|
| Flujos de Login y 2FA | [Login (MAGIA-155)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687640/Login) |
| ABM EGP / Proveedor / Usuarios / Notificaciones / Roles | [Gestión de ABM (MAGIA-5)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625686041/Gesti+n+de+ABM) |
| Grilla, pestañas, habilitar/bloquear, máquina de estados | [Confirming (MAGIA-346)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687845/Confirming) |
| Carga individual, masiva, QR, fecha de pago | [Gestión de Facturas (MAGIA-347)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687859/Gesti+n+de+Facturas) |
| Simulación individual/múltiple y freeze de límite | [Simulación de Adelantos (MAGIA-348)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687873/Simulaci+n+de+Adelantos) |
| CORE y avisos de préstamo / factura | [Desembolso (MAGIA-349)](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1625687887/Desembolso) |
| Prototipos | [FIGMA](https://bancoatlaspy.atlassian.net/wiki/spaces/~5ffedd6764208901414b0121/pages/1654915073/FIGMA) |

Diagramas de user flow ABM (entes, usuarios, notificaciones): [repositorio de la POC — `/assets/diagramas`](https://github.com/MarianaIntive/atlas-confirming-poc/tree/master/assets/diagramas).

---

## 9. Cómo leer la POC vs el producto

| En la POC | En el producto Atlas Trade |
|---|---|
| Todo corre en el navegador (`auth.js`, `app.js`) | FE + BFF + BE + Keycloak + AD + Core + notificaciones |
| Datos seed (entes, usuarios, facturas, plantillas) | Persistencia real y APIs MAGIA |
| Permisos simulados en sesión | Keycloak + permisos en BD |
| CORE con error aleatorio 15 % | Integración real de solicitud de crédito |
| Home Banking y AD *simulados* | Integraciones a cerrar en spikes |
| QR, reportes y KPIs de dashboard | Maqueta / fases posteriores |

**Mesa de Ayuda (textos de Login):** interno 1500 · mesadeayuda@bancoatlas.com.py
