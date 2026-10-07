#!/usr/bin/env python3
"""Valida que un PRD respete la estructura fija de references/prd-template.md.

Uso: python validate_prd.py <prd.md> [--template]
  --template  valida el esqueleto (permite placeholders ⟦…⟧).
Salida: PASS/FAIL por chequeo + conteos (RF, RNF, H, O, S, R, OBJ).
Exit code 1 si falla algún chequeo.
"""
import re
import sys
from pathlib import Path

H2 = [
    r"## 1\. Resumen ejecutivo — dónde está el corte",
    r"## 1\.bis Decisiones confirmadas el ",
    r"## 2\. Contexto y problema",
    r"## 3\. Objetivos de la .+ y métricas de éxito",
    r"## 4\. Actores y sistemas",
    r"## 5\. El corte del MVP — regla de decisión y matriz de .+",
    r"## 6\. Alcance por épica",
    r"## 7\. Alcance diferido — Épicas? .+",
    r"## 8\. Requerimientos funcionales de la .+",
    r"## 9\. Requerimientos no funcionales y restricciones",
    r"## 10\. Hallazgos de la documentación .+ que condicionan el alcance",
    r"## 11\. Observaciones sobre el backlog borrador \(.+\)",
    r"## 12\. Riesgos, dependencias y decisiones abiertas",
    r"## 13\. Plan de entrega contra el .+",
    r"## 14\. Criterios de aceptación de la .+ \(DoD de fase\)",
]
H3 = [
    r"### Qué significa .+ en el diccionario de .+",
    r"### Objetivo de negocio", r"### Objetivos de producto", r"### Métricas",
    r"### No-objetivos explícitos de la .+",
    r"### 4\.1 Actores", r"### 4\.2 Sistemas y componentes",
    r"### 5\.1 La regla", r"### 5\.2 Matriz de .+ por épica",
    r"### 5\.3 El corte en la dirección .+",
    r"### 5\.4 Capacidades transversales: dónde corta cada una",
    r"### Épica \d+ — .+",
    r"### 8\.1 .+", r"### 8\.2 .+", r"### 8\.3 .+",
    r"### 9\.1 Tecnología \(impuesta por .+\)",
    r"### 9\.2 .+ \(impuesto por .+\)",
    r"### 9\.3 Requerimientos no funcionales del producto",
    r"### 12\.1 Decisiones abiertas — a resolver en la Épica 1",
    r"### 12\.2 Riesgos", r"### 12\.3 Dependencias del .+",
]
HEADER = ["Versión", "Fecha", "Actualizado", "Producto", "Alcance de este documento",
          "Fecha límite comprometida", "Autor", "Fuentes"]
CLOSING = "*Documento generado como insumo para el refinamiento de historias de usuario con el agente `po-expert-user-stories`.*"
TABLE_HEADS = ["| # | Objetivo | Cómo se verifica |", "| Actor | Descripción |",
               "| Componente | Responsabilidad | Épica |", "| Decisión | Definición confirmada | Qué cambia |",
               "| # | Hallazgo | Impacto |", "| # | Observación | Acción propuesta |",
               "| ID | Pregunta | Impacto si no se resuelve | Propuesta del PO |",
               "| ID | Riesgo | Impacto | Mitigación |",
               "| Dependencia | Requerida para | Fecha límite sugerida |",
               "| Etapa | Duración | Ventana estimada | Entregable de cierre |"]
ANON = re.compile(r"(hacial cliente|desdel cliente|apruebal cliente|mesal cliente|\bde el cliente\b)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    template = "--template" in sys.argv
    if not args:
        print(__doc__)
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    text = Path(args[0]).read_text(encoding="utf-8")
    if template:  # el esqueleto vive dentro de un bloque ````markdown
        m = re.search(r"````markdown\n(.*?)\n````", text, re.S)
        text = m.group(1) if m else text
    lines = text.splitlines()
    fails = []

    def check(ok, msg):
        if not ok:
            fails.append(msg)

    # Orden y presencia de secciones ## (fuera de bloques de código)
    pos = []
    for pat in H2:
        idx = next((i for i, l in enumerate(lines) if re.match(pat, l)), None)
        check(idx is not None, f"falta sección: {pat}")
        pos.append(idx if idx is not None else -1)
    found = [p for p in pos if p >= 0]
    check(found == sorted(found), "las secciones ## no están en el orden de la plantilla")
    for pat in H3:
        if template and pat in (r"### 8\.2 .+", r"### 8\.3 .+"):
            continue  # el esqueleto trae un solo grupo de muestra
        check(any(re.match(pat, l) for l in lines), f"falta subsección: {pat}")
    if not template:
        check(len([l for l in lines if re.match(r"### Épica \d+ — ", l)]) >= 2,
              "se esperan ≥2 subsecciones '### Épica N — …' (§6 y §7)")

    check(bool(lines) and re.match(r"# PRD [-—–] ", lines[0]) is not None,
          "el título debe empezar con '# PRD - '")
    head = "\n".join(lines[:15])
    for key in HEADER:
        check(f"**{key}:**" in head, f"falta campo de cabecera: {key}")
    check("## Tabla de contenidos" in text, "falta '## Tabla de contenidos'")
    toc = [l for l in lines if re.match(r"^\d{1,2}\. \[", l)]
    check(len(toc) == 14, f"la tabla de contenidos debe tener 14 entradas (tiene {len(toc)})")
    check("**Las tres preguntas que resuelven cualquier caso dudoso:**" in text,
          "falta 'Las tres preguntas…' en §1")
    check("**Por qué este corte es el correcto y no uno arbitrario:**" in text,
          "falta 'Por qué este corte es el correcto…' en §1")
    for th in TABLE_HEADS:
        check(th in text, f"falta tabla con encabezado: {th}")
    check("| ID | Requerimiento |" in text, "faltan tablas '| ID | Requerimiento |' (§8/§9.3)")
    check("| Aspecto | Definición |" in text, "faltan tablas '| Aspecto | Definición |' (§9.1/§9.2)")
    check(bool(re.search(r"^- \[ \] ", text, re.M)), "§14 sin checkboxes '- [ ]'")
    check(text.rstrip().endswith(CLOSING), "falta la línea de cierre del documento")
    check(text.count("**Dentro de alcance**") >= 1, "§6 sin '**Dentro de alcance**'")
    check("**Criterio de salida:**" in text, "§6 sin '**Criterio de salida:**'")

    if not template:
        check("⟦" not in text and "⟧" not in text, "quedan placeholders ⟦…⟧")
        m = ANON.search(text)
        check(m is None, f"resto de anonimización: «{m.group(0) if m else ''}»")

    counts = {
        "OBJ": len(set(re.findall(r"\bOBJ-\d+", text))),
        "RF": len(set(re.findall(r"\bRF-\d+(?:\.\d+)?", text))),
        "RNF": len(set(re.findall(r"\bRNF-\d+", text))),
        "H": len(set(re.findall(r"\*\*H-\d+\*\*", text))),
        "O": len(set(re.findall(r"\*\*O-\d+\*\*", text))),
        "S": len(set(re.findall(r"\*\*S-\d+\*\*", text))),
        "S_resueltas": len(re.findall(r"\*\*S-\d+\*\* ✅", text)),
        "S_sin_definir": len(re.findall(r"\*\*S-\d+\*\* ⏳", text)),
        "R": len(set(re.findall(r"\*\*R-\d+\*\*", text))),
        "chars": len(text),
    }
    for f in fails:
        print(f"FAIL | {f}")
    print(("PASS" if not fails else f"FAIL ({len(fails)})") + " | conteos: " +
          ", ".join(f"{k}={v}" for k, v in counts.items()))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
