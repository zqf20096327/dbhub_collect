# TiDB Cloud Demos

Three production-ready demos showcasing TiDB Cloud Serverless — "Kill Your Data Pipeline" concept.
Each demo includes a live dashboard, a Playwright recorder, and a narration script for generating a demo video.

## Demos

| Folder | Theme | Audience |
|--------|-------|----------|
| `demo-fintech/` | Real-time payment processing | Fintech engineering teams |
| `demo-ecommerce/` | Live order analytics | VP / executive stakeholders |
| `demo-iot/` | IoT sensor data | Developer meetups / talks |

## Requirements

```bash
pip3 install flask pymysql python-dotenv playwright
python3 -m playwright install chromium
brew install ffmpeg   # for narrated video
```

## Running a Demo

Each folder is self-contained. Steps are the same for all three:

**1. Configure credentials**
```bash
cd demo-fintech          # or demo-ecommerce / demo-iot
cp .env.example .env
# Edit .env with your TiDB Cloud credentials
```

**2. Start the dashboard** (Terminal 1)
```bash
python3 tidb_demo.py     # or tidb_ecommerce_demo.py / tidb_iot_demo.py
# Open http://localhost:5001
```

**3. Record the demo video** (Terminal 2)
```bash
python3 demo_record.py
# When done: ffmpeg -i demo_recording/*.webm tidb-demo.mp4
```

**4. Add narration**
```bash
python3 add_narration.py
# Output: tidb-demo-narrated.mp4
```

## TiDB Cloud Credentials

Your `.env` should look like:

```
TIDB_HOST=gateway01.us-east-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=<prefix>.root
TIDB_PASSWORD=your_password
TIDB_DATABASE=FinanceDB       # or OrdersDB / IoTData
TIDB_SSL_CA=/etc/ssl/cert.pem
```

> The `TIDB_USER` must include the cluster prefix (e.g. `3XcPuW3ssBWXGgP.root`).
> Find it in TiDB Cloud Console → your cluster → Connect.

The database is created automatically on first run if it doesn't exist.
