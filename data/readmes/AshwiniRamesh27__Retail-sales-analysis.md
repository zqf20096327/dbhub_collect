🛒 Retail Order Data Analysis Dashboard

This is a Streamlit-based interactive dashboard for analyzing retail order data stored in a MySQL/TiDB database. The dashboard provides insights into sales performance, profitability, discounts, pricing, and market trends with dynamic queries and visual outputs.

📋 Table of Contents

✨ Features

⚙️ Installation

🗄️ Database Configuration

🚀 Usage

📊 Query Categories & Insights

📝 Closing Notes

✨ Features

🔗 Connects to a remote MySQL/TiDB database using PyMySQL.

📊 Fetches retail order data dynamically and displays it in tables.

💡 Provides insights and actionable recommendations for each query.

🗂️ Categorizes queries into tabs for better navigation:

🚀 Usage

Open the app in your browser (default: http://localhost:8501).

Navigate through the tabs:

*Sales Analysis – Track top-selling products, monthly sales, and regional performance.

*Profit Analysis – Identify high/low profit products, top cities, and category profitability.

*Discount & Pricing – Analyze discount impact, average pricing, and category-level discounts.

*Market Trends – Understand seasonal trends, revenue fluctuations, and top customer segments.

Click any query button to fetch data and view corresponding insights.

Insights provide actionable recommendations for sales, marketing, and pricing strategies.

📊 Query Categories & Insights

💰 Sales Analysis

*Top-selling products

*Monthly sales trends

*Regional sales performance

*Top 10 highest revenue products

*Yearly revenue trends

📈 Profit Analysis

*High-profit products

*Lowest-profit products

*Top cities by profit margin

*Total profit per category

*Most profitable product category

🏷️ Discount & Pricing

*Products with discounts > 20%

*Impact of discount on sales

*Total discounts by category

*Average sale price per product category

*Average discount percentage per region

🌐 Market Trends

*Highest sales by month/year

*Lowest monthly and yearly sales

*Revenue per category

*Regions with highest average sale price

*Top segments by order quantity

📝 Closing Notes

Ensure the database contains the kaggle_project.kaggle table with appropriate fields (order_date, category, sub_category, quantity, sale_price, cost_price, discount, discount_percent, profit, region, city, segment).

Properly close the app to ensure database connections are released.

Designed for retail analysts and business decision-makers to quickly extract actionable insights from sales data.
