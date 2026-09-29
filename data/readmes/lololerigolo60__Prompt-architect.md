PROMPT ARCHITECT PRO
=====================
A 100% local desktop app (Tkinter/CustomTkinter) that turns raw text or images
into structured prompts (subject, environment, style, lighting, technical),
stored in a local SQLite database. All AI processing runs through Ollama —
no data ever leaves your machine.


KEY FEATURES
------------

- Text Analysis (.txt)
  Splits a novel/script/notes file into blocks and runs a two-pass AI
  pipeline: semantic segmentation (splitting by scene/location) followed by
  JSON structuring of each detected segment.

- Image Analysis
  Analyze a single image or batch-scan an entire folder (recursively) using
  a vision model, extracting structured prompts in parallel.

- Book Context Injection
  Load a companion .txt file (summary, character/location sheets) that gets
  injected into the analysis passes to improve prompt consistency, without
  being analyzed itself.

- Hardware VRAM Profiles
  Auto-adjusts context size, generation length, and worker count based on
  your GPU (8GB to 32GB+ profiles, plus a fully manual Custom profile).

- Hybrid Mix Generator
  Randomly recombines existing prompt fields from the database into brand
  new creative prompts, without calling the AI again.

- Character Builder (Character tab)
  A dedicated tab for building a character from scratch. Choose fixed
  attributes via editable dropdowns (gender, age, animal hybrid, eye/skin/
  hair colour, hairstyle, accessory, body pose, facial expression) — every
  dropdown also accepts free-typed custom values for non-standard settings.
  Add two free-text drafts (clothing, style/aesthetic) that the LLM expands
  and combines with the chosen attributes into a single, ready-to-use
  character description. Result can be copied to clipboard or saved
  directly to the database as a new prompt.

- Database Editor (built-in)
  Search, browse, and edit stored prompts. Per-field AI regeneration
  ("Generate with AI" per field), ID-range deletion, and ID renumbering
  (reset gaps after deletions).

- Duplicate & Corruption Handling
  Automatically skips duplicate entries and rejects malformed/corrupted AI
  responses (invalid JSON, repetition, degeneration) before saving.

- VRAM Purge Between Blocks
  Unloads the model from Ollama between processing blocks to prevent memory
  buildup during long runs.

- Advanced Settings Panel
  Manually fine-tune num_ctx / num_predict for detection, structuring,
  vision, and field completion, plus block size and worker counts.


REQUIREMENTS
------------
- Ollama server running and reachable (default: http://localhost:11434,
  configurable in the app and persisted to settings_vram.json).
- No official Ollama Python client is used — all LLM calls go through plain
  HTTP requests (the `requests` library).
- Two API modes, switchable live in Advanced Settings:
    - "native" (default) -> /api/generate endpoint. Full access to
      Ollama-specific options (num_ctx, repeat_penalty, repeat_last_n,
      think, format=json...). Required for fine VRAM control.
    - "openai" -> OpenAI-compatible /v1/chat/completions endpoint. Useful
      for pointing at other backends (e.g. llama.cpp) exposing the same
      API. Limitation: num_ctx / repeat_penalty / repeat_last_n aren't
      part of that schema and are NOT sent in this mode (falls back to
      the model's default context).
- A text/structuring model (default: gemma4:31b) and a vision-capable
  model for image analysis — either the same model or two separate ones,
  selected independently in the sidebar.
- Python packages: customtkinter, Pillow (recommended), requests.


HOW TO RUN
----------
python prompt_architect.py
Opens a 1280x860 dark-themed window with two tabs: Analysis and Database.


LICENSE / DATA
---------------
100% local processing. No data sent over the internet.
SQLite database (WAL mode) with safe shutdown on window close.

