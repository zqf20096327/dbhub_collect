# Notion Worker: Tidbyt Message Screen

This repository contains a Notion Worker (TypeScript) that exposes one tool:

- `setTidbytMessageScreen({ message, iconKeyword?, iconColor? })`

The tool normalizes and validates a message, renders it into a simple high-contrast 64x32 PNG, and pushes that image to a fixed Tidbyt app installation slot so your Tidbyt rotation always shows the newest message for that slot.

## Example
![Screenshot](images/tidbyt.jpeg)

## Notion Workers SDK wiring

This worker uses the template-style SDK pattern:

- `import { Worker } from "@notionhq/workers"`
- `const worker = new Worker();`
- `worker.tool("setTidbytMessageScreen", { ... })`
- `export default worker`

## What the tool does

1. Validates `message` is a non-empty string.
2. Normalizes whitespace (`trim` + collapse multiple whitespace to single spaces).
3. Enforces max length (`MAX_MESSAGE_LENGTH`, default 180 chars), truncating with `…` if needed.
4. Optionally builds a Notion custom agent avatar URL from `iconKeyword` + `iconColor`.
5. Looks up a bundled local PNG icon (generated offline from the Notion avatar URL pattern).
6. Falls back to bundled `mailbox-green` when the requested icon is missing.
7. Renders the final output to a 64x32 PNG (24x24 icon on the left when available).
8. Calls Tidbyt API to update a dedicated app installation.
9. Dedupe in-memory by hashing the final displayed message plus icon selector (if the worker instance stays warm, duplicate payloads are skipped).

Tool return shape:

```json
{ "ok": true, "displayedMessage": "...", "iconRendered": true, "iconUrl": "..." }
```

## Tidbyt API details used

This worker uses Tidbyt's push endpoint:

- `POST https://api.tidbyt.com/v0/devices/{TIDBYT_DEVICE_ID}/push`

Request body fields used:

- `installationID` (from `TIDBYT_INSTALLATION_ID`) to target a specific installed app slot.
- `image` (base64 PNG bytes).
- `background` (optional boolean, from `TIDBYT_BACKGROUND`, defaults to `false`).

### Required identifiers / env vars

Set these with `ntn workers env set` (never commit secrets):

- `TIDBYT_API_TOKEN` (Tidbyt bearer token)
- `TIDBYT_DEVICE_ID` (target device ID)
- `TIDBYT_INSTALLATION_ID` (the app installation/slot ID to overwrite)

Optional:

- `TIDBYT_BACKGROUND` (`true` or `false`)

> If your Tidbyt account/API surfaces different naming for slot/install IDs, use that value in `TIDBYT_INSTALLATION_ID`.

## Custom agent icon selector

The tool can optionally render a Notion custom agent avatar next to the message using:

- `iconKeyword` (example: `alarm`)
- `iconColor` (example: `green`)

Note: the Notion Workers SDK requires all schema properties to be present, so callers
should pass `null` for `iconKeyword` and `iconColor` when no icon is desired.

When both are provided, the worker builds:

- `https://www.notion.so/images/customAgentAvatars/{iconKeyword}-{iconColor}.webp`

At runtime, the worker renders from a bundled PNG icon set generated offline from this URL pattern.

If the requested selector is unavailable in the bundled icon set, the worker falls back to:

- `https://www.notion.so/images/customAgentAvatars/mailbox-green.webp`

If the bundled fallback icon also fails to load, the worker still pushes a text-only frame.

## Image format + rendering approach

- Format sent: **PNG**, base64-encoded in the `image` field.
- Resolution: **64x32**.
- Renderer: built-in Tronbyt/Tidbyt-style 5x7 bitmap font in `src/index.ts` (no native binaries).
- Styling: white text on black background for high contrast.
- Icon layout: 24x24 icon on the left, text region on the right.

## Message/wrapping limitations

- Hard cap: 180 characters before rendering (`MAX_MESSAGE_LENGTH`).
- Font is fixed-width 5x7 with 1px spacing.
- Text is capped to 3 visible lines and truncates with `…` on the 3rd line.
- With the current icon layout, practical capacity is very small (roughly 3 short lines, ~6 chars/line).

## Icon asset generation (setup requirement)

The worker bundles icon PNG bytes in `src/custom-agent-icon-pngs.generated.ts`.

Regenerate the bundled icon set before first deploy (and whenever you change icon assets):

```bash
npm run icons:build
```

This script downloads/caches Notion avatar WebPs, extracts frame 1 from animated WebPs, converts to PNG, resizes to 24x24, and regenerates the bundled TS file.

`generated/` is local build output/cache only and is not required at runtime once `src/custom-agent-icon-pngs.generated.ts` exists.

## Local usage (manual test)

```bash
# Example tool invocation after `ntn workers dev` or deployed worker context
ntn workers exec setTidbytMessageScreen --data '{"message":"Consistency compounds. Keep going.","iconKeyword":"alarm","iconColor":"green"}'
```

See [DEPLOY.md](./DEPLOY.md) for full setup and deployment.

## Custom Agent snippet

Copy from [AGENT_SNIPPET.md](./AGENT_SNIPPET.md).

## Custom Agent tool-call instructions (Notion)

Add this exact block to your Custom Agent instructions if you want it to trigger the tool with a fixed message/icon:

```text
When asked to run, call the notion-to-tidbyt tool

Use exactly:
- message: “Custom Agent Ran!”
- iconKeyword: "rock"
- iconColor: "blue"

Do not add any other text before or after the tool call.
Do not vary capitalization or punctuation.
```

Cost note:

- A Custom Agent that only performs this tool call averages about **6.3 credits per call**.

## Acceptance checklist

Copy from [ACCEPTANCE_TEST_CHECKLIST.md](./ACCEPTANCE_TEST_CHECKLIST.md).
