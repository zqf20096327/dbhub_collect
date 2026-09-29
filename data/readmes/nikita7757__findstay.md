# 🏡 FindStay

FindStay is a full-stack Airbnb-inspired property rental platform where users can browse, search, and book accommodations. Hosts can list and manage their properties, while users can explore destinations, view property details, and make bookings through a modern and responsive interface.

## 🚀 Live Demo

---

## 📸 Screenshots

> Add screenshots of your application here.

Example:

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/52752e62-8c26-4739-9557-13cecfc202ce" />

<img width="936" height="534" alt="image" src="https://github.com/user-attachments/assets/cab042db-e47f-4404-aa1c-c11c449a8633" />


<img width="901" height="490" alt="image" src="https://github.com/user-attachments/assets/29670301-8704-4a95-8abe-d3f16c9c241f" />

<img width="951" height="503" alt="image" src="https://github.com/user-attachments/assets/db6ce9bb-a069-4e94-ad09-5b252854874b" />
<img width="936" height="532" alt="image" src="https://github.com/user-attachments/assets/a92377ec-2b78-4a0f-9b62-53217ea2f463" />

---

## ✨ Features

### User Features

- User Registration & Login
- Browse available properties
- Search properties by location
- View detailed property information
- Book accommodations
- View booking details
- Responsive design for desktop and mobile

### Host Features

- Add new properties
- Edit property details
- Delete properties
- Manage listed properties

---

## 🛠 Tech Stack

### Frontend

- Angular
- TypeScript
- HTML5
- CSS3
- Bootstrap

### Backend

- Java 17
- Spring Boot
- Spring Data JPA
- Hibernate
- REST APIs

### Database

- MySQL

### Tools

- Git
- GitHub
- Maven
- Postman
- Render
- Vercel

---

## 📂 Project Structure

```
FindStay
│
├── frontend/
│   ├── src/
│   ├── angular.json
│   └── package.json
│
├── backend/
│   ├── src/
│   ├── pom.xml
│   └── application.properties
│
└── README.md
```

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/nikita7757/Findstay.git
cd Findstay
```

---

## Backend Setup

```bash
cd backend
```

Configure your database in:

```
src/main/resources/application.properties
```

Example:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/findstay
spring.datasource.username=YOUR_USERNAME
spring.datasource.password=YOUR_PASSWORD
```

Run the application:

```bash
./mvnw spring-boot:run
```

Backend runs on:

```
http://localhost:8091
```

---

## Frontend Setup

```bash
cd frontend
npm install
ng serve
```

Frontend runs on:

```
http://localhost:4200
```

---

## REST API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /properties/all | Get all properties |
| GET | /properties/{id} | Get property by ID |
| POST | /properties/add-property | Add new property |
| PUT | /properties/{id} | Update property |
| DELETE | /properties/{id} | Delete property |

---

## Future Enhancements

- JWT Authentication
- Spring Security
- Wishlist
- Payment Gateway
- Email Notifications
- Reviews & Ratings
- Admin Dashboard

---

## Learning Outcomes

This project helped me gain hands-on experience with:

- Full Stack Web Development
- REST API Development
- Angular Components & Routing
- Spring Boot Architecture
- Database Design
- CRUD Operations
- Git & GitHub Version Control
- Frontend & Backend Deployment

---

## Author

**Nikita Shedage**

- GitHub: https://github.com/nikita7757
- LinkedIn: https://www.linkedin.com/in/nikita-shedage/

---

## 📄 License

This project is intended for educational and portfolio purposes only.

© 2026 Nikita Shedage. All rights reserved.
