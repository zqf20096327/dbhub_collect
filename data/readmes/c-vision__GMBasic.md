# GMBasic

> **AI-powered BASIC — four independent backends, native database engines, a built-in LLM model compiler (quantization + training), SDL2 graphics, full TUI.**
>
> BASIC with 500+ built-in functions, executed by four independent backends (a P-Code VM in C#,
> IL/NativeAOT, a C virtual machine, a C99 transpiler), SDL2 GPU-accelerated graphics, **six
> embedded database engines — ISAM, DBF/xBase, SPEED, LEDGER, SQLite, VectorDB — with native C
> implementations for the C backends**, and a complete **local-AI stack**: agents with tool-calling,
> MCP server and 52 connectors, RAG and knowledge graphs (installable *brains*), a **model compiler
> with per-tensor quantization** (`q2_k…q6_k`, `q4_0`/`q8_0`, `iq1_s`/`iq2_*`/`iq3_*`, `mxfp4`,
> `nvfp4`, `f16`/`bf16`, activation quantization, imatrix, QuantIR, MLX↔GGUF conversion) and
> **training** (fine-tune, LoRA, distillation, DPO/GRPO, eval gates) — plus a true-color
> Clipper-compatible TUI (20+ controls), HTTP/WebSocket server, linear algebra, statistical
> analysis, trading/finance, and a full networking stack.

**Repository:** [github.com/c-vision/GMBasic](https://github.com/c-vision/GMBasic)

## Install from a release (no build)

Releases ship a **ready-to-run archive** per RID (currently `osx-arm64`): compilers, runtime,
headers, `LLMEnv` (Apache-2.0) and settings. No .NET required; `cc` (Xcode Command Line Tools)
is needed to compile programs.

```sh
unzip gmbasic-1.0.0-osx-arm64.zip
cd gmbasic-1.0.0-osx-arm64
export PATH="$PWD/bin:$PATH"

gmb doctor              # 18/18 ok
gmb doctor --verify     # checks EVERY file against release-manifest.json (sha256)
gmb eval "PRINT 40+2"   # 42
gmb hello.bas           # build + run of a program
```

The archive is verified **before** publishing: `sha256sum -c *.sha256`, `gmb doctor`,
`gmb doctor --verify`, `gmb eval`, a textual program built and executed, `IMPORT AI` compiled,
and `otool -l` reporting **zero** absolute paths. What is inside, what is not, and the limits:
`RELEASE-NOTES-1.0.0.md`.

## Repository layout

**One repository, no submodules:** `git clone` is enough, `--recurse-submodules` is not needed.
The folders are domains, not separate repos:

| Folder | Contents |
|---|---|
| `GMBasic/` | **C** compiler and runtime: frontend, C99Native, VM/C, shared runtime, native libraries |
| `GMBasicSharp/` | **C#** compiler and runtime: lexer/parser/linker, IL backend, StdLib, REPL/CLI |
| `shared/` | material shared by both: MiniTests, samples, spec/registry, settings, skills, plugins |
| `tools/` | tooling (BASIC/C/shell) at the repo root, shared by both worlds |

The two IDEs (`GMBasicIDE/` — native macOS GUI, VB6-style; `GMBasicTuiIDE/` — TUI written in BASIC)
are **in development and are not part of this repository** for now: they are excluded until
complete. The REPL's own TUI (`IDE` command: `REPL/ide.c`, shared logic in `gmb_runtime_c/src/gmb_ide.c`) **is** in the repo,
because it is part of the canonical C REPL.

Two things are deliberately **outside** this repository and are never cloned as submodules:
the LLM engine [`c-vision/LLMEnv`](https://github.com/c-vision/LLMEnv) (built and cached as native
libraries — see [LLM engine](#llm-engine--the-llmenv-sibling-repository)) and the **data** repos
[`GMBasicModules`](https://github.com/c-vision/GMBasicModules) /
[`GMBasicBrains`](https://github.com/c-vision/GMBasicBrains) (release assets downloaded on demand —
see [Download](#download-what-which-command-where-it-lands)).

## Download: what, which command, where it lands

Large data is **not in git**. The code lives here; native libraries, market feeds and brains live
in the **releases** of two companion repos and are downloaded **only when needed** (resumable,
**sha256 verified** before extraction).

| repo | visibility | what you find there |
|---|---|---|
| **`c-vision/GMBasic`** | public | this monorepo: compilers, runtime, samples, tools |
| **`c-vision/GMBasicModules`** | public | **binaries and data**: native libraries (one release per group), market feeds (`fixtures-v1`), ML/Chromium/OCR components |
| **`c-vision/GMBasicBrains`** | private | **brains** (Second Brain): RAG and knowledge graph, shipped as release assets |

The other two repos never need to be cloned: the commands below fetch from their releases. The
whole administrative surface is **C** (there is no C# CLI any more); the **interactive REPL is the
C binary** `REPL/build/gmbrepl` (see `REPL/README.md`).

### Build from a checkout (order matters)

```sh
# 1. runtime C: statiche + dylib (BASE di tutto il resto)
cmake -S GMBasic/native/gmb_runtime_c  -B GMBasic/native/gmb_runtime_c/build  && cmake --build GMBasic/native/gmb_runtime_c/build
# 2. compilatore nativo (produce bin/gmb)
cmake -S GMBasic/native/gmb_compiler_c -B GMBasic/native/gmb_compiler_c/build && cmake --build GMBasic/native/gmb_compiler_c/build --target gmb
# 3. CLI amministrativo (pkg/libs/brain/doctor) — richiede il passo 1
cmake -S GMBasic/native/gmbadmin -B GMBasic/native/gmbadmin/build && cmake --build GMBasic/native/gmbadmin/build
# 4. VM/C: gmb_vm_host (+ libgmb_eval/libgmb_bsp per EVAL, REPL, notebook)
cmake -S GMBasic/native/gmb_vm_c -B GMBasic/native/gmb_vm_c/build && cmake --build GMBasic/native/gmb_vm_c/build

export PATH="$PWD/bin:$PATH"
gmb doctor --fix          # installa LLMEnv (serve per compilare) e le librerie mancanti
gmb eval "PRINT 40+2"     # 42
```

Il passo 1 **deve** precedere il 3: `gmbadmin` include `gmb_runtime_c` e senza la sua build dir
fallisce con «build dir assente». `gmb doctor` elenca cosa manca e con quale comando produrlo;
`gmb doctor --fix` scarica LLMEnv (Apache-2.0, repo separato) e le librerie native.
Su macOS il compilatore C è `cc`; sulle altre piattaforme `zig` (vedi `tools/sh/zcc`).

### First time — the four commands that actually matter

```sh
gmb libs ensure                 # missing native libraries
gmb fixtures ensure             # market feeds for the samples
gmb brain login --github        # once: GitHub token (scope "repo") for the private GMBasicBrains
gmb brain install brainvault    # download + install + register (sha256 verified)
```

`ensure` downloads **only what is missing**, so you can re-run it whenever you like.

### What it downloads, with which command, and where it puts it

| item | command | destination |
|---|---|---|
| **native libraries** | `gmb libs ensure` (`status`, `check`, `prune`) — also automatic on first use of a function that needs one | `~/.gmbasic/libs/<rid>/` (in a development checkout the freshly built `GMBasic/build/libs/<rid>/` wins) |
| **external components** (torch/ML, Chromium, Obscura, OCR) | `gmb setup TORCH` · `BROWSER` · `OBSCURA` · `OCR` · `ALL` (or automatic on first use) | `~/.gmbasic/libs/<component>/<rid>/` |
| **market feeds** (`markets`, `option_chains`, `rates`, `darkpool`) | `gmb fixtures list` · `ensure` · `pull markets` | `shared/samples/Fixtures/<name>/` — the **only** place, no symlinks |
| **brains** (RAG and/or graph) | `gmb brain install <name[@ver]>` · `list` · `remove` (from BASIC: `AI BRAIN INSTALL "name"`) | `~/.gmbasic/brains/<name>/<version>/{rag,graphs}` |
| **packages** with external dependencies | `gmb pkg install <name[@ver]>` · `gmb restore` · `gmb update` | `~/.gmbasic/packages` (client) · `<checkout>/packages` (development) · `<exe>/packages` with `--local` · `vendor/` for pins |
| **skill/plugin marketplaces** | `AI SKILLS MARKETPLACE "url"` · `AI PLUGINS MARKETPLACE "url"` | `~/.gmbasic/{skills,plugins}-marketplaces` |

**What is NOT downloaded:** skills, plugins and settings live in the repo (`shared/skills`,
`shared/plugins`, `shared/settings`). When you compile a program, the **bundle** next to the
executable carries only what is needed: minimal settings, `Resources/`, the declared brains
(`<exe>.brains.txt`), the libraries actually used (`<exe>.libs.txt`), the **providers**
(`config/providers.json`, always) and — **only when declared** in the program's `app.settings.json`
— `skills`, `plugins` and extra config files:

```json
{ "brains": ["brainvault"], "fixtures": ["markets"], "skills": ["board"], "plugins": ["web-fetch"], "config": ["mcp.json"] }
```

### Where the state lives (and what never goes into git)

- **`REPL/`** — la REPL unica (in C) e i suoi `helps/*.json`.
- **`~/.gmbasic/`** — per-user data root: `libs/`, `brains/`, `packages/`, `skills-marketplaces/`,
  `plugins-marketplaces/`, `github.token` (`chmod 600`).
- **`GMBasic/config/`** (or `<exe>/config` in a distributed program) — **local state**: active
  providers, MCP servers, installed brains, skill/plugin indexes. **Never in git**: it holds
  machine-specific paths. If a file is missing, the runtime falls back to the **seed** in
  `shared/settings/` or to the defaults in the code.
- **`shared/samples/Fixtures/`** — the feeds, and nothing else.

## LLM engine — the LLMEnv sibling repository

The local-LLM engine is **not** in this repository. It lives in the **public** repo
**`c-vision/LLMEnv`** — *"Inference engine for local LLMs on Apple Silicon: MLX and GGUF back ends,
model codecs, tokenizers and chat templates. The engine behind FastLLM."*

GMBasic consumes it as a **sibling checkout**, not as a submodule and not as a copy:

```
../LLMEnv/            ← $LLMENV (default: ~/Documents/Projects/LLMEnv)
  LLMEngine/          MLX and llama.cpp/GGUF back ends, MoE streaming, plugin ABI (llmengine.h)
  LLMCodec/           dequant + shared quantize helpers, GGUF/safetensors containers
  LLMToken/ LLMDesc/  tokenizers, chat templates (jinja), model descriptors/arch tables
```

How the pieces connect:

| step | what happens |
|---|---|
| **build** | `LLMEnv/tools/build_ai_libs.sh` builds the engine (`cmake -DLLMENV_BUILD_ENGINE=ON`, artifacts in `LLMEnv/build/dist/<rid>/`); GMBasic's packaging step then installs them into the user cache as `libgmb_ai_mlx`, `libllm_ai_llamacpp`, `libllmtoken`, `libllmengine_moe_stream`, … |
| **use** | the C runtime and the C# backends load them from `~/.gmbasic/libs/<rid>/` (C# via **P/Invoke**; the C side links them). The ABI contract is verified by [`shared/runtime-abi`](shared/runtime-abi/README.md): `gmb_ai_mlx`, `llm_ai_llamacpp`, `llmtoken`, `llmengine_moe_stream`, `gmb_ai_llm`, `gmb_ai_modelio` |
| **CI** | `.github/workflows/libs.yml` clones it through the `LLMENV_REPO` variable (`c-vision/LLMEnv`) or uses a prebuilt `LLMENV_DIR` |

**License boundary (do not break it).** LLMEnv is **Apache-2.0** and must stay
*inference-complete*: it loads and runs models. Everything that **produces or alters weights**
(training, LoRA, quantization encode, model compiler/surgery, MLX↔GGUF conversion) lives in
[`GMBasic/gmbllm/`](GMBasic/gmbllm/README.md) under the **PUL** license. The dependency is
one-way — **`gmbllm` → LLMEnv**, never the reverse — and `LLMEnv/tools/gmb_license_gate.py` must
exit 0 after touching LLM code.

Get it next to this checkout:

```sh
git clone https://github.com/c-vision/LLMEnv ../LLMEnv
bash ../LLMEnv/tools/build_ai_libs.sh          # engine → ~/.gmbasic/libs/<rid>/ (via GMBasic packaging)
```

## Build & run

```sh
dotnet build GMBasicSharp/GMBasicSharp.slnx
```

Three separate programs, one job each:

| program | what it is |
|---|---|
| `REPL/build/gmbrepl` | **the REPL** and runner of the C world (canonical): `RUN`, `EVAL`, `AST`, `DASM`, `COMPILE`, `IDE`, packages/fixtures. No dependency on the C# world. |
| `GMBasicSharp/CompilerCli` → `gmbcs` | **headless CLI of the C# engine**: `check`, `dump ast\|pcode\|il\|disasm`, `build --target il\|pcode`, `run`/`eval --engine il\|pcode`, `debug`. |
| `GMBasic/native/gmbadmin` → `gmbadmin` | **administrative CLI in C** (front end: `gmb`): packages, brain/toolchain, libs, setup, daemon, rag/graph, grep, hf/mlx. |
| `Notebook/build/gmbnotebook` | **notebook server** (C): a stateful BASIC session over HTTP on 127.0.0.1 (`/execute`, `/vars`, `/reset`). |

One block per engine:

```sh
# PCodeVM — P-Code executed in-process by a C# VM (no native code)
dotnet run --project GMBasicSharp/CompilerCli -- run --engine pcode <file.bas>

# IL — .NET IL, managed JIT
dotnet run --project GMBasicSharp/CompilerCli -- run --engine il <file.bas>
dotnet run --project GMBasicSharp/CompilerCli -- build --target il <file.bas>

# VM/C — the SAME P-Code in the C VM (external gmb_vm_host, driven by the C REPL)
cmake -S GMBasic/native/gmb_vm_c -B GMBasic/native/gmb_vm_c/build && cmake --build GMBasic/native/gmb_vm_c/build
REPL/build/gmbrepl <file.bas>
dotnet run --project tools/runners/GMBASIC.Conformance -- vmtest <file.bas>

# C99Native — C front end + C emitter, `cc` against the shared C runtime, no VM.
# The script cds into GMBasic/ itself, so sample paths are relative to GMBasic/ (../shared/...):
bash tools/sh/gmb_c99native_run.sh ../shared/samples/Network/WebSocketEcho.bas

# All engines on the same sample, comparing the normalized output
zsh tools/sh/parity4 ../shared/samples/Ai/AiPlugins.bas
```

> NativeAOT (`-n`) is **not** in `gmbcs` yet: the canonical native path is the C compiler
> (`gmb build --project <dir>`). Reintroducing `-n` in `gmbcs` is tracked in `TODO.md` §6 (F4c).

## Architecture

One **C# front end** produces P-Code; from there execution forks into **four independent
backends**. C99Native is the exception on the left side: it has its own **C front end** and
emits C, so it never touches the C# front end.

```
C# front end:  Lexer → Parser → Linker → Compiler → P-Code
                                                      ├─ PCodeVM    (C#, in-process)
                                                      ├─ IL         (C#, .NET IL)
                                                      └─ VM/C       (C, gmb_vm_host — same P-Code)

C front end:   .bas → Lexer/Parser → C99 emitter → cc → native executable   (C99Native)
```

| Backend | Written in | How it runs | Invocation |
|---|---|---|---|
| **PCodeVM** | C# | P-Code executed in-process by a C# VM | `gmbcs run --engine pcode` |
| **IL** | C# | .NET IL, managed JIT | `gmbcs run --engine il` |
| **VM/C** | C | the **same P-Code** in a C VM, external process | `gmbrepl`, `gmbchunk` + `gmb_vm_host` |
| **C99Native** | C | `.bas` → C99 → `cc`; no VM, no bytecode | `gmb` (default), `gmbnative` |

PCodeVM and VM/C execute **the same P-Code**: that is the semantic contract the parity suite
checks (`tools/sh/parity4`). C99Native has its own C front end and emitter, so it does not go
through the C# front end at all. VM/C and C99Native share the same C runtime library
(`GMBasic/native/gmb_runtime_c/`): no duplicated built-in implementations between them.

## Clipper-style forms: `@ SAY` / `@ GET` / `READ`

The Clipper screen model is intact: `@ row, col SAY` writes, `@ row, col GET` declares an input
field, and a single `READ` activates **every field declared since the previous `READ`** (the
Clipper "get list"), then applies the edited values back to the variables. Commands take **no
parentheses**; the qualifiers are keywords.

```basic
IMPORT CONSOLE

SUB Main()
  DIM nameVal AS STRING
  DIM ageVal AS INTEGER
  DIM activeVal AS INTEGER

  nameVal = "John" : ageVal = 30 : activeVal = 1
  @ 3, 5 SAY "Name:"    @ 3, 15 GET nameVal   TYPE "C" PICTURE "@!"
  @ 4, 5 SAY "Age:"     @ 4, 15 GET ageVal    TYPE "N" MIN 0 MAX 120 STEP 1
  @ 5, 5 SAY "Active:"  @ 5, 15 GET activeVal TYPE "K" CAPTION "Active"
  READ

  PRINT "name="; nameVal; " age="; ageVal; " active="; activeVal
END SUB
```

| clause | meaning |
|---|---|
| `TYPE "C"` / `"N"` / `"K"` / `"D"` | text, number, checkbox, date |
| `PICTURE "@!"` | Clipper picture: `@!` uppercase, `999.99` numeric mask |
| `MIN` / `MAX` / `STEP` | numeric bounds |
| `CAPTION` | label of the widget |
| `ITEMS {…}` / `ITEMS […]` | listbox / combobox choices |
| `SIZE w[, h]` | field size |
| `WHEN expr` | the field is **skipped** while false: no focus, no key wait |
| `VALID expr` | re-prompts until the expression is true |

The **same code** works in pixel graphics: `SCREEN 12` turns the get list into real widgets
(text, spinner, checkbox, colorpicker, combobox) and `READ` drives them, while the window is
pumped by `WINDOW PUMP` in the event loop.

```basic
IMPORT WINDOWS

SCREEN 12
DIM nome AS STRING
DIM eta AS DOUBLE
DIM attivo AS DOUBLE

SUB Main()
  WINDOW THEME "Turbo"
  nome = "Mario Rossi" : eta = 30 : attivo = 1
  @ 2, 2 SAY "Nome:"     @ 2, 12 GET nome   SIZE 22
  @ 4, 2 SAY "Eta:"      @ 4, 12 GET eta    TYPE "spinner" MIN 0 MAX 120 STEP 1 SIZE 10
  @ 6, 2 SAY "Attivo:"   @ 6, 12 GET attivo TYPE "checkbox" CAPTION "Abilita"
  READ
  GO SUB EventLoop()
END SUB

SUB EventLoop()
  DO WHILE WINDOWCLOSED() = 0
    WINDOW PUMP 16
  LOOP
END SUB
```

Samples: `shared/samples/Clipper/ClipperAdvanced.bas` (console) and
`shared/samples/graphics/ClipperGraphics.bas` (pixel). The drawing primitives — `CLS`,
`LINE (x,y)-(x,y), colour, "BF"`, `CIRCLE`, `PAINT`, `PSET`, `DRAW TEXT` — are covered in
[Graphics](#graphics).

## Samples and tests

- **[`shared/samples/`](shared/samples/)** — runnable BASIC programs, one folder per category
  (Arrays, Databases, Ai, graphics, Network, …). Each one builds and runs on the four backends.
- **[`shared/minitests/`](shared/minitests/)** — the parity corpus: one `EXPECT:` per file, executed
  on all four backends by `tools/sh/parity4` and `tools/sh/minitest_parity_perdomain.sh`.
- **`shared/samples/Fixtures/`** — input data. The four market feeds are not committed: they are
  downloaded on demand with `gmb fixtures ensure`.

## AI & LLM

Four namespaces, one axis each (`AGENTS.md` §6.4): **`AI`** serving/agents/RAG (274 functions),
**`LLM`** model compiler (61), **`TRAIN`** weight production, **`TORCH`** tensor runtime (76).

| Subsystem | What it does | Where |
|---|---|---|
| **Providers** | MLX, llama.cpp/GGUF and MoE streaming engines, OpenAI-compatible/Ollama/ONNX, auto-failover, credits and quotas | `GMBasicSharp/common/AI/Providers/` + engine in [`LLMEnv`](https://github.com/c-vision/LLMEnv) |
| **Agents** | agent records, tool loop, permissions, memory (ISAM-backed), multi-agent teams, structured output | `GMBasicSharp/common/AI/Agents/` |
| **MCP** | MCP server (stdio/http) and client, audit sink, 52 connectors | `GMBasicSharp/common/AI/Mcp/`, `.../Connectors/` |
| **RAG** | ingestion, chunking, embeddings, retrieval, eval harness | `GMBasicSharp/common/AI/`, `common/Databases/VectorDB/` |
| **Knowledge graph** | graph store, PageRank/Louvain/max-flow, provenance, graph-backed Q&A | `GMBasicSharp/common/AI/Graph/` |
| **Brains** | installable RAG + graph bundles (`rag`, `graph`) | `~/.gmbasic/brains` — see [Download](#download-what-which-command-where-it-lands) |
| **Skills / Plugins** | prompt archives and agent capability descriptors | `shared/skills/`, `shared/plugins/` |
| **Model compiler — quantization** | format policies, per-tensor planning, QuantIR, imatrix, activation quantization, dequant, MLX↔GGUF converter | `GMBasic/gmbllm/` (**PUL**) |
| **Training** | fine-tune, LoRA, distillation, DPO/GRPO, eval gates, merge, prune | `GMBasic/gmbllm/` (**PUL**) |
| **Tensor runtime** | tensors/ops/devices, metrics, datasets, MiniLM embeddings | `GMBasic/native/gmb_torch/` + `TORCH` bindings |

### Quantization — the `LLM` namespace

Post-training quantization (PTQ) with **per-role and per-tensor precision**, driven from BASIC:

```basic
' per-role policies (the same names the compressor pipeline uses)
LLM POLICY SET "ROUTED_EXPERT", "iq2xxs"   ' MoE experts: ~2 bit
LLM POLICY SET "ATTENTION",     "q8_0"     ' attention projections
LLM POLICY SET "EMBEDDING",     "q4_k"     ' the biggest tensor
LLM POLICY SET "DEFAULT",       "q4_k"

' inspect what the policy actually resolves to, per operation and per tensor
LLM TENSOR QUANTIR   "model.gguf"          ' effective precision: w / activation / accum / output
LLM TENSOR AUTOPOLICY "model.gguf"         ' a policy proposed from the architecture
```

| surface | what it gives you |
|---|---|
| `LLM POLICY SET` / `DEFINE` / `ITEM(S)` / `APPLY` / `DIFF` / `GATE` | named policies and per-role entries: conditions (`ROLE=`, `ARCH=`, `LAYER<op><n>`, `IMP<op><value>` on the **imatrix**), action = a format or **4-axis** `w=…,a=fp8,acc=f16,o=f16`, `DEFAULT:` fallback; `DIFF`/`GATE` compare and vet two policies |
| `LLM QUANTIR` | the **QuantIR**: effective precision per operation and per tensor, resolved from the `.gmbarch` + the policy (`SETITEM` > DSL > role), overrides marked `*`; it is an editable IR |
| `LLM TENSOR` / `ACTIVATIONSTATS` / `QUANTERROR` / `IMATRIX` | tensor inspection (dense/compare), activation statistics (actquant), quantization error, importance matrix |
| **formats** | `q2_k … q6_k`, `q4_0`, `q8_0`, `iq1_s`, `iq2_xxs`/`iq2_xs`/`iq2_s`, `iq3_xxs`/`iq3_s`, `mxfp4`, `nvfp4`, `f16`/`f32`/`bf16`, `NOQUANT` |

**Where the code lives** — and why it matters for the license: the **encode** side
(quantization/training/conversion that *produces* weights) is in
[`GMBasic/gmbllm/`](GMBasic/gmbllm/README.md) under **PUL**; the **dequant** and the forward used to
*run* a quantized model stay in the Apache engine ([`LLMEnv`](https://github.com/c-vision/LLMEnv)).
The native C build links `libgmbllm.a`, so a compiled program can carry the compiler with it.

### Training — the `TRAIN` namespace

Weights production from BASIC, same engine abstraction (`engine: "mlx"|"torch"`):

| verb | what it does |
|---|---|
| `TRAIN DATASET BUILD` / `SAMPLE` · `DATASETSTATS` | dataset preparation and statistics |
| `TRAIN FINETUNE` · `TRAIN RESUME` | fine-tune (LoRA SFT) with checkpoints and resume |
| `TRAIN LORA APPLY` / `MERGE` / `SAVE` / `LOAD` · `LORALIST` | LoRA adapters: apply, merge, persist, list |
| `TRAIN DISTILL BUILD` / `SAMPLE` (`DISTILLCKPT`, `DISTILLEVAL*`) | self-distillation with acceptance/token gates |
| `TRAIN DPO` · `TRAIN GRPO` | preference and reinforcement-style objectives |
| `TRAIN EVAL` · `EVALGATE` / `GATE` · `QUALITY` | perplexity/NLL evaluation, gates, quality metrics |
| `TRAIN MERGE` · `PRUNE` · `EXPORT` | merge/prune/export the produced weights |
| `RUNS`, `RUNSJSON`, `RUNSITEM`, `RUNSCLEAR` | training-run registry (resume/inspection) |

Dylib: `gmb_ai_finetune` (ABI listed in [`shared/runtime-abi`](shared/runtime-abi/README.md)).
`TRAIN` is the **PUL boundary** in the language: everything here produces or alters weights, and its
implementation lives in `gmbllm`.

## Graphics

SDL2-based GPU-accelerated console. Full-screen, multiple screens, sprites, fonts, TTF rendering.

```basic
SCREEN 640, 480, 32
CIRCLE (320, 240), 100, RGB(255, 0, 0)
SPRITE 1, "sprite.png", 0, 0
```

Dependencies: `libSDL2.dylib`, `libSDL2_ttf.dylib`, `libfreetype.6.dylib`, `libharfbuzz.0.dylib`
(downloaded into `~/.gmbasic/libs/<rid>/` on demand).

## Standard Library

| Namespace | Functions |
|-----------|-----------|
| `SYSTEM` | `Next`, `Tab`, `Sys`, `Iif`, `Empty`, `SizeOf`, `VarPtr`, `StrPtr`, `UBound`, `LBound`, `Count`, `TypeName`, `CType`, `Choose` |
| `MATH` | `Rnd`, `Pi`, `Abs`, `Sgn`, `Sqr`, `Log`, `Exp`, `Sin`, `Cos`, `Tan`, `Atn`, `Round`, `Floor`, `Ceiling`, `Min`, `Max`, `Clamp`, `Fact`, `Perm`, `Comb` |
| `STRINGS` | `Left`, `Right`, `Mid`, `Len`, `Asc`, `Chr`, `Str`, `Instr`, `Replace`, `Split`, `Join`, `Format`, `Upper`, `Lower`, `Trim`, `Reverse`, `Pascal`, `Camel`, `Snake`, `Kebab`, `Contains`, `StartsWith`, `EndsWith` |
| `DATETIME` | `Now`, `Today`, `DateAdd`, `DateDiff`, `DateSerial`, `TimeSerial`, `WeekDay`, `EoMonth`, `DateFromUnix`, `UnixTimestamp` |
| `CONVERSIONS` | `CStr`, `Val`, `Hex`, `Oct`, `Bin`, `CSng`, `CDbl`, `CInt`, `CLng`, `CByte` |
| `IO` | `EOF`, `LOF`, `FreeFile`, `Open`, `Close`, `Read`, `Write`, `Seek`, `FileExists`, `DirExists`, `MkDir`, `RmDir`, `ChDir`, `Cwd` |
| `CONCURRENCY` | `SleepAsync`, `TaskYield` |
| `JOYSTICK` | `Joy`, `JoyCount`, `JoyName`, `JoyPresent` |

## Databases — six engines, native on both worlds

**Five native engines plus vector search**, all reachable from BASIC, all usable without a server:

| Engine | Type | Native implementation |
|--------|------|-----------------------|
| **ISAM** | key-value B-tree, WAL, concurrent readers, relations and joins | **C** (`GMBasic/native/gmb_db_c/`) + C# |
| **DBF** | dBASE/xBase files (read/write, NTX/NDX indexes, compound, memo, RDD layer) | **C** (`gmb_db_c/dbf`) + C# |
| **SPEED** | LSM-tree, high throughput, crash recovery, group commit | **C** (`gmb_db_c/speed`) + C# |
| **LEDGER** | append-only ledger with PACK compaction | **C** (`gmb_db_c/ledger`) + C# |
| **SQLite** | embedded SQL | embedded **SQLite C** library (both worlds) |
| **VectorDB** | cosine/dot similarity, IVF index, embeddings, chunking — the RAG/brains store | C# (`common/Databases/VectorDB/`) |

```basic
DBF USE "data/customers.dbf" ALIAS C
DBF GO TOP
DO WHILE NOT DBF.EOF()
  PRINT C.NOME, C.CITTA
  DBF SKIP
END DO

ISAM OPEN "data/items.isdb" OF Item ALIAS I INDEXED BY ID   ' B-tree + WAL, crash-safe
```

**How they run on each backend.** The C engines are a *parallel implementation of the same
semantics*, exposed through `gmb_db.h` (DBF / ISAM / SPEED / LEDGER, syscalls `GMB_SYS_ISAM_*`,
`GMB_SYS_DBF_*`, …):

- **C99Native** links `libgmb_db.a` + SQLite **by default**: a compiled native program gets the
  database engines without the C# runtime.
- **VM/C** dispatches the DB syscalls when built with `-DGMB_HAS_COMMERCIAL_DB=ON` (off by default).
- **IL / PCodeVM** use the C# implementation in `GMBasicSharp/common/Databases/`.

The two implementations are cross-checked with the C# one as **oracle**
(`GMBasicSharp/tests/GMBASIC.Database.Native.Tests/`), so a program sees the same behaviour on every
backend.

## HTTP & Networking

```basic
' HTTP client
DIM response = HTTP.Fetch("https://api.example.com/data")

' WebSocket client
DIM ws = WS.Connect("wss://echo.websocket.org")
WS.Send(ws, "Hello")
DIM reply = WS.Receive(ws)

' TCP/UDP
DIM sock = TCP.Connect("example.com", 80)
TCP.Send(sock, "GET / HTTP/1.1\r\n\r\n")
DIM data = TCP.Receive(sock, 1024)

' HTTP server
HTTP.Listen 8080
```

## Concurrency (GPM)

Cooperative multitasking with green threads (goroutine-style `GO SUB`/channels), modeled on Go's
GPM (M:P:G). **Each backend has its own GPM implementation** — VM/C uses a pthread-based model,
C99Native a green-thread model. Language surface (identical across backends):

```basic
' Start a concurrent task
GO SUB BackgroundTask()

' Synchronization
WAIT      ' Wait for all GO tasks
SEND ch, value    ' Channel send
RECEIVE ch => var ' Channel receive

' Sleep without blocking the scheduler
CALL SleepAsync(1000)
```

## Language features

| Feature | Status |
|---------|--------|
| Line-numbered BASIC (classic) | ✅ |
| Named subroutines (`SUB`/`FUNCTION`/`END SUB`) | ✅ |
| Block IF/THEN/ELSE/END IF | ✅ |
| SELECT CASE | ✅ |
| FOR/NEXT (single and nested) | ✅ |
| DO/LOOP WHILE/UNTIL | ✅ |
| WHILE/WEND | ✅ |
| EXIT FOR/DO/WHILE | ✅ |
| CONTINUE FOR/DO/WHILE | ✅ |
| Labeled loops (`EXIT OuterLoop`, `CONTINUE Middle`) | ✅ |
| `FOR EACH` (arrays, lists, matrices, dictionaries) | ✅ |
| GOTO/GOSUB/RETURN | ✅ |
| ON ERROR GOTO/RESUME | ✅ |
| TRY/CATCH | ✅ |
| STATIC variables | ✅ |
| User-defined types (UDT) | ✅ |
| Classes with methods/properties | ✅ |
| Generics (`LIST OF T`, `FUNCTION Foo<T>`) | ✅ |
| Nullable types (`INTEGER?`, `STRING?`) | ✅ |
| Attributes (`<Serializable>`, `<Required>`) | ✅ |
| Lambda expressions, closures | ✅ |
| List/dict comprehensions | ✅ |
| Macro system | ✅ |
| Module system (`IMPORT`/`REQUIRE`) | ✅ |

✅ = working · 🔶 = partial/known issue

The loop rows are covered by MiniTests that run green on all four backends:
`shared/minitests/loops/loop_labeled_exit_continue.bas` (labeled `EXIT`/`CONTINUE`),
`loops/foreach_matrix_2x3.bas`, `loops/foreach_dict_kvp.bas`, `loops/foreach_string_matrix.bas`,
`collections/dict_foreach.bas`.

## TODO

The main open work items are tracked in **[TODO.md](./TODO.md)**:

- **the two IDEs are not in this repo yet** — the GUI (`GMBasicIDE`, VB6-style: form designer, code
  window, build/run, debug) and the TUI (`GMBasicTuiIDE`, written in BASIC) are developed locally and
  will be published when complete (GUI backlog ~51 items over groups G0–G7, TUI 11 items);
- **`libs` CI workflow is red** at the macOS system-dependencies step (so releases and
  `libs-manifest.json` have never been published from CI).

## Tests

| Area | Command |
|------|---------|
| Compile + P-Code codegen, all samples | `dotnet run --project tools/runners/GMBASIC.Conformance` |
| VM/C (compile → P-Code → run as external `gmb_vm_host`) | `dotnet run --project tools/runners/GMBASIC.Conformance -- vmtest <file.bas>` |
| PCodeVM (P-Code VM in C#) | `dotnet run --project tools/runners/test_pcode -- <file.bas>` |
| IL backend execution (xUnit, incl. Clipper/Loops samples) | `dotnet test GMBasicSharp/tests/GMBASIC.IlBackend.Tests` |
| C99Native backend (C frontend + emitter → `cc` → run) | `bash tools/sh/gmb_c99native_run.sh ../shared/samples/<file>.bas` |
| One engine at a time (IL / PCode / VMC) | `dotnet run --project tools/runners/test_ilrun -- --engine=il\|pcode\|vmc <file.bas>` |
| All four legs on one MiniTest | `zsh tools/sh/test_minitests_parity.sh "<domain>/<file>.bas"` |
| Native C database module (oracle vs. C# implementation) | `dotnet test GMBasicSharp/tests/GMBASIC.Database.Native.Tests` |
| Native C runtime/VM unit tests | CMake build of `GMBasic/native/gmb_runtime_c` (`--target test`) |
| AI agents/RAG | `dotnet test GMBasicSharp/tests/AI.Tests` |
| AI eval harness (fixture, no network) | `dotnet run --project tools/runners/AI.Eval` |
| ABI contract C→C# (13 dylibs) | `bash shared/runtime-abi/check_all.sh` |

## Commands reference

See [COMMANDS.TXT](./COMMANDS.TXT) for the complete list of supported commands and functions.

## REPL commands

`RUN`, `LIST`, `NEW`, `SAVE`, `LOAD`, `DELETE`, `SAMPLE <n>`, `AUTO`, `RENUM`, `CLS`, `HELP`, `QUIT`,
`LEXER ON/OFF`, `PARSER ON/OFF`, `EXECUTOR ON/OFF`.

## Configuration

- `shared/settings/system.settings.json` — global defaults (paths, console, engine, compiler)
- `<project>/app.settings.json` — per-project overrides (`paths`, `consoleConfiguration`, `engine`,
  plus the optional `brains`/`fixtures`/`skills`/`plugins`/`config` declarations)
- `GMBasic/config/` (or `<exe>/config`) — **local state**, never in git: see
  [GMBasic/config/README.md](GMBasic/config/README.md)

## License

**PERSONAL USE LICENSE (PUL) v1.1** — see [LICENSE](./LICENSE). No activation key, no online
check, no trial: PUL is a personal-use license and the software runs as-is.

The **LLM engine** in the [`LLMEnv`](https://github.com/c-vision/LLMEnv) sibling repository is
released under **Apache-2.0**, and so is the engine code GMBasic consumes from it. Everything that
**produces or transforms model weights** (training, LoRA, quantization encode, model compiler,
MLX↔GGUF conversion) lives in [`GMBasic/gmbllm/`](GMBasic/gmbllm/README.md) under the **PUL**
license — the dependency is one-way (`gmbllm` → LLMEnv), see
[LLM engine](#llm-engine--the-llmenv-sibling-repository).

### What publishing this repository means

- **It is not open source, by design.** PUL grants personal/educational use and **public forks**, but
  **commercial use is forbidden**: the community will not treat this as open source, and GitHub shows
  *License: other*. The source is public and readable — that is the point of the license, not a
  claim of OSI openness.
- **Forks are not retractable.** Whoever clones or forks keeps their copy: switching the repository
  back to private does **not** recall forks, mirrors, package caches or clones already taken.
- **Every copy/fork/derivative must keep `LICENSE`, `NOTICE` and the repository URL** (PUL §5-§6).
- **The ecosystem is coherent by design:** the engine
  [`LLMEnv`](https://github.com/c-vision/LLMEnv) is already **public under Apache-2.0**;
  [`GMBasicModules`](https://github.com/c-vision/GMBasicModules) is **public** and publishes its
  binaries in the **releases**, with the README describing what each asset is;
  [`GMBasicBrains`](https://github.com/c-vision/GMBasicBrains) stays **private** — brains are
  installed with a token (`gmb brain login --github`).
