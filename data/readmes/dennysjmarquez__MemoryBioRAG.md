# BioRAG — Memoria Cognitiva Biomimética y Simbólica para Agentes de IA

> **Versión Oficial:** v35.0
> **Paradigma:** Motor Python + SQLite FTS5. **Sin embeddings densos, GPU ni llamadas a APIs externas** en el path de búsqueda.
> **Motor:** Arquitectura modularizada (18 submódulos `core/memory/` + 15 submódulos `core/mcp_server/` + fachada delgada) + SQLite FTS5 WAL + PPMI-SVD (100 dimensiones) + espacio semántico de 13 ejes + grafo sináptico Hebbiano + SDM (2048 bits) + calibración conforme + activación ACT-R + Concept Hubs + validación simétrica fail-fast de sustantivos clave + **neurona de reordenamiento que aprende sola** (29 señales → 6 ocultas → 1 corrección, con piso en la fórmula a mano) + **neurona asociativa cerrada de fábrica** (5 agujas → fuerza 0–1: ¿dos recuerdos tienen que ver?; examinada, aún no decide en el motor) + enlaces del agente intocables.
> **Idiomas:** Español e inglés (stemming bilingüe, expansión simbólica con WordNet, Concept Hubs de 5 ángulos y Domain Dict).

**BioRAG** es una memoria simbólica persistente para agentes de IA que aborda la pérdida de contexto entre sesiones mediante recuperación híbrida. “Biomimética” describe una inspiración de diseño; no significa que el motor simule literalmente un cerebro humano. Los resultados de rendimiento se limitan a los benchmarks y snapshots indicados.

---

## 📊 Métricas de la suite oficial (v33.0 · 2026-10-14 · vigentes en v34.0)

> **v34.0:** con una DB nueva, o sin campeón, la neurona no actúa y estos números se mantienen **idénticos** (son el piso). Con el campeón ya aprendido sobre la copia del snapshot (`despertar_neurona.sh`, 500 ciclos), la misma suite da **Recall@5 100.00 % · Recall@1 94.06 % (823/875) · MRR 0.964 · FP 0/40**, sin ninguna categoría por debajo del piso. Detalle en [La Neurona de BioRAG](#-novedades-de-la-versión-v340--la-neurona-de-biorag).
>
> **v35.0:** la QA oficial sale **idéntica** antes y después de todos los cambios de la v35 (Recall@5 100.00 % · Recall@1 91.89 % · MRR 0.950 · FP 0/40, misma máquina y semilla). Detalle en [La Neurona Asociativa](#-novedades-de-la-versión-v350--la-neurona-asociativa-sináptica).
>
> **Cada base tiene su propia neurona.** La neurona aprende con los recuerdos de la base donde vive y se guarda dentro de ella. Esta tabla mide una copia del snapshot oficial, que no trae neurona entrenada: por eso muestra la fórmula a mano sola (el piso), aunque tu neurona esté trabajando en tu DB viva. La QA ahora lo dice antes de medir y nombra el parámetro para verla: `python scripts/evaluar_qa.py --con-neurona`. Detalle en [La neurona en la QA](#la-neurona-en-la-qa-cada-base-tiene-la-suya).

Evaluación sobre el snapshot congelado oficial canónico (**921 casos totales en suite QA**):
- **Archivo:** `snapshots/qa_escape_qcr_20260811.db`
- **SHA-256:** `104dd2902aaf24c3ce93624492ea95a719acbdcca50f4f6bc123ac8317749796` (Git blob `ecc15b7513ff6ddd1356e934a0aa13821337bca4`).
- **Composición del dataset:** **875 consultas de recuperación** evaluadas para Recall y MRR, **40 controles negativos** evaluados para tasa de falsos positivos, y **6 casos ambiguos** (consultas con etiquetas contradictorias) analizados por separado fuera del denominador de recuperación global.

| Métrica | Resultado observado | Contexto y Significado Científico |
|---|---:|---|
| **Recall@5 global** | **100.00% (875/875)** | **100% de cobertura en ventana de trabajo**: todo recuerdo gold ingresa al Top-5 del agente sin fallos de recuperación (0 fallos). |
| **Recall@1 (Top-1)** | **91.77% (803/875)** | **Precisión de primer resultado**: 803 de 875 casos quedan en primer lugar directo (métrica complementaria observada en benchmark). |
| **MRR (Mean Reciprocal Rank)** | **0.950** | Posición recíproca promedio ponderada (0.9497 sin redondear; métrica complementaria observada). |
| **Falsos positivos** | **0/40 (0.00%)** | Calibración conforme efectiva en los 40 controles negativos del benchmark (FP rate observada 0.00%). |
| **Casos ambiguos (

[...截断...]

contradictorios)** | **6 casos (2 con cobertura parcial)** | Evaluados por separado del Recall global; 2 casos no cubren al menos una de las etiquetas contradictorias. |
| **Tests unitarios** | **430/430 aprobados** (v35.0) | Cobertura completa de invariantes, validación pre-DB fail-fast, contratos MCP, normalización, catálogo, las 18 capas de protección de la neurona, el script de despertar, la neurona asociativa, los enlaces del agente intocables y el MCP sin sugerencias de enlace. |
| **Suite Concept Hub** | **5/5 TOP-1 (100.00%)** | Precisión perfecta en los 5 casos de prueba de puentes asociativos registrados. |
| **Abismo léxico (EXP-Q)** | **3/3 Pool · 2/3 Top-5 · 1/3 Top-1** | 3/3 descubiertos en pool de grafo; 2/3 en Top-5 (pos #1 y #4) y 1/3 en Top-1 (pos #1). |
| **Sinónimos · Recall@5 / Recall@1** | **100% (55/55) / 56.36%** | Cobertura total en Top-5; el 43.64% restante queda entre Top-2 y Top-5. |
| **Por tema · Recall@5 / Recall@1** | **100% (65/65) / 63.08%** | Cobertura total en Top-5; ordenamiento Top-1 guiado por Jaccard y PPMI-SVD (MRR: 0.772). |
| **Pregunta natural · R@5 / R@1** | **100% (65/65) / 93.85%** | Alta precisión Top-1 en formulaciones conversacionales. |
| **Cruce de idioma · R@5 / R@1** | **100% (8/8) / 62.50%** | Rescate bilingüe en Top-5; Top-1 asistido por WordNet y Concept Hubs. |
| **Smoke multicampo en DB local** | **Objetivo #2 → #1** | Promoción de `version_actual_biorag` de #2 a #1 por convergencia multicampo. |
| **Tiempo de la evaluación global** | **~877 s** | Ejecución determinista de la suite QA de 921 casos en CPU local (sin GPUs ni APIs). |

> **Aclaración Metodológica — Umbrales de Gate vs. Métricas Observadas:**
> - Los **umbrales formales del Gate** de calidad (`_evaluar_gate()` en `scripts/evaluar_qa.py`) exigen: Recall@5 $\ge$ 97.0%, Fallos $\le$ 24, Tasa de Falsos Positivos $\le$ 15.0%.
> - **Recall@1 (91.77%)** y **MRR (0.9497)** son métricas complementarias observadas en el benchmark sobre este corpus congelado, no umbrales que el gate imponga ni garantías universales para cualquier consulta arbitraria.
> - **R@5 = 100.00% (875/875):** Demuestra empíricamente que el conjunto híbrido (FTS5 BM25 + Sustantivos Clave + Grafo Sináptico Hebbiano + PPMI-SVD + Concept Hubs + Reranker Multicampo) logra **cobertura completa (875/875) dentro de la ventana Top-5 de trabajo del agente en este corpus evaluado**.
> - **R@1 = 91.77% (803/875):** Refleja la precisión exacta del primer candidato. En tareas con solapamiento léxico directo (`literal`, `pregunta_natural`), R@1 supera el 95%–99%. En tareas donde el vocabulario difiere radicalmente (`sinonimo` 56.36%, `por_tema` 63.08%), el sistema ubica el recuerdo dentro del Top-5 pero no siempre en Top-1. R@1 representa el área de optimización continua para el desempate fino sin embeddings densos.

---

## 🧬 Novedades de la Versión v35.0 — La Neurona Asociativa (sináptica)

<p align="center">
  <img src="docs/Mi%20neurona%20en%20el%20sistema/imagenes/neurona_asociativa_biorag.jpg" alt="La neurona asociativa de BioRAG: un cuerpo dentro de la silueta de un hipocampo, cinco dendritas que tocan dos recuerdos y un puente de luz que nace entre ellos" width="100%">
</p>
<p align="center"><em>La neurona asociativa de BioRAG (ilustración). El cuerpo vive dentro de la silueta de un hipocampo, la parte del cerebro que decide qué se une con qué. Sus cinco dendritas (oro: el texto; celeste: el tiempo; verde: las etiquetas) tocan dos recuerdos. Arriba nace la sinapsis entre ellos. Los hilos grises del fondo son las conexiones con ruido que la neurona sabe reconocer.</em></p>

> **En una frase:** BioRAG ya tiene su **segunda neurona**. Mira dos recuerdos y responde una sola pregunta: **¿de verdad tienen que ver?** Nace calibrada de fábrica, no aprende de tu memoria, decide en tiempo constante y **ya está examinada**, también por una persona a mano.

**Estado honesto al cerrar la v35.** La neurona está **construida, calibrada, examinada y cerrada**, pero 