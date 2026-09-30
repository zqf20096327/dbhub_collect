# DB_Agent Dify Plugin  
**DB_Agent Dify Plugin, Powered by PolarDB for AI**  

---

## Overview  
The **DB_Agent Dify Plugin** is a **graphical database interaction tool** designed for enterprise-level intelligent data querying.  
Leveraging **PolarDB for AI's LLM-based Natural Language to SQL (NL2SQL) model**, it enables developers and business users to **interact with databases via natural language** without writing SQL code.  

### Core Capabilities  
- **Natural Language to SQL (NL2SQL)**:  
  Convert natural language queries (e.g., *"Show total sales in Q1 2024"*) into precise SQL statements.  
- **Intelligent Chart Generation (NL2Chart)**:  
  Automatically transform SQL query results into dynamic visualizations (bar charts, pie charts, line graphs).  
- **Data Summarization (NL2SQL_SUMMARY)**:  
  Generate high-level insights and summaries of query results (e.g., *"Sales in the East region increased by 15% YoY"*).  

**Use Cases**:  
- Business users to quickly retrieve data answers  
- Data analysts to accelerate exploratory analysis  
- Developers to build automated data pipelines  

---

## Configuration  

### 1. No Database Credentials Stored  
The plugin **does not persist any database credentials or sensitive information**. Connection parameters are used only during the session.  

### 2. Install the Plugin  
**Steps**:  
1. Open Dify → **Plugin Marketplace**  
2. Search for **DB_Agent**  
3. Click **Install**  

### 3. Ready to Use  
After installation, add a **DB_Agent node** to your workflow and interact via the graphical interface.  

---

## Key Features  

### ✅ **Natural Language to SQL (NL2SQL)**  
- **Supports Complex Logic**:  
  - Date arithmetic (e.g., *"Sales last month"* → `WHERE date = DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)`)  
  - Mapping comprehension (e.g., *"Valid orders"* → `isValid = 1`)  
  - Default conditions (e.g., `datastatus=1` for active records)  
- **Model Advantages**:  
  - Deep semantic understanding via large language models (LLMs)  
  - Generates SQL with aggregation functions, subqueries, and advanced syntax  

### 📊 **Intelligent Chart Generation (NL2Chart)**  
- **One-Click Visualization**:  
  Input natural language (e.g., *"Compare sales across regions"*) to generate corresponding charts.  
- **Dynamic Reports**:  
  Supports bar charts, pie charts, line graphs, and real-time data updates.  

### 🧠 **Data Summarization (NL2SQL_SUMMARY)**  
- **High-Level Insights**:  
  Summarize query results to reveal trends and anomalies (e.g., *"Inventory warnings: 3 categories below threshold"*).  

---

### Core Advantages  
- **Code-Free Operation**:  
  Interact with databases using natural language—no SQL expertise required.  
- **Enterprise-Grade Intelligence**:  
  - Understands business-specific mappings (e.g., `"Active users" → status = 'active'`)  
  - Supports advanced SQL constructs (e.g., nested queries, window functions)  
- **End-to-End Automation**:  
  Natural language → SQL → Visualization → Data summary, all within Dify.  

---

## 🛠️ Installation and setup instructions
- Dify v0.1.0 or higher

---

## 📦 Tools List and Usage
 
### 1. **polardb4ai_nl2sql**  
**Purpose**:  
- Parses natural language (e.g., *"Query Q1 2024 sales"*) into precise SQL statements.  
**Use Case**:  
- Non-technical users generate complex SQL queries through conversational input.  

### 2. **polardb4ai_nl2chart** 
**Purpose**:  
- Converts natural language queries (e.g., *"Show sales trends"*) into visualizations (e.g., bar charts, pie charts).  
**Use Case**:  
- Users describe requirements in natural language, and the system automatically generates corresponding charts.  

### 3. **polardb4ai_nl2sql_summary**  
**Purpose**:  
- Summarizes SQL query results into high-level insights (e.g., *"East region sales increased by 15% YoY"*).  
**Use Case**:  
- Provides concise summaries of data results for quick decision-making.  

### 4. **polardb4ai_schema_index_show**  
**Purpose**:  
- Displays schema index information (e.g., table structures, field definitions).  
**Use Case**:  
- Database administrators or developers view existing schema index structures.  

### 5. **polardb4ai_schema_index_build**  
**Purpose**:  
- Builds or updates database schema indexes to optimize query performance.  
**Use Case**:  
- Rebuild schema indexe.  

### 6. **polardb4ai_pattern_index_show**  
**Purpose**:  
- Displays query pattern index information (e.g., frequently used query paths).  
**Use Case**:  
- Analyze common query patterns to optimize index strategies.  

### 7. **polardb4ai_pattern_index_editor**  
**Purpose**:  
- Customizes or adjusts query pattern index configurations (e.g., add/remove pattern rules).  
**Use Case**:  
- Optimize index generation logic for specific business needs.  

### 8. **polardb4ai_llm_config_show**  
**Purpose**:  
- Displays current configuration infomation

### 9. **polardb4ai_llm_config_editor.yaml**  
**Purpose**:  
- Modifies configuration infomation (e.g., replace text, extra knowledge).  
**Use Case**:  
- Optimize agent behavior based on business requirements (e.g., improve SQL generation accuracy).  

### 10. **polardb4ai_task_monitor.yaml**  
**Purpose**:  
- Monitors tool execution status and task progress in real-time (e.g., query duration, error logs).  
**Use Case**:  
- Track task execution and troubleshoot performance bottlenecks or errors.  

---

### Contact  
For questions, feedback, or collaboration:  
- **GitHub**: [https://github.com/AAAMHJ/PolarDB4AI_Dify_Plugin_DB_Agent](https://github.com/AAAMHJ/PolarDB4AI_Dify_Plugin_DB_Agent)  
- **Website**: [@help.aliyun.com](https://help.aliyun.com/zh/polardb/polardb-for-mysql/user-guide/db-agent/?spm=a2c4g.11186623.help-menu-2249963.d_5_27_1.c8d37838s05Ivf)

---

**Last Updated**: 2025/07/23 
