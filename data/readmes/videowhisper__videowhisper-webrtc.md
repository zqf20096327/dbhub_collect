# VideoWhisper WebRTC Free Server

**Add live webcam broadcasting, private video calls, random matching and small
video conferences to your website.** This Node.js signaling server connects the
Free VideoWhisper browser apps and WordPress integrations, with account access,
room chat, plan limits and retry-safe usage statistics.

[Try the demos](https://consult.videowhisper.com/demo/) ·
[Free developer streaming account](https://webrtchost.com/hosting-plans/#Streaming-Only) ·
[Get setup help](https://consult.videowhisper.com/?department=Setup) ·
[Turnkey live sites](https://site2stream.com/live/)

Version **2026.11.11** · Node.js **22+** · **GPL-2.0-or-later**.
No front-end build is required for this server; the apps have their own source
and build instructions.

## Try the supported apps

### Video Conference — meet, share and invite

![Video Conference with a four-person gallery and chat](snapshots/video-conference.png)

*Current conference interface; the four fictional participants are AI-generated
marketing imagery, not a customer meeting.*

[Open Video Conference](https://demo.videowhisper.com/video-conference/) ·
[Conference source and PHP/WordPress editions](https://github.com/videowhisper/WebRTC-Video-Conference)

The Free edition supports up to four participants, camera/microphone and screen
sharing, chat, raised hands, host controls, public/private invitation links,
responsive panels and system/light/dark themes. Share the room's invite link so
participants join the same meeting. The signaling namespace is `/conference`;
roles and access are verified by the website callback, not the browser.

### Webcam Streaming — broadcast and watch

![Current webcam broadcasting interface](snapshots/webcam-broadcast-v2.png)

[Broadcast demo](https://demo.videowhisper.com/Webcam-Streaming-WebRTC/) ·
[App source](https://github.com/videowhisper/Webcam-Streaming-WebRTC)

Publish a webcam feed, share a playback URL and chat with viewers. The same app
includes dedicated broadcaster, viewer and room-chat views. Capacity depends on
peer bandwidth and account limits; this is peer-to-peer media rather than an SFU
or a packaged HLS/CDN distribution service.

### Private calls and random video chat

![Private two-way call interface](snapshots/webcam-call-v2.png)

[Private call demo](https://demo.videowhisper.com/Webcam-Streaming-WebRTC/?view=CallChat)

![Random videochat matching interface](snapshots/webcam-random-v2.png)

[Random chat demo](https://demo.videowhisper.com/Webcam-Streaming-WebRTC/?view=RandomChat)

Use a shared channel for a private call or a matching queue for RandomChat, with
camera controls, text chat and configurable filters. The three webcam screenshots
show the captured current app with AI-generated fictional video participants,
not customer sessions. The generated portraits are supplied as synthetic camera
feeds; the application renders the controls and full-frame video itself.

The established [PHP livestreaming](https://demo.videowhisper.com/vws-html5-livestreaming/)
and [PHP two-way call](https://demo.videowhisper.com/p2p-html5-videocall/)
integrations remain supported. For recording rather than live signaling, use
the separate [Webcam, Microphone & Screen Recorder](https://demo.videowhisper.com/webcam-microphone-screen-recorder/).

## Included in the Free server

- HTTPS and Socket.IO signaling for publishing, subscribing and peer negotiation.
- Legacy broadcast/playback, room/private calls, room chat and RandomChat queues.
- Opt-in conference v1, server-enforced roles, stream ownership, room limits,
  locks/removal, resynchronization and participant/session cleanup.
- Static test token, database account token and server-verified user/PIN access.
- MySQL accounts/plans, suspension and configured connection/media-profile limits.
- STUN/TURN configuration for browsers and optional native ICE diagnostics.
- Protected health/diagnostics, rate limiting and account-scoped statistics v2
  with a private durable outbox and transactional retry deduplication.

**Not included:** nginx integration, restreaming, scheduled playout, SFU media
forwarding or server-side recording. Optional-module compatibility hooks remain
for existing installations; no advanced implementation is hidden behind a Free
flag. A separate TURN service provides relay when peer connectivity requires it.

## Install and configure

1. Use Node.js 22 or newer and an HTTPS hostname. Clone this repository.
2. Install the locked core without native diagnostics:

   ```sh
   npm ci --omit=optional --ignore-scripts
   cp .env.example .env
   chmod 600 .env
   ```

3. Edit the private `.env`: set your TLS file prefix, API key and authentication.
   Generate independent random secrets locally, for example `openssl rand -hex 32`.
   The example contains no working credentials. Keep production mode enabled.
4. TLS uses `CERTIFICATE.key`, `.crt` and `.pem` (certificate/chain). The default
   listen address is loopback; review your trusted proxy or bind/firewall setup
   before external access. Configure a separate coturn service as needed.
5. For public apps, configure an account and its trusted `loginURL` callback.
   The server POSTs `{account,user,pin,token}` and expects `{login:true}` or denial.
   Verify identity and issue short-lived PINs on the website. Keep account tokens
   server-side; a shared token placed in browser config is visible to visitors.
6. For conferences, enable `CONFERENCE_ENABLED=1` and implement the additional
   expiring room/role claims in [the conference contract](docs/free-conference.md).
   The public conference PHP and WordPress hosts implement this integration.
7. Start with `npm start`, or install PM2 separately and use
   `pm2 start ecosystem.config.js --env production`. Run one signaling worker per
   account allocation. Preserve private configuration across updates.

The default `.env.example` disables database access. Set `DB_HOST`, `DB_PORT`,
`DB_NAME`, `DB_USER` and `DB_PASSWORD` for account/plan and durable statistics
storage; the database module creates its required tables. Use a dedicated
application database and inspect schema/backups before upgrades.

The optional `wrtc` package is used only for the server's ICE diagnostic, not for
browser signaling or media. A missing/unsupported native binary no longer stops
the server. Install optional dependencies only on a tested supported platform,
or set `WEBRTC_PROBE_DISABLED=1`. An unavailable probe requires a browser TURN
check; it does not certify connectivity. Existing operator-supplied
`WEBRTC_PROBE_MODULE` paths remain supported.

## Integrate and operate

| Endpoint | Access / purpose |
| --- | --- |
| `/` | Public version, available capabilities and ICE diagnostic |
| `/health` | `X-API-Key`; account, database, module and reporting health |
| `/connections`, `/channels`, `/stats`, `/status` | Operator diagnostics; API-key protection in production |
| `/update-accounts` | Protected account-cache refresh |
| `/api/stats/v2?hours=24` | Server-to-server `Authorization: Bearer ACCOUNT_TOKEN`, scoped to that account |

Keep API keys and account bearer tokens out of browser requests and public URLs.
Legacy query-key compatibility remains, but headers are preferable. See
[statistics semantics and limits](docs/statistics-v2.md): configured bitrates and
signaling durations are estimates, not measured traffic or proof of watched video.
Historical counters are preserved, not silently corrected. Abrupt termination
can lose active in-memory events/unfinished durations; durable batches retry
without double-counting.

## Test, package and update

```sh
npm test
npm run check
# Disposable loopback vws_fixture database only:
VWS_TEST_DB_PORT=3307 npm run check
npm run export:free -- /new/empty/free-source
npm run package:server
```

Tests cover legacy events, auth/denial, roles/capacity, signaling ownership,
cleanup, native-probe fallback, statistics/retries and public-source boundaries.
SQL/full HTTPS integration checks need the isolated fixture database. Real
browser media and TURN/device acceptance remain part of the release checklist.
Read [Free publishing and rollback](docs/free-publishing.md) before an upgrade.

Source publication does not upgrade any hosted server. Private configuration,
certificates, logs, media, internal development material and advanced modules are
excluded from the source export. Do not upload the repository wholesale.

## Hosting and help

[WebRTCHost](https://webrtchost.com/) provides developer and managed streaming
options. [Site2Stream live plans](https://site2stream.com/live/) combine hosting
and turnkey live-site setup. Check current service limits and availability on
the plan pages. Self-hosting does not require a VideoWhisper service account;
external streaming/TURN infrastructure and website integrations are your choice.

[Request a free consultation](https://consult.videowhisper.com/) for installation,
WordPress integration, access workflows, scaling or a custom build. Please use
[private support](SECURITY.md) for security reports. See [LICENSE](LICENSE) and
[notices](NOTICE.md).
