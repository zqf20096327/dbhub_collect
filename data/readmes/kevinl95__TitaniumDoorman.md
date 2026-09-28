# TitaniumDoorman

<p align="center">
  <img src="assets/titaniumdoormanlogo.png" alt="TitaniumDoorman Logo" width="200">
</p>

[![Lint CloudFormation Template](https://github.com/kevinl95/TitaniumDoorman/actions/workflows/main.yml/badge.svg)](https://github.com/kevinl95/TitaniumDoorman/actions/workflows/main.yml)

Hardware-less doorbell for the [TiDB AgentX Hackathon](https://tidb-2025-hackathon.devpost.com). Visitors can scan a QR code → interact with an AI agent → resident gets notified via a text on their phone! No transformer, batteries, wires, or chime required. This makes it perfect for apartments, condos, or older homes. Best of all, it deploys with a single click with no coding or cloud experience required!

## Quick Deploy

[![Deploy to AWS](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=titanium-doorman&templateURL=https://titaniumdoorman.s3.us-east-1.amazonaws.com/cloudformation.yml)

**Prerequisites:**
- AWS Account with permissions for Lambda, API Gateway, SNS, S3, Secrets Manager, Bedrock
- **Enable Bedrock model access**: Go to AWS Console → Bedrock → Model access → Request access for "Titan Text G1 - Express"
- TiDB Serverless cluster (get free at [tidbcloud.com](https://tidbcloud.com))

**Setup Steps:**
1. Create TiDB Serverless cluster at [tidbcloud.com](https://tidbcloud.com)
2. Click "Connect" → "Generate Password" → copy the connection string, which is in the tab next to the `Parameters` on the connection modal
3. Click "Deploy to AWS" button above
4. Enter your TiDB connection string and notification email address
5. Deploy the stack (takes ~3 minutes)
6. **Check your email** and confirm the SNS subscription (click the confirmation link)
7. Open the "QRCodeUrl" from stack outputs
8. Print the QR code page and post by your door!
9. Done! Visitors can now scan and interact with your virtual doorman

## How It Works

<p align="center">
  <img src="assets/architecture.png" alt="TitaniumDoorman Architecture" width="800">
</p>

**Multi-Step Agentic AI Workflow:**

1. **Data Ingestion** → Visitor messages stored in TiDB with session tracking
2. **Historical Context** → Agent checks previous visits for returning visitor detection  
3. **AI Classification** → Amazon Bedrock (Titan Text Express) analyzes message context
4. **AI Response Generation** → Personalized responses based on visitor history
5. **External Actions** → Email notifications sent to resident with visit context

**Intelligence Features:**
- Recognizes returning visitors and personalizes responses
- Tracks historical visit patterns in TiDB
- Provides visit context to residents via email
- Fallback classification ensures reliability

## Architecture

- **S3 Static Website** - Visitor interface and QR code generation
- **API Gateway** - Public endpoints for visitor interactions
- **Lambda Functions** - Session management and AI agent orchestration  
- **TiDB Serverless** - Stores visits and transcripts with historical search
- **AWS Bedrock** - AI for visitor intent classification and response generation
- **SNS** - Email notifications to residents
- **Secrets Manager** - Secure TiDB credential storage