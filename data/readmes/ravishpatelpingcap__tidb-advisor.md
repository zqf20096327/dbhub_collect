# TiAdvisor

**Compare, Evaluate & Estimate for TiDB**

Live: [tidb-advisor.vercel.app](https://tidb-advisor.vercel.app/)

TiAdvisor is a tool for Account Executives, Solutions Engineers, and prospects to evaluate TiDB against their workload requirements. It provides data-driven recommendations across three modules.

## Modules

### Compare Databases
Side-by-side feature comparison of TiDB against 25+ databases — MySQL, PostgreSQL, Aurora, CockroachDB, Spanner, PlanetScale, Vitess, and more. Covers scalability, HA, security, AI/vector, HTAP, and ecosystem features. Filter by presets (OLTP, HTAP, Cloud-Native, etc.) or view all features with a differences-only toggle.

### Fit Assessment
A guided questionnaire that evaluates workload fit for TiDB based on pain signals — sharding complexity, write scaling, analytics gaps, and more. Produces:
- **Fit score** with clear reasoning
- **Tier recommendation** (Starter, Essential, Dedicated, BYOC, Self-Managed)
- **Compatibility warnings** and validation checklist
- **Alternative suggestions** when TiDB isn't the best fit
- **Persona-driven next steps** (developer, DBA, architect, manager)

### Cost Calculator
Estimate monthly costs across all TiDB Cloud tiers and Self-Managed deployments. Adjust compute, storage, and traffic parameters to model pricing for your workload.

## Tech Stack

- **React** + **Vite**
- Vanilla CSS (no external dependencies)
- Self-contained SVG logos (no CDN)
- Deployed on **Vercel** with auto-deploy from `main`

## Getting Started

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
```
