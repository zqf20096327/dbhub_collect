# 💊 Curo - Smart Pharmacy Management System

A modern **Java Swing (GUI)** desktop application designed for pharmacy inventory control, role-based user authentication, automated billing operations, and real-time stock alert notifications backed by a **Microsoft SQL Server (MSSQL)** database.

---

## 📌 Project Overview
The **Curo Smart Pharmacy Management System** streamlines daily pharmacy operations through an intuitive graphical interface. It handles real-time stock tracking, secure staff login, automated bill calculations with discounts, emergency bill cancellations, and smart warning alerts for low stock and expiring medicines.

---

## 👥 Project Team & Modules

- **Tharusha Wijesekara (Lead)** - `ICT/25/954` - *System Architecture, Main Engine & MSSQL Database Integration*
- **Maleesha Senura** - `ICT/25/936` - *Staff & Authentication Module & Co-Integration*
- **Sachintha Mihiranga (Core Setup)** - `ICT/25/893` - *Repository Setup, Scaffolding & Inventory Module*
- **Wimansha Wijesinghe** - `ICT/25/956` - *Billing & Sales Operations Module*
- **Sachintha Dilsara** - `ICT/25/860` - *Cancellations & Notification Alerts Module*

---

## 🧩 OOP Concepts Covered

- **Encapsulation:** Model classes (`Medicine`, `StaffMember`, `Bill`, `BillItem`) utilize `private` fields with public Getters/Setters to protect sensitive data structures.
- **Inheritance:** Custom Exception classes extend Java's standard `Exception` class (e.g., `ExpiredMedicineException`, `OutOfStockException`) and Swing components extend `JFrame`/`JPanel`.
- **Polymorphism & Abstraction:** Abstract Database Access Objects (DAOs) and interface abstractions for service layers, dynamic billing workflows, and alert evaluations.
- **Modular Software Design:** Clean separation of concerns into distinct structural packages (`auth`, `inventory`, `billing`, `alerts`, `database`, `ui`).

---

## ✨ Key Features

- **Role-Based Authentication:** Secure GUI Login with distinct authorization levels for Cashiers and Pharmacy Owners.
- **Smart Inventory Management:** Real-time stock levels, automated stock updates, dynamic reorder warnings, and Fast/Slow moving item classification.
- **Billing System:** 
  - Automated point-of-sale GUI billing interface with real-time total calculation.
  - Automatic 5% discount rules and owner-authorized Free Issue billing options.
- **Safety & Security:**
  - Emergency 3-minute bill cancellation with automatic SQL stock reversal.
  - Smart alert notifications for low stock thresholds and 7-month advance expiration dates.
- **Relational Data Persistence:** All system data, user profiles, stock logs, and transactions are securely stored and queried using Microsoft SQL Server.

---

## 🛠️ System Architecture

- **User Interface:** Java Swing (GUI)
- **Programming Language:** Java (JDK 17)
- **Database Management System:** Microsoft SQL Server Express Edition (MSSQL)
- **JDBC Driver:** Microsoft JDBC Driver for SQL Server (`mssql-jdbc.jar`)
- **Version Control:** Git & GitHub

---

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tharusha5010/curo-pharmacy-system.git
