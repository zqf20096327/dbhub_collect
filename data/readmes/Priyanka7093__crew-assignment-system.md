# Crew Assignment System

A full-stack web application for managing airline crew assignments, flights, and crew members.

The system provides a centralized platform to manage flight information, crew availability, and crew-to-flight assignments through a modern Angular frontend and Spring Boot backend.

## Features

- Flight management
- Crew member management
- Crew assignment management
- View and manage crew availability
- RESTful APIs for frontend-backend communication
- Exception handling and validation
- MySQL database integration
- Angular-based responsive frontend
- Spring Boot backend architecture

## Technology Stack

### Frontend

- Angular
- TypeScript
- HTML
- CSS

### Backend

- Java
- Spring Boot
- Spring Data JPA
- REST APIs

### Database

- MySQL

### Tools

- Git
- GitHub
- Postman
- Maven

## Project Structure

```text
crew-assignment-system/
│
├── crew-assignment-backend/
│   └── crew-assignment-backend/
│       ├── src/
│       │   └── main/
│       │       ├── java/
│       │       │   └── com/crewmanagement/
│       │       └── resources/
│       │           └── application.properties
│       └── pom.xml
│
├── crew-assignment-frontend/
│   ├── src/
│   │   └── app/
│   │       ├── about/
│   │       ├── dashboard/
│   │       ├── faq/
│   │       ├── home/
│   │       ├── models/
│   │       └── services/
│   ├── public/
│   └── package.json
│
└── .gitignore
```

## Application Architecture

![Application Architecture](screenshots/crew%20management%20architecture%20diagram.png)

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Priyanka7093/crew-assignment-system.git
```

### 2. Configure MySQL

Create the database:

```sql
CREATE DATABASE crew_assignment_db;
```

### 3. Configure Database Credentials

The backend uses the following configuration:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/crew_assignment_db
spring.datasource.username=root
spring.datasource.password=${DB_PASSWORD}
```

Set your database password through the `DB_PASSWORD` environment variable.

### 4. Run the Spring Boot Application

Navigate to the backend directory:

```bash
cd crew-assignment-backend/crew-assignment-backend
```

On Windows:

```bash
mvnw.cmd spring-boot:run
```

## Frontend Setup

Navigate to the frontend directory:

```bash
cd crew-assignment-frontend
```

Install dependencies:

```bash
npm install
```

Start the Angular development server:

```bash
ng serve
```

Then open:

```text
http://localhost:4200
```

## Security

Database credentials are not stored directly in the repository.

The application uses the `DB_PASSWORD` environment variable for the database password.

## Project Status

**Under active development**

The project is being developed as a full-stack crew assignment management application using Angular, Spring Boot, and MySQL.

## Technologies

`Angular` `TypeScript` `Java` `Spring Boot` `REST API` `MySQL` `JPA` `Git` `GitHub` `Maven`

---
## Application Screenshots

### Home Page
![Home Page](screenshots/Home.png)

### Dashboard
![Dashboard](screenshots/Dashboard.png)

### Flights Management
![Flights Management](screenshots/flights.png)

### Crew Management
![Crew Management](screenshots/crew.png)

### Assignments Management
![Assignments Management](screenshots/assignment.png)

### FAQ
![FAQ](screenshots/FAQ.png)

### About
![About 1](screenshots/about1.png)
![About 2](screenshots/about2.png)
![About 3](screenshots/about3.png)

If you find this project useful, consider giving it a star.
