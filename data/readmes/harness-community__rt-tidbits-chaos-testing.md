# RT | Tidbits | Chaos Testing 
> **Bite-sized how-to** | ~20 min setup

---

## What is Resilience Testing?

Deployments can pass all tests and still introduce regressions that only show up in production — a pod crash under load, a service that goes down when a node is drained, a dependency that causes cascading failures. By the time you notice, users are already impacted.

Harness Resilience Testing addresses this by letting you deliberately inject failures into your running system in a controlled environment. You define a fault — such as deleting a pod — and Harness injects it while probes continuously check whether your application is still functioning. The result is a **Resilience Score** that tells you exactly how well your application held up.

**How it works:**

1. You connect your Kubernetes cluster to Harness via a **Chaos Infrastructure** agent
2. Harness discovers your services and creates **Application Maps**
3. Harness generates **Chaos Experiments** — each combining a fault and a resilience probe
4. You run an experiment and view the live execution timeline
5. The **Resilience Score** is calculated from the probe results

---

## What does this Tidbit demonstrate?

A full resilience testing cycle using the Harness e-commerce Spring Boot application deployed in a fresh Kubernetes namespace:

1. **Deploy the e-commerce app** — two replicas in a new `chaos-demo` namespace
2. **Set up Chaos Infrastructure** — connect the cluster via the Expert onboarding wizard
3. **Run a Pod Delete experiment** — Harness deletes one pod and checks if the application stays healthy
4. **View the live execution** — timeline view, probe result, and Resilience Score

---

## Key Concepts

**Chaos Infrastructure** — the Harness agent deployed on your Kubernetes cluster. It receives instructions from Harness and executes fault injections.

**Application Map** — Harness's representation of the services discovered in your cluster, grouped by namespace. Used to determine what to target with experiments.

**Chaos Experiment** — the test definition combining a fault (Pod Delete) and a resilience probe (health check). Created automatically by Harness based on your discovered services.

**Fault** — the specific failure being injected. Pod Delete terminates a running pod. Kubernetes attempts to reschedule it.

**Resilience Probe** — a health check that runs continuously during the experiment. Validates whether the application is still responding. Results feed into the Resilience Score.

**Resilience Score** — a percentage calculated from probe results. 100% means the application remained fully healthy throughout the fault injection.

---

## Prerequisites

Before you start, make sure you have:

- A Harness account with the Resilience Testing module enabled
- A Kubernetes cluster with a Harness delegate running inside it
- `kubectl` installed and configured to connect to your cluster

---

## Step 1 — Deploy the E-Commerce App

Create a fresh namespace and deploy the e-commerce application with two replicas:

```bash
kubectl create namespace chaos-demo
```

```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
  namespace: chaos-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ecommerce-app
  template:
    metadata:
      labels:
        app: ecommerce-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      containers:
        - name: ecommerce-app
          image: nidayra/ecommerce-cv-app:stable
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: ecommerce-app
  namespace: chaos-demo
spec:
  selector:
    app: ecommerce-app
  ports:
    - port: 8080
      targetPort: 8080
EOF
```

Verify both pods are running:

```bash
kubectl get pods -n chaos-demo
```

You should see two pods in `Running` state.

---

## Step 2 — Set Up Chaos Infrastructure

1. Go to **Resilience Testing → Project Settings → Infrastructures**
2. Click **+ New Infrastructure**
3. You will be prompted to create a new Environment first:
   - Name: `chaos-env`
   - Environment Type: **Pre-Production**
   - Setup: **Inline**
   - Click **Save**
4. After saving the environment, Harness prompts you to configure the Infrastructure:
   - Name: `chaosinfra`
   - Select your **Kubernetes cluster connector**
   - Namespace: the namespace where the chaos agent will be deployed (e.g., `hce`)
   - Click **Next** — Harness generates the chaos agent manifest
   - Copy the manifest command and apply it to your cluster:
     ```bash
     kubectl apply -f <generated-manifest-url> -n hce
     ```
   - Wait for the infrastructure status to show **ACTIVE** in the Infrastructures list
5. Once the infrastructure is ACTIVE, click **+ New Experiment** or navigate to the **Create Chaos Experiments** wizard and select **Expert** mode, then click **Go!**

---

## Step 3 — Discover Services

Harness scans your cluster to find all running services and nodes. Wait for the discovery to complete — it scans all namespaces including `chaos-demo` where the e-commerce app is running.

Click **Next** to proceed to Application Maps.

---

## Step 4 — Create Application Maps

Select **Yes** to let Harness automatically create Application Maps from the discovered services. Harness creates one Application Map per namespace — you will see `namespace chaos-demo` with 1 service listed.

Click **Next: Create Experiments**.

---

## Step 5 — Choose Fault Types

Select **Only a few** — this creates Pod Delete and Network Chaos experiments for all discovered services. Click **Go!**.

Harness creates the experiments in the background. You will see `namespace chaos-demo → Created 1 experiment` once complete.

Click **Next** to view the Cluster Summary.

---

## Step 6 — Run the Pod Delete Experiment

1. Navigate to **Resilience Testing → Chaos Experiments**
2. Find the experiment named **ecommerce-app-pod-delete-xxxxx** (targeting the `chaos-demo` namespace)
3. Click on it to open the **Chaos Studio**

The Chaos Studio shows the experiment visually:
- **PROBE** — a pod-level health check that validates the app is still responding during the fault
- **FAULT** — the Pod Delete fault that will terminate one of the ecommerce-app pods

4. Click the green **Run** button (top right) to start the experiment

---

## Step 7 — View the Live Execution

The execution view opens automatically and shows:

- **Timeline** — a real-time view of the experiment duration
- **PROBE** — the health check running continuously, showing `Observed: Actual value: '[Pass]: AUT check passed'`
- **FAULT** — the pod delete fault injecting, showing `Target: ecommerce-app`

Watch the experiment run for approximately 2 minutes. Once complete, the **Resilience Score** appears in the top right corner.

---

## Understanding the Resilience Score

The e-commerce app was deployed with **2 replicas**. When the Pod Delete fault terminated one pod, the second replica continued serving traffic. Kubernetes rescheduled the deleted pod in the background. The probe never detected a failure — hence **100% Resilience Score**.

This is the key insight: **resilience comes from redundancy**. Deploy with a single replica and the score drops — the app is briefly unavailable during the pod reschedule window.

---

## Resources

- [Harness Resilience Testing Overview](https://developer.harness.io/docs/resilience-testing/overview/)
- [Get Started with Chaos Testing](https://developer.harness.io/docs/resilience-testing/chaos-testing/get-started/)
- [Pod Delete Fault](https://developer.harness.io/docs/chaos-engineering/faults/chaos-faults/kubernetes/pod/pod-delete/)
- [Resilience Probes](https://developer.harness.io/docs/resilience-testing/chaos-testing/probes/)
