# Tidbyt Internet Speed Tracker (Pi-to-Tidbyt)

A lightweight application for Raspberry Pi that pushes local internet speed results directly to a Tidbyt display. By passing data directly from your local speed-test script, this app bypasses the need for external APIs.

## ✨ Features
- **Zero-API Dependency**: Data is passed directly from your local test script to Pixlet.
- **Animated UI**: Features a bouncing download arrow.
- **Smart Stale-Handling**: Displays "NO VALUE" if the data passed is older than 60 minutes.
- **Local Automation**: Managed entirely via shell scripts on your Raspberry Pi.

---

## 🛠️ Environment Setup (Raspberry Pi)

1. **Install Pixlet**:
   ```bash
   curl -LO [https://github.com/tidbyt/pixlet/releases/download/v0.34.0/pixlet_0.34.0_linux_arm64.tar.gz](https://github.com/tidbyt/pixlet/releases/download/v0.34.0/pixlet_0.34.0_linux_arm64.tar.gz)
   tar -xvf pixlet_0.34.0_linux_arm64.tar.gz
   sudo mv pixlet /usr/local/bin/
   ```

2. **Configure Secrets**:
   Create a `.env` file in the project root:
   ```bash
   TIDBYT_DEVICE_ID="your_device_id"
   TIDBYT_API_KEY="your_api_key"
   ```

---

## 🚀 Deployment Workflow

### 1. Local Preview
To test the layout with sample data:
```bash
pixlet serve speed.star -i 0.0.0.0 -t data="2026-01-16T23:08:22Z,548912592,41435344"
```

### 2. Integrated Deployment
In your Python or Bash speed-test script, once you have your CSV string (e.g., `$LATEST_SPEED`), run:

```bash
# Load credentials
export $(grep -v '^#' .env | xargs)

# Render using the local variable
pixlet render speed.star -t data="$LATEST_SPEED"

# Push to Tidbyt
pixlet push --api-token "$TIDBYT_API_KEY" "$TIDBYT_DEVICE_ID" speed.webp --installation-id speed_tracker --background
```

---

## 📋 Data Input Format
The `-t data` flag expects: `TIMESTAMP,DOWNLOAD_BPS,UPLOAD_BPS`

**Example:** `2026-01-16T23:08:22Z,548912592,41435344`

---
*Developed using [Pixlet](https://github.com/tidbyt/pixlet).*
