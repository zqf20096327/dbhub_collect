# Pi Durable: tutorial companion

Companion code for **Alejandro AO's video tutorial, “Pi Durable Explained: Build Always-On Agents with Local Models.”** The tutorial covers what Pi Durable is, how a harness differs from an application, and how to build a minimal agent with persistent state.

This repository contains the **two terminal examples shown in the video**:

| Example | Command | What it demonstrates |
| --- | --- | --- |
| [`chat.mjs`](chat.mjs) | `npm run chat` | Configure a harness and start a fresh conversation on every launch. |
| [`chat-resume.mjs`](chat-resume.mjs) | `npm run chat:resume` | Reopen a saved conversation and resume interrupted work from SQLite. |

These are learning examples, **not a production agent or hosted service**. Pi Durable's APIs are experimental; the Pi packages are pinned to **1.2.0** to match the recording. This repo deliberately omits the earlier experimental web dashboard and storage-debugging UI.

## Requirements

- **Node.js 24+**, including its built-in SQLite support. With nvm: `nvm install && nvm use`.
- npm.
- Optional: a running llama.cpp server or your own OpenAI API credentials.

## 1. Install and try it without a model

```bash
git clone https://github.com/alejandro-ao/pi-durable-demo.git
cd pi-durable-demo
npm ci --ignore-scripts
npm run chat
```

Type a message, then `/quit` to exit. With no model configured, the example uses a **keyless local echo provider** through the real Harness and SQLite storage. It does not download model weights, make model API calls, or intelligently use tools. If your shell already sets `OPENAI_MODEL` or `LLAMA_BASE_URL`, unset those first to try the offline mode.

Optional configuration goes in `.env`:

```bash
cp .env.example .env
```

The chat scripts load this file automatically. Existing shell environment variables take precedence. Never commit real credentials or share your `.env`.

## 2. Run with the local model from the video

Install a current [llama.cpp](https://github.com/ggml-org/llama.cpp) build with Qwen3.5 support. On macOS, for example:

```bash
brew install llama.cpp
```

In another terminal, start the server:

```bash
llama-server \
  -hf unsloth/Qwen3.5-0.8B-GGUF:BF16 \
  --alias qwen3.5-0.8b-bf16 \
  --jinja \
  --reasoning off \
  -c 16384 --parallel 1 -ngl 999 \
  --host 127.0.0.1 --port 8080
```

**The first server launch downloads model weights** from [unsloth/Qwen3.5-0.8B-GGUF](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF). `-ngl 999` requests GPU offload where supported; adapt this flag to your hardware. Wait for the server to be ready, then run:

```bash
npm run chat:llama
```

Try the prompt used in the video:

```text
Read README.md and tell me the secret phrase.
```

**The secret phrase is: Reachy Mini is very cute.**

The `:llama` scripts select `http://127.0.0.1:8080/v1`, even if `.env` also configures OpenAI. No OpenAI key is required. To use another endpoint or a server with authentication, set `LLAMA_BASE_URL` and, if needed, `LLAMA_API_KEY` in `.env`, then use `npm run chat` or `npm run chat:resume` instead.

[`llama-provider.mjs`](llama-provider.mjs) adapts llama.cpp's OpenAI-compatible API to Pi AI. The request model ID must match the server's `--alias`. Its 16,384-token context and 2,048-token answer limit are example settings; adjust the adapter together with the server if changing models. This tiny 0.8B model is for learning, not reliable coding or complex tool use.

The recording uses `--chat-template-kwargs '{"enable_thinking":false}'`. Current llama.cpp builds warn that this is deprecated in favor of `--reasoning off`, used above. The demo sends text-only requests with thinking disabled.

## 3. Interrupt and recover

```bash
npm run chat:resume:llama
```

1. Ask the agent to read project documentation and summarize it.
2. Press **Ctrl+C while it is still working**. With a fast model, you may need a longer task to catch an unfinished request.
3. Run **the same command** again, keeping llama.cpp running.
4. The script reopens the saved conversation, resumes pending work, and displays its answer before accepting another message.

If the request already finished, restarting displays the last saved answer without another model request. Display replay occurs on every launch; it is not exactly-once delivery. The CLI awaits complete answers rather than streaming tokens.

Recovery is from **persisted checkpoints**, not a frozen JavaScript stack or shell process. Reopening SQLite alone does not supervise or restart your application: the host must run again. Tools replay only according to the harness's replay policy; external effects such as emails or payments still need idempotency or explicit recovery checks.

### Where state lives

| Command | Default SQLite database |
| --- | --- |
| `npm run chat` | `data/simple-chat/chat.sqlite` |
| `npm run chat:llama` | `data/simple-chat-llama/chat.sqlite` |
| `npm run chat:resume` | `data/terminal-chat/chat.sqlite` |
| `npm run chat:resume:llama` | `data/terminal-chat-llama/chat.sqlite` |

`CHAT_DATA_DIR=/absolute/path` overrides the data directory. Keep fresh-chat and recovery databases separate. Each directory has one owner process. Saved conversations retain their model and working directory; reopen them with the same provider available, or use a new data directory.

`harness.resume()` enables **all pending conversations in that database**, not just the displayed chat. The fresh example's first `submit()` also enables scheduling in its database, even though it does not replay older chats. Recovery with a paid provider may incur charges.

To start over without deleting anything, stop the CLI and select a new `CHAT_DATA_DIR`. Do not copy a live SQLite file alone; stop its owner first or use a SQLite-aware backup.

## Optional: use OpenAI

Set both values in your private `.env`:

```dotenv
OPENAI_MODEL=your-model-id
OPENAI_API_KEY=your-key
```

Choose a model ID supported by the pinned Pi AI catalog, then run `npm run chat` or `npm run chat:resume`. Leave `LLAMA_BASE_URL` empty to select OpenAI. **Real model requests can cost money**, including recovery of unfinished work.

## Reading the code: six setup steps

Both entry points keep the setup visible, in the same order as the video:

1. **Models:** create the model catalog and register a provider.
2. **Registry:** install `CodingTools` (`read`, `write`, `edit`, `bash`).
3. **Storage:** open SQLite.
4. **Harness:** call `Harness.open()` with models, registry, and execution environment.
5. **Conversation:** create a new one, or find and reopen the saved conversation.
6. **Input:** submit a message, await settlement, and display the answer.

The recovery example additionally inspects saved submissions and calls `harness.resume()`. Reconnecting to a submission and displaying its result is application code; resuming the scheduler does not do that automatically.

| File | Responsibility |
| --- | --- |
| `chat.mjs` | Minimal fresh conversation. |
| `chat-resume.mjs` | Saved conversation, pending submission recovery, answer replay. |
| `llama-provider.mjs` | Local llama.cpp provider configuration. |
| `chat-support.mjs` | Shared paths, execution environments, tool-call display, cleanup. |
| `terminal-input.mjs` | Interactive/piped input and signal handling. |
| `lock.mjs` | Simple local single-owner PID guard, not a distributed lock. |
| `cli-colors.mjs` | Optional terminal colors (`NO_COLOR=1` disables them). |
| `test/` | Offline tests with disposable state and scripted/mock model responses. |

## Safety and limitations

- **Tools execute locally with your user permissions, not in a sandbox.** Use a disposable working directory and review requests carefully. There is no approval UI around tool execution in this demo.
- Tool arguments are printed; transcripts and SQLite state can contain private paths, prompts, and file contents. Do not publish runtime data.
- `Ctrl+C` closes the Harness gracefully and preserves unfinished work. It is **not** a durable abort. SIGKILL/power-loss recovery is not exercised by this repository's tests.
- SQLite process-crash recovery is not a guarantee that the latest commit survives a host or power failure.
- The PID guard is a teaching convenience. PID reuse and races make it unsuitable for production locking.
- `.env`, runtime data, databases, and `node_modules` are Git-ignored. `private: true` in `package.json` prevents accidental npm publishing; the GitHub source repository is public.

## Tests

```bash
npm test
```

Tests cover fresh versus saved conversations, interrupted-request recovery, answer replay, coding tools, provider setup, local mock HTTP streaming, signal cleanup, and colors. They use temporary databases, a scripted local provider, and a mock llama.cpp endpoint. **No real model calls or downloaded weights are required.** Real-model quality and an actual llama.cpp server are not tested by this suite.

## Resources

- [Pi Durable introduction](https://earendil.com/posts/pi-durable/)
- [Pi source code](https://github.com/earendil-works/pi)
- [Pi](https://pi.dev/)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Qwen3.5-0.8B model](https://huggingface.co/Qwen/Qwen3.5-0.8B)
- [Demo GGUF weights](https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF)

The companion video URL will be added after the tutorial is published.
