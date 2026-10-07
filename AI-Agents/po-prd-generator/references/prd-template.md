# Plantilla PRD — esqueleto obligatorio (14 secciones)

Reglas de uso: copiar el esqueleto tal cual, en este orden y con esta numeración.
Texto fuera de `⟦…⟧` = fijo, no se reescribe. `⟦…⟧` = placeholder o instrucción: se
reemplaza por contenido del input y **no puede quedar ningún `⟦` en el entregable**.
Una sección sin insumo se conserva con `No aplica — ⟦motivo⟧` o con la pregunta
trasladada a §12.1; nunca se omite ni se renumera. Cómo completar: [prd-guidance.md](prd-guidance.md).

````markdown
# PRD - ⟦Producto⟧ — ⟦Fase / alcance corto⟧ (⟦Épicas 1 a N⟧)

> **Versión:** v1.0.0 · **Fecha:** ⟦AAAA-MM-DD⟧ · **Actualizado:** ⟦AAAA-MM-DD⟧ — ⟦motivo del cambio⟧
> **Producto:** ⟦nombre⟧
> **Alcance de este documento:** ⟦épicas/fases cubiertas, con nombre⟧
> **Fecha límite comprometida:** ⟦fecha o «sin fecha comprometida»⟧
> **Autor:** Product Owner
> **Fuentes:**
> - `⟦archivo⟧` (⟦qué es, versión, fecha, páginas⟧)

---

## Tabla de contenidos

1. [Resumen ejecutivo — dónde está el corte](#1-resumen-ejecutivo--dónde-está-el-corte)
2. [Contexto y problema](#2-contexto-y-problema)
3. [Objetivos de la ⟦Fase⟧ y métricas de éxito](#⟦ancla⟧)
4. [Actores y sistemas](#4-actores-y-sistemas)
5. [**El corte del MVP — regla de decisión y matriz de ⟦mensajes|capacidades⟧**](#⟦ancla⟧)
6. [Alcance por épica](#6-alcance-por-épica)
7. [Alcance diferido — Épicas ⟦X e Y⟧](#⟦ancla⟧)
8. [Requerimientos funcionales de la ⟦Fase⟧](#⟦ancla⟧)
9. [Requerimientos no funcionales y restricciones](#9-requerimientos-no-funcionales-y-restricciones)
10. [Hallazgos de la documentación ⟦fuente⟧ que condicionan el alcance](#⟦ancla⟧)
11. [Observaciones sobre el backlog borrador (⟦formato⟧)](#⟦ancla⟧)
12. [Riesgos, dependencias y decisiones abiertas](#12-riesgos-dependencias-y-decisiones-abiertas)
13. [Plan de entrega contra el ⟦fecha límite⟧](#⟦ancla⟧)
14. [Criterios de aceptación de la ⟦Fase⟧ (DoD de fase)](#⟦ancla⟧)

---

## 1. Resumen ejecutivo — dónde está el corte

⟦Una frase en negrita que resume el MVP: qué hace el producto y qué todavía no hace.⟧

⟦Una frase: el corte no es por cantidad ni esfuerzo sino por el criterio elegido (efecto, riesgo, valor).⟧

| | ⟦Épicas del documento (fase, fecha)⟧ | ⟦Épica N — nombre⟧ | ⟦Épica M — nombre⟧ |
|---|---|---|---|
| **Qué hace el producto** | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| **Efecto sobre ⟦estado del sistema/datos/mercado⟧** | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| **Riesgo de un defecto** | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| **⟦Mensajes/interfaces⟧ salientes** | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| **⟦Mensajes/interfaces⟧ entrantes** | ⟦⟧ | ⟦⟧ | ⟦⟧ |
| **Habilita** | ⟦⟧ | ⟦⟧ | ⟦⟧ |

**Las tres preguntas que resuelven cualquier caso dudoso:**

1. ⟦Pregunta → épica diferida 1, sin excepción.⟧
2. ⟦Pregunta → épica diferida 2.⟧
3. ⟦Pregunta → MVP.⟧

**Por qué este corte es el correcto y no uno arbitrario:**

- **⟦Argumento 1 en negrita.⟧** ⟦Explicación.⟧
- **⟦Argumento 2.⟧** ⟦Explicación.⟧
- **⟦Argumento 3.⟧** ⟦Explicación.⟧

> ⟦✅ Confirmación o ⚠️ riesgo principal del corte, con fecha y enlace a la decisión de §12.1.⟧

---

## 1.bis Decisiones confirmadas el ⟦AAAA-MM-DD⟧

⟦Frase: cuántas definiciones cerradas y qué modifican. Sin decisiones en el input: una fila «—» y «Sin decisiones confirmadas a la fecha; las preguntas viven en §12.1».⟧

| Decisión | Definición confirmada | Qué cambia |
|---|---|---|
| **⟦Tema⟧** | ⟦Qué se confirmó, quién, cuándo⟧ | ⟦Efecto sobre diseño, alcance o riesgo⟧ |

⟦Subsecciones opcionales, una por ronda o contingencia (repetibles):⟧
### Ronda adicional de definiciones — ⟦AAAA-MM-DD⟧
⟦Misma tabla de 3 columnas.⟧
### Definición revisada o desestimada — ⟦AAAA-MM-DD⟧: ⟦tema⟧
⟦Narrativa: qué se evaluó, por qué se descartó, flujo resultante y **Consecuencia** sobre el alcance.⟧
### ⟦Contingencia o nota derivada⟧ — ⟦AAAA-MM-DD⟧
⟦Consecuencia sobre riesgos (R-n) y spikes nuevos (S-nn).⟧

---

## 2. Contexto y problema

⟦2-3 párrafos: quién es el cliente, qué construye, qué necesita, qué se construye, prioridad fijada por el cliente y objetivo de negocio de la fase.⟧

### Qué significa ⟦término(s) clave⟧ en el diccionario de ⟦fuente/dominio⟧

⟦Glosario de los 2-4 términos que definen el corte; viñetas con **término** — definición — por qué importa.⟧

⟦Cierre en negrita: el corte no es una concesión de alcance sino fiel a lo que esos términos significan.⟧

---

## 3. Objetivos de la ⟦Fase⟧ y métricas de éxito

### Objetivo de negocio

⟦Un párrafo con el resultado de negocio y la fecha.⟧

### Objetivos de producto

| # | Objetivo | Cómo se verifica |
|---|---|---|
| OBJ-1 | ⟦⟧ | ⟦Criterio medible⟧ |

### Métricas

| Métrica | Objetivo ⟦Fase⟧ |
|---|---|
| ⟦⟧ | ⟦Valor + «a validar» si no viene del input⟧ |

### No-objetivos explícitos de la ⟦Fase⟧

- ⟦No se …⟧

---

## 4. Actores y sistemas

### 4.1 Actores

| Actor | Descripción | Rol en ⟦Fase⟧ |
|---|---|---|
| **⟦⟧** | ⟦⟧ | ⟦⟧ |

### 4.2 Sistemas y componentes

| Componente | Responsabilidad | Épica |
|---|---|---|
| **⟦⟧** | ⟦⟧ | ⟦N⟧ |

---

## 5. El corte del MVP — regla de decisión y matriz de ⟦mensajes|capacidades⟧

### 5.1 La regla

> **Entra en el MVP ⟦criterio positivo⟧:** ⟦enumeración⟧.

> **Queda fuera de ⟦la Fase⟧** ⟦criterio negativo⟧ (Épica ⟦N⟧) y ⟦criterio negativo 2⟧ (Épica ⟦M⟧).

⟦Corolario de una frase.⟧

### 5.2 Matriz de ⟦mensajes|capacidades⟧ por épica

#### ⟦Capa o bloque 1⟧ — **⟦dentro del MVP (Épica N)⟧**

| ⟦Elemento⟧ | ⟦Identificador⟧ | ⟦Dir.⟧ | ⟦Por qué está en el MVP | Épica | Criterio⟧ |
|---|---|---|---|

⟦Un bloque `####` por capa/dominio (3-6). Marcar «el corte pasa por acá» donde el criterio parta un bloque.⟧

> **Decisión de alcance explícita y necesaria:** ⟦acotación de cualquier término ambiguo que arrastre alcance (cf. R-n).⟧

### 5.3 El corte en la dirección ⟦flujo/integración principal⟧

⟦Frase de introducción.⟧

| Flujo ⟦de integración⟧ | Épica | Detalle |
|---|---|---|
| **⟦Origen → Destino⟧** | **⟦N⟧** | ⟦⟧ |

### 5.4 Capacidades transversales: dónde corta cada una

⟦Frase: dónde la fuente y el backlog no coinciden y se decide.⟧

| Capacidad | En el MVP (Épica ⟦N⟧) | Diferido a Épica ⟦M⟧ (⟦nombre⟧) |
|---|---|---|
| **⟦p. ej. Recuperabilidad, Idempotencia, Auditoría, Observabilidad, Alta disponibilidad⟧** | ⟦⟧ | ⟦⟧ |

> ⟦Nota que cita la fuente que justifica la separación.⟧

---

## 6. Alcance por épica

### Épica 1 — ⟦Nombre⟧

**Objetivo:** ⟦⟧
**Duración prevista:** ⟦T0 + N meses (N sprints)⟧.

**Dentro de alcance**

1. ⟦Entregable numerado, con enlaces a S-nn/R-n donde aplique.⟧

**Fuera de alcance:** ⟦⟧

**Criterio de salida:** ⟦condiciones verificables⟧

> **Restricción de planificación:** ⟦opcional; vigencias, dependencias de terceros⟧

---

⟦Repetir el bloque por cada épica del alcance (Dentro de alcance puede ser tabla Bloque | Contenido).⟧

---

## 7. Alcance diferido — Épicas ⟦X e Y⟧

### Épica ⟦X⟧ — ⟦Nombre⟧ (⟦T0 + N meses⟧)

⟦Qué cambio de naturaleza la habilita y de dónde se derivan sus requisitos.⟧

| Bloque | Contenido |
|---|---|
| ⟦⟧ | ⟦⟧ |

**Dependencias que no existen en la ⟦Fase⟧:** ⟦⟧

⟦Repetir por épica diferida; cerrar con **Consideración de ⟦tema⟧:** si hay una decisión de la Épica 1 que condiciona la diferida.⟧

---

## 8. Requerimientos funcionales de la ⟦Fase⟧

### 8.1 ⟦Grupo funcional⟧

| ID | Requerimiento |
|---|---|
| RF-01 | ⟦Enunciado verificable, una sola obligación; RF-01.1 para subrequisitos⟧ |

⟦8.2 a 8.n: grupos funcionales del dominio (mínimo 3); cierre sugerido: Auditoría y observabilidad; Seguridad, operación y configuración.⟧

---

## 9. Requerimientos no funcionales y restricciones

### 9.1 Tecnología (impuesta por ⟦el cliente⟧)

| Aspecto | Definición |
|---|---|
| ⟦⟧ | ⟦⟧ |

> ⚠️ ⟦Verificación técnica a hacer en la Épica 1.⟧

### 9.2 ⟦Protocolo y conectividad|Integración y datos⟧ (impuesto por ⟦tercero⟧)

| Aspecto | Definición |
|---|---|
| ⟦⟧ | ⟦⟧ |

### 9.3 Requerimientos no funcionales del producto

| ID | Requerimiento |
|---|---|
| RNF-01 | ⟦Con umbral medible (p95, %, segundos)⟧ |

---

## 10. Hallazgos de la documentación ⟦fuente⟧ que condicionan el alcance

⟦Intro: hallazgos que cambian o acotan lo que asumen la propuesta o el backlog; cada uno tiene su decisión en §12.⟧

| # | Hallazgo | Impacto |
|---|---|---|
| **H-1** | **⟦Hecho citado de la fuente⟧** ⟦detalle literal⟧ | ⟦Efecto; ✅ Resuelto ⟦fecha⟧ + ref §1.bis y S-nn, o → S-nn⟧ |

---

## 11. Observaciones sobre el backlog borrador (⟦formato⟧)

⟦Intro: el backlog es una buena base pero tiene inconsistencias; se listan para el refinamiento, no como crítica. Sin backlog: «No aplica — no se recibió backlog borrador» y una O-1 sobre su ausencia.⟧

| # | Observación | Acción propuesta |
|---|---|---|
| **O-1** | **⟦Observación⟧** ⟦evidencia⟧ | ⟦Acción⟧ |

---

## 12. Riesgos, dependencias y decisiones abiertas

### 12.1 Decisiones abiertas — a resolver en la Épica 1

| ID | Pregunta | Impacto si no se resuelve | Propuesta del PO |
|---|---|---|---|
| **S-01** ⏳ **SIN DEFINIR** | **⟦Pregunta⟧** | ⟦⟧ | ⟦Propuesta accionable⟧ |

### 12.2 Riesgos

| ID | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| **R-1** | **⟦⟧** | ⟦Alto/Medio/Bajo — consecuencia⟧ | ⟦⟧ |

### 12.3 Dependencias del ⟦cliente⟧

| Dependencia | Requerida para | Fecha límite sugerida |
|---|---|---|
| ⟦⟧ | ⟦Épica/RF⟧ | ⟦⟧ |

---

## 13. Plan de entrega contra el ⟦fecha límite⟧

⟦Supuestos de T0 y duración de sprint.⟧

| Etapa | Duración | Ventana estimada | Entregable de cierre |
|---|---|---|---|
| **Épica 1** — ⟦Nombre⟧ | ⟦N sprints⟧ | ⟦⟧ | ⟦⟧ |
| **Holgura hasta ⟦fecha⟧** | ⟦⟧ | ⟦⟧ | ⟦Qué absorbe⟧ |

**Lectura del PO sobre la fecha (⟦actualizada al AAAA-MM-DD⟧):** ⟦camino crítico, holgura, riesgo de alcance vs calendario.⟧

En consecuencia, las prioridades del sprint 0 son:

1. **⟦Acción⟧** ⟦por qué es la más urgente⟧

---

## 14. Criterios de aceptación de la ⟦Fase⟧ (DoD de fase)

La ⟦Fase⟧ se considera completa cuando:

- [ ] ⟦Criterio verificable y medible⟧

---

*Documento generado como insumo para el refinamiento de historias de usuario con el agente `po-expert-user-stories`.*
````
