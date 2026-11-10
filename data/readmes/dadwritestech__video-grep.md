# vgrep: grep for every video you own

You remember *that* moment: someone said "budget" in a meeting recording, a slide said
`BUG #1187`, or there was a shot of a rocket on the pad. You don't remember which file or
which minute. `vgrep` indexes a folder of videos **on your machine**:

- **speech** comes from Whisper, with per-word timestamps.
- **on-screen text** comes from OCR on frames sampled every 2 s.
- **scenes** come from a local vision model that captions each visual cut.

All three go into one SQLite full-text index. A search returns the file, the second, which
signal matched, a snippet, and the command that opens your player at that second.

```
$ vgrep "we choose to go to the moon"
President_Kennedy_speech_on_the_space_effort_at_Rice_University_September_12_1962.ogv  08:40  [speech]  Why does Rice play Texas? «We choose to go to the moon». «We choose»…
    mpv --start=519.0 "D:\video-grep\corpus\commons\President_Kennedy_speech_on_the_space_effort_at_Rice_University_September_12_1962.ogv"

$ vgrep budget
team_standup.mp4  00:10  [ocr+speech]  «BUDGET» $42,000
    mpv --start=9.0 "D:\video-grep\corpus\generated\team_standup.mp4"
President_Kennedy_speech_on_the_space_effort_at_Rice_University_September_12_1962.ogv  14:10  [speech]  That «budget» now stands at $5,400,000,000 a year,
    mpv --start=849.1 "D:\video-grep\corpus\commons\President_Kennedy_speech_on_the_space_effort_at_Rice_University_September_12_1962.ogv"

$ vgrep "spacecraft over cratered surface" -k scene
A_New_Look_at_the_Apollo_11_Landing_Site_xUcYQ7slmRw.webm  00:34  [scene]  A «spacecraft» is visible in the center of a «cratered» lunar «surface», appearing as…
    mpv --start=33.0 "D:\video-grep\corpus\commons\A_New_Look_at_the_Apollo_11_Landing_Site_xUcYQ7slmRw.webm"
```

The `vgrep serve` web UI is a contact sheet of hits. Each card shows the frame at the matched
second, and clicking it plays from there:

![vgrep web UI searching "rocket booster" across a shuttle launch, an SLS booster test and JFK's Rice speech](docs/web-ui.png)

The MCP server lets an agent search your videos and **cite moments**, for example
`STS-135_Space_Shuttle_Launch.webm @ 02:08`, instead of guessing.

Nothing is uploaded. Whisper and OCR run in-process. Scene captions and the optional
embeddings go to an OpenAI-compatible server you run yourself (llama.cpp's `llama-server`
by default, on `localhost:8080`).

## Install

```bash
python -m venv .venv && .venv/Scripts/pip install -e ".[mcp]"
```

`ffmpeg` and `ffprobe` must be on `PATH`. Whisper (`faster-whisper`, large-v3-turbo) uses
CUDA when it can. It falls back to CPU int8 when there's no GPU or no free VRAM, including
an out-of-memory error mid-file. OCR is `rapidocr-onnxruntime`, so Tesseract isn't needed.
Scene captions need a vision model behind `/v1/chat/completions`. We use gemma-4-12b on
llama-server:

```bash
llama-server -m gemma-4-12b.gguf --mmproj mmproj.gguf --port 8080 --api-key "$LLAMA_API_KEY"
```

If the server needs a key, export `VGREP_LLM_KEY` (or `LLAMA_API_KEY`). The key is read
from the environment and never written to the index.

## Use

```bash
vgrep index ~/Videos                      # all three signals; resumable, re-run any time
vgrep index ~/Videos --signals speech,ocr # skip the VLM (about 17x real time, see below)
vgrep "postgres migration"                # search (the default command)
vgrep "launch pad" -k scene -n 5          # only scene captions, top 5
vgrep "budget" --json                     # machine-readable; exit code 1 when nothing matches
vgrep serve                               # web UI on http://127.0.0.1:8765
vgrep mcp                                 # MCP server on stdio
vgrep stats
```

Indexing is **per signal and resumable**. A `done` table records which signals finished for
which file, so a run that dies (or a VLM server that's down) only redoes the missing
signal. A file whose size or mtime changed gets re-indexed. `--force` redoes everything.

Useful knobs:

- `--frame-every 2`: the OCR and keyframe sampling step.
- `--caption-gap 6 30`: caption on a visual cut, but no closer than 6 s apart and at least every 30 s.
- `--vad 0.2`: the speech detection threshold. See *what we learned* below.
- `--embed`: adds dense vectors for `vgrep -s` hybrid search.

### MCP

```json
{ "mcpServers": { "vgrep": { "command": "vgrep", "args": ["mcp"] } } }
```

| tool | what it returns |
|---|---|
| `search_videos(query, limit, signals)` | citations: `file`, `timestamp`, `seconds`, `signals`, `text`, a `file:///…#t=SS` URI, and the player command |
| `get_moments(file, start_seconds, end_seconds)` | everything indexed in a time range (transcript, slide text, captions), so the agent can read around a hit |
| `list_videos()` | the library |

## How it works

```
video ─┬─ ffmpeg → 16 kHz PCM ─→ faster-whisper (VAD, word timestamps) ──→ speech moments
       ├─ ffmpeg 1 frame / 2 s ──→ RapidOCR ─→ merge near-identical frames ─→ ocr moments
       │                        └→ keyframes on visual cuts ─→ VLM caption ─→ scene moments
       └──────────────────────────────────────────────→ SQLite: moments + FTS5 (porter stemming)
```

- **Search** runs FTS5 in three tiers: the exact phrase, then all non-stopword terms, then any
  term. Results are ranked by bm25. Every term is quoted, so user input can't inject FTS syntax.
- Hits within 5 s of each other in one video merge into **one moment** and list the extra signals
  (`[ocr+speech]`).
- **Jump time** for speech is the word timestamp at the start of the densest cluster of query
  terms, not the start of the segment. A 38 s Whisper segment becomes a jump to the right second.
- With `--embed`, `-s` fuses the lexical and embedding rankings using reciprocal rank fusion.
- **Web UI**: stdlib `http.server` only, with no build step and no CDN. Thumbnails are cut by
  ffmpeg on demand and cached. Video is served with HTTP Range, so seeking works. Browsers
  can't decode Theora (`.ogv`). Chrome plays the audio with a black 0x0 picture and raises no
  error, so the player checks `videoWidth` and switches to a server-side H.264 transcode
  that starts at the hit.
- **Local-only server**: it binds 127.0.0.1. It rejects foreign `Host` headers (DNS rebinding),
  and the "open in mpv" endpoint requires a custom header that a cross-site form can't send.

## Measured

Everything below was measured on one machine: 2x 16 GB NVIDIA GPUs, both shared with other
models while the test ran.

### Test corpus (34 min, all freely licensed)

| set | what | license |
|---|---|---|
| `commons` (8 files, 31.6 min) | JFK at Rice University 1962 (17.8 min), Apollo 11 first steps, LRO's new look at the Apollo 11 site, SLS booster test, *Built to Explore* SLS, Suni Williams' ISS cupola tour, STS-135 final shuttle launch, Artemis II #NASAMoonCrew | all **public domain** (NASA / US government works), fetched from Wikimedia Commons by `scripts/fetch_corpus.py`, which checks each file's license field and records sources in `SOURCES.json` |
| `generated` (3 files, 1.2 min) | a stand-up meeting, a cooking class and a physics lecture: TTS narration over text slides, built by `scripts/gen_clips.py`, with exact ground truth in `truth.json` | ours |

The videos aren't committed. Run `python scripts/fetch_corpus.py && python scripts/gen_clips.py` to rebuild them.

### Indexing speed

Speed is minutes of video indexed per minute of wall-clock time (higher is better).

| run | video | wall | speed | notes |
|---|---|---|---|---|
| speech + OCR, `commons` | 31.6 min | 1.9 min | **16.6x** | Whisper on GPU (58.8 s) and OCR on CPU (100.7 s) run side by side |
| speech only, `commons` (re-run, VAD 0.2) | 31.6 min | 1.1 min | **29.1x** | Whisper model already cached on disk |
| OCR only, `commons` (re-run after the timestamp fix) | 31.6 min | 16.1 min | 2.0x | the same OCR, but the CPU was at 93% from other jobs; shows how much OCR depends on free cores |
| scenes, 4 `commons` clips | 4.2 min | 23.7 min | **0.18x** | 37 captions, about 38 s each on a single-slot server shared with other sessions; the least-contended clip ran at 7.5 s per caption |

Scenes are the slow signal by two orders of magnitude, which is why indexing is per signal:
search works on speech and text minutes after you start, and captions fill in later. The
scene pass over the 17.8 min Kennedy speech and the last three clips was still queued
behind other sessions' generations when these numbers were taken, so scene search here
covers 4 of the 8 `commons` files plus the 3 generated clips. That scene pass also started
before the frame-timestamp fix below, so its caption spans are 1 s late. OCR was
re-indexed after the fix; the eval's ±2 s slack absorbs the caption offset.

### Precision

`scripts/eval.py` runs 54 labeled queries (`eval/queries.json`). A hit is correct if it is
the right file **and** the jump time falls inside the labeled span, ±2 s.

| set | queries | P@1 | Hit@5 | MRR |
|---|---|---|---|---|
| `generated` (exact labels) | 20 | 1.00 | 1.00 | 1.00 |
| `commons` (speech + on-screen text) | 31 | 0.97 | 0.97 | 0.97 |
| `scenes` (visual-only words, captioned clips) | 3 | 1.00 | 1.00 | 1.00 |
| **all** | **54** | **0.98** | **0.98** | **0.98** |

The one miss is "christina koch": the name is only on screen, and OCR reads it as
`CHRISTINAKOCH` (see below). The three `scenes` queries use words that are neither spoken nor
on screen ("american flag on the test stand", "lunar lander with its arm out", "workers in
high visibility vests"), so only a caption can find them. Three queries is a smoke test, not
a measurement.

How the labels were made: the `generated` labels are exact, taken from the clip builder. The
`commons` labels were set by Claude (the AI that built this), who read the transcripts and
looked at sampled frames. No blind human annotator was involved, and most queries share
words with what was said or shown. Read this as "does the pipeline find and place the
moment", not as a retrieval benchmark.

### What we learned building it

- **The VAD default ate the most famous line.** Silero's default speech threshold (0.5)
  classified "one small step for man" on the Apollo 11 downlink as noise, and Whisper never
  saw it. With VAD off, Whisper finds the line but hallucinates a closing "Thank you." on
  silence. A threshold of 0.2 recovers the line and still yields no speech on a music-only
  clip, so 0.2 is the default (`--vad`).
- **Segment starts are bad jump targets.** On noisy archival audio Whisper emits 20–40 s
  segments. Jumping to the first word matching any query term landed on "surface" at 0:08
  for "surface like a powder", when the phrase is at 0:13–0:21. Jumping to the densest cluster
  of distinct terms fixed it.
- **OCR on stylised lower-thirds glues words together.** NASA's name captions come out as
  `CHRISTINAKOCH` and `BUILTFOR | DEEPSPACE`, so a query for "christina koch" can't match
  that frame. This is the one remaining miss in the eval. Scene captions or embeddings are the
  fallback.
- **Small VLMs misread old footage.** gemma-4-12b describes the grainy 1969 lunar-surface
  video as "a person standing in a dark, indoor setting". On clean modern footage its captions
  are good ("a lunar lander stands on the surface of the Moon with a robotic arm extended").
- **ffmpeg's `fps` filter lies about time.** `fps=1/2` picks frames from the middle of each
  2 s interval but stamps them with the interval's start. Every OCR and scene timestamp was
  1 s late. A generated clip whose brightness ramps with time showed it: the frame labelled
  4.0 s had the 5.0 s brightness. vgrep now keeps the first frame of each interval with
  `select` and `-fps_mode vfr`, which preserves real presentation times. The ramp clip is now
  a regression test.
- **The VLM is the bottleneck.** Speech and OCR are faster than real time by an order of
  magnitude. Captioning is a remote call per keyframe, and on a shared single-slot server it
  queues behind everyone else's requests.

## Limitations (v0)

- Scene captioning is slow on a busy server. Run `--signals speech,ocr` first, then add
  `--signals scene` overnight. Because indexing is per signal, the second run only does scenes.
- Embeddings (`--embed`, `vgrep -s`) are implemented and unit-tested but **not benchmarked
  here**. The shared llama-server was at its model limit, and loading the embedding model
  would have evicted someone else's model.
- One caption covers the span until the next keyframe (6 to 30 s). Fast-cut edits cut faster
  than that: in *Built to Explore* the 0:24 caption ("people in hard hats in a hangar") also
  covers 0:26, where the frame shows a rocket stage being hoisted into a tower at night.
- English-first: Whisper detects the language per file, but the stopword list and the
  porter stemmer are English.
- The web UI's transcode fallback streams fragmented MP4, so the player's progress bar
  only covers the transcoded stretch.

## Tests

```bash
pip install -e ".[mcp,dev]" && pytest
```

29 tests pass in about 25 s. They cover the FTS quoting and hostile queries, moment merging, jump times,
resumable and failing-signal indexing on a real ffmpeg-generated clip, keyframe selection, true frame timestamps (on a brightness-ramp clip),
the VLM request shape (no-thinking flag, auth header) against a fake server, the CLI, the web
server (search, thumbnails, Range, Host/CSRF refusals) and the MCP tools. The tests need no
GPU, no models and no network.

## License

[AGPL-3.0](LICENSE). Self-hosting is free; if you run a modified version as a service, share your changes.
