# Movie Discovery & Recommendation Platform

## Backend

Backend service for the Movie Recommender application, built with Java and Spring Boot.

The backend provides REST APIs for retrieving and filtering movie data stored in the production TiDB Cloud database. It is deployed independently from the React frontend.

---

## 🚀 Live API

The production backend is deployed on Render.

**Production Base URL:**

https://movie-recommender-1hpp.onrender.com

**Frontend Application:**

https://movie-recommender-lyart.vercel.app/

**Frontend Repository:**

https://github.com/mlokesh01/movie-recommendation-frontend.git

**Backend Repository:**

https://github.com/mlokesh01/movie-recommendation-backend.git

### Example Production API

```text
GET https://movie-recommender-1hpp.onrender.com/api/movies/industry?industry=tollywood
```

The endpoint returns matching movie records as JSON.

---

## 🛠️ Tech Stack

### Backend

- **Java 17** - Backend programming language
- **Spring Boot 4.0.1** - Backend application framework
- **Spring Web MVC** - REST API development
- **Spring Data JPA** - Repository abstraction and database access
- **Hibernate ORM** - JPA implementation
- **Maven** - Dependency management and project build
- **Lombok** - Boilerplate reduction

### Database

- **TiDB Cloud Serverless** - Production relational database
- **MySQL Connector/J** - JDBC driver used to connect the application to the MySQL-compatible TiDB database

### Data Sources

The movie dataset used by the application was assembled by combining information collected from two external sources.

**IMDb-derived movie metadata:**

- Movie name
- Release year
- Genre
- Cast
- Director
- Other movie metadata

**TMDB-derived information:**

- Movie name
- Release year
- Poster URL
- Trailer URL

The information from both sources was matched and merged into the movie dataset before being stored in the production database.

The production backend does not request TMDB for every user request. It retrieves the prepared movie data from TiDB Cloud.

### Deployment and Tools

- **Render** - Backend deployment
- **GitHub** - Source-code repository
- **UptimeRobot** - External availability monitoring
- **Docker** - Containerized deployment

---

## 🏗️ Architecture

```text
                ┌───────────────────────┐
                │         IMDb          │
                │                       │
                │ Movie metadata        │
                │ • Name                │
                │ • Year                │
                │ • Genre               │
                │ • Cast                │
                │ • Director            │
                └───────────┬───────────┘
                            │
                            │
                ┌───────────▼───────────┐
                │       TMDB API        │
                │                       │
                │ • Movie information   │
                │ • Poster URLs         │
                │ • Trailer URLs        │
                └───────────┬───────────┘
                            │
                            │ Matching
                            │ + Merging
                            ▼
                ┌───────────────────────┐
                │    Prepared Movie     │
                │       Dataset         │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │     TiDB Cloud        │
                │    Production DB      │
                └───────────┬───────────┘
                            │
                            │ JDBC
                            ▼
                ┌───────────────────────┐
                │   Spring Boot API     │
                │   Java + JPA +        │
                │      Hibernate        │
                └───────────┬───────────┘
                            │
                         REST/HTTPS
                            │
                            ▼
                ┌───────────────────────┐
                │    React + Vite       │
                │      Frontend         │
                └───────────────────────┘
```

The application is divided into three independently deployed layers:

```text
Frontend  →  Backend API  →  Database
 Vercel       Render          TiDB Cloud
```

The backend acts as the middle layer between the frontend and the database.

The frontend does not connect directly to the production database.

---

## ✨ Features

### Movie Data Retrieval

The backend provides REST endpoints for retrieving movie information from the production database.

### Industry-Based Movie Retrieval

Movies can be retrieved according to their movie industry.

The application currently supports:

- Tollywood
- Kollywood
- Mollywood
- Sandalwood
- Bollywood
- Hollywood

Example:

```text
GET /api/movies/industry?industry=tollywood
```

### Movie Filtering

The backend supports filtering movies using the following parameters:

- Industry
- Year
- Genre
- Minimum rating
- Maximum rating

The frontend sends these preferences to the backend, which processes the request and retrieves matching records from the database.

### Multiple Genre Filtering

The backend can process multiple comma-separated genres.

Example:

```text
GET /api/movies/filter/tollywood?year=2023&genre=action,drama&ratingMin=6
```

### REST API

The backend exposes HTTP endpoints that allow the React frontend to communicate with the movie data through the Spring Boot application.

### Database Integration

Spring Data JPA and Hibernate are used for database access.

The backend uses MySQL Connector/J to establish the JDBC connection with TiDB Cloud.

### Repository-Based Data Access

Database operations are organized through Spring Data JPA repository interfaces.

Each supported movie industry has its corresponding repository and entity.

---

## 🔌 API

### 1. Get Movies by Industry

**Endpoint**

```text
GET /api/movies/industry
```

**Query parameter**

```text
industry
```

**Example**

```text
GET /api/movies/industry?industry=tollywood
```

**Production request**

```text
https://movie-recommender-1hpp.onrender.com/api/movies/industry?industry=tollywood
```

**Response**

Returns movie records as JSON.

---

### 2. Filter Movies

**Endpoint**

```text
GET /api/movies/filter/{industry}
```

**Path parameter**

```text
industry
```

**Optional query parameters**

```text
year
genre
ratingMin
ratingMax
```

### Example

```text
GET /api/movies/filter/tollywood?year=2023&genre=action&ratingMin=6
```

### Multiple Genres

```text
GET /api/movies/filter/tollywood?year=2023&genre=action,drama&ratingMin=6
```

### Production Example

```text
https://movie-recommender-1hpp.onrender.com/api/movies/filter/tollywood?year=2023&genre=action&ratingMin=6
```

The response contains the matching movie records in JSON format.

---

## 🔄 Request Flow

A typical movie-search request follows this flow:

```text
1. User selects movie preferences
             ↓
2. React frontend sends an HTTP request
             ↓
3. Render receives the request
             ↓
4. Spring Boot processes the request
             ↓
5. MovieController receives the API request
             ↓
6. MovieService processes the filtering logic
             ↓
7. Spring Data JPA repository queries the database
             ↓
8. Hibernate generates and executes the required SQL
             ↓
9. TiDB Cloud returns matching records
             ↓
10. Spring Boot serializes the results as JSON
             ↓
11. JSON response is sent to the frontend
             ↓
12. React displays the movies
```

---

## 📁 Project Structure

The backend follows a layered Spring Boot structure:

```text
movie-recommendation-backend/
│
├── .mvn/
│   └── wrapper/
│
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── movie_recommendation/
│   │   │           └── movie_recommendation/
│   │   │               ├── controller/
│   │   │               │   └── MovieController.java
│   │   │               │
│   │   │               ├── entity/
│   │   │               │   ├── Industry.java
│   │   │               │   ├── Tollywood.java
│   │   │               │   ├── Kollywood.java
│   │   │               │   ├── Mollywood.java
│   │   │               │   ├── Sandalwood.java
│   │   │               │   ├── Bollywood.java
│   │   │               │   └── Hollywood.java
│   │   │               │
│   │   │               ├── repository/
│   │   │               │   └── ...
│   │   │               │
│   │   │               ├── service/
│   │   │               │   └── MovieService.java
│   │   │               │
│   │   │               └── MovieRecommendationApplication.java
│   │   │
│   │   └── resources/
│   │       └── application.yaml
│   │
│   └── test/
│
├── Dockerfile
├── mvnw
├── mvnw.cmd
├── pom.xml
├── .gitignore
└── .gitattributes
```

### Layer Responsibilities

```text
Controller
    ↓
Receives HTTP requests and exposes REST endpoints

Service
    ↓
Processes industry selection and filtering logic

Repository
    ↓
Communicates with the database through Spring Data JPA

Entity
    ↓
Represents the movie data model
```

---

## ⚙️ Configuration

The application uses Spring Boot externalized configuration.

Production database configuration is supplied through environment variables rather than being hard-coded into the application.

The production configuration uses:

```text
SPRING_DATA_SOURCE_URL
SPRING_DATA_SOURCE_USERNAME
SPRING_DATA_SOURCE_PASSWORD
PORT
```

The application also configures HikariCP connection-pool settings.

### Important

**Never commit production database credentials to GitHub.**

If you run the application locally, provide your own accessible TiDB/MySQL-compatible database configuration.

---

## 🗄️ Database

The production database is hosted on **TiDB Cloud Serverless**.

The backend connects to TiDB using JDBC through MySQL Connector/J.

```text
Spring Boot
     ↓
Spring Data JPA
     ↓
Hibernate
     ↓
JDBC
     ↓
MySQL Connector/J
     ↓
TiDB Cloud
```

TiDB's MySQL compatibility allows the application to use the MySQL JDBC driver.

### Database Configuration

The application uses:

- HikariCP for connection pooling
- Spring Data JPA for repository access
- Hibernate for ORM
- `ddl-auto: update`
- `open-in-view: false`

---

## 🧩 JPA and Hibernate

Spring Data JPA provides the repository abstraction used by the backend.

Hibernate provides the JPA implementation and handles ORM operations between Java entities and database records.

The application uses repository interfaces to access movie data instead of manually handling low-level JDBC operations throughout the application.

---

## 🔐 Security and Secrets

Production credentials and private configuration should not be stored directly in source code.

The following should never be committed to a public repository:

```text
Database passwords
Database credentials
Private API credentials
Deployment secrets
```

Production configuration should be supplied through Render's environment-variable configuration.

The repository should contain only non-sensitive configuration and source code.

---

## 💻 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/mlokesh01/movie-recommendation-backend.git
cd movie-recommendation-backend
```

### 2. Configure the database

Provide the required database configuration for your development environment.

The local application must have access to an appropriate TiDB/MySQL-compatible database.

### 3. Build the project

Using the Maven Wrapper:

**Windows**

```bash
mvnw.cmd clean package
```

**Linux / macOS**

```bash
./mvnw clean package
```

Alternatively, if Maven is installed globally:

```bash
mvn clean package
```

### 4. Run the application

Using the Maven Wrapper:

**Windows**

```bash
mvnw.cmd spring-boot:run
```

**Linux / macOS**

```bash
./mvnw spring-boot:run
```

Alternatively:

```bash
mvn spring-boot:run
```

### 5. Test the API

Once the application is running, access an API endpoint through a browser, Hoppscotch, Postman, curl, or another HTTP client.

Example:

```text
http://localhost:8080/api/movies/industry?industry=tollywood
```

---

## 🏭 Production Build

The project uses Maven for dependency management and building.

Build the application with:

```bash
./mvnw clean package
```

On Windows:

```bash
mvnw.cmd clean package
```

The resulting Spring Boot JAR can be run with:

```bash
java -jar target/<application-name>.jar
```

---

## 🐳 Docker

The repository includes a Dockerfile for containerized deployment.

The Docker image uses Java 17 and builds the application using the Maven Wrapper.

The container exposes port `8080`, while the application is configured to use Render's dynamically supplied `PORT` value when deployed.

---

## ☁️ Deployment

The backend is deployed on **Render**.

### Deployment Flow

```text
GitHub
   │
   │ Source code
   ▼
Render
   │
   │ Spring Boot application
   ▼
Production API
   │
   │ JDBC
   ▼
TiDB Cloud
```

### Production API

```text
https://movie-recommender-1hpp.onrender.com
```

The backend repository is connected to the Render service for deployment.

---

## 🌐 Frontend Integration

The backend is consumed by the separately deployed React frontend.

```text
Frontend
https://movie-recommender-lyart.vercel.app/

            │
            │ HTTPS / REST
            ▼

Backend
https://movie-recommender-1hpp.onrender.com

            │
            │ JDBC
            ▼

Database
TiDB Cloud Serverless
```

The frontend does not connect directly to the production database.

```text
React → Spring Boot → TiDB
```

This keeps database access and database credentials on the backend side.

---

## 📡 Production API Example

Example request:

```text
GET https://movie-recommender-1hpp.onrender.com/api/movies/industry?industry=tollywood
```

The production endpoint returns movie records as JSON.

Example response fields include:

```text
movie_id
title
release_year
genre
rating
cast
director
movie_poster
trailer_link
```

---

## 🩺 Monitoring

The deployed backend is monitored using **UptimeRobot**.

The monitoring service periodically sends requests to the production backend to detect availability problems.

UptimeRobot provides external availability monitoring. It does not replace application logging, error tracking, or application-level health checks.

---

## ⚠️ Production Considerations

### Render Service Availability

The backend is hosted on Render.

Depending on the Render service configuration, the service may become idle and require time to start when a request arrives.

This can result in a slower response to the first request after inactivity.

### Database Availability

The backend depends on the availability of the TiDB Cloud database.

If the database connection cannot be established, the backend cannot retrieve movie records.

Therefore:

```text
Backend available
        +
Database available
        =
Movie API works
```

A functioning frontend alone cannot compensate for a backend or database failure.

---

## 🧪 Testing

The deployed backend should be tested independently from the frontend.

Important checks include:

- Backend starts successfully
- Database connection succeeds
- API endpoints respond correctly
- Movie data is returned as JSON
- Industry retrieval works
- Year filtering works
- Genre filtering works
- Minimum-rating filtering works
- Maximum-rating filtering works
- Frontend can communicate with the production API
- Database credentials are not exposed
- Production API remains reachable

### Production API Test

```text
https://movie-recommender-1hpp.onrender.com/api/movies/industry?industry=tollywood
```

---

## 📦 Deployment Stack

| Layer | Technology / Platform |
|---|---|
| Programming language | Java 17 |
| Backend framework | Spring Boot 4.0.1 |
| Web framework | Spring Web MVC |
| Data access | Spring Data JPA |
| ORM | Hibernate |
| Database | TiDB Cloud Serverless |
| Database driver | MySQL Connector/J |
| Connection pool | HikariCP |
| Build / dependency management | Maven |
| Boilerplate reduction | Lombok |
| Containerization | Docker |
| Source control | Git + GitHub |
| Backend deployment | Render |
| Frontend deployment | Vercel |
| Monitoring | UptimeRobot |

---

## 🎬 Data Collection and Preparation

The movie dataset was prepared by combining information from IMDb and TMDB.

### IMDb-derived information

The dataset includes movie metadata such as:

- Movie name
- Release year
- Genre
- Cast
- Director
- Other movie metadata

### TMDB-derived information

The dataset includes:

- Movie name
- Release year
- Poster URL
- Trailer URL

The information from the two sources was matched and merged into the dataset used by the application.

The prepared dataset was then stored in the TiDB Cloud production database.

The production backend serves this stored data rather than making TMDB API requests for every user query.

> IMDb and TMDB are external sources. This project is not affiliated with or endorsed by IMDb or TMDB.

---

## 📌 Repository

This repository contains **only the backend** of the Movie Recommender project.

**Backend Repository:**

https://github.com/mlokesh01/movie-recommendation-backend.git

The frontend is maintained separately:

**Frontend Repository:**

https://github.com/mlokesh01/movie-recommendation-frontend.git

**Live Application:**

https://movie-recommender-lyart.vercel.app/

The two repositories together form the complete application:

```text
Movie Recommender
│
├── movie-recommendation-frontend
│       └── React + Vite frontend
│
└── movie-recommendation-backend
        └── Java + Spring Boot backend
```

---

## ⚠️ Project Scope

This repository contains the backend application responsible for:

- Receiving API requests
- Processing movie-filtering requests
- Accessing the production database
- Retrieving movie records
- Returning movie data as JSON
- Providing the API consumed by the frontend

It does **not** contain:

- The React frontend source code
- The production TiDB database itself
- Production database credentials
- Private deployment secrets
- The underlying IMDb or TMDB databases

---

## 🔗 Complete Application

The Movie Recommender application consists of three independently deployed components:

```text
                         MOVIE RECOMMENDER
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
             FRONTEND                      BACKEND
              Vercel                        Render
                 │                             │
                 │        HTTPS / REST         │
                 └─────────────►───────────────┘
                                               │
                                               │ JDBC
                                               ▼
                                        TiDB Cloud
```

### Production Services

**Frontend**

```text
https://movie-recommender-lyart.vercel.app/
```

**Backend**

```text
https://movie-recommender-1hpp.onrender.com
```

**Database**

```text
TiDB Cloud Serverless
```

---

## 👨‍💻 Development

Built as a full-stack movie application with independently maintained frontend and backend repositories.

The backend provides the API layer between the React frontend and the production TiDB Cloud database.
