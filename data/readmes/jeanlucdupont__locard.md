# Locard Forensics - Local AI-Assisted Digital Forensics


# THIS PAGE IS A HOT MESS!
# THAT'S OK. LOCARD IS UNDER _HEAVY_ DEVELOPMENT
# I'LL CLEAN IT UP WHEN LOCARD IS IN A MORE STABLE PHASE


Long interactive operations use a shared delayed activity line (`⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏`):
advisory context/model waits, bounded investigation phases, guided evidence
discovery and CSV dumps. Animation starts after 300 ms and refreshes every 100 ms;
fast operations stay quiet. Existing ingestion file/record counters are preserved.
It clears before approval input and final output. Color-disabled sessions can
still animate on a capable terminal; redirected, JSON, paged and file output do
not animate. DEBUG logging disables animation to keep diagnostics readable.
See [bounded investigation diagnostics](docs/v4.md#budgets-and-termination).

|||
| :---: | :--- |
| <img width="60%" alt="image" src="https://github.com/user-attachments/assets/d98f7fa8-76a3-4d37-b796-9d2f9a27f28e" /><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Locard is a local Windows forensic investigation CLI, named after Edmond Locard and the principle that **every contact leaves a trace**.<br><br>Locard was designed around a foundational principle: **A forensic investigation should never require sending sensitive evidence to an external AI service.** To ensure trust and accuracy in the investigative process, Locard improves reliability through strict systemic safeguards rather than relying on LLM scale. It preserves source provenance, normalizes events into SQLite, retrieves evidence deterministically, and optionally asks MiniCPM5 through a local llama.cpp server to analyze retrieved records.<br><br>[Watch Locard's introduction video](https://youtube.com/shorts/UTP8ayRAmsk) <br><br><br><br><br><br><br><br>|


| Safeguard Mechanism | Description |
|---|---|
| Deterministic Extraction | Keeps the core evidence extraction process strictly deterministic. |
| Data Provenance | Preserves original evidence IDs and their sources throughout the analysis. |
| Context Bounding | Strictly limits and controls the context supplied to the model. |
| Citation Validation | Validates all citations made by the model to ensure they map to real evidence. |
| Clear Distinctions | Distinctly separates verifiable observations, correlations, and detections from AI-generated hypotheses and unknowns. |
| Execution Prevention | Strictly prevents the model from directly executing commands or querying the database. |


## Reminders

The bounded `investigate-ai` engine is assessed in [the investigation architecture
and safety review](V4.md), including its tool inventory, limits, privacy boundaries
and requirements for future reuse. The normal `!` interface supports advisory guidance and bounded investigation with per-tool approval.

For pre-model startup failures, enable the standard Python DEBUG logger
`forensic_assistant.investigation_ai`. It reports content-free phase timings,
remaining overall time and child-watchdog time. See the [startup diagnosis and
PowerShell acceptance commands](V4.md#664-startup-correction--pending-manual-acceptance).
Startup uses the remaining overall budget; it is not capped by the 45-second
tool-operation watchdog. Fingerprints still cover all authoritative case content.

`investigate-ai --max-seconds` uses one deadline, including local model calls,
worker startup, tools, transcript finalization and analyst approval 

[...截断...]

waiting.
Cancellation/timeout has an additional maximum five-second cleanup allowance.
Inspect the returned `termination`; command completion does not mean a supported
forensic conclusion. Interrupted runs explicitly mark their transcript incomplete.

Investigation transcripts default to `DATABASE.investigations`. They are sensitive
local **derived output, not evidence**: questions, model responses, evidence
excerpts, IDs and source metadata may be retained. `--transcripts` must name local
storage without traversal, symlinks or Windows reparse redirection. Use a directory
with appropriate analyst-controlled permissions; Locard does not change its ACLs.
Locard does not transmit transcripts externally. Analysts control retention and
deletion according to policy; there is no automatic deletion schedule.

Evidence establishes facts. Model output is analysis, not evidence. Locard is an
investigative aid, not a replacement for validation by a forensic analyst.

SEMANTIC SIMILARITY != FORENSIC EVIDENCE. RAG helps locate evidence; it does not create evidence.

<img width="523" height="359" alt="image" src="https://github.com/user-attachments/assets/a2c59b56-ed24-49d1-a8de-d3eaa55a14c9" />


## Locard V6

**WARNING: This project is not finalized**

The interactive CLI in V6 uses the existing V0-V5 forensic capabilities. Even though this project is its in Version 6, which is supposed to be its final form, there is still a **lot** left to be done. At this stage Locard is a solution that did not pass the test of running in a live environment. It's more like and advanced prototype.

<img width="1623" height="744" alt="image" src="https://github.com/user-attachments/assets/56802195-95b9-4f9d-8dbe-48ddc18ee59e" />

## Description
### Architecture and workflow

<img width="4152" height="2544" alt="locard-runtime (1)" src="https://github.com/user-attachments/assets/54524163-8c67-45b6-ba56-9e4eb93881e5" />

### MiniCPM
Locard relies on the **MiniCPM5-2B** base model, which was created and released by OpenBMB (an open-source AI project team backed by ModelBest and Tsinghua University's Natural Language Processing Laboratory).  [https://github.com/openbmb/minicpm](https://github.com/openbmb/minicpm)
<img width="510" height="269" alt="image" src="https://github.com/user-attachments/assets/d689307d-ddd5-42df-ba53-8a63d07339ad" />

MiniCPM5-2B is an incredible, highly optimized model. It packs capabilities typically reserved for much larger models (in the 4B–8B parameter range) into a lightweight 2.5B parameter footprint. This makes it perfectly designed for edge devices, laptops, and local agents. Despite its small size, MiniCPM5-2B punches well above its weight class. On benchmarking suites that measure tool calling, coding, and multi-step reasoning, it frequently matches or beats larger models like Qwen3.5-4B and Granite 4.2 3B, all while consuming a fraction of the VRAM.

By utilizing a small, efficient model like MiniCPM5-2B, Locard makes a fully local workflow practical. Analysts can run the system directly on their laptops without needing access to a massive GPU server. 

Locard does not need a massive general-purpose LLM because the AI is not responsible for uncovering the facts. The forensic facts are produced by deterministic parsers, database queries, correlation logic, and detection rules *before* the model is ever called. Locard deliberately prevents model intelligence from becoming part of the evidence chain, recognizing that simply increasing a model's size does not make its generated statements forensic evidence.

#### The Role of the AI Assistant

Locard does not ask the model to reconstruct an investigation from millions of raw events. Instead, deterministic retrieval and correlation reduce the case down to a small, bounded evidence bundle first.  The model serves as an analysis assistant layered on top of the forensic engine. **It is not the forensic engine itself.** 

| What MiniCPM DOES Do | What MiniCPM DOES NOT Do |
|---|---|
