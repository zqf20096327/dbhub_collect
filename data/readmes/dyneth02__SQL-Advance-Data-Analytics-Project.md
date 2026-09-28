# 📊 Advanced SQL Analytics – Time Series, Segmentation & Reporting

This project extends the previous SQL EDA repository with **advanced, real-world data analytics techniques** used in BI, data warehousing, and analytical engineering.  
It focuses on time-series analysis, cumulative trends, performance benchmarking, segmentation logic, part-to-whole evaluation, and full customer/product analytical reporting.

---

## 📁 Project Structure & Script Summaries

### **01_change_over_time_analysis.sql**  
Tracks trends over time using yearly/monthly grouping, `DATETRUNC()`, and formatted date buckets.  
Analyzes sales, customers, and quantity changes over time.  
:contentReference[oaicite:0]{index=0}

---

### **02_cumulative_analysis.sql**  
Computes running totals and moving averages using window functions (`SUM() OVER`, `AVG() OVER`).  
Useful for cumulative revenue tracking and rolling-average price analysis.  
:contentReference[oaicite:1]{index=1}

---

### **03_performance_analysis.sql**  
Performs **Year-over-Year (YoY)** and **Average-vs-Actual** performance benchmarking.  
Uses `LAG()` for prior-year comparisons and `AVG() OVER()` to classify products as above/below average.  
:contentReference[oaicite:2]{index=2}

---

### **04_data_segmentation.sql**  
Implements custom segmentation for both **products** and **customers**.  
Techniques used:  
- CASE segmentation  
- Spend-based customer grouping (VIP, Regular, New)  
- Product cost-range segmentation  
:contentReference[oaicite:3]{index=3}

---

### **05_part_to_whole_analysis.sql**  
Quantifies category-level contribution to overall revenue.  
Uses windowed totals to compute percentage-of-whole KPIs.  
:contentReference[oaicite:4]{index=4}

---

### **06_report_customers.sql**  
Creates the **`gold.report_customers`** analytical view.  
Outputs:  
- Age grouping  
- Customer segmentation  
- Recency  
- Total orders, revenue, quantity  
- Avg order value, avg monthly spend  
Useful for churn, CLV, and marketing analytics.  
:contentReference[oaicite:5]{index=5}

---

### **07_report_products.sql**  
Builds the **`gold.report_products`** analytical view.  
Outputs product-level KPIs:  
- Performance segments (High-Performer, Mid-Range, Low-Performer)  
- Lifespan, recency  
- Avg selling price  
- Total orders, sales, quantity  
- Avg monthly revenue  
:contentReference[oaicite:6]{index=6}

---

## 🧠 Key SQL Techniques Demonstrated

- **Time-Series Analytics:** DATETRUNC, FORMAT, date bucketing  
- **Cumulative Metrics:** Running totals & moving averages  
- **Window Functions:** `RANK()`, `ROW_NUMBER()`, `LAG()`, `SUM() OVER`  
- **Segmentation Frameworks:** Behavioural & product segmentation  
- **Part-to-Whole Metrics:** Windowed totals & contribution percentages  
- **Analytical Reporting:** Customer & product analytical views  

---

## 🎯 Business Insights Enabled

- Revenue and customer growth trends  
- Monthly/annual performance benchmarking  
- Product lifecycle behaviour  
- Customer lifecycle metrics (recency, spending, lifespan)  
- Category contribution analysis  
- High-value vs low-value customer/product differentiation  

---

## 🚀 How to Use

1. Load dimension and fact tables from the previous EDA project.
2. Run scripts **in order**:
          01_change_over_time_analysis.sql
          02_cumulative_analysis.sql
          03_performance_analysis.sql
          04_data_segmentation.sql
          05_part_to_whole_analysis.sql
          06_report_customers.sql
          07_report_products.sql
3. Query the views to generate BI dashboards or export datasets.

---

## 🏗️ Recommended Folder Structure

          datasets/
          docs/
          scripts/
          │
          ├── 01_change_over_time_analysis.sql
          ├── 02_cumulative_analysis.sql
          ├── 03_performance_analysis.sql
          ├── 04_data_segmentation.sql
          ├── 05_part_to_whole_analysis.sql
          ├── 06_report_customers.sql
          ├── 07_report_products.sql
          └── README.md


---

## 🏫 Academic / Portfolio Context

This project demonstrates **intermediate-to-advanced SQL analytics**, suitable for roles in:  
Data Analytics · BI Engineering · Data Warehousing · Analytics Engineering  

---

## 👨‍💻 Author
D G A D Hirusha


