# 📦 Inventory Hub

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![TiDB](https://img.shields.io/badge/TiDB-3A2B59?style=for-the-badge&logo=tidb&logoColor=white)

**Inventory Hub** is a premium, full-stack web application designed for efficient inventory management. Built with a React (Vite) frontend and a Node.js/Express backend, it allows users to effortlessly track, update, and bulk-add inventory items. 

The application uses **MySQL (TiDB Serverless)** for robust relational data storage and features a custom-built, modern glassmorphism design system.

---

## ✨ Key Features

- **Bulk Item Submission:** Add multiple inventory items in a single transaction via a dynamic, multi-row form.
- **Real-time Inventory Tracking:** View all inventory items instantly in a beautifully formatted data table.
- **Full CRUD Functionality:** Seamlessly Create, Read, Update, and Delete inventory items.
- **Relational Database (`JOIN` Operations):** Categories and items are linked relationally, ensuring data integrity.
- **Premium UI/UX:** 
  - Sleek dark mode aesthetics with responsive glassmorphism cards.
  - Interactive micro-animations and glowing focus states.
  - Interactive **SweetAlert2** popups for beautiful success/error handling and confirmations.
- **Backend Validation:** Secure backend API ensuring no malformed data reaches the database.

---

## 🛠️ Tech Stack

**Frontend:**
* React 18 (Vite)
* Custom Vanilla CSS (No CSS Frameworks used)
* Axios (Data Fetching)
* Lucide React (Icons)
* SweetAlert2 (Popups/Toasts)

**Backend:**
* Node.js & Express.js
* MySQL2 (Database Driver)
* TiDB Serverless (Cloud MySQL Database)
* CORS & Dotenv

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites
* Node.js (v20+ recommended)
* A TiDB / MySQL Database

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/inventory-hub.git
cd inventory-hub
```

### 2. Backend Setup
```bash
cd backend
npm install
```
Create a `.env` file in the `backend` directory and add your TiDB/MySQL credentials:
```env
PORT=5000
TIDB_HOST=your_host_url
TIDB_PORT=4000
TIDB_USERNAME=your_username
TIDB_PASSWORD=your_password
TIDB_DATABASE=test
```
Start the backend server:
```bash
npm start
```
*(The server will automatically initialize the database tables and seed default categories upon startup).*

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
```
Start the frontend development server:
```bash
npm run dev
```

The application will be running at `http://localhost:5173`.

---

## 📂 Project Structure (Monorepo)

```text
inventory-hub/
├── backend/                # Node.js Express API
│   ├── db.js               # Database connection & init logic
│   ├── server.js           # API endpoints & routing
│   └── package.json
└── frontend/               # React Application
    ├── src/
    │   ├── components/     # UI Components (Table, Form)
    │   ├── App.jsx         # Main application logic
    │   └── index.css       # Premium design system
    └── package.json
```

---

## 🌐 Deployment
This application is designed to be deployed as separated services:
- **Frontend:** Vercel or Netlify.
- **Backend:** Render or Railway.
- **Database:** Hosted on TiDB Serverless.

---

## 🧪 Comprehensive Test Guide

Follow this guide to thoroughly test the application functionality locally.

### Phase 1: Form Validation
1. **Empty Submit:** Leave all fields blank and click the "Submit Purchase" button. The browser will prevent submission and highlight the "Item Name" field.
2. **Partial Submit:** Enter "Test Item", leave the Category unselected, and click "Submit". The browser will catch the missing selection.

### Phase 2: Single & Bulk Submission
1. **Single Add:** Fill out the form with a single item (e.g., "Dell XPS 15", "Electronics", check "In Stock") and submit. Verify it appears in the "Current Inventory" table with the correct category name (verifying the MySQL JOIN).
2. **Bulk Add:** Fill out the first row. Click **Add Row** and fill out the second row. Click "Submit Purchase". Verify the form resets to a single row and both items appear simultaneously in the table.

### Phase 3: Update Operation
1. Locate an item in the table and click the **Pencil (Edit)** icon.
2. The row will transform into editable input fields.
3. Modify the name, category, or stock status.
4. Click the green **Check (Save)** icon. A SweetAlert2 success toast will appear, and the table will permanently display the updated data.
5. (Optional) Click Edit again, make changes, and click the red **X (Cancel)** icon to verify changes are discarded.

### Phase 4: Delete Operation
1. Click the **Trash (Delete)** icon next to an item.
2. A beautiful SweetAlert2 warning dialog will appear asking for confirmation.
3. Click "Cancel" to verify the item remains.
4. Click the "Trash" icon again and select "Yes, delete it!". The item will be removed from the database and the table will refresh.
