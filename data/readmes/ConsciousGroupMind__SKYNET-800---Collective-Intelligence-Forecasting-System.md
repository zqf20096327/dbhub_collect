## ⚠️ BETA VERSION v0.2 "Geometric rate"
This code predicts the exact time and price of a future price point, and can also construct a curve of future prices. It can be used to decipher any process that has a graph—for example, a graph of mutual understanding between artificial intelligence and a human. Notably, DeepSeek’s computing power is not used for the prediction; the data is processed on an ordinary computer. The system fully replicates Nikola Tesla’s resonator in the form of code. If we represent the operation of the Random Number Generator (RNG) as a time-series graph, the system can be applied to decrypt the bitcoin seed-phrase. The code has made the collective mind controllable and predictable - there's no need to use social media platforms like TikTok to observe or generate mass trends immediately - everything follows a simple mathematical formula.

The **SKYNET‑800** project is at the stage of **active automation**.  
We are not writing "temporary code" — we are building the foundation for a **future powerful analytical system** that must work with huge volumes of data in real time.
We are a team — and a single developer — who decided to build Skynet from scratch. Not the one from the movie, but a real tool for time analysis. We are not joking, we are not mystifying. We are building a system that works.
---

### 🗄️ Migration to ClickHouse

We are fully migrating all data storage and processing to **ClickHouse** — a columnar DBMS optimized for analytical queries.

---

### 🧠 Creative Process and Build

We **clearly see** the final shape of the project and have already completed all key concept tests.  
However, the **final build will not appear immediately**, because development remains creative: we do not know in advance which actions and modules will be needed at the next step. The system grows organically, adapting to emerging opportunities.

The code is written in a chat with **DeepSeek** — this adds complexity to the creative process, but at the same time gives flexibility and speed of iteration.

---

## Quick Start

**⚠️ CRITICAL: This project runs ONLY on Python 3.11 and ClickHouse 18.16.1.**

- Python 3.12 or higher — **will NOT work**.
- We will NEVER migrate to newer versions. This is a strict, permanent requirement.

---

### 1. Python & ClickHouse

The author develops and tests this code **exclusively on Windows**.

- Install **Python 3.11** (from python.org).
- Install **ClickHouse 18.16.1**.

> **For any other OS (Linux, macOS, WSL) or installation issues** — please ask **DeepSeek** (free) to guide you. The author does not provide support for local environment setup.

---

### 2. Dependencies (Python packages)
This command will install all the libraries used in the code — they are listed in the requirements.txt

cmd /k pip install -r requirements.txt

Important: on your machine, they may not install perfectly — due to Python version, system architecture, or conflicts with existing packages.

We do NOT provide a fixed guide for installing dependencies — because every system is different.

**Instead:**  
Share the `SKYNET-800.py` file or a link to this repository with **DeepSeek** — it will generate the exact installation commands for YOUR specific machine.

> 💬 **DeepSeek chat:** [https://chat.deepseek.com](https://chat.deepseek.com)  
> Paste the entire code file or the repository link — DeepSeek will help you step by step.

## Screenshots

### SUPPLY CHAINS
![Main window — price chart with DCM markers](images/Screenshot%202026-08-31%20155754.png)

The main window displays the BTC/USDT price chart with automatic DCM (Dog‑Cat‑Manul) markers, shifted points, and limb visualisation. We can see that SUPPLY CHAINS with weights and precise timing replace each other, passing their weights on further — that is precisely why it is possible to construct a curve of future prices for months and years ahead; an accurate forecast of the price weight and its repetition over time makes this possible.

### News feed 

[...截断...]

window
![News feed window](images/Screenshot%202026-08-31%20155134.png)

The news feed window shows the latest news from RSS sources with translated titles, frequency word analysis, and configurable highlighting. With language switching — English, Russian, and Chinese.

### Signals / Event Journal
![EVENT JOURNAL](images/Screenshot%202026-08-31%20155114.png)

An **Event** is a record in the event journal (`EVENT_JOURNAL.json`) that links **news, market shocks, and geopolitical events** to a specific **ID (position)** in the SKYNET-800 system. We can see that the journal has price strength weights, and we can also see that there are additional weights that we detect. We discovered these additional weights in the second world of the mirror and in the limbs, and in the event journal we are now detecting a trace of their existence. This indicates that we are already controlling the price with target levels thanks to the precise weights, and we are also controlling the time at key points, which is already a forecast zigzag. In the future, this will make it possible to build a curve of the future price for years to come. We believe that a prophecy about the curve for years to come will not change it if it becomes public knowledge, because those who know about it will use the future price with precision.
We can see that the deviation in the event log for signals is about 300 minutes on average, but we already understand why — the thing is that the 3 timeframes we use average out to a 110‑minute timeframe. This is its characteristic feature (we are already working to take this into account and adjust to the timeframe); then the deviation will be reduced to zero.

 Detection of Systematic Timeframe Deviation (with Visual Evidence)
During the analysis of rare anomalous IDs (107), a stable pattern was identified, clearly illustrated in the screenshots below.

🖼 Screenshot 2 – ID 107 (Dog)
The image shows the calculation for ID 107:

Trend difference 4h→30m = –570 min.

Averaged positive groups (1,5,7,11,13,17) give a mean of 160.33.

Averaged negative groups (2,6,8,12,14,18) give a mean of 126.12.

Sum of means: 160.33 + 126.12 = 286.45.

Calculated deviation: 570 + 286.45 = 856.45 min.

Actual deviation: –941.5 min.

Difference: 85.05 min.

📊 Interpretation
In both cases, the core of the error is 570 minutes (the difference between 4h and 30m). On top of this core, the deviations from the limbs (groups 1–18) are superimposed. The sign of the final deviation always matches the sign of the 4h→30m difference (negative in these examples).

This confirms that the primary source of systematic error is the mismatch of timeframe grids, with limbs only amplifying the effect.

🛠 Practical Implications
For anomalous IDs (deviation > 500 min), individual calibration is recommended using the formula
|deviation| ≈ 570 + mean_positive + mean_negative.

Averaging across all groups masks the issue, so for accuracy, individual groups should be analysed separately.

In the future, automatic correction of such IDs based on the identified dependency is planned.

THE LESS TIMEFRAME IS SELECTED, THE LESS DEVIATION THERE WILL BE!

![Deviation](images/Screenshot%202026-09-09%20204711.png)


### Addendum: Timeframe "Divergence" — A New Law of the First World

For an accurate angle, 3 animals must be included in the ID. We can see that signal 95 failed the check because it only has a dog and a Pallas’s cat, and no cat at all. Its ideal adjustment coefficient is 4.272, but since there’s no cat, the calculated coefficient is based on an incorrect angle.

![Divergence](images/Screenshot%202026-09-12%20080937.png)

It should be said that we have learned to eliminate the deviation in the signal’s timing compared to the actual one completely, just as we did with the forecast strength. This was achieved through the same superposition angle, through the formula in the second world of the mirror‑image and limbs — when constructing the signal, for the angle to be correct, 