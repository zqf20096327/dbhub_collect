# world-ears

**Search what TV news around the world is saying, right now, on your own GPU.**

world-ears listens to N live news channels at once (public streams from the
[iptv-org](https://github.com/iptv-org/iptv) playlists) and transcribes each one with
whisper. It translates everything to English with a local LLM and puts it in a SQLite
full-text index, with timestamps and a link into a saved 30-second audio clip.

```
$ world-ears search Trump
2026-10-29 10:13:08  [QA] Al Jazeera (ar)
    The methodology of redrawing Israel's political map is correct—President Donald «Trump»'s
    support for Benjamin Netanyahu's right-wing government may have…
    > ومنهجية إعادة رسم الخارطة السياسية الإسرائيلية صحيح أن دعم الرئيس الأمريكي دولارد ترامب لبن يمين نتنياهو
    clip: data/media/al-jazeera/20261029-094721/000051.mp3  @ 27.6s
```

![world-ears web UI: search results across channels, trending per country](docs/screenshot.png)

You can search English or the original language: `séisme` finds French channels and
`earthquake` finds everyone. A "trending this hour" panel shows, per country, the words
its channels are saying that are rare elsewhere. A second list shows names that several
countries' TV are talking about at the same time.

Everything runs locally: whisper large-v3-turbo on one GPU, any OpenAI-compatible LLM
server for translation, SQLite FTS5, and a stdlib web server.

## Quick start

```bash
pip install -e .                      # Python 3.11+, ffmpeg on PATH, CUDA GPU
world-ears pick --languages hi,te,fr,ar,de,en,es --per-language 1   # probe iptv-org, write channels.json
world-ears run --duration 3600        # ingest; Ctrl-C to stop
world-ears search "pension reform"    # from another terminal, any time
world-ears trending --hours 1
world-ears serve                      # http://127.0.0.1:8765
```

Translation needs an OpenAI-compatible server (llama-server, vLLM, LM Studio, …) at
`--server` (default `http://127.0.0.1:8080`) with `--model` loaded. Set `LLAMA_API_KEY`
if it needs a key.

## How it works

```
channel × N   ffmpeg ─┬─ PCM 16 kHz ─ silero VAD ─ chunker (≤12 s, cut at 0.5 s silence) ─┐
                      ├─ 30 s mp3 clips (segment muxer, same clock)                         │
                      └─ one thumbnail per clip                                              │
asr  × 1      one whisper model, FIFO over all channels  ◄──────────────────────────────────┘
              └─► SQLite + FTS5 immediately, with the source text (searchable in ~6-10 s)
mt   × 1      LLM backfills English: newest first, 8 chunks per request;
              anything that waited > 15 min stays source-only
```

- **One clock for text and clips.** Both audio outputs of the same ffmpeg use
  `aresample=async=1:first_pts=0`, so "seconds into the stream" mean the same thing for
  the transcript and the clips. Clip *n* covers [30n, 30n+30). A search hit links to
  `clip.mp3#t=offset` with no extra bookkeeping. HLS delivers audio in bursts, so a
  separate arrival clock maps media time to the wall time it reached us.
- **Translation can't block indexing.** The first version translated before indexing.
  On a shared GPU the LLM fell behind (107 chunks queued after 3 minutes) and nothing
  new became searchable. Now ASR commits the source text at once, and translation is a
  backfill that updates the row; an FTS5 update trigger re-indexes it. The backlog is
  processed newest-first, so English stays fresh rather than falling further behind.
- **Batch translation.** Numbered lines go in and a JSON object comes out. 8 chunks per
  request amortise the prompt. An item missing from the reply is retried alone. The
  model's own remarks (`[unclear]`, `**bold**`) are stripped, and a reply that only says
  "I can't decipher this" counts as no translation.
- **Trending without NER.** score = (segments in this country's last hour that mention
  the term) × IDF over the whole index. The cross-country list keeps only name-like terms:
  words that are capitalised mid-sentence at least 60% of the time in the English text.
  "Netanyahu" passes; "according" doesn't.
- **Per-channel decoding state, shared model.** Each channel keeps its own prompt
  (the last 200 characters) and repeat guard, so one channel's hallucination loop can't
  leak into another's. All channels share one model instance.

## Measured: 7 channels, 7 languages, 29 minutes

Run on 2026-10-29, 09:47–10:16 CET, on an RTX 5080: ABP News (Hindi), TV9 Telugu, France 24
(French), Al Jazeera (Arabic), WELT (German), DW Español, Al Jazeera English. Whisper
large-v3-turbo int8_float16, beam 1. Translation: ministral-3-3b-instruct Q4_K_M on a
llama-server that other jobs were also using.

The run was planned for 75 minutes. At 10:16 the machine ran out of RAM (other processes:
57 MB of 32 GB free, 1.8 GB of commit left) and everything started paging, so every whisper
call took 40+ s. The run was stopped there, and the numbers below cover only the healthy
window (`scripts/report.py data/runs/<run> --until 10:16:35`).

| | |
|---|---|
| segments indexed | **1,316** (≈22 min of speech per channel) |
| speech arriving | 5.5 s of speech per wall-clock second (79% of airtime is speech) |
| whisper GPU busy | **27% mean, 40% p95** for 7 channels; 0.076 s of GPU per s of speech |
| ASR queue | max 4 chunks: ASR never fell behind |
| source text searchable after it aired | **p50 6–10 s, p90 11–20 s** per channel |
| English searchable after it aired | p50 28–33 s, p90 46–64 s |
| translated | 80% of non-English chunks (the rest: dropped after 15 min, or MT timeouts) |
| translation busy | **100%**: the bottleneck |

**How many channels one GPU sustains:**
- **ASR:** about 20+. At 27% busy for 7 channels (40% p95), 7 more fit with headroom, and
  the real limit is around 3× that. Chunks of ≤12 s at beam 1 are cheap.
- **Translation, with a 3B model on a shared server:** about 4–5 non-English channels.
  In a 2-channel run it was 42% busy and translated everything; with 6 non-English
  channels it was saturated. A dedicated GPU, a larger `--mt-batch`, or a parallel-slot
  server raises this. gemma-4-12b translates better but did 6–8 tok/s on the contended
  GPU and could not keep up even with 2 channels.

Latency floor: a chunk closes at the first 0.5 s pause or at 12 s, and HLS segments
arrive in 6–10 s bursts. So the source-text latency is mostly waiting for audio, not
compute.

### Transcription quality per language

There is no human transcript of live TV, so this is **whisper's own confidence**, not
accuracy: the mean token log-prob of every chunk in the healthy window, and the share of
chunks below -0.5, which in practice means they read as garbled.

| channel | lang | chunks | mean log-prob | chunks < -0.5 | got English |
|---|---|---|---|---|---|
| Al Jazeera | ar | 165 | -0.082 | 1% | 80% |
| DW Español | es | 210 | -0.127 | 7% | 80% |
| WELT | de | 208 | -0.144 | 4% | 83% |
| Al Jazeera English | en | 264 | -0.162 | 3% | 100% |
| France 24 | fr | 159 | -0.164 | 8% | 77% |
| ABP News | hi | 187 | -0.195 | 11% | 76% |
| TV9 Telugu | te | 123 | **-0.425** | **29%** | 81% |

Not measured yet: `scripts/quality.py` re-transcribes saved clips offline with whisper
large-v3 (beam 5) and computes the CER of the live text against it. That shows what live
chunking and greedy decoding cost. It could not run here, because the machine had no free
RAM to load a second model. Run `python scripts/quality.py --clips 8` after a capture.

What the samples look like:

- **Arabic, French, German, Spanish**: fluent news text. The translator also fixes
  ASR errors: whisper heard "دولارد ترامبو" ("Dollard Trumpo") and the English says
  "President Donald Trump".
- **Hindi**: mostly right. Misspellings pass through: "अस्पिनाल" for hospital became
  "*Aspinal* hospital".
- **Telugu**: whisper is bad at Telugu, as expected. Output includes fragments that
  start mid-syllable, romanized gibberish ("Kithru Da Tharalul, 2.1.6.0"), and a storm
  story with half the names garbled. Before the cleaning step, the translator's
  "[unintelligible]" remarks were the top trending terms for India. Don't trust Telugu
  results beyond the gist.

## Rights and storage

world-ears stores only transcripts and short audio clips with thumbnails, locally. By
default it deletes clips older than 24 h (`--keep-hours`). It never re-streams or
re-broadcasts anything; the web UI only lets you play back your own saved clips. The
stream URLs come from the public iptv-org playlists, and geo-blocked entries are
skipped. Whether you may record a given channel depends on where you are and on the
channel's terms; check before you run it.

## Layout

```
world_ears/
  playlist.py   iptv-org m3u fetch/parse, language × news intersection, stream probing
  chunker.py    VAD-driven chunking (from babel-tv)
  asr.py        faster-whisper wrapper, hallucination filter, per-channel repeat guard
  translate.py  batched LLM translation, reply parsing, cleanup
  ingest.py     ffmpeg per channel, ASR thread, MT backfill, metrics, clip janitor
  index.py      SQLite schema + FTS5, search, clip references, trending
  server.py     JSON API + media with Range support
  ui.html       single-page UI
scripts/
  report.py     capacity and latency from a run
  quality.py    live-vs-offline CER per channel
```

`pytest` runs 47 tests, including an end-to-end engine run on a generated .ts file
(fake ASR and MT, real ffmpeg).

## Limitations

- Translation is the bottleneck on shared hardware. The design degrades gracefully
  (source text is always indexed), but English for some chunks never arrives.
- Trending needs volume: in the first ~20 minutes of a run, every term is "rare".
- Telugu (and probably other low-resource languages) are not usable for search
  beyond names and numbers.
- Search is lexical (FTS5). "Strike" doesn't find "walkout".

## License

[AGPL-3.0](LICENSE). Self-hosting is free; if you run a modified version as a service, share your changes.
