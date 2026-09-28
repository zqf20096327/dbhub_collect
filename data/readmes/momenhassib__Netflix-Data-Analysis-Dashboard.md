# 🎬 Netflix Data Analysis Dashboard

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mo'men_Hassib-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/momenhassib)

---

## 📌 Overview

This project analyzes the Netflix titles dataset to uncover content trends and business insights through an interactive Power BI dashboard. The dataset was cleaned and restructured in Excel, loaded into MySQL for relational modeling, then visualized in Power BI using DAX measures.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Excel | Initial data cleaning and splitting multi-value fields (cast, country, director, genre) into separate sheets |
| MySQL | Unpivoting multi-value columns and building analysis-ready tables |
| Power Query | Data transformation before loading into Power BI |
| Power BI | Dashboard development |
| DAX | Business calculations and measures |

---

## 🚀 Project Overview

The raw Netflix dataset stores multiple values (cast members, countries, directors, genres) as repeated columns per title (e.g. `cast_1` to `cast_50`). This project:

- Splits and cleans these multi-value fields in **Excel**, producing separate sheets for cast, country, directors, and genres.
- Unpivots each of these sheets in **MySQL** using `UNION ALL` queries, turning wide columns into normalized rows.
- Builds an interactive **Power BI** dashboard on top of the resulting tables.

---

## 📊 Dashboard Features

- 📅 Release Year Filter
- 🌍 Country Filter
- 🎭 Genre / Category Breakdown
- ⭐ Rating Distribution
- 📈 Content Added Over Time
- 🔍 Single Title Deep-Dive View
- ⚡ Dynamic DAX Measures

---

## 📈 Key Performance Indicators (KPIs)

- 🎬 Total Titles
- 🎞️ Movies vs TV Shows Split
- 🌍 Top Countries by Content Volume
- 📅 Titles Added per Year
- ⭐ Most Common Ratings

---

## 💡 Business Insights

The dashboard helps answer questions such as:

- Which countries produce the most Netflix content?
- How has content volume changed year over year?
- What are the most common genres and ratings?
- How does content distribution differ between Movies and TV Shows?

---

## 📷 Dashboard Preview

### Overview Dashboard
![Dashboard 1](Dashboard1.png)

### Single Title Analysis Dashboard
![Dashboard 2](Dashboard2.png)

---

## 📂 Repository Structure

```
Netflix-Data-Analysis-Dashboard
│
├── Netflix_Data_Analysis_Dashboard.pbix
├── netflix_titles.xlsx
├── netflix.dataset.sql
├── create.cast.sql
├── create.countries.sql
├── create.directors.sql
├── create.listed_in.sql
├── Dashboard1.png
├── Dashboard2.png
└── README.md
```

---

## 🎯 Project Highlights

✔ Excel-based Data Cleaning & Multi-Value Splitting

✔ MySQL Unpivoting with UNION ALL

✔ Interactive Power BI Dashboard

✔ Custom DAX Measures

✔ Genre, Rating & Country Analysis

---

## 👨‍💻 Author

## Momen Ahmed Hassib

**Data Analyst**

📍 Giza, Egypt

### 🔗 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mo'men_Hassib-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/momenhassib)

---

⭐ If you found this project useful, consider giving it a Star.

Made with ❤️ by **Momen Ahmed Hassib**
