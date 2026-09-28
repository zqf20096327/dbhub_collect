# LOFAU Multivendor Ecommerce Platform

## Overview
Lofau is a full-stack multivendor ecommerce platform that allows multiple vendors to register, manage products, and process orders in a shared marketplace environment.

The system supports three roles: Admin, Vendor, and Customer, each with specific permissions and responsibilities. It is built using Spring Boot for the backend, React for the frontend, and MySQL as the database, with JWT handling authentication and security.

---

## Tech Stack

Backend:
Spring Boot, Spring Data JPA, Hibernate, MySQL, JWT Authentication

Frontend:
React, Tailwind CSS, Material UI

Tools:
Git, GitHub, Maven

---

## Core Features

The platform includes user authentication with secure JWT login and role-based access control. Vendors can register, manage products, and track their orders. Admins can approve or reject products, manage users, and moderate the system. Customers can browse products, view details, and place orders.

Order management is fully integrated, allowing order creation, tracking, and status updates across the system.

---

## System Architecture

The system follows a client-server architecture. The React frontend communicates with the Spring Boot backend through REST APIs. The backend handles all business logic including authentication, product management, and order processing. MySQL is used as the persistent storage layer for users, products, orders, and roles.

---

## Project Structure

The backend is organized into a standard Spring Boot layered architecture. Inside the backend, the src/main/java directory contains controllers for handling API requests, services for business logic, repositories for database access, models for entity definitions, and a security package for JWT configuration and authentication. The src/main/resources folder contains the application.properties file used for configuration.

The frontend is structured into reusable components, pages for different views, services for API communication, and the main App.js file that controls routing and application flow.

---

## API Endpoints

Authentication includes endpoints for user registration and login. Products can be created, updated, fetched, or deleted depending on user roles. Orders allow customers to create and view their purchases. Admin endpoints handle user management and product approval workflows.

---

## Database Design

The system includes tables for users, roles, products, orders, order items, and categories. Users are linked to roles, vendors own products, and each order can contain multiple items. This relational structure ensures data consistency and scalability.

---

## Setup Instructions

To run the project locally, first clone the repository using git clone <your-repo-url> and navigate into the project folder.

For the backend, go into the backend directory, configure the database settings inside application.properties including MySQL URL, username, and password, then run the Spring Boot application using Maven.

For the frontend, navigate to the frontend directory, install dependencies using npm install, and start the development server using npm start.

---

## Future Improvements

The system can be extended with payment gateway integration, email notifications, an advanced analytics dashboard for admins, a product recommendation engine, and real-time order tracking features.

---

## Known Limitations

The frontend is still under active development, and payment processing has not yet been implemented. The moderation system is also basic and can be improved further.


## Screenshots

Below are key UI and system views of the LOFAU Multivendor Ecommerce Platform:

### Home / Landing Page
![Image 0](./ecommerce-multivendor/image0.png)

### Login Page
![Image 1](./ecommerce-multivendor/image1.png)

### Deals
![Image 2](./ecommerce-multivendor/image2.png)

### Product Details Page
![Image 3](./ecommerce-multivendor/image3.png)

### HomePage
![Image 4](./ecommerce-multivendor/image4.png)

### Product Listing
![Image 5](./ecommerce-multivendor/image5.png)

### Product view
![Image 6](./ecommerce-multivendor/image6.png)

### ### Cart / Checkout Page
![Image 7](./ecommerce-multivendor/image7.png)
---

## Author

Benedict Juma

---

## License

This project is intended for educational and portfolio use.
