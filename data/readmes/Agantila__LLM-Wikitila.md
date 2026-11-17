# LLM-Wikitila

**Schnelle, belegte Suche + lokaler Wissensgraph für jeden Projekt-Ordner** — ohne Vector Store, ohne Cloud, ohne Modell im Laufzeitpfad.

LLM-Wikitila macht einen Projekt-Ordner (Second Brain, Dokumentations-Ordner, Markdown-Vault) in Sekunden durchsuchbar und liefert **belegte Aussagen statt bloßer Fundstellen**: Datei, Überschrift und Originalpassage, mit Authority-, Ablösungs- und Gültigkeits-Prüfung. Ein optionaler lokaler Wissensgraph (Graphify + kleines lokales Modell) ergänzt Navigation und Querbezüge — er ist nie die Belegquelle.

> English version: [README.en.md](README.en.md)

## Belegte Vorteile (gemessen)

| Vorteil | Messwert |
|---|---|
| Trefferquote | **R@10 1,00** auf einem 50-Fragen-Katalog; `graphify query` (Graph-RAG) erreicht 0,25 |
| Geschwindigkeit | ~20 ms je Suche, deterministisch, kein Dienst, keine GPU |
| Beleg statt Behauptung | Originalpassage + Zitat statt Graph-Zusammenfassung |
| Gültigkeit statt Relevanz | Authority-Register löst ab, welche Quelle maßgeblich und noch aktuell ist |
| Kontrolliertes „nicht belegt“ | Signale für fehlendes Wissen statt plausibler Falschantwort |
| Kein Vector Store nötig | SQLite FTS5/BM25 reicht; Embedding ist messbar überflüssig |
| Kein Modell im Laufzeitpfad | Decision-Modelle verschlechterten Ranking und Antwort-Tor gemessen |

Details und Messgrenzen: [docs/benefits.de.md](docs/benefits.de.md) · [docs/validation.de.md](docs/validation.de.md)

## Schnellstart

```bash
# 1. In einem Projekt-Ordner einrichten (idempotent)
./install.sh /pfad/zum/projekt-ordner

# 2. Suchen (rund 20 ms)
python3 wikitila.py --root /pfad/zum/projekt-ordner search "Wie hoch ist der Preis?" -k 5

# 3. Coverage und Aktualität prüfen
python3 wikitila.py --root /pfad/zum/projekt-ordner manifest
python3 wikitila.py --root /pfad/zum/projekt-ordner check
```

Jede Antwort trägt `answer_status` (`belegt` · `widersprüchlich` · `belegt_gueltigkeit_unbestaetigt` · `nicht_belegt`), Flags wie `kanonisch` / `überholt durch` / `veraltet` und die Originalpassagen (`passages`).

## Installation

Für Menschen: [docs/installation.de.md](docs/installation.de.md) — Voraussetzungen, Schritt für Schritt, Fehlerbehebung.
Für KI-Agenten: [docs/agentic-setup.de.md](docs/agentic-setup.de.md) — Installation, Nutzung, Antwortvertrag und Pflege-Regeln für Agenten (Englisch: [docs/agentic-setup.en.md](docs/agentic-setup.en.md)).

## Was mitgeliefert wird

```
LLM-Wikitila/
├── wikitila.py                # Hauptwerkzeug: build · search · status · manifest · check · eval · embed
├── wikitila_graph.py          # optional: lokale Graphify-Extraktion (Ollama, ohne Thinking)
├── validate_catalog.py        # Validierung gegen einen Fragenkatalog (3 Messebenen)
├── test_wikitila.py           # 32 Unit-Tests (synthetischer Korpus, ohne Netz/Ollama)
├── install.sh                 # Installer für einen Ziel-Ordner
├── config.example.toml        # Beispielkonfiguration (→ wikitila.toml)
├── authority_register.example.json  # Vorlage für das Authority-Register
├── golden_catalog.example.jsonl     # Vorlage für den Fragenkatalog
├── AGENTS.md                  # Arbeitsanweisung für KI-Agenten (Entwicklung, Gates, Memory, PM)
├── CLAUDE.md                  # Verweis auf AGENTS.md für Claude Code
├── CHANGELOG.md               # Versionshistorie
├── examples/demo-corpus/      # Synthetischer Mini-Ordner zum Beispielkatalog (CI-Validierung)
├── pm/                        # Projektmanagement: Status, Backlog, Roadmap, Pläne, ADRs, Memory, Sitzungen
├── .github/                   # CI (Tests + Demo-Validierung), Dependabot, Issue-/PR-Vorlagen
├── skills/llm-wikitila/       # Skill für KI-Agenten (mit Referenz)
├── diagrams/                  # Stack-Kompositions-Diagramm (PNG + editierbares .excalidraw)
├── review/                    # Review-Metaprompt (DE + EN) und Review-Berichte
└── docs/                      # Dokumentation (deutsch + englisch)
```

## Stack-Komposition

![LLM-Wikitila Stack-Komposition](diagrams/stack-komposition.png)

Quelle: [diagrams/stack-komposition.excalidraw](diagrams/stack-komposition.excalidraw) — editierbar unter [excalidraw.com](https://excalidraw.com) (Datei per Drag-and-Drop öffnen); neu erzeugen mit `diagrams/generate_diagram.py`. Beschreibung der Komponenten: [docs/architecture.de.md](docs/architecture.de.md).

## Abhängigkeiten

| Baustein | Anforderung | Pflicht? |
|---|---|---|
| Python | **≥ 3.11** (Standardbibliothek reicht für die Suche) | ja |
| SQLite mit FTS5 | in Python ≥ 3.11 enthalten | ja |
| Ollama + `maternion/ling-3.0-tiny:8b` | nur für den Wissensgraphen | optional |
| Graphify-Paket (`pip install graphifyy==0.4.16 networkx==3.6.1`) | nur für den Wissensgraphen | optional |
| `embeddinggemma:latest` (Ollama) + `numpy` | nur für optionales Embedding | optional |

Kein Docker, kein Vector-Store-Dienst, keine Cloud. Der Suchindex liegt als eine SQLite-Datei im Ziel-Ordner (`.wikitila/index.db`).

## Dokumentation

| Thema | Deutsch | English |
|---|---|---|
| Installation | [docs/installation.de.md](docs/installation.de.md) | [docs/installation.en.md](docs/installation.en.md) |
| Architektur | [docs/architecture.de.md](docs/architecture.de.md) | [docs/architecture.en.md](docs/architecture.en.md) |
| Authority-Register | [docs/authority-register.de.md](docs/authority-register.de.md) | [docs/authority-register.en.md](docs/authority-register.en.md) |
| Betrieb & Pflege | [docs/operations.de.md](docs/operations.de.md) | [docs/operations.en.md](docs/operations.en.md) |
| Validierung | [docs/validation.de.md](docs/validation.de.md) | [docs/validation.en.md](docs/validation.en.md) |
| Belegte Vorteile | [docs/benefits.de.md](docs/benefits.de.md) | [docs/benefits.en.md](docs/benefits.en.md) |
| Agentische Installation | [docs/agentic-setup.de.md](docs/agentic-setup.de.md) | [docs/agentic-setup.en.md](docs/agentic-setup.en.md) |

## Lizenz

[MIT](LICENSE) — offen und kommerziell nutzbar. Entwickelt von AGANTILA als LLM-Wiki-Erweiterung mit Graphify und belegtem Evidenz-Vertrag.
