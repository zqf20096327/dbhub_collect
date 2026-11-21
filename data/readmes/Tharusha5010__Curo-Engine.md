# 💊 Curo — Pharmacy Loss-Prevention Engine

A modern **Java Swing (GUI)** desktop application engineered for proactive pharmacy loss prevention, regulatory prescription compliance, automated multi-batch FEFO billing, and real-time in-memory operational intelligence backed by a **Microsoft SQL Server (MSSQL)** database.

---

## 📌 Project Overview
The **Curo Engine** (*Curo Smart Pharmacy Management System*) transforms traditional pharmacy operations into a zero-wastage, risk-controlled workflow. Unlike generic stock trackers, Curo enforces batch-level **FEFO (First Expired, First Out)** deductions, triggers a **7-month advance expiry re-export shield**, dynamically adapts reorder thresholds based on **7-day sales velocity**, enforces **prescription verification rules**, generates **`.txt` thermal receipts**, and protects financial integrity through **owner-authorized bill cancellations and stock reversals**.

---

## 👥 Project Team & Modules

- **Tharusha Wijesekara (Team Lead)** — `ICT/25/954` — *Project Vision, System Architecture, Main Engine & MSSQL Database Integration*
- **Sachintha Mihiranga (Technical Co-Lead)** — `ICT/25/893` — *Core Systems Engineering, Cross-Module Integration, Batch-Wise Inventory Module & Team Technical Support*
- **Maleesha Senura** — `ICT/25/936` — *Staff Management & Role-Based Authentication Module*
- **Sachintha Dilsara** — `ICT/25/860` — *Bill Cancellations, Custom Exceptions & Smart Notification Alerts Module*
- **Wimansha Wijesinghe** — `ICT/25/956` — *FEFO Billing, POS Operations & Receipt Generation Module*

---

## 📸 System Screenshots

> *(Add your UI screenshots inside a `screenshots/` folder in the repository root using the filenames below to display them automatically on GitHub)*

| Login & Authentication | Main Dashboard Overview |
| :---: | :---: |
| ![Login Screen](screenshot/login.jpg) | ![Dashboard](screenshot/dashboard.jpg) |

| FEFO Billing (POS) & Thermal Receipt | Batch-Wise Inventory & Smart Alerts |
| :---: | :---: |
| ![Billing POS](screenshot/pos.jpg) | ![Inventory & Alerts](screenshot/inventory.jpg) |

---

## 🧩 OOP Concepts Covered

- **Encapsulation:** Model classes (`Medicine`, `StaffMember`, `Bill`, `BillItem`, `CanceledBill`, `Notification`) strictly protect data using `private` fields, defensive collection copies (`Bill.getItems()`), and validated Getters/Setters (e.g., auto-defaulting `moving_type` to `"SLOW"` and empty cancellation reasons).
- **Abstraction:** Abstract `BaseDAO` class and DAO layers (`BillingDAO`, `InventoryDAO`, `UserDAO`) encapsulate all SQL queries, JDBC transactions, and multi-batch FEFO algorithms away from the UI.
- **Inheritance:** Custom exception hierarchy (`PharmacyException` extended by `ExpiredMedicineException`, `OutOfStockException`, `InvalidStaffIdException`, `UnauthorizedAccessException`), DAOs extending `BaseDAO`, and modular UI views extending `JFrame` and `JPanel`.
- **Polymorphism:** Runtime polymorphism (Dynamic Method Dispatch) via `BaseDAO` references (`getTableName()`), constructor/method overloading, and dynamic billing workflows.
- **Exception Handling:** ACID-compliant SQL transactions (`setAutoCommit(false)`, `commit()`, `rollback()`) paired with domain-specific checked exceptions (`UnauthorizedAccessException`, `OutOfStockException`, `ExpiredMedicineException`, `InvalidStaffIdException`).
- **Collections & Generics:** Generic `Repository<T, ID>` interface implemented by `InventoryDAO`, alongside `ArrayList`, `LinkedHashMap`, `HashMap`, and thread-safe `CopyOnWriteArrayList`.
- **File Handling:** External credential loading via `FileInputStream` & `Properties` (`db.properties`) and automated `.txt` receipt writing/reading via `BufferedWriter` & `FileWriter` (`ReceiptWriter.java`).
- **Interfaces & Packages:** Custom `Repository<T, ID>` interface, Observer pattern listeners in `NotificationManager`, and clean modular separation across 8 packages (`models`, `exceptions`, `database`, `auth`, `inventory`, `billing`, `alerts`, `ui`).

---

## ✨ Key Features

- **Role-Based Access Control (RBAC):** Secure GUI authentication separating **Owners (`OWNER`)** and **Cashiers (`CASHIER`)**, blocking unauthorized access to Staff Management, Bill Cancellations, Free Issues, and Prescription Overrides via `UnauthorizedAccessException`.
- **Zero-Wastage Batch & FEFO Engine:**
  - Tracks inventory by individual batch (`batch_number`, `stock_date`, `exp_date`)—restocking inserts new batch records rather than overwriting existing batches.
  - Auto-suggests medicines as you type (`SuggestBox`) and automatically deducts stock from the earliest non-expired batch first (rolling over seamlessly across multiple batches if needed).
- **Compliance-Driven Dual-Path POS & Receipt Generator:**
  - Supports **Normal Billing** (with single-condition 5% discount tracking: *Bill > Rs. 1000*, *Senior Citizen > 55*, *Regular Customer*, or *Bulk Order*) and Owner-authorized **Free Issue** billing (`Net Total = 0.00`).
  - Enforces prescription verification (`is_prescription_checked`) for prescription-only medicines with Owner-only override privileges.
  - Exports formatted `.txt` receipts (including the marketing discount reason while omitting internal prescription flags) into `receipts/` and displays a Virtual Thermal Receipt preview.
- **Proactive Smart Alerts & Self-Adapting Velocity (In-Memory RAM):**
  - Triggers **7-month advance expiry warnings** (giving pharmacies a 1-month window before the 6-month supplier re-export cutoff).
  - Evaluates **7-day sales velocity** and enforces **50% low-stock restock thresholds** (`FAST` > 300 units/week -> target 5000 / alert < 2500; `SLOW` -> target 200 / alert < 100) in real time via `NotificationManager`[cite: 13].
- **Owner-Authorized Bill Cancellations:** Reverses billed quantities back into their exact inventory batches inside an atomic SQL transaction and logs the audit trail in `canceled_bills`.

---

## 🗄️ Database Schema Overview (`curo_db`)

| Table Name | Primary Key | Foreign Keys | Description |
| :--- | :--- | :--- | :--- |
| **`staff`** | `staff_id` | — | Stores Owner and Cashier login credentials, roles (`OWNER`/`CASHIER`), and account status (`ACTIVE`/`INACTIVE`). |
| **`inventory`** | `medicine_id` | — | Stores batch-wise medicine records (`batch_number`, `unit_price`, `stock_quantity`, `exp_date`, `requires_prescription`, `moving_type`). |
| **`bills`** | `bill_id` | `staff_id` → `staff` | Stores bill headers, timestamps, net totals, billing type (`NORMAL`/`FREE_ISSUE`), and discount reasons. |
| **`bill_item`** | `item_id` | `bill_id` → `bills`<br>`medicine_id` → `inventory` | Stores line-item quantities, batch deductions, and `is_prescription_checked` audit flags. |
| **`canceled_bills`** | `cancel_id` | `bill_id` → `bills`<br>`canceled_by` → `staff` | Logs Owner-authorized bill cancellations, timestamps, and mandatory cancellation reasons. |

---

## ⚠️ Custom Exceptions & Business Rules

| Exception Class | Trigger Condition | System Action |
| :--- | :--- | :--- |
| **`ExpiredMedicineException`** | Attempting to bill a batch where `exp_date <= TODAY`. | Blocks sale, rolls back SQL transaction, and alerts cashier to remove batch. |
| **`OutOfStockException`** | Requested billing quantity exceeds total valid non-expired stock across all batches. | Halts billing safely without partial deductions and displays available stock. |
| **`UnauthorizedAccessException`** | A `CASHIER` attempts Owner-restricted operations (Staff, Cancel Bill, Free Issue, Prescription Override, Delete/Update Stock). | Denies action and prompts for temporary Owner password elevation (`OwnerAccess`). |
| **`InvalidStaffIdException`** | Invalid credentials, inactive staff account login, or duplicate `staff_id` during registration. | Prevents authentication/registration and displays a validation error dialog. |

---

## 🛠️ System Architecture & Tech Stack

- **User Interface:** Java Swing (GUI) with FlatLaf Modern Look & Feel (`flatlaf.jar`)
- **Programming Language:** Java (JDK 17+)
- **Database Management System:** Microsoft SQL Server Express Edition (MSSQL)
- **JDBC Driver:** Microsoft JDBC Driver for SQL Server (`mssql-jdbc.jar`)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
curo-pharmacy-system/
├── lib/
│   ├── flatlaf.jar
│   └── mssql-jdbc.jar
├── screenshots/
│   ├── login.png
│   ├── dashboard.png
│   ├── billing.png
│   └── inventory.png
├── src/
│   ├── Main.java
│   ├── alerts/
│   │   ├── AlertsPanel.java
│   │   └── NotificationManager.java
│   ├── auth/
│   │   ├── LoginFrame.java
│   │   ├── StaffPanel.java
│   │   ├── UserDAO.java
│   │   └── UserSession.java
│   ├── billing/
│   │   ├── BillingDAO.java
│   │   ├── BillingPanel.java
│   │   ├── CancelBillPanel.java
│   │   └── ReceiptWriter.java
│   ├── database/
│   │   ├── BaseDAO.java
│   │   ├── DBConnection.java
│   │   └── Repository.java
│   ├── exceptions/
│   │   ├── ExpiredMedicineException.java
│   │   ├── InvalidStaffIdException.java
│   │   ├── OutOfStockException.java
│   │   ├── PharmacyException.java
│   │   └── UnauthorizedAccessException.java
│   ├── inventory/
│   │   ├── InventoryDAO.java
│   │   ├── InventoryPanel.java
│   │   └── SuggestionLogic.java
│   ├── models/
│   │   ├── Bill.java
│   │   ├── BillItem.java
│   │   ├── CanceledBill.java
│   │   ├── Medicine.java
│   │   ├── Notification.java
│   │   └── StaffMember.java
│   └── ui/
│       ├── DashboardFrame.java
│       ├── FitScrollPane.java
│       ├── OwnerAccess.java
│       ├── SuggestBox.java
│       ├── Theme.java
│       └── UIHelper.java
├── curoDB.sql
├── db.properties.example
├── run.bat
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Prerequisites
- **Java Development Kit (JDK 17 or higher)** installed and configured in your system `PATH`.
- **Microsoft SQL Server Express** and **SQL Server Management Studio (SSMS)**.

### 2. Clone the Repository
```bash
git clone https://github.com/Tharusha5010/curo-pharmacy-system.git
cd curo-pharmacy-system
```

### 3. Database & SQL Server Configuration
1. Open **SSMS**, connect to your local SQL Server instance (e.g., `localhost\SQLEXPRESS01`), and execute `curoDB.sql` to create the `curo_db` database, tables (`staff`, `inventory`, `bills`, `bill_item`, `canceled_bills`), and default Owner account.
2. In SSMS, right-click your Server Instance -> **Properties** -> **Security** -> ensure **SQL Server and Windows Authentication mode** is enabled, and verify your SQL login (`curoAdmin`) has read/write permissions on `curo_db`.
3. Open **SQL Server Configuration Manager**:
   - Navigate to **SQL Server Network Configuration** -> **Protocols for SQLEXPRESS01** -> Right-click **TCP/IP** and select **Enable**.
   - Navigate to **SQL Server Services** -> Ensure **SQL Server Browser** is Running (*Start Mode: Automatic*), then right-click **SQL Server (SQLEXPRESS01)** and click **Restart**.

### 4. Configure Local Database Credentials
1. Copy `db.properties.example` in the project root directory and rename the copy to `db.properties` (keep it in the root folder alongside `curoDB.sql` and `run.bat`).
2. Open `db.properties` and update your local SQL Server instance name (using double backslashes `\\`) and password:
```properties
db.url=jdbc:sqlserver://localhost\\SQLEXPRESS01;databaseName=curo_db;encrypt=true;trustServerCertificate=true;
db.user=curoAdmin
db.password=ict25954
```

### 5. Launch the Application
- **Option A — One-Click Launcher (Recommended on Windows):**
  Double-click `run.bat` in the project root folder. It automatically links `lib/flatlaf.jar` and `lib/mssql-jdbc.jar` to the classpath, compiles all source files into `bin/`, and launches the application.
- **Option B — Using an IDE (VS Code / IntelliJ):**
  Add both `lib/flatlaf.jar` and `lib/mssql-jdbc.jar` to **JAVA PROJECTS -> Referenced Libraries**, then run `src/Main.java`.

---

## 🔑 Default Admin Login Credentials

- **Staff ID:** `O001`
- **Password:** `1234`

---

### 📄 Printable User Guide (English)
For pharmacy staff and owners, a printable **User Manual** (covering daily POS operations, FEFO rules, 7-month expiry re-export workflow, and weekly database backups) is included in this repository:

👉 **[📖 View / Download Printable User Guide (PDF)](curo_engine_user_guide.pdf)**
