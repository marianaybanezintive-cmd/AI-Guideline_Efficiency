# Guía de criterio — cómo completar el PRD

Complementa [prd-template.md](prd-template.md) (estructura). Acá vive el *criterio* de un SR PO.

## 1. Análisis previo (antes de escribir)

Del input, extraer y anotar con su fuente: producto y cliente, objetivo de negocio,
fecha límite, alcance pedido (épicas/fases), actores, sistemas, restricciones impuestas
(tecnología, protocolo, terceros), backlog existente, estimaciones, riesgos declarados y
**contradicciones entre fuentes** (cada una → un H-n en §10 y una pregunta S-nn en §12.1).

## 2. La regla de corte (§1, §5)

El corte entre MVP y diferido se define por **un criterio binario y verificable**, no por
cantidad ni esfuerzo. Criterios útiles: efecto sobre el estado del sistema (leer vs
escribir), riesgo financiero/regulatorio de un defecto, volumen o criticidad de operación,
dependencia de terceros.
Ejemplo: «entra todo lo que *observa* sin modificar el estado del sistema externo; queda
fuera todo lo que crea, modifica o cancela».

Validar el corte con tres preguntas de sí/no que clasifiquen cualquier caso dudoso, y con
argumentos de «por qué no es arbitrario»: riesgo acotado, infraestructura difícil
ejercitada primero, ausencia de retrabajo. §5.2 baja la regla a una matriz por
elemento (mensaje, endpoint, evento, pantalla, job) con su épica y criterio.

## 3. Trazabilidad e IDs

| Prefijo | Dónde | Notas |
|---------|-------|-------|
| OBJ-n | §3 | Cada uno con verificación medible |
| RF-nn / RF-nn.m | §8 | Un requerimiento = una obligación verificable |
| RNF-nn | §9.3 | Con umbral numérico |
| H-n / O-n | §10 / §11 | Estables: no se renumeran entre versiones |
| S-nn | §12.1 | Marca de estado en la celda ID |
| R-n | §12.2 | Impacto Alto/Medio/Bajo |

Estados en §12.1: sin marca = abierta; `⏳ **SIN DEFINIR**` = consultada sin respuesta;
`✅ **RESUELTO dd-mm**` = cerrada (la propuesta pasa a describir la resolución y se refleja
en §1.bis). Referencias cruzadas con anclas Markdown (`[S-02](#12-riesgos-…)`).

## 4. Fidelidad al input

- Nada inventado: cifras, fechas, nombres, versiones y límites salen de las fuentes.
- Lo que el input no dice se escribe como supuesto (`⏳ a validar`) y se registra en §12.1.
- Citar la fuente al afirmar un hecho técnico (documento, sección o página).
- Usar el nombre real del cliente y del producto; nunca dejar «el cliente» pegado a una
  preposición ni restos de anonimización (`hacial cliente`).

## 5. Criterio por sección

- **§2:** el glosario explica los 2-4 términos del dominio que definen el corte.
- **§3:** un objetivo medible por cada capacidad crítica; métricas con «a validar» si no
  vienen del input; no-objetivos = lo que alguien podría asumir incluido.
- **§6:** cada épica del alcance con objetivo, duración, dentro/fuera, criterio de salida.
  Sin duración en el input: derivarla de la estimación o marcarla «a estimar».
- **§7:** de cada épica diferida, el cambio de naturaleza que la habilita y las
  dependencias que no existen todavía.
- **§8:** agrupar por capacidad del dominio (mínimo 3 grupos); cada RF rastreable a OBJ-n.
- **§10:** hallazgos de la documentación externa que cambian lo que asume el backlog o la
  propuesta; siempre con impacto y vínculo a su decisión.
- **§11:** buscar historias sin detalle, mal clasificadas, numeración inconsistente entre
  hojas, redacción con UI donde no hay UI, historias faltantes (errores, observabilidad,
  seguridad), estimación vs velocidad, roadmap incompleto, columnas corridas.
- **§12.3:** toda dependencia de terceros con fecha límite sugerida y épica que bloquea.
- **§13:** T0 y sprints de 2 semanas salvo que el input diga otra cosa; camino crítico,
  holgura y 3-5 acciones de sprint 0 ordenadas por urgencia. Sin fecha límite:
  «sin fecha comprometida» y plan por duración.
- **§14:** DoD verificable (cada ítem con medida, entorno o evidencia); cubre todos los OBJ.

## 6. Actualizar un PRD existente

Incrementar versión (major = cambia el corte; minor = nuevas definiciones o alcance),
completar «Actualizado», agregar la ronda en §1.bis, marcar S-nn resueltas, no renumerar
IDs. Guardar como archivo nuevo con la fecha del día (copia del anterior editada por
secciones); no pisar el anterior.

## 7. Chequeo final de calidad

- ¿Todo RF cae del lado correcto del corte de §5?
- ¿Cada H-n tiene decisión asociada y cada S-nn tiene propuesta accionable?
- ¿§14 verifica todos los OBJ-n? ¿Los supuestos ⏳ están en §12.1?
