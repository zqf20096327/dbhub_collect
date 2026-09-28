# mybutler

**Ask anything, privately. No account, no cloud, no limits.**

I built mybutler after ending up with something like a hundred open chats across ChatGPT and Claude, and no idea what was in half of them. Every new conversation started from zero, memory features cost tokens and time on every request, and there was nowhere to ask a single one-off question without it becoming part of a permanent history somewhere.

mybutler is a local-first AI assistant that lives in your menu bar. It answers through a local model running on your own machine via [Ollama](https://ollama.com), and it never sends a single question anywhere else.

## Demo

[![mybutler demo: asking a question in the Ask window](https://alexcloudstar.github.io/mybutler-website/assets/ask-my-butler-poster.jpg)](https://alexcloudstar.github.io/mybutler-website/assets/ask-my-butler.mp4)

## The problem with every other AI assistant

Chats aren't built for this. Start a new conversation and you're starting from zero, unless you go dig up the old one. Not knowing where a piece of context lives means recreating it somewhere new, so duplicates pile up. And retrieving relevant history from a large chat memory costs tokens and time, on every single request, even from the built-in memory features that are supposed to fix this.

There's also the account itself. ChatGPT, Claude's desktop app, Gemini: all of them are somebody else's server. Every question you ask leaves your machine the moment you hit enter, and it becomes part of a product you don't control.

mybutler works differently. Facts live in a local store, not inside a specific chat, so there's nothing to lose track of and nothing to duplicate.

| | mybutler | ChatGPT / Claude desktop |
|---|---|---|
| Account required | No | Yes |
| Your data leaves your machine | Never | Every message |
| Rate limits | None, it's your hardware | Yes, on free tiers |
| Works offline | Yes, after setup | No |
| Ongoing cost | Free, local compute | Free tier limits, paid plans for more |

## What it does

**Answers privately.** Every question is handled by a model running locally through Ollama. Nothing you type is sent anywhere.

**Remembers what matters, outside of any single chat.** mybutler builds a memory of facts as you use it, and scores each one by relevance, recency, and how often it actually gets used. The Ask window still shows a normal back-and-forth for that session, but closing it doesn't lose anything: what persists is the memory underneath, not the window.

**Only retrieves what's relevant, not everything.** Instead of feeding a whole memory or chat history into the model on every request, mybutler searches for what's actually relevant to the current question and compresses that into a short summary first. Retrieval itself is fast, usually well under a second; how long the actual answer takes still depends on your hardware and the local model generating it.

**Admits what it doesn't know about you.** If a question depends on a fact about you that isn't in memory, mybutler says so instead of guessing. General-knowledge questions still get answered normally either way.

**Doesn't turn a one-off question into a permanent transcript.** There's no chat log to manage or delete. mybutler still looks at everything you ask for anything worth remembering; most one-off questions just don't produce any.

**Stays out of your way.** One click from the menu bar. No tab to hunt for, no app to remember to open.

## How it works

mybutler runs as an Electron menu bar app. When you ask a question, it searches your local memory two ways at once: keyword search (SQLite FTS5) and semantic search (`sqlite-vec`), then merges the results. The relevant facts get compressed into a short, focused summary before a local model (`qwen3:14b` by default) answers, along with the last few turns of that session's conversation so follow-ups still make sense, not your whole memory at once.

## Get started

```
bun install
bun run start
```

You'll need [Ollama](https://ollama.com) running locally, with a reasoning model (`qwen3:14b`) and an embedding model (`nomic-embed-text`) pulled. mybutler opens as a menu bar icon (🎩). Click **Ask** to start.

## What's next

mybutler is provider-agnostic by design. Local is the default. Cloud is always something you turn on, never something that happens without asking.

- **Claude via API**, for anyone who wants to bring their own key.
- **Claude via a local Claude Code process**, so people who already pay for a Claude subscription get frontier-model answers without a second bill.

## Questions

**Is it free?** Yes. It runs on your own hardware with your own local models. No subscription for the core assistant.

**Does it need the internet?** Only once, to install Ollama and pull a model. After that, it works fully offline.

**What models does it support?** `qwen3:14b` and `nomic-embed-text` are what it ships with. Swapping either for a different Ollama model means editing two constants in the source, there's no settings UI for that yet.

**Is my data really private?** Yes. Nothing you ask, and nothing mybutler remembers, leaves your machine unless you explicitly turn on a cloud provider.
