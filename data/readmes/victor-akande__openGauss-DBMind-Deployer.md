# openGauss DBMind Deployer

An interactive deployment workbench and configuration orchestrator designed to streamline the provisioning, configuration, and background initialization of the **openGauss DBMind** autonomic monitoring and indexing engine.

---

## 🚀 Key Features

* **Dynamic Script Generation**: Automatically tailors execution scripts (`deploy_dbmind.sh` and `start_dbmind.sh`) based on host architecture (`x86_64` / `aarch64`), database endpoints, and customized ports.
* **Root-Level Startup Script**: Generates a dedicated startup script (`start_dbmind.sh`) that sets high-performance network sockets (`net.ipv4.tcp_tw_reuse=1`), terminates conflicting port bindings, switches context to the `omm` system user, and initializes all telemetry exporters and DBMind background services.
* **Component Configurations**: Generates ready-to-use configs including `dbmind.conf` and `prometheus.yml` based on UI parameters.
* **Manual Setup Guides**: Generates step-by-step documentation detailing exactly how database schema modifications, Python virtual environments, and exporters must be installed manually.

---

## 🛠️ Technology Stack

* **Frontend**: React 19, TypeScript, Vite, TailwindCSS (for sleek, responsive aesthetics), Motion (for micro-animations), Lucide React (icons).
* **Backend**: Express (Node.js runtime server) serving production assets and running dev middleware.

---

## 📋 Prerequisites

Before utilizing the generated scripts on your destination server, ensure the following requirements are met:
1. **Target Operating System**: Linux (CentOS, openEuler, Ubuntu, or RedHat).
2. **Database Engine**: A running instance of openGauss Database.
3. **Environment Context**:
   - The setup/install script `deploy_dbmind.sh` should be run under the `omm` (openGauss system database owner) user context.
   - The startup script `start_dbmind.sh` **must be run as the `root` user** to successfully modify kernel parameters (`sysctl`) and clean up port bindings.

---

## 💻 Running the Deployer Locally

### 1. Install Dependencies
Ensure Node.js is installed, then run:
```bash
npm install
```

### 2. Start the Application

#### Development Mode
To launch the Vite development server with hot-reloading:
```bash
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

#### Production Build & Run
To compile and bundle for production environments:
```bash
# Build the React frontend and server entrypoint
npm run build

# Start the Node.js production server
npm run start
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## 📄 Explanation of Generated Files

Within the graphical user interface, you can configure your deployment settings and copy or download the following configuration assets:

| Asset Name | Target Environment | Executing User | Description |
| :--- | :--- | :--- | :--- |
| **`deploy_dbmind.sh`** | Target Linux Server | `omm` | Downloads, unpacks, installs DBMind, provisions the database schema, installs Python libraries, configurations, and verifies initial exporters. |
| **`start_dbmind.sh`** | Target Linux Server | `root` | Root startup script that applies system network optimizations (`sysctl`), kills prior background processes, switches user context to `omm`, starts openGauss, Node Exporter, DBMind exporters, Prometheus Server, and the Main DBMind Service. |
| **`dbmind.conf`** | DBMind Config Path | N/A | Configuration parameters linking DBMind workers, metadata databases, agents, web interface, and timeseries endpoints. |
| **`prometheus.yml`** | Prometheus Config Path | N/A | Defines scraping endpoints and poll intervals for Prometheus to fetch metrics from openGauss, node, command, and reprocessing exporters. |
| **`Manual Guide`** | Markdown Document | Developer | Detailed manual instructions mapping step-by-step commands to replicate the installer pipeline manually. |