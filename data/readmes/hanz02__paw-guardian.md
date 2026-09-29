# 🐾 Paw Guardian - Animal Shelter Management System

**Paw Guardian** is a web-based platform designed to bridge the gap between animal shelters and the community. This system simplifies volunteering for workshops, managing donations, and providing administrative oversight for shelter operations.

**Live Deployed Site:** [https://paw-guardian.onrender.com/](https://paw-guardian.onrender.com/)
---

### ⚠️ Security Disclaimer
> **Note:** This live site is a **students group project** intended for educational purposes only. It is **not secure** for real-world use or sensitive data storage. Please do not use real passwords or personal information.

---

## 👥 Team Members

| Name | Student ID | Role |
| :--- | :--- | :--- |
| **Khaw Han Zhe** | SWE2302061 | Developer 
| **Tey Wei Song** | SWE2302063 | Developer 
| **Nicholas Ng Yan Zhe** | SWE2304252 | Developer 
| **Ong Shi Ning** | SWE2304370 | Developer & Report Writing
| **Yap En Yin** | SWE2304371 | Developer & Report Writing

---

### 🏛️ Academic Context
* **University:** Xiamen University Malaysia
* **Course Code:** SWE306
* **Course Name:** Programming Elective II (1)
* **Lecturer:** Talal Ali

---

## 🛠️ Tech Stack

* **Backend:** Java Spring Boot 3
* **Frontend:** Thymeleaf, HTML5, CSS3, JavaScript
* **Database:** TiDB (MySQL Compatible)
* **Security:** Spring Security (BCrypt Encryption)
* **Media Storage:** ImgBB API (Cloud Image Hosting)
* **Deployment:** Render

---

## ✨ Features

### 🖼️ Cloud-Based Profile Management (ImgBB Integration)
To solve the challenge of ephemeral storage on Render's free tier, the system implements a cloud-based image solution.
* **Multipart Handling:** Backend controllers leverage `MultipartFile` to handle image data streams.
* **URL Persistence:** The system stores **permanent direct URLs** in the TiDB database, ensuring user avatars persist across server restarts.

### 🛡️ Secure Role-Based Access Control (RBAC)
* **Dual Security Filters:** Distinct `SecurityFilterChain` configurations separate user and administrator contexts.
* **Encrypted Credentials:** All passwords are protected using **BCrypt** hashing.

### 📅 Workshop & Donation Ecosystem
* **Volunteer Booking:** A real-time engine connecting user profiles with shelter events.
* **Donation Tracking:** A structured repository for recording and viewing community contributions.

---

## 🛠️ Technical Implementation

### 1. ImgBB API Integration
The system processes uploads by converting `MultipartFile` data into **Base64-encoded strings** for RESTful transmission.

```java
private String uploadToImgBB(MultipartFile file) {
    try {
        String url = "[https://api.imgbb.com/1/upload?key=](https://api.imgbb.com/1/upload?key=)" + imgbbApiKey;
        RestTemplate restTemplate = new RestTemplate();
        String base64Image = Base64.getEncoder().encodeToString(file.getBytes());
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("image", base64Image);

        Map<String, Object> response = restTemplate.postForObject(url, body, Map.class);
        Map<String, Object> data = (Map<String, Object>) response.get("data");
        return (String) data.get("url");
    } catch (Exception e) {
        e.printStackTrace();
        return null; 
    }
}
```

## 2. Database Design & Persistence (TiDB)
The application utilizes **TiDB**, a MySQL-compatible distributed SQL database, to manage relational data. TiDB provides the consistency and scalability required for a growing community of volunteers and donors.

* **URL Storage:** The `profile_picture` column in the `user` table is optimized as a `VARCHAR(500)` to store the full web URLs returned by the ImgBB API.
* **Relational Schema:** The database manages complex relationships between users, workshops, and volunteer bookings using foreign key constraints to ensure data integrity.
* **Spring Data JPA:** The backend interacts with TiDB through repository interfaces, leveraging Hibernate for automated query generation and transaction management.

## 3. Spring Security Configuration
The application employs a **dual-filter-chain architecture** to separate User and Admin security contexts. We use ordered beans to ensure administrative paths are checked with priority.

```java
@Bean
@Order(1) // Priority order for Admin requests
public SecurityFilterChain adminSecurityFilterChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/admin/**")
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/admin/login").permitAll()
            .anyRequest().hasRole("ADMIN")
        )
        .formLogin(form -> form
            .loginPage("/admin/login")
            .defaultSuccessUrl("/admin/dashboard", true)
        );
    return http.build();
}
```

## 🔐 Admin Access
The administration dashboard allows management of workshops, user accounts, and donation tracking. 

The credential to log into the admin site dashboard is as below, however you can modify the login email to your own liking in the database after running the SQL txt code file.

* **Email:** `admin@gmail.com`
* **Password:** `12345678`

## 🚀 Getting Started

### 1. Database Setup
* Create a database named `paw_db` in your **TiDB** or **MySQL** environment.
* Execute the queries found in `db_sql_creation.txt` to generate the necessary tables and seed the initial admin account.

### 2. Environment Variables
To run this project, you will need to add the following environment variables (especially for **Render** deployment):

* **`SPRING_DATASOURCE_URL`**: Your TiDB/MySQL connection string.
* **`SPRING_DATASOURCE_USERNAME`**: Your DB username.
* **`SPRING_DATASOURCE_PASSWORD`**: Your DB password.
* **`IMGBB_API_KEY`**: Your free API key from [api.imgbb.com](https://api.imgbb.com/).

### 3. Build and Run
```bash
./mvnw clean package
java -jar target/pawguardian-0.0.1-SNAPSHOT.jar
