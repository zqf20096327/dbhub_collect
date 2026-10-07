# FME | Tidbits | SDK – Feature Flag Across 3 Languages

> **Bite-sized how-to** | ~20 min setup

---

## What is a Feature Flag?

A feature flag is a toggle that controls whether a piece of functionality is active — without deploying new code. You define the flag once in Harness FME, implement it in your application using an SDK, and then turn it on or off from the Harness UI instantly.

The same flag can be evaluated by any SDK language — Python, Java, React — all receiving the same treatment from the same central source. This is the power of centralized feature management.

---

## What does this Tidbit demonstrate?

One feature flag `show-discount-banner` implemented across three SDK languages:

- **Python (server-side)** — CLI script that prints banner status based on flag treatment
- **Java (server-side)** — Spring Boot REST endpoint that returns banner config as JSON
- **React (client-side)** — Browser app that shows or hides a discount banner component

**The demo:** Toggle the flag `on` or `off` in the Harness FME UI → all three apps respond with the new treatment instantly — no code changes, no deployments.

---

## Repository Structure

```
fme-tidbits-sdk-feature-flag/
├── python-app/
│   ├── app.py            — Python SDK implementation
│   ├── requirements.txt  — splitio_client dependency
│   └── flags.yaml        — local testing (localhost mode)
├── java-app/
│   ├── pom.xml           — Spring Boot + Split Java SDK
│   └── src/main/java/com/harness/featureflag/
│       ├── FeatureFlagApp.java
│       └── BannerController.java — GET /banner endpoint
└── react-app/
    ├── src/
    │   ├── App.js          — SplitFactory wrapper
    │   ├── DiscountBanner.js — flag-controlled banner component
    │   └── index.js
    ├── public/index.html
    └── package.json
```

---

## Prerequisites

- A Harness account with the Feature Management & Experimentation module enabled
- Python 3.x, Java 17+, Node.js 18+
- An FME environment (e.g., `Prod-nida-pract`) with the `show-discount-banner` flag created

---

## Step 1 — Create the Feature Flag in Harness FME

1. Go to **Feature Management & Experimentation → Feature Flags → + Create feature flag**
2. **Name:** `show-discount-banner`
3. **Traffic Type:** `user`
4. **Description:** `Controls the discount banner on the e-commerce store. ON shows the banner, OFF hides it.`
5. Click **Create**
6. Click **Initiate Environment** on your production environment
7. Set **Default treatment:** `off`
8. Save

---

## Step 2 — Get SDK Keys

1. Go to **FME Settings → Projects → [your project] → SDK API Keys**
2. Note the **Server-side** key — used for Python and Java
3. Note the **Client-side** key — used for React

---

## Step 3 — Run the Python App

```bash
cd python-app
pip install -r requirements.txt
```

Replace `YOUR_SERVER_SIDE_SDK_KEY` in `app.py` with your real Server-side SDK key, then:

```bash
python3 app.py
```

**Local testing (no Harness connection):**
Change `SDK_KEY = "localhost"` in `app.py` and edit `flags.yaml` to set `treatment: "on"` or `treatment: "off"`.

---

## Step 4 — Run the Java App

```bash
cd java-app
```

Create `src/main/resources/application.properties`:
```properties
fme.sdk.key=YOUR_SERVER_SIDE_SDK_KEY
```

Then:
```bash
mvn spring-boot:run
curl http://localhost:8080/banner
```

---

## Step 5 — Run the React App

Replace `YOUR_CLIENT_SIDE_SDK_KEY` in `react-app/src/App.js`, then:

```bash
cd react-app
npm install
npm start
```

Open `http://localhost:3000` — the banner shows or hides based on the flag treatment.

---

## Step 6 — Toggle the Flag

1. Go to **Feature Flags → show-discount-banner → [your environment]**
2. Change the targeting rule from `off` to `on`
3. Click **Review changes → Save**

All three apps will respond to the new treatment:
- Python — run `python3 app.py` again → `✅ DISCOUNT BANNER: ON`
- Java — `curl http://localhost:8080/banner` → `"showBanner": true`
- React — refresh the browser → green banner appears

---

## Resources

- [Harness FME Documentation](https://developer.harness.io/docs/feature-management-experimentation/)
- [Python SDK](https://help.split.io/hc/en-us/articles/360020525091-Python-SDK)
- [Java SDK](https://help.split.io/hc/en-us/articles/360020405151-Java-SDK)
- [React SDK](https://help.split.io/hc/en-us/articles/360038851551-React-SDK)
