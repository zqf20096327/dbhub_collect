# Enhanced ETL Workflow with Python and TiDB Cloud.

## 📌 Project Overview
This project implements a full **ETL (Extract, Transform, Load) pipeline** using Python and **TiDB Cloud** as the remote data warehouse. The pipeline extracts data from multiple formats (**CSV, JSON, XML**), applies necessary transformations (**unit conversion, cleaning**), and loads the transformed data into **TiDB Cloud**.

By leveraging **TiDB Cloud**, this project simulates a real-world cloud-based ETL workflow, allowing **scalable, distributed database management**. TiDB Cloud Services provides **high availability, strong consistency, and MySQL compatibility**, making it an ideal choice for data engineering projects that require real-time analytics and efficient data handling. **Cloud integration** enhances **performance, monitoring, and security** while reducing operational overhead.

## 🏆 Problem Statement
Handling structured data from multiple sources requires a robust **ETL process** to ensure **data consistency and quality**. This project aims to:
- **Extract** structured data from CSV, JSON, and XML files.
- **Transform** the extracted data, performing **unit conversions (inches to meters, pounds to kg)** and cleaning.
- **Load** the transformed data into a **remote TiDB Cloud database**.

## 🛠️ Tools & Technologies Used
- **Python** 🐍 (for scripting the ETL pipeline)
- **Pandas** (for data manipulation & transformation)
- **MySQL Connector** (for connecting to TiDB Cloud)
- **TiDB Cloud** (as a scalable, distributed database)
- **Logging** (for tracking ETL operations)
- **GitHub** (for version control & repository hosting)

  🌍 Why TiDB Cloud?
Unlike traditional relational databases, TiDB Cloud Services provides:
✅ Horizontal scalability – Dynamically expands to handle large datasets.
✅ Distributed transactions – Ensures consistency and fault tolerance.
✅ Real-time analytics – Supports hybrid OLTP + OLAP workloads without data migration.
✅ Cloud-native flexibility – Designed for modern data-intensive applications.
By integrating Python-based ETL workflows with TiDB Cloud, this project simulates a real-world cloud data pipeline that can scale seamlessly for big data engineering, data warehousing, and real-time analytics.

🚀 Key Features in This Project.
1️⃣ Extract: Reads data dynamically from CSV, JSON, and XML sources.
2️⃣ Transform: Converts height (inches → meters) and weight (pounds → kilograms). Cleans and standardizes raw data. Logs every transformation step for auditability.
3️⃣ Load: Stores transformed data into TiDB Cloud using MySQL Connector. Uses distributed storage to ensure reliability and scalability.
Leverages real-time querying capabilities for analytics.
4️⃣ Scalability & Cloud Optimization: Uses serverless TiDB Cloud clusters for dynamic performance scaling.
Designed to work with additional cloud integrations such as AWS S3, RDS, and Glue.

## 📂 Project Structure
```
├── extract_data.py        # Extract data from CSV, JSON, XML
├── transform_data.py      # Perform transformations (unit conversion, cleaning)
├── load_data_tidb.py      # Load transformed data into TiDB Cloud
├── utils.py               # Helper functions (logging, error handling)
├── main_orchestrate.py    # Orchestrates the full ETL process
├── transformed_data.csv   # Transformed dataset (output)
├── log_file.txt           # Log file for tracking progress
├── README.md              # Project documentation
```

## How to Run the Project
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-github-username/Enhanced-ETL-TiDB.git
   cd Enhanced-ETL-TiDB
   ```

2. **Install Dependencies**
   ```bash
   pip install pandas mysql-connector-python
   ```

3. **Set Up TiDB Cloud Connection**
   - Update `load_data_tidb.py` with your **TiDB Cloud credentials**.
   - Replace `ssl_ca` path with the correct **certificate file location**.

4. **Run the ETL Pipeline**
   ```bash
   python main_orchestrate.py
   ```

5. **Verify Data in TiDB Cloud**
   - Log into **TiDB Cloud Console** → `Clusters` → `SQL Editor`
   - Run:
     ```sql
     SELECT * FROM census_data;
     ```

## 🎯 Expected Output
- **Extracted Data** is read from CSV, JSON, XML files.
- **Transformed Data** is saved as `transformed_data.csv`.
- **Loaded Data** is successfully stored in TiDB Cloud.
- **Active Logs** are stored in `log_file.txt`.

## 🔥 Insights & Learnings
- Handling structured data across different file formats.
- Implementing **secure connections to a cloud database**.
- Automating the **ETL pipeline for real-world data engineering**.
- By integrating **cloud-based databases like TiDB Cloud**, data engineers benefit from:
  - **Scalability**: TiDB Cloud supports distributed storage for handling large datasets.
  - **High Availability**: Ensures data consistency and failover support.
  - **Real-Time Querying**: Enables fast analytical processing on transformed data.
  - **Seamless MySQL Compatibility**: Makes it easy to integrate with existing tools.

    💡 How This ETL Workflow Benefits Data Engineers.
🚀 Scalability: TiDB Cloud's distributed nature ensures the ETL pipeline can process large datasets without bottlenecks.
🔥 Real-time Processing: Supports both transactional and analytical workloads without data duplication.
🔎 Better Observability: Logging is integrated for traceability, debugging, and auditing.
⚡ Future-Ready: Can be extended to integrate with Apache Spark, AWS Lambda, or Airflow for advanced workflow orchestration.

## 📌 Future Improvements
- Integrate **AWS S3** for cloud-based data storage.
- Use **Airflow** for scheduling the ETL process.
- Perform **data quality checks** before loading into TiDB Cloud.

---
Made with ❤️ by [Tauhid Alam] By GUVI.🚀
This project serves as a real-world example of building cloud-native ETL workflows, enabling efficient data processing, transformation, and real-time analytics using TiDB Cloud and Python.
