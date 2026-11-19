<div align="center">

<img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/crumb.png" alt="AgentCake" width="112">

# AgentCake — AI Agent Traffic Analytics

[![Releases: download](https://img.shields.io/badge/Releases-download-ff5c8a?style=flat)](https://github.com/tartini-ai/agent-traffic-analytics/releases)
[![Issues: report a bug](https://img.shields.io/badge/Issues-report%20a%20bug-ff5c8a?style=flat)](https://github.com/tartini-ai/agent-traffic-analytics/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-ff5c8a?style=flat)](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/LICENSE)

**English** · [简体中文](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/docs/locales/zh-CN/README.md)

</div>

## The problem

Is your website getting plenty of traffic, but your conversion rate is staying the same or even decreasing? Could some
of those visits be coming from AI agents?

HUMAN Security found that
[traffic from AI agents and agentic browsers grew 7,851% year over year](https://www.humansecurity.com/newsroom/2026-state-of-ai-traffic-cyberthreat-benchmark-report/).
If your analytics can't recognize these agents, their visits may be counted as human traffic, making your daily
reports misleading.

## The solution

We've launched AgentCake, a self-hosted AI agent traffic analytics platform. It records each visit as a session replay.
Our behavioral model and rules then identify whether a human, an AI agent or both drove each session.

Here's what AgentCake can help you understand:

1. **What AI agents found**: See which pages AI agents viewed and whether they found the information they needed. Find
   out whether they only browsed or began signing up.
2. **Where AI agents got stuck**: See the steps where agents stopped. Then decide whether to adapt those steps to make
   your website more agent-friendly.
3. **Which AI agents visit most**: See which agents visit your website most often, such as Claude in Chrome, Grok Bot
   and Muse. Use what you learn to optimize your website for them and increase conversions.

![This animation scrolls through the dashboard, opens the session list, then replays a hand-off from Claude in Chrome to a human.](https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/demo.png)

*The recording shows Claude in Chrome adding a T-shirt to the cart on a test shop and a human taking over to check out.*

### Dashboard preview

<!-- The line of no-break spaces under each picture keeps it this wide: without it a browser shrinks the six to fit one row instead of letting the row scroll sideways. -->
<table>
  <tr>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-key-metrics.png" alt="Key metrics" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-top-agents.png" alt="Top agents and Trends" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-paths.png" alt="Paths and Sources" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-devices.png" alt="Devices and Geography" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-sessions.png" alt="Session replay" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
    <td width="720">
      <img src="https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/main/docs/assets/readme/preview-session-replay.png" alt="Session replay: Claude in Chrome, then a human" width="720"><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
</table>

- **Human, AI agent or bot**: AgentCake gives each session a single classification. Agent sessions are
  split into Agent only and Human + agent.
- **Agent names and confidence levels**: AgentCake identifies agents by name, such as Claude in Chrome, ChatGPT and
  Muse, and labels each name Verified or Likely. Agents it can't identify appear as Unnamed.
- **Timeline and reasons**: A timeline shows when a human or an agent was in control during each session and marks
  each hand-off. Next to the replay, you can view the reasons for each classification.
- **Human and agent traffic**: See sessions, visitors, page views and active time for humans and agents. Break down
  the traffic by path, source, device and geography.
- **Self-hosted and open source**: AgentCake runs on your computer or server as a single program. It uses one SQLite
  database and sends no telemetry. The code is available under the MIT License.

## Install

Open Claude Code, Codex or another coding agent in a new, empty folder and paste these instructions:

```text
Install AgentCake 0.5.1 by following the guide at https://raw.githubusercontent.com/tartini-ai/agent-traffic-analytics/v0.5.1/INSTALL.md step by step.
Use curl or the GitHub CLI to download the guide.
Finally, print the address of the AgentCake local page and the steps to connect a website.
```

Your agent downloads the release and verifies it. The agent then starts AgentCake and runs `agentcake doctor`, which
checks that the installation works.

Next, open http://127.0.0.1:7878/ and register your installation. The page guides you through connecting your website.

AgentCake runs on macOS and Linux and requires uv or Python 3.11 or later. To install manually, follow the steps in
[`INSTALL.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/INSTALL.md).

## How it decides

To identify agent sessions and the agents behind them, AgentCake checks four layers of evidence on your machine.

- **Name**: AgentCake matches the name in the User-Agent string against the agent lists included in each release.
- **Verification**: On a server, AgentCake verifies self-reported agent names with request signatures and published IP
  ranges.
- **Environment**: AgentCake detects automation traces, spoofed browsers and the page markers that some agents add.
- **Behavior**: Our behavioral model analyzes pointer movement, keyboard timing and scrolling for every action in a
  session.

AgentCake's test data includes 1,118 agent sessions from our own recordings and 7,122 human sessions. AgentCake can
make mistakes, and we're continuing to improve the model's performance.

For details on how each number is counted, see the
[evaluation report](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/eval/README.md).

## Your data stays yours

The page script sends visit data only to your own AgentCake installation. The installation doesn't send any usage data.
AgentCake accesses the internet only when you register, update its agent lists or run a site check.

AgentCake doesn't record what visitors type or which keys they press. It also doesn't record passwords, card numbers,
cookies or IP addresses.

To count visitors, AgentCake stores a random ID in each visitor's browser without using a cookie. The ID expires a year
after the visitor's last visit. AgentCake keeps only the domain of the referring page.

AgentCake sends your registration details only once, when you select **Register and continue**. AgentCake records visits
whether or not you register.

For details about how AgentCake handles data, see [`PRIVACY.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/PRIVACY.md).
To inform your visitors, you can use the template in
[`docs/privacy-notice-template.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/docs/privacy-notice-template.md).

## Connect your website

After you register, copy the setup instructions from the local page. Open a coding agent in your website's project
folder, and paste the instructions. The agent asks for your website's address and the machine that will run AgentCake.

To load cake.js on every page, the agent adds one line of code to your shared page layout. The cake.js script is 48 KB
gzipped. The agent can also add server middleware for Next.js, Express, Flask, FastAPI, Django, PHP and WordPress.

You can also complete these steps manually.

For a public website, run AgentCake on a server with Docker or systemd. Open the dashboard through an SSH tunnel to keep
it private. For step-by-step instructions, see
[`SERVER.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/SERVER.md).

## Help and contributing

For answers to common questions, see [`docs/FAQ.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/docs/FAQ.md).
If AgentCake misclassifies a session or doesn't recognize an agent, open an
[issue](https://github.com/tartini-ai/agent-traffic-analytics/issues/new?template=wrong_verdict.yml).
Describe what happened without including any visitor data.

The rules and the model's parameters are JSON files in `agentcake/data/`. When you send a pull request, include the
`agentcake eval` results from before and after your change. A pull request is merged only if it does not increase the
number of humans classified as agents.

For contribution guidelines, see [`CONTRIBUTING.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/CONTRIBUTING.md).
For coding agent instructions, see [`AGENTS.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/AGENTS.md).

To report a security vulnerability, email [admin@tartini.ai](mailto:admin@tartini.ai) instead of opening an issue. For
more information, see [`SECURITY.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/SECURITY.md).

## License

AgentCake is released under the MIT License, copyright Tartini AI. For the full license, see
[`LICENSE`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/LICENSE).

Third-party components bundled with AgentCake retain their respective licenses. For the list, see
[`THIRD_PARTY.md`](https://github.com/tartini-ai/agent-traffic-analytics/blob/v0.5.1/THIRD_PARTY.md).

<sub>AgentCake is an independent product and isn't affiliated with the developers of the agents and tools it names.
Those developers don't endorse or sponsor AgentCake. All trademarks belong to their owners.</sub>
