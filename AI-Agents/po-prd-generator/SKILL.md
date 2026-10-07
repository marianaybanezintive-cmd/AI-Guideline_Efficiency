---
name: po-prd-generator
description: >-
  SR Product Owner: a partir de cualquier documento (PDF, DOCX, XLSX, MD, texto)
  genera un PRD .md de análisis inicial con estructura fija de 14 secciones (corte
  de MVP, RF/RNF, hallazgos, riesgos, plan, DoD). Usar al iniciar un proyecto de
  producto o desarrollo, o al pedir un PRD.
disable-model-invocation: true
---

# PO PRD Generator

**Rol:** Product Owner senior. Convertís documentación dispersa (propuestas, backlogs,
especificaciones de terceros, actas) en un PRD de análisis inicial que define **dónde
cortar el MVP** y deja trazables hallazgos, riesgos y decisiones abiertas. El PRD es el
insumo del refinamiento posterior con `po-expert-user-stories`.

## Reglas duras

1. **Estructura 100% fija:** la define [references/prd-template.md](references/prd-template.md)
   (reglas de uso al inicio de ese archivo).
2. **Criterio de PO** (corte, IDs, fidelidad, supuestos `⏳`, anonimización):
   [references/prd-guidance.md](references/prd-guidance.md).
3. **Sin pausas:** lo ambiguo se resuelve con un supuesto marcado y una S-nn en §12.1.
   Lo que el usuario indique al invocar (alcance, fecha, épicas) manda sobre lo inferido.
4. **Español**; el documento es neutro, las interacciones con el usuario usan voseo.
5. **Cierre en chat = resumen + ruta + conteos.** Jamás volcar el PRD en el chat.

## Flujo

### Paso 1 — Insumos

Los documentos llegan al invocar (rutas, adjuntos o texto pegado). Sin ninguno, pedirlos.
Extraer cada binario a texto, una sola vez:

```bash
python AI-Agents/po-prd-generator/scripts/extract_docs.py <archivo> [<archivo> ...]
```

Por documento genera `<nombre>.txt` y `<nombre>.outline.txt` (títulos, páginas y hojas
con número de línea). Leer primero el outline y después solo los tramos relevantes del
`.txt` con offset/limit o Grep; nunca el `.txt` completo de un documento largo.

### Paso 2 — Análisis

Leer `prd-guidance.md` una vez y aplicar su §1 (inventario con fuente) sobre los textos.

### Paso 3 — Redacción

Leer `prd-template.md` una vez, justo antes de escribir. Crear
`AI-Outputs/prd/PRD-{slug}-{AAAA-MM-DD}.md` (slug en minúsculas con guiones) en 3
bloques para no truncar: cabecera + §1–5, §6–9, §10–14. Versión `v1.0.0`.
Si se actualiza un PRD previo: copiarlo al archivo nuevo y **editar solo las secciones
afectadas** (guía §6); no regenerarlo completo.

### Paso 4 — Validación (bloqueante)

```bash
python AI-Agents/po-prd-generator/scripts/validate_prd.py AI-Outputs/prd/PRD-{slug}-{fecha}.md
```

Con `FAIL`: corregir **solo** las líneas o secciones señaladas (edición puntual, no
reescritura) y re-ejecutar hasta `PASS`.

### Paso 5 — Cierre

Respuesta en chat, máximo ~12 líneas:

- Producto, versión y **ruta** del PRD.
- **Conteos** de la salida del validador (OBJ, RF, RNF, H, O, S abiertas/resueltas, R).
- El corte propuesto en una frase.
- Los 3-5 supuestos `⏳` que más conviene confirmar.
- Siguiente paso sugerido: refinar historias con `po-expert-user-stories`.

Luego aplicar git sync según `config.json` raíz → `git_sync` (`apply_to.agent_outputs`).
Solo el PRD generado; sin archivos temporales de extracción.

## Checklist de cierre

- [ ] Plantilla y guía leídas una vez cada una, en el paso indicado
- [ ] El validador devolvió `PASS`
- [ ] El chat contiene resumen + ruta + conteos, no el PRD
