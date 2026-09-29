# 🎓 CEMS: Campus Event Management System (v1.1)

CEMS is a robust, 3-tier enterprise application designed to streamline the proposal, approval, and registration of academic and extracurricular events across a university campus. 

---

## 🏗️ System Architecture (3-Tier)

CEMS utilizes a strict 3-Tier architecture to prevent direct client-to-database communication:

1. **Presentation Layer (Client):** A lightweight **Java Swing** desktop application. Features asynchronous network handling (`SwingWorker`) for non-blocking UI and loading states.
2. **Application Layer (API):** A **Spring Boot** RESTful API. Acts as the secure middleman, handling all business logic, validation, transaction rollbacks, and database routing.
3. **Data Layer (Database):** A **TiDB / MySQL** relational database structured in 3NF, enforcing data integrity via strict Foreign Key constraints.

---

## ✨ Key Features

* **Role-Based Access Control (RBAC):** Dedicated portals and permissions for Students, Organizers, and Administrators.
* **Event Lifecycle Management:** Organizers propose events, Admins approve/reject them, and Students browse and register for active events.
* **Smart Capacity Tracking:** Real-time venue capacity validation prevents overbooking during student registration.
* **Dynamic Timeline Math:** The API dynamically calculates whether an event is "Upcoming", "Ongoing", or "Completed" based on real-time server dates.
* **Zero-Trust Client:** The desktop application contains zero SQL queries and zero database credentials, relying entirely on HTTP requests to the REST API.

---

## 🚀 Installation & Setup

Because CEMS is a distributed application, you will need to run both the API and the Client.

### 1. The API (Spring Boot)
1. Clone the repository and open the `cems-api` folder in your IDE.
2. Update the `application.properties` file with your TiDB/MySQL database credentials.
3. Run `ApiApplication.java` to start the embedded Tomcat server on `localhost:8080`.

### 2. The Client (Java Swing)
1. Open the `cems-client` folder in your IDE.
2. Navigate to `src/utils/HttpUtils.java`.
3. Ensure the `BASE_URL` is pointing to your API (e.g., `http://localhost:8080/api` for local testing, or your Render URL for production).
4. Compile and run the application.

---

## 🧹 Configuration: Nightly Data Reset (Portfolio Mode)

By default, this API is configured for a public portfolio/demo environment. To prevent database clutter from test users, a Spring Boot `@Scheduled` cron job runs at exactly **00:00:00** every night. 

This job performs a "Scorched Earth" total wipe of all events, venues, departments, and user accounts (except permanent Administrators) while safely respecting Foreign Key constraints.

⚠️ **If you are deploying this for real-world campus use, you MUST disable this feature:**

1. Open `src/main/java/com/cems/api/ApiApplication.java`.
2. Remove the `@EnableScheduling` annotation from the top of the class.
3. *(Optional)* Delete the `DatabaseCleanupService.java` file entirely from the `services` package.

---

## 🛠️ Recent Updates
* **Security Upgrade:** Deprecated legacy DAO architecture. Removed `mysql-connector-java` from the client.
* **Network Handling:** Implemented `HttpUtils` for standard REST communication (GET, POST, PUT, DELETE).
* **UI/UX Enhancement:** Wrapped all HTTP calls in `SwingWorker` threads to prevent UI freezing during network latency.
* **Bug Fix (Ghost Sessions):** Synchronized client session IDs with database auto-generated IDs by chaining asynchronous login requests immediately after successful account creation.
