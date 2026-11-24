<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/aivision-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/aivision-logo-light.svg">
    <img src="docs/assets/aivision-logo-light.svg" width="320" alt="Ant AI Vision">
  </picture>
</p>

<p align="center">
  <em>See what your agents did. Know what to improve.</em>
</p>

<p align="center">
  Ant AI Vision is an open-source, self-hosted platform for agent observability and diagnostics.
</p>

<p align="center">
  <a href="#personal-deployment"><img src="https://img.shields.io/badge/Personal-All--in--One-3974BF?style=flat-square&amp;labelColor=273044" alt="Personal deployment: All-in-One"></a>
  <a href="#team-deployment"><img src="https://img.shields.io/badge/Teams-Docker%20%2F%20K8s-3974BF?style=flat-square&amp;labelColor=273044" alt="Team deployment: Docker or Kubernetes"></a>
  <a href="#langfuse-integration"><img src="https://img.shields.io/badge/Langfuse-SDK-548B66?style=flat-square&amp;labelColor=273044" alt="Langfuse SDK compatibility"></a>
  <a href="https://aivision.mintlify.site/en/integrations/relay"><img src="https://img.shields.io/badge/NeMo-Relay-548B66?style=flat-square&amp;labelColor=273044" alt="NVIDIA NeMo Relay integration"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-547F72?style=flat-square&amp;labelColor=273044" alt="Apache License 2.0"></a>
</p>

<p align="center">
  English · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <strong><a href="#quick-start">Quick start</a></strong> · <a href="#capabilities">What you can do</a> · <a href="#compare-langfuse">Compare with Langfuse</a> · <a href="https://aivision.mintlify.site/en/introduction">Docs</a>
</p>

Two runs of the same task both succeeded. Why did one take so much longer? Pull up the traces side by side to see what retried and where token usage went up. Once you've made a change, run the same checks on new traces to see if the problem comes back.

> Jointly developed by Ant Group’s observability team and OceanBase.

https://github.com/user-attachments/assets/d1976037-ac4b-42ba-aa10-238df307e871

> [!NOTE]
> **Personal deployment** · Send this message to an AI assistant that can run terminal commands.
>
> Use the `aivision-deploy` skill from `ob-labs/ai-vision-skills` to deploy Ant AI Vision All-in-One locally and verify that it’s running.

**Connect your agent**

- **Building your own?** Reuse supported instrumentation or follow the [integration examples](https://aivision.mintlify.site/en/integrations/frameworks) for LangGraph, Deep Agents, or Go with Eino.
- **Using an existing app?** Install the [collection plugin](https://aivision.mintlify.site/en/integrations/agents) for an app such as Codex, Claude Code, or OpenClaw to see what happens during everyday tasks.

<a id="capabilities"></a>

## 🧭 See the run. Understand it. Improve it.

- **[See the run](#see)**. Find the trace you need, narrow down long runs, and check token usage and cost.
- **[Understand it](#understand)**. See which tools ran, what the agent recalled from memory, and what changed between runs.
- **[Improve it](#improve)**. Schedule rule checks, inspect the steps behind each finding, and verify your fix.

<a id="see"></a>

### 🔎 See the run · Find the steps that matter

When traces pile up, how do you find yesterday’s slow run and work out which call held it up?

- **Start with the trace list.** Filter by agent, time, duration, status, step count, or total tokens, and sort by usage. Look up a trace by ID or search captured inputs and outputs where the data source supports it.
- **Find the right turn in a session.** Skim the conversation and open the trace for the turn you want to investigate.
- **Narrow down a long trace.** Focus on a subagent’s branch, failed tool calls, or model calls with high input token counts. The call tree keeps the matching steps’ parent paths visible, and you can save filters you use often. See the [trace investigation guide](https://aivision.mintlify.site/en/guides/traces#combine-filters-in-a-long-trace).

**Did token usage and cost change, too?** Start at the dashboard and drill down to individual calls to check for retries, longer context, or changes in cache hits. Cost details show where prices came from and which usage they cover. With [model pricing](https://aivision.mintlify.site/en/guides/model-pricing) (beta), you can recalculate estimates for past runs using the prices in effect at the time, without rerunning the agent.

<details>
<summary>How do cost estimates handle missing data and subscriptions?</summary>

Regular input, cached input, and output can have different rates. Usage or pricing that’s missing stays unknown. For subscriptions and coding plans, estimates based on published model rates are a reference. Check your bill for the amount you actually paid.

</details>

<a id="understand"></a>

### 🧩 Understand it · Follow the agent’s actions in context

In the built-in demo, both runs finish the task. In one run, a storage policy lookup times out and the agent retries it. [Compare the traces side by side](https://aivision.mintlify.site/en/guides/trace-compare) to check the failed call’s arguments and error, or compare skills, memory, and decisions. Use the call tree, graph, or timeline to see what the model received, what the tool returned, and what the agent did next.

| What to inspect | What you can see |
| --- | --- |
| [Execution](https://aivision.mintlify.site/en/guides/trace-process) | Follow messages, model output, and tool interactions in order. Open steps with source records to check inputs and outputs, and see which tools were available when their definitions were captured. |
| [MCP](https://aivision.mintlify.site/en/guides/mcp-observability) | Group calls by server and tool, then check arguments, status, latency, and errors. |
| [Skills](https://aivision.mintlify.site/en/guides/skill-observability) | See which skills loaded and tell reported calls apart from reads inferred from execution records. |
| [Memory](https://aivision.mintlify.site/en/guides/memory-observability) | See what was retrieved and where it came from. When the data is available, check whether it made it into the model input. |
| [Decisions](https://aivision.mintlify.site/en/guides/decision-traces) | Review routing or approval options and their outcomes. Look for follow-up steps linked by an explicit ID or inferred from nearby records. |

**Open the inputs and deliverables.** Check the image the model received or the report the agent produced. Traces can preview [captured images, audio, video, and PDFs](https://aivision.mintlify.site/en/guides/multimedia), plus [recognized Markdown and static HTML](https://aivision.mintlify.site/en/guides/trace-document-preview). See the [Python multimedia instrumentation example (Simplified Chinese)](ai-vision/agent-plugins/langfuse/README.md#python-多媒体-tracelangchain).

What you can inspect depends on the integration and the data it reports. The dedicated MCP, Skill, memory, and decision views are in beta.

<a id="improve"></a>

### 🛠️ Improve it · Catch recurring issues and verify fixes

You found a failed tool call or a retry. How do you tell if it keeps happening?

1. **Try a rule, then schedule it.** [Run built-in checks](https://aivision.mintlify.site/en/guides/use-diagnosers#builtin-diagnoser-overview) on a few traces to spot failed tool calls, repeated calls, or [code changes that skipped verification](https://aivision.mintlify.site/en/guides/use-diagnosers#builtin-verification-case). When the rule fits, set up [scheduled diagnostics](https://aivision.mintlify.site/en/guides/continuous-diagnosis#3-schedule-checks-that-you-have-already-validated) in a team space.
2. **[Review the evidence.](https://aivision.mintlify.site/en/guides/quality#review-one-badcase)** Use the **Quality Board** to track changes across batches. Open a BadCase and follow it back to the recorded step. Check the actual deliverable before confirming the issue, marking a false positive, or leaving it undetermined.
3. **Test the fix.** [Run similar tasks again](https://aivision.mintlify.site/en/guides/continuous-diagnosis#2-verify-an-application-fix-with-a-new-trace) and apply the same checks to the new traces.

For checks with clear acceptance criteria, run [enhanced Python rules](https://aivision.mintlify.site/en/guides/sandbox) in the optional OpenShell sandbox. Use `pytest` to check code captured in a trace, or recompute a result from a reference table. Use LLM-based diagnostics when you need to judge whether an answer is relevant or its explanation is supported.

<details>
<summary>What data do diagnostics need?</summary>

Ant AI Vision can run diagnostics on traces it has received and stored, including new traces sent through the Langfuse SDK. An external Langfuse source is read-only for this workflow. Checks may return an undetermined result when required data is missing.

</details>

<a id="compare-langfuse"></a>

## ⚖️ How does it compare with Langfuse?

Ant AI Vision focuses on investigating real runs and checking fixes on similar tasks.

- **Work out why an agent took an extra step.** Both support MCP and Skill tracing. Ant AI Vision’s [behavior views](#understand) put tool responses, memory retrieval, and routing choices in the context of a run and let you compare what changed.
- **Start with a small self-hosted setup.** The official Langfuse Docker Compose setup runs multiple services. Ant AI Vision All-in-One runs the platform and embedded seekdb in one container. The optimized image archive measured about 200 MiB compressed. You can try the built-in demo without configuring a model.
- **Run the same acceptance checks repeatedly.** Both support deterministic code checks, which can save LLM judge calls. Langfuse’s standard evaluator environment provides language standard libraries. Ant AI Vision’s [optional sandbox](https://aivision.mintlify.site/en/guides/sandbox) includes dependencies such as `pytest`, so you can check deliverables with your existing tests and reference files.

**Where Langfuse goes further.** Langfuse has more complete support for versioning prompts and skills and for running and comparing experiments on a shared dataset.

> [!NOTE]
> **What we’re working toward.** We plan to open-source data governance tools and explore ways to tune collection and retention by use case, so teams can keep enough data to debug issues and manage long-term storage costs. LangSmith SDK integration is also planned.

<a id="langfuse-integration"></a>

**Already instrumented with Langfuse?** Reuse a supported SDK and send new traces to Ant AI Vision. See the [integration guide](https://aivision.mintlify.site/en/integrations/langfuse) for supported versions, collection settings, and query coverage. Plan any historical data migration separately.

<a id="self-hosting"></a>
<a id="quick-start"></a>

## 🚀 Get to your first trace

<a id="personal-deployment"></a>

- **Personal deployment.** Use [All-in-One](https://aivision.mintlify.site/en/deployment/all-in-one) to run Ant AI Vision and embedded seekdb in one Docker container on Linux x86-64 or ARM64. Online installation requires [read access to the Skills repository](skills/README.md). An authorized offline bundle also works.
- <a id="team-deployment"></a>**Team deployment.** Run the services separately with OceanBase CE and use spaces, members, and roles to share observability and diagnostics. Deploy with [Docker](https://aivision.mintlify.site/en/deployment/docker) or follow the [Kubernetes CLI guide](https://aivision.mintlify.site/en/deployment/kubernetes) on an existing cluster with OB Operator managing OceanBase CE.
- <a id="deploy-with-skills"></a>**Use a skill or the CLI.** Use `aivision-deploy` to deploy and check the service, or `aivision-quickstart` to try collection and diagnostics on a running instance. You can also use the CLI to [deploy](https://aivision.mintlify.site/en/deployment/overview) or [query traces](https://aivision.mintlify.site/en/guides/cli).

> [!TIP]
> **[Start with the demo.](https://aivision.mintlify.site/en/try-sample#import-sample)** After you sign in, open **Demo examples** in your personal space, choose **Full walkthrough**, and create the demo data. Try trace comparison and rule checks without configuring a model. In a team space, you’ll need permission to manage Agents, issue ingest tokens, and run diagnoses.

**Send a real trace.** Use **Agent Access** to configure an SDK or runtime for [an agent you built](https://aivision.mintlify.site/en/integrations/frameworks). For an existing app, install its [plugin](https://aivision.mintlify.site/en/integrations/agents) on the machine where it runs and restart the app. In Codex, review and trust the Ant AI Vision hooks in `/hooks`, then start a new session. Run a task that calls a model and a tool, then open the new trace in **Agent traces** and check the tool call’s arguments and status.

Supported plugins offer a [Privacy collection mode](https://aivision.mintlify.site/en/guides/privacy) that filters prompts, responses, and tool inputs and outputs on the agent’s machine while retaining call structure and usage.

<details>
<summary>Which data does Privacy mode cover?</summary>

Privacy mode applies to new data collected after you enable it. Handle previously stored data and records kept by the agent itself separately.

</details>

<a id="repository"></a>

## 🤝 Contribute

> [!TIP]
> **When did you last get stuck debugging an agent?** [Open an issue](https://github.com/antgroup/ai-vision/issues) and tell us what you were looking for and where you got stuck. One concrete example is enough. If you can share the agent version, the steps you took, or a redacted trace, that helps us reproduce it.

Have an idea you’d like to try? Start a discussion or open a [pull request](https://github.com/antgroup/ai-vision/pulls) to improve integrations, views, diagnostic rules, or docs. The [contribution guide](CONTRIBUTING.md) explains how to get involved. The [source and developer index](docs/README.md) points to the implementation, and the [governance guide](GOVERNANCE.md) explains how the project is maintained. Thanks to everyone who [contributes](https://github.com/antgroup/ai-vision/graphs/contributors).
