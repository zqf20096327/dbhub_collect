# STO | Tidbits | Policy Enforcement

> **Bite-sized how-to** | ~10 min setup

---

> ## ⚠️ This repo pins vulnerable dependencies on purpose
>
> Both branches pin old libraries with known CVEs. **Do not** copy `requirements.txt` into a real project.
>
> | Branch | What the scan is for |
> |---|---|
> | `main` | **Pass.** A Harness Trivy scan reported 1 Critical and 4 High. The total is 5, and the policy allows 5. |
> | `more-than-five-critical` | **Fail.** Older pins, including Django 1.11, Pillow 6.2.0, and PyJWT 1.5.3, so the High + Critical total is greater than 5. |

---

## What is policy enforcement?

**Policy enforcement** is the setting on a scan step that runs a Security Tests policy **after** the scan finishes. The scanner still publishes results. The policy reads those counts and either lets the step pass or stops the pipeline.

This tidbit’s rule is a count threshold: **if High + Critical is greater than 5, fail.** Five or fewer is allowed. Six or more is a red pipeline.

`fail_on_severity` cannot express that. It fails on **any** finding at or above a severity, with no count. This pipeline sets `fail_on_severity` to `none` and puts the threshold in [`policies/fail-high-critical-over-five.rego`](./policies/fail-high-critical-over-five.rego). You attach that file to a **Policy Set** (entity **Security Tests**, event **On Step**, action **Error and exit**), then reference the set on the Trivy step under **Policy Enforcement** (`enforce.policySets`).

A zero-tolerance Critical gate is a different rule. That one is in the [policy configuration tidbit](https://github.com/harness-community/sto-tidbits-policy-configuration).

---

## Prerequisites

Before you start, make sure you have:

- A Harness account with a **Project** (note org + project identifiers).
- **STO** enabled. Permission to create **Policies** and **Policy Sets**.
- A GitHub connector that can clone this public repo. Set the connector up in the [connector usage tidbit](https://university-registration.harness.io/self-paced-training-tidbit-introduction-to-cd-connector-usage). This tidbit does not cover connector setup.
- Harness Cloud build credits.

---

## Step 1 — Look at the two scan targets

The scan input is [`requirements.txt`](./requirements.txt). The same pipeline runs either branch. You do not need a fork.

- **`main`** keeps a small pin set. The recorded scan is 1 Critical and 4 High, total 5, so the policy allows it.
- **`more-than-five-critical`** swaps in older pins (Django 1.11, Pillow 6.2.0, PyYAML 5.1, cryptography 2.3, lxml 4.2.1, PyJWT 1.5.3, paramiko 2.0.0, pycrypto 2.6.1, and similar) so the total is greater than 5.

If you do not have a GitHub connector yet, create one in the [connector usage tidbit](https://university-registration.harness.io/self-paced-training-tidbit-introduction-to-cd-connector-usage).

---

## Step 2 — Create the policy

1. **Project Settings → Policies → New Policy** (or Account/Org Policies, same idea).
2. Name it `Fail over five High or Critical`.
3. Paste [`policies/fail-high-critical-over-five.rego`](./policies/fail-high-critical-over-five.rego).
4. Save.

That file adds `CRITICAL` and `HIGH` from the scan output. `total > 5` → deny.

---

## Step 3 — Create the Policy Set

1. **Policies → Policy Sets → New Policy Set**.
2. Name: `STO High Critical Over Five`. The identifier must be `STO_High_Critical_Over_Five`. That is the id the pipeline references.
3. **Entity type:** Security Tests. **Pipeline / On Run** does not see the scan output, so the policy passes.
4. **Event:** On Step.
5. **Add Policy:** `Fail over five High or Critical`.
6. **Action:** Error and exit.
7. Finish. Leave the set **Enforced**.

---

## Step 4 — Import the pipeline

1. **Pipelines → Create a Pipeline** → YAML.
2. Paste [`.harness/pipeline.yaml`](./.harness/pipeline.yaml).
3. Set org and project. `repoName` stays `harness-community/sto-tidbits-policy-enforcement`. Branch is a runtime input.
4. Save.

`fail_on_severity` is `none`, so Trivy publishes results and the scan command itself does not fail the step. Under **Policy Enforcement**, `enforce.policySets` lists `STO_High_Critical_Over_Five`. That set is what blocks the step when the count is greater than 5.

---

## Step 5 — Run both branches

**Run** twice. Same Git connector and repo. Change only the branch.

### Pass — branch `main`

Trivy finishes. Open **Trivy SCA**, then **Policy Enforcement**. The recorded counts are 1 Critical and 4 High. The total is 5, and the rule is `total > 5`, so the set allows the step. The pipeline is green.

**Green is the correct outcome on `main`.**

### Fail — branch `more-than-five-critical`

Run again and set the branch to `more-than-five-critical`. Trivy finishes. Policy Enforcement denies with `Fail: N High/Critical issue(s). Threshold is 5.` The pipeline is red.

**Red is the correct outcome on this branch.** The scan still published the findings. The policy stopped the pipeline. The exact count follows Trivy’s database.

---

## Policy and pipeline reference

[`policies/fail-high-critical-over-five.rego`](./policies/fail-high-critical-over-five.rego):

```rego
package securityTests

deny[msg] {
  input[i].name == "output"
  critical := to_number(input[i].outcome.outputVariables.CRITICAL)
  high := to_number(input[i].outcome.outputVariables.HIGH)
  total := critical + high
  total > 5
  msg := sprintf("Fail: %d High/Critical issue(s). Threshold is 5.", [total])
}
```

[`.harness/pipeline.yaml`](./.harness/pipeline.yaml) — Aqua Trivy on this public repo, branch `<+input>`, `fail_on_severity: none`, and `enforce.policySets: STO_High_Critical_Over_Five`.

---

## Common Issues & Tips

**`main` is green.** That is the pass case. 1 Critical + 4 High is not greater than 5.

**`more-than-five-critical` is red.** That is the fail case. Open the step’s policy evaluation and read the High + Critical total.

**Pipeline is green and Security Tests shows more than five High or Critical findings.** The step’s `enforce.policySets` id does not match the set, the set is not Enforced, the entity is not **Security Tests**, or the event is not **On Step**. **Pipeline / On Run** evaluates the pipeline, not the scan output, so that set stays green.

**You wanted any Critical to fail, with no count.** Use the [policy configuration tidbit](https://github.com/harness-community/sto-tidbits-policy-configuration). `fail_on_severity: high` also fails on any High or Critical, and it fails inside the scan command, before policy evaluation.

**Want a different budget.** Change `total > 5` and the message. The policy set identifier can stay the same.

---

## What's next?

- **Warn & continue** on the Policy Set instead of Error and exit — same threshold, no hard fail.
- Block only **new** findings with `NEW_CRITICAL` and `NEW_HIGH` once a baseline exists.
- [Exemptions](https://developer.harness.io/docs/security-testing-orchestration/get-started/key-concepts/exemptions/) for a finding you accept so it drops out of the count you care about.

---

## Resources

- [Policy as Code for Security Tests](https://developer.harness.io/docs/platform/governance/policy-as-code/policy-as-code-for-security-tests/)
- [Create OPA policies for STO](https://developer.harness.io/docs/security-testing-orchestration/policies/create-opa-policies/)
- [Enforce OPA policies](https://developer.harness.io/docs/security-testing-orchestration/policies/enforce-opa-policies/)
- [Fail pipelines based on scan results](https://developer.harness.io/docs/security-testing-orchestration/key-concepts/fail-pipelines-by-severity/)
- [Aqua Trivy step](https://developer.harness.io/docs/security-testing-orchestration/sto-techref-category/trivy/aqua-trivy-scanner-reference/)
