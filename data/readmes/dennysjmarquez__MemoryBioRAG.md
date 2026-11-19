# BioRAG — Memoria Cognitiva Biomimética y Simbólica para Agentes de IA

> **Versión del código en esta rama:** v36.0 (cierre técnico). La integración/publicación en `master` y el tag aún están pendientes.
> **Paradigma:** Motor Python + SQLite FTS5. **Sin embeddings densos, GPU ni llamadas a APIs externas** en el path de búsqueda.
> **Motor:** Arquitectura modularizada (18 submódulos `core/memory/` + 15 submódulos `core/mcp_server/` + fachada delgada) + SQLite FTS5 WAL + PPMI-SVD (100 dimensiones) + espacio semántico de 13 ejes + grafo sináptico Hebbiano + SDM (2048 bits) + calibración conforme + activación ACT-R + Concept Hubs + validación simétrica fail-fast de sustantivos clave + **neurona de reordenamiento que aprende sola** (29 señales → 6 ocultas → 1 corrección, con piso en la fórmula a mano) + **neurona asociativa cerrada de fábrica** (5 agujas → fuerza 0–1: ¿dos recuerdos tienen que ver?; examinada, aún no decide en el motor) + enlaces del agente intocables + **destino canónico del córtex en `~/.biorag/`** + **instalador de configuración MCP para clientes compatibles**.
> **Idiomas:** Español e inglés (stemming bilingüe, expansión simbólica con WordNet, Concept Hubs de 5 ángulos y Domain Dict).

**BioRAG** es una memoria simbólica persistente para agentes de IA que aborda la pérdida de contexto entre sesiones mediante recuperación híbrida. “Biomimética” describe una inspiración de diseño; no significa que el motor simule literalmente un cerebro humano. Los resultados de rendimiento se limitan a los benchmarks y snapshots indicados.

---

## 📊 Resultados históricos de la suite oficial (baseline v33.0 · 2026-10-14)

> **v34.0:** con una DB nueva, o sin campeón, la neurona no actúa y estos números se mantienen **idénticos** (son el piso). Con el campeón ya aprendido sobre la copia del snapshot (`despertar_neurona.sh`, 500 ciclos), la misma suite da **Recall@5 100.00 % · Recall@1 94.06 % (823/875) · MRR 0.964 · FP 0/40**, sin ninguna categoría por debajo del piso. Detalle en [La Neurona de BioRAG](#-novedades-de-la-versión-v340--la-neurona-de-biorag).
>
> **v35.0:** la QA oficial sale **idéntica** antes y después de todos los cambios de la v35 (Recall@5 100.00 % · Recall@1 91.89 % · MRR 0.950 · FP 0/40, misma máquina y semilla). Detalle en [La Neurona Asociativa](#-novedades-de-la-versión-v350--la-neurona-asociativa-sináptica).
>
> **Validación de v36.0 en copias temporales:** no se usó la DB viva. El recuento de pytest procede de una corrida aislada registrada previamente; la QA oficial se repitió sobre una copia fresca del snapshot durante esta revisión.
> - **Pruebas unitarias (registro previo):** `PYTHONHASHSEED=0 python -m pytest tests/` — 852 passed, 18 skipped (870 recopilados; 240.19 s), Python 3.11.2.
> - **QA oficial (re-ejecución aislada):** `bash scripts/run_qa_suite.sh --qa-only`, con `BIORAG_QA_GATE=1` y `PYTHONHASHSEED` sin fijar — 921 casos (875 de recuperación, 40 negativos y 6 ambiguos fuera del denominador global). R@5 **100.00% (875/875)**, R@1 **93.03% (814/875)**, MRR **0.9566**, FP **0/40**; `[GATE] OK` (719.53 s). El artefacto de esta corrida está en `scripts/qa_metrics.json`.
> - La copia medida no tenía un campeón de la neurona de ranking, así que esta no actuó. El archivo aislado `scripts/casos_fallidos.jsonl` contiene dos entradas de categoría `ambiguo`, aparte de las métricas globales de recuperación.
> - El snapshot de referencia es `snapshots/qa_escape_qcr_20260811.db` (SHA-256 `104dd2902aaf24c3ce93624492ea95a719acbdcca50f4f6bc123ac8317749796`); la QA se ejecutó sobre una copia temporal. La tabla siguiente conserva métricas históricas del baseline v33.0, no resultados de v36.0. La integración y el tag de v36.0 en `master` siguen pendientes.
>
> **Cada base tiene su propia neurona.** La neurona aprende con los recuerdos de la base donde vive y se guarda dentro de ella. Esta tabla mide una copia del snapshot oficial, que no trae neurona entrenada: por eso muestra la fórmula a mano sola (el pis

[...截断...]

o), aunque tu neurona esté trabajando en tu DB viva. La QA ahora lo dice antes de medir y nombra el parámetro para verla: `python scripts/evaluar_qa.py --con-neurona`. Detalle en [La neurona en la QA](#la-neurona-en-la-qa-cada-base-tiene-la-suya).

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
| **Casos ambiguos (contradictorios)** | **6 casos (2 con cobertura parcial)** | Evaluados por separado del Recall global; 2 casos no cubren al menos una de las etiquetas contradictorias. |
| **Pruebas unitarias de v36.0** | **852 passed · 18 skipped** | `PYTHONHASHSEED=0 python -m pytest tests/` en copia aislada (870 recopilados; 240.19 s; Python 3.11.2). Resultado registrado para el cierre. |
| **Smoke de Concept Hub (5 paráfrasis)** | **5/5 TOP-1** | Repetido sobre una copia aislada del snapshot oficial (851 nodos activos, 6 hubs y 30 puentes); evidencia focal, no sustituto de las pruebas de escala. |
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
> - **R@1 = 91.77% (803/875):** Refleja la pr