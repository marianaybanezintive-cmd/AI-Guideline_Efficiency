# po-prd-generator

Agente (skill) que actúa como **Product Owner senior** y genera un **PRD de análisis
inicial en `.md`** a partir de cualquier documentación (PDF, DOCX, XLSX, MD, texto).
Respeta al 100% la estructura del PRD de referencia del proyecto Conector FIX ↔ A3
(14 secciones: resumen ejecutivo con el corte de MVP, decisiones, contexto, objetivos,
actores, matriz de alcance, épicas, RF, RNF, hallazgos, observaciones de backlog,
riesgos/decisiones abiertas, plan de entrega y DoD).

## Cómo usarlo

En Cursor, invocalo por nombre y pasale los documentos:

> Usá el skill po-prd-generator con `C:\ruta\propuesta.docx` y `C:\ruta\backlog.xlsx`.
> Alcance: épicas 1 a 3. Fecha límite: 31-dic.

Podés indicar alcance, fecha, épicas o cliente; si no, se infieren de los documentos y
lo dudoso queda como decisión abierta (§12.1) marcada `⏳`.

## Salida

`AI-Outputs/prd/PRD-{slug}-{AAAA-MM-DD}.md`. Luego se refina con `po-expert-user-stories`.

## Estructura

| Archivo | Para qué |
|---------|----------|
| `SKILL.md` | Rol, reglas duras y flujo |
| `references/prd-template.md` | Esqueleto de las 14 secciones (fuente de verdad de la estructura) |
| `references/prd-guidance.md` | Criterio de PO: regla de corte, IDs, fidelidad, calidad |
| `scripts/extract_docs.py` | PDF/DOCX/XLSX/PPTX → `.txt` UTF-8 en carpeta temporal |
| `scripts/validate_prd.py` | Valida estructura contra la plantilla y cuenta OBJ/RF/RNF/H/O/S/R |

Dependencias de los scripts: `pypdf`, `python-docx`, `openpyxl` (y `python-pptx` para `.pptx`).

Origen de la plantilla: `PRD-conector-fix-a3-fase1-2026-09-23-v2.md` (v2.0.0), generalizado.
