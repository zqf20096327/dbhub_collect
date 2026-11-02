# 🚀 FinAI - Smart AI-Powered Expense Tracker

FinAI is a modern, full-stack personal finance and expense tracking application built using **React**, **Node.js/Express**, and **MySQL**. It leverages **Groq AI** to provide smart financial insights, automated budget tracking, and real-time transaction management.

---

## ✨ Features

- **🔐 Secure Authentication**: User signup and login with JWT token support and session-based protection (`sessionStorage`).
- **📊 Interactive Dashboard**:
  - Summary cards for total income, expenses, and remaining budget.
  - Expense analysis with visual charts (`FinanceChart`).
  - View and filter recent transactions.
- **🤖 Smart AI Insights**: Powered by **Groq AI** to evaluate your spending habits and offer actionable financial tips.
- **⚠️ Dynamic Budget Alerts**: Set monthly budget limits and get instant warnings when spending exceeds thresholds.
- **📜 Transaction History**: Dedicated page to manage and view past transactions.
- **👑 Go Pro Feature**: Dynamic premium tier page for scaling features.

---

## 🛠️ Tech Stack

### **Frontend**

- **React.js** (Functional Components, React Hooks)
- **React Router DOM v6** (Client-side routing & Protected Routes)
- **Axios** (API Requests)
- **CSS3** (Custom Responsive Slate/Indigo Dark Theme Styling)

### **Backend**

- **Node.js** & **Express.js** (REST API)
- **Groq SDK / AI Integration**
- **JWT (JSON Web Tokens)** for Auth
- **MySQL** with MySQL2

---

## 📁 Project Structure

```text
finai-expense-tracker/
├── client/                     # React Frontend
│   ├── public/
│   │   └── logo.png
│   └── src/
│       ├── components/
│       │   ├── AddTransaction.jsx
│       │   ├── BudgetAlert.jsx
│       │   ├── FinanceChart.jsx
│       │   ├── GoProPage.jsx
│       │   ├── HistoryPage.jsx
│       │   ├── Login.jsx
│       │   ├── Navbar.jsx
│       │   ├── Navbar.css
│       │   ├── Signup.jsx
│       │   ├── SmartInsights.jsx
│       │   ├── SummaryCards.jsx
│       │   └── TransactionList.jsx
│       ├── App.jsx
│       ├── App.css
│       └── index.js
│
└── server/                     # Node.js/Express Backend
    ├── controllers/
    ├── models/
    ├── routes/
    ├── middleware/
    ├── .env
    └── server.js
```

⚙️ Getting Started Project

# Navigate to backend directory

cd backend

# Install dependencies

npm install

# Create a .env file in the server directory

touch .env or ni .env

# for .env

PORT=5000
MySQL
JWT_SECRET=your_jwt_secret_key
GROQ_API_KEY=your_groq_ai_api_key

# Run the backend server:

npm start

# For frontend

# Navigate to frontend directory

cd frontend

# Install dependencies

npm install

# Start React development server

npm run dev
