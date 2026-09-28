# Multi-user RAG Chat in Azure

## Introduction

Multiuser RAG Chat uses [Neon Serverless Postgres](https://learn.microsoft.com/en-us/azure/partner-solutions/neon/overview) on Azure to allow organizations to deploy a private chat tenant in their Azure Subscription with a dedicated database per user on Neon. It is a modified version of [Azure Chat Solution Accelerator](https://github.com/microsoft/azurechat) with [Neon](https://neon.tech/) for chat data storage and search functionality.

![Tenant AI Chat Solution Accelerator with Neon](/assets/Multiuser%20AI%20Chat%20Solution%20Accelerator%20App%20View%201.png)

## Features

- 📀 **Database per user**: Keeps chat data isolated by creating a separate database instance per user.
- 🔑 **Authentication and User Management**: Allows flexible login options, including OAuth providers like Google, GitHub, and Microsoft Entra ID (Azure AD).
- 🧠 **AI-Powered Conversations**: Chat with documents such as PDF. You can also build your own prompt templates.
- 💾 **Chat History**: Stores chat history with multiple chat threads, messages, and metadata.
- 🎨 **Customizable Chat Personas**: Personalizes conversations with user-defined chat personas. Manage persona settings directly from the application interface.
- 🛠️ **Extensions Support**: Extends chat functionalities by defining custom extensions. Store and manage extensions in the database, allowing dynamic interaction with custom workflows.
- 🎙️ **Speech and Voice Support**: Enables multilingual voice interactions in the chat application. Integrate Azure Speech Service for speech-to-text and text-to-speech capabilities.
- 🌐 **Deployment-Ready Architecture**: Fully deployable to Azure App Service with scalability for enterprise workloads.

## Demo

![Azure Tenant AI Chat Solution Accelerator Demo](/assets/Neon%20Tenant%20AI%20Chat%20Demo.gif)

## Solution Benefits

- **Private**: Offers both application and database level isolation with the standalone single-tenant app with a single-tenant database. You can use it with your own internal data sources (PDFs, Docs) or integrate with your internal services (APIs)
- **Cost-Efficient**: Combines relational storage, and vector storage in a single platform reduces the need for additional services, lowering costs. Scale efficiently as your user base grows while keeping costs manageable.



## Technologies Used

### Azure Services

| **Service**                        | **Usage in the Project**                                                                                                     |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **Azure OpenAI**                    | Provides models like GPT-4o for generating AI-powered conversational responses and vector embeddings for semantic search. |
| **Azure Key Vault**                 | Securely stores sensitive information such as API keys, secrets, and connection strings. Used for authentication and APIs.    |
| **Azure Blob Storage**              | Handles file storage and uploads for documents or media used in the chat system. Scalable solution for data backups.         |
| **Azure App Service**               | Hosts the web application, REST APIs, and back-end services. Provides a managed environment to deploy and run the solution.   |
| **Azure Monitor**                   | Tracks and monitors application performance, errors, and logs. Helps in diagnosing issues and optimizing performance.         |
| **Microsoft Entra ID (Azure AD)**   | Provides secure user authentication and authorization through OAuth2.0. Integrates with organizational identity systems.       |
| **Azure Document Intelligence**     | Automates data extraction from uploaded documents using AI and OCR (Optical Character Recognition).                          |
| **Azure Speech Service**            | Converts speech to text and vice versa, enabling voice commands or responses in the chat system. Supports multilingual use.   |


### Development Tools

- [Node.js 18](https://nodejs.org/en): an open-source, cross-platform JavaScript runtime environment.

- [Next.js 13](https://nextjs.org/docs): enables you to create full-stack web applications by extending the latest React features

- [NextAuth.js](https://next-auth.js.org/): configurable authentication framework for Next.js 13

- [OpenAI sdk](https://github.com/openai/openai-node) NodeJS library that simplifies building conversational UI

- [Tailwind CSS](https://tailwindcss.com/): is a utility-first CSS framework that provides a series of predefined classes that can be used to style each element by mixing and matching

- [shadcn/ui](https://ui.shadcn.com/): re-usable components built using Radix UI and Tailwind CSS. 


## Solution Architecture

The following high-level diagram depicts the architecture of the solution accelerator:

![Azure Tenant AI Chat solution Architecture](/assets/Multiuser%20AI%20Chat%20Solution%20Accelerator%20App%20View%202.png)

## 👨🏻‍💻 Run Locally

Clone this repository locally or fork it to your Github account.

### Prerequisites

- Neon Account: Create a Neon account on [Neon Console](https://console.neon.tech/) or via the [Azure](https://fyi.neon.tech/azureportal). If you have created your Azure resources using the [Deployment Options](#deployment-options) in this repo, it will create automatically Neon instance on Azure.

- Identity Provider (Optional): For local development, you do not need it. If you prefer to use an Identity Provider, [follow the instructions](/docs/add-identity.md) to configure one.

### Steps

1. Change directory to the `src` folder
2. Rename the file `.env.example` to `.env.local` and populate the environment variables (At least [Azure OpenAI service](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Capi-key%2Cjavascript-keyless%2Ctypescript-keyless%2Cpython-new&pivots=programming-language-typescript#retrieve-resource-information) to test out AI Chat feature).
3. Retrive the Neon API Key: Create [create a new API Key](https://neon.tech/docs/manage/api-keys#creating-api-keys) and set it in the `.env.local ` file to the value of `NEON_API_KEY`.
4. Install npm packages by running `npm install`
5. Start the app by running `npm run dev`
6. It automatically creates a new database for each new user on Neon database and populates schemas from `./data/schema.sql` SQL file used in the application.
7. Access the app on [http://localhost:3000](http://localhost:3000)

> [!NOTE]
> If using Basic Auth (DEV ONLY) any username you enter will create a new user id (hash of username@localhost). You can use this to simulate multiple users. Once successfully logged in, you can start creating new conversations.


## Deployment Options

### Prerequisites

- **Azure account**. If you're new to Azure, [get an Azure account for free](https://azure.microsoft.com/free/cognitive-search/) and you'll get some free Azure credits to get started.
 - Your Azure account must have `Microsoft.Authorization/roleAssignments/write` permissions, such as [Role Based Access Control Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview), [User Access Administrator](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#user-access-administrator), or [Owner](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#owner). If you don't have subscription-level permissions, you must be granted [RBAC](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles#role-based-access-control-administrator-preview) for an existing resource group and [deploy to that existing group](docs/deploy_existing.md#resource-group).
  - Your Azure account also needs `Microsoft.Resources/deployments/write` permissions on the subscription level.

You can deploy the application using one of the following options:

- [1. Azure Developer CLI](#azure-developer-cli)
- [2. Azure Portal Deployment](#azure-portal-deployment)

### 1. Azure Developer CLI

> [!IMPORTANT]
> This section will create Azure resources and deploy the solution from your local environment using the Azure Developer CLI. Note that you do not need to clone this repo to complete these steps.

1. Download the [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)
2. Run `azd auth login` and log in using your Azure account credentials.
3. If you have not cloned this repo, run `azd init -t https://github.com/neondatabase-labs/azure-tenant-ai-chat`. If you have cloned this repo, just run 'azd init' from the repo root directory.
4. Run `azd up` to provision and deploy the application.
5. To complete the application setup and run it successfully, you will need to follow [Application Settings Setup](#application-settings-setup) guide.

### 2. Azure Portal Deployment

> [!WARNING]
> This button will only create Azure resources. You will still need to deploy the application by following the [deploy to Azure section](/docs/deploy-to-azure-github-actions.md) to build and deploy the application using GitHub actions.

Click on the Deploy to Azure button to deploy the Azure resources for the application.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fneondatabase-labs%2Fazure-tenant-ai-chat%2Fmain%2Finfra%2Fmain.json)

> [!IMPORTANT]
> The application is protected by an identity provider and follow the steps in [Add an identity provider](/docs/add-identity.md) section for adding authentication to your app.

## Application Settings Setup

Open running Azure Web App service [App Settings](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal) page and populate the environment variables manually.  

### Configure GitHub as an identity provider

  1. Navigate to GitHub OAuth Apps setup https://github.com/settings/developers
  2. Create a `New OAuth App` https://github.com/settings/applications/new
  3. Fill in the following details

   ```default
   Application name:  Production
   Homepage URL: https://YOUR-WEBSITE-NAME.azurewebsites.net
   Authorization callback URL: https://YOUR-WEBSITE-NAME.azurewebsites.net/api/auth/callback/github
   ```

  > [!NOTE]
  > After completing the above step, ensure that you set `AUTH_GITHUB_ID` and `AUTH_GITHUB_SECRET` to Azure Web App environment variables.

### Retrive the Neon API Key
  
  1. From [Azure portal](https://portal.azure.com/), find the Neon Serverless Postgres Organization service and click on the Portal URL that brings you to the Neon Console.
  2. Create [create a new API Key](https://neon.tech/docs/manage/api-keys#creating-api-keys) and add in the Azure Web App environment variables to the value of `NEON_API_KEY`.

### [Optional] Review other services

Check other services connection details are correctly set. At least [Azure OpenAI service](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Capi-key%2Cjavascript-keyless%2Ctypescript-keyless%2Cpython-new&pivots=programming-language-typescript#retrieve-resource-information) to test out AI Chat feature.


## Azure Deployment Costs

Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.
However, you can try the [Azure pricing calculator - Sample Estimate](https://azure.com/e/6575aeb258c54e9a84e06e90d4a0ab0c) for the resources below.

- Neon Serverless Postgres: Free US$0.00/month, free plan includes 10 projects, 0.5 GB storage, 190 compute hours, autoscaling up to 2 CU, read replicas, 90+ Postgres extensions including pgvector extension.
- Azure App Service: Premium V3 Tier 1 CPU core, 4 GB RAM, 250 GB Storage. Pricing per hour. [Pricing](https://azure.microsoft.com/pricing/details/app-service/linux/)
- Azure Open AI: Standard tier, ChatGPT and Embedding models. Pricing per 1K tokens used, and at least 1K tokens are used per question. [Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- Form Recognizer: SO (Standard) tier using pre-built layout. Pricing per document page, sample documents have 261 pages total. [Pricing](https://azure.microsoft.com/pricing/details/form-recognizer/)
- Azure Monitor: Pay-as-you-go tier. Costs based on data ingested. [Pricing](https://azure.microsoft.com/pricing/details/monitor/)

To reduce costs, you can switch to free SKUs for Azure App Service and Form Recognizer by changing the parameters file under the `./infra` folder. There are some limits to consider; for example, you can have the free Form Recognizer resource only analyzes the first 2 pages of each document. You can also reduce costs associated with the Form Recognizer by reducing the number of documents you upload.

> [!WARNING]
> To avoid unnecessary costs, remember to destroy your provisioned resources by deleting the resource group.


## About Neon

 [Neon](https://neon.tech/) is a serverless, fully managed PostgreSQL database service optimized for modern applications. Neon's advanced features include autoscaling, scale-to-zero, database branching, instant point-in-time restore, and time travel queries. Neon manages the Postgres infrastructure, including database configuration, maintenance, and scaling operations, allowing you to focus on building and optimizing your applications.
