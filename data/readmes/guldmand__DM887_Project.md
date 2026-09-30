# DM887 GRPO for Control

This repository contains my DM887 Reinforcement Learning term project:

> **GRPO for Control**

The project investigates whether a variant of **Group Relative Policy Optimization (GRPO)** can be adapted to control tasks and compared against standard reinforcement learning baselines: **PPO**, **SAC**, and **TD3**.

At the current **midway/interim stage**, the final GRPO-control method has **not yet been implemented**. The current contribution is a completed and validated baseline foundation for the final comparison.

---

## Main midway submission files

The two main files for the midway submission are:  
<a href="report/DM887_Report.pdf">report/DM887_Report.pdf</a>   
<a href="notebooks/DM887_Project_GRPO_Midway_PoC.ipynb">notebooks/DM887_Project_GRPO_Midway_PoC.ipynb</a>   


The report presents the current interim write-up.

The notebook is the final report-facing midway notebook. It validates and analyzes the completed PPO/SAC/TD3 baseline results. It is read-only with respect to experiments: it loads existing result CSV files and existing figures, but does not launch training or overwrite results.

---

## What the midway submission contains

The midway submission establishes the experimental baseline foundation for the final GRPO-control comparison.

The completed midway baseline matrix is:

```text
Algorithms:   PPO, SAC, TD3
Environments: cartpole_swingup, acrobot_swingup, car_racing_continuous
Seeds:        0, 1, 2, 3, 4
Total runs:   45
Total rows:   900
```

The environments are handled through two implementation paths:

| Environment | PPO | SAC | TD3 | Implementation path |
|---|---:|---:|---:|---|
| `cartpole_swingup` | yes | yes | yes | ObjectRL vector-control workflow |
| `acrobot_swingup` | yes | yes | yes | ObjectRL vector-control workflow |
| `car_racing_continuous` | yes | yes | yes | Project-side PyTorch CNN workflow |

The vector-control environments use ObjectRL. CarRacing uses project-side CNN implementations because it is based on image observations rather than vector observations.

The midway report focuses on:

- related work and baseline motivation,
- formal RL/control methodology,
- PPO/SAC/TD3 baseline setup,
- completed baseline result validation,
- learning curves based on undiscounted evaluation episode return,
- limitations and next steps toward the final GRPO-control method.

---

## Result and figure locations

The validated midway result CSV files are stored in:

```text
results/processed/project_baselines/
```

The main midway figures are stored in:

```text
figures/midway/
```

Important midway figures:

```text
figures/midway/midway_cartpole_swingup_baselines.png
figures/midway/midway_acrobot_swingup_baselines.png
figures/midway/midway_car_racing_continuous_baselines.png
figures/midway/midway_vector_env_baselines.png
```

---

## Reproducing the midway notebook analysis

The midway notebook can be executed with:

```bash
conda run -n <ENV> python -m nbconvert \
  --to notebook \
  --execute \
  --inplace notebooks/DM887_Project_GRPO_Midway_PoC.ipynb \
  --ExecutePreprocessor.timeout=180
```

Expected validation result:

```text
45 / 45 CSV files
900 / 900 evaluation rows
3 algorithms
3 environments
5 seeds
0 missing combinations
0 execution errors
```

The notebook does not run training. It only validates and analyzes existing outputs.

---

## Recreating the baseline summary and figures

The summary CSVs and baseline plots can be regenerated from the existing processed results with:

```bash
conda run -n <ENV> python scripts/summarize_project_baselines.py --prefix midway
```

This produces or updates the midway summary outputs, including:

```text
results/processed/project_baselines/midway_vector_summary.csv

figures/midway/midway_cartpole_swingup_baselines.png
figures/midway/midway_acrobot_swingup_baselines.png
figures/midway/midway_car_racing_continuous_baselines.png
figures/midway/midway_vector_env_baselines.png
```

---

## Training scripts

The training code is kept separate from the report-facing notebook.

### Vector-control baselines

The ObjectRL-based vector-control baselines are run with:

```text
scripts/run_project_objectrl_baseline.py
```

This path is used for:

```text
cartpole_swingup
acrobot_swingup
```

Example command pattern:

```bash
conda run -n <ENV> python scripts/run_project_objectrl_baseline.py \
  --mode midway \
  --algorithm ppo \
  --project-env cartpole_swingup \
  --seed 0 \
  --run
```

### CarRacing CNN baselines

The CarRacing baselines are run through the project-side CNN implementation:

```text
scripts/run_carracing_cnn_baseline.py
scripts/carracing_cnn.py
```

This path is used for:

```text
car_racing_continuous
```

Example command pattern:

```bash
conda run -n <ENV> python scripts/run_carracing_cnn_baseline.py \
  --mode midway \
  --algorithm ppo \
  --seed 0 \
  --device cuda \
  --run
```

The CarRacing runs were executed on Google Colab with CUDA and copied back into the local repository.

---

## Notes on notebooks

The main notebook for the midway submission is:

```text
notebooks/DM887_Project_GRPO_Midway_PoC.ipynb
```

This is the final report-facing midway notebook. It validates and analyzes the completed baseline results and is the notebook that should be read together with the midway report.

The notebook:

```text
notebooks/DM887_Project_GoogleColab.ipynb
```

was used for GPU-based execution of the CarRacing CNN baselines on Google Colab with CUDA. The resulting CarRacing outputs were copied back into the local repository and are included in the validated midway result matrix.

Other notebooks in `notebooks/` are development or provenance material from earlier AI-assisted workflows. They are not required for reading or reproducing the midway report.

---


## Final project direction

The final project stage will build on the validated PPO/SAC/TD3 baseline matrix by formulating, implementing, and evaluating a GRPO-control variant under the same experimental structure.

The final report will extend the current work with:

- the concrete GRPO-control method,
- theoretical analysis,
- comparison against PPO, SAC, and TD3,
- final experimental results,
- final discussion and conclusion.


## Disclaimer: AI usage

AI tools were used extensively during this project, both for code development and report writing support.

The main AI CLI tools used were:

- Claude Code
- GitHub Copilot CLI
- OpenAI Codex

Other AI-assisted tools used were:

- OpenAI ChatGPT 5.5
- GitHub Copilot Chat extension in Visual Studio Code, especially `/plan` and `/agent` mode

AI was used for tasks such as planning the repository structure, drafting and refining code, debugging, improving notebooks, generating report-section drafts, reviewing LaTeX, improving academic wording, and checking consistency between the assignment, code, notebook, and report.

Examples of AI prompts and agent instructions are included in the `/prompts` folder.

All final implementation choices, experimental design decisions, result validation, interpretation of outputs, and report content remain my responsibility. AI tools were not used to fabricate experimental results. The reported results are based on project-generated CSV files and figures validated in the final midway notebook.