# 🚆 QR Code Based Train Ticket Booking System

A **Full Stack Java Web Application** built using **Spring Boot** for the backend and **HTML, CSS, and JavaScript** for the frontend. The application enables users to book train tickets online, generates a unique QR code for each booking, and provides downloadable PDF tickets.

🌐 **Live Demo:** https://qr-train-ticket-app-d0bxengcbmgyeyck.indiasouthcentral-01.azurewebsites.net/

---

## 🚀 Features

- 👤 User Registration & Authentication
- 🚆 Search Available Trains
- 🎫 Book Train Tickets
- ❌ Cancel Booked Tickets
- 📱 QR Code Generation for Every Ticket
- 📄 Download Tickets as PDF
- 🗄️ Database Integration using JPA (Hibernate)
- 🌐 RESTful API Architecture
- 🏗️ Layered Architecture (Controller, Service, Repository)
- 👨‍💼 Admin Module for Application Management

---

## 🛠️ Tech Stack

### Backend
- Java 21
- Spring Boot
- Spring Data JPA (Hibernate)
- Maven

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- MySQL (Development)
- TiDB Cloud (Production)

### Libraries
- ZXing (QR Code Generation)
- OpenPDF (PDF Generation)

### Cloud & Deployment
- Azure App Service
- Linux
- Basic B1 Plan
- GitHub Actions
- TiDB Cloud

---

## ⚙️ Tools & Technologies

- IntelliJ IDEA
- Postman
- Git & GitHub
- GitHub Actions
- Maven
- Azure App Service

---

## 🏗️ Architecture

The application follows a **layered architecture**:

```text
Client
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```

- **Controller:** Handles HTTP requests and REST API endpoints
- **Service:** Contains application and business logic
- **Repository:** Handles database persistence using Spring Data JPA
- **Frontend:** Provides the user interface using HTML, CSS, and JavaScript

---

## 📂 Project Structure

```text
src
├── controller
├── dto
├── model
├── repository
├── service
├── resources
│   ├── static
│   │   ├── html
│   │   ├── css
│   │   └── js
│   └── application.properties
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DB_URL=your_database_url
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
PORT=8080
```

> ⚠️ Never commit database credentials or sensitive environment variables to GitHub.

---

## ▶️ Running the Project Locally

1. Clone the repository.

```bash
git clone https://github.com/afeez-07/qr-train-ticket-booking-system.git
```

2. Navigate to the project directory.

```bash
cd qr-train-ticket-booking-system
```

3. Create a `.env` file with your database credentials.

4. Configure your TiDB Cloud or MySQL database.

5. Run the project using:

```bash
mvn spring-boot:run
```

6. Open your browser and visit:

```text
http://localhost:8080
```

---

## ☁️ Deployment

The application is deployed on **Microsoft Azure App Service** using a Linux-based **Basic B1** App Service plan.

### Deployment Configuration

- **Platform:** Azure App Service
- **Operating System:** Linux
- **Runtime:** Java 21
- **App Service Plan:** Basic B1
- **Region:** India South Central
- **Database:** TiDB Cloud
- **CI/CD:** GitHub Actions
- **Source Branch:** `azure-deployment`

GitHub Actions is used to automatically build and deploy the application from the `azure-deployment` branch to Azure App Service.

### Production Architecture

```text
GitHub Repository
      │
      │ GitHub Actions
      ▼
Azure App Service
Linux • Java 21 • Basic B1
      │
      │ JDBC
      ▼
TiDB Cloud
```

---

## 📸 Application Screenshots

Screenshots of the application interface and major modules are available in the repository.

---

## 📌 Future Enhancements

- Email Ticket Confirmation
- Seat Selection
- Payment Gateway Integration
- Booking History
- Responsive UI Improvements

---

## 👨‍💻 Author

**Afeez S**

Java Developer | Full Stack Developer | Spring Boot | REST APIs | Azure | AWS | TiDB Cloud

---
