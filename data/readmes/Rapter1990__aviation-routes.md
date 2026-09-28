## Case Study - Aviation Routes (Spring Boot + React)

<p align="center">
  <img src="screenshots/main_image.png" alt="Aviation Routes - Main Screen" width="900" height="520">
</p>

### 📖 Information

### Project Definition — Aviation Routes

A Spring Boot service that stores **Locations** and **Transportations** and provides REST APIs to:

- **Manage Locations** (create / update / delete / list)
- **Manage Transportations** (create / update / delete / list)
- **Search valid Routes** between an origin and destination with the rule set:
  - max **3 legs**
  - **exactly 1 flight**
  - max **1 pre-flight transfer** (non-flight before the flight)
  - max **1 post-flight transfer** (non-flight after the flight)
- **Filter routes by date** using `Operating Days` (bonus complexity)

All responses are wrapped in a consistent `CustomResponse<T>` envelope, and paging is returned as `CustomPage<T>` (or `CustomPagingResponse<T>` depending on your naming).

---

### Domain Model

#### 1) Location

A `Location` represents a stop such as an airport or a point in a city.

- `name`
- `country`
- `city`
- `code` (unique, used for search; e.g., `IST`, `LHR`, `WEMBLEY`)

#### 2) Transportation

A `Transportation` represents a directed connection:

- `origin` (Location)
- `destination` (Location)
- `type` (e.g., `BUS`, `SUBWAY`, `UBER`, `FLIGHT`)
- `operatingDays` (optional bonus):
  - `[1..7]` means Monday..Sunday
  - empty / null ⇒ **operates every day**

#### 3) Route (Result)

A `Route` is a sequence of 1..3 `legs` that follows the validity rules and date constraints.

Each `leg` contains:
- `transportationId`
- `type`
- `originCode`
- `destinationCode`

---

### Route Validity Rules (Core Requirement)

A sequence of connected transportations is a **valid route** if:

- ✅ It contains **at most 3 legs**
- ✅ It contains **exactly 1 flight**
- ✅ It contains **at most 1 pre-flight** transfer (non-flight before the flight)
- ✅ It contains **at most 1 post-flight** transfer (non-flight after the flight)

Valid examples:

- ✅ `UBER → FLIGHT → BUS`
- ✅ `FLIGHT → BUS`
- ✅ `UBER → FLIGHT`

Invalid examples:

- ❌ `UBER → BUS → FLIGHT` (multiple pre-flight transfers)
- ❌ `UBER → BUS` (no flight)
- ❌ `UBER → FLIGHT → FLIGHT` (multiple flights)
- ❌ `FLIGHT → SUBWAY → UBER` (multiple post-flight transfers)

---

### Operating Days & Date Filtering (Bonus)

Each transportation can define `operatingDays`:

- `[1, 3, 5, 6]` ⇒ Monday, Wednesday, Friday, Saturday
- `[]` or `null` ⇒ **every day**

When the route search endpoint receives a `date`, the service:

- converts date to day-of-week (1..7)
- **excludes** any route that contains a leg not active on that day

Example:

Route:
- `BUS (TAKSIM → IST)` days `[2, 3, 5]`
- `FLIGHT (IST → LHR)` days `[2, 3, 7]`
- `UBER (LHR → WEMBLEY)` days `[3, 5]`

- `2025-03-12` (Wednesday = 3) ⇒ ✅ route returned
- `2025-03-11` (Tuesday = 2) ⇒ ❌ route excluded (post-transfer not active)

---

## End-to-end Flow

### 1) Manage Locations

#### Create Location (`POST /api/locations`)
- Client sends `CreateLocationRequest` containing:
  - `name`, `country`, `city`, `code`
- Service validates request and persists to DB.
- Returns:
  - `200 OK` with `CustomResponse<LocationResponse>`

#### List Locations (Paged) (`POST /api/locations/list`)
- Client sends paging request (`CustomPagingRequest`)
- Returns:
  - `200 OK` with `CustomResponse<CustomPage<LocationResponse>>`

---

### 2) Manage Transportations

#### Create Transportation (`POST /api/transportations`)
- Client sends `CreateTransportationRequest` containing:
  - `originCode`, `destinationCode`, `type`
  - optional `operatingDays`
- Service resolves origin/destination by code and persists to DB.
- Returns:
  - `200 OK` with `CustomResponse<TransportationResponse>`

#### List Transportations (Paged) (`POST /api/transportations/list`)
- Client sends paging request (`CustomPagingRequest`)
- Returns:
  - `200 OK` with `CustomResponse<CustomPage<TransportationResponse>>`

---

### 3) Search Routes (`POST /api/routes/search`)

- Client sends `FindRoutesPagedRequest`:
  - `filter.origin` (code)
  - `filter.destination` (code)
  - `filter.date` (optional, ISO `YYYY-MM-DD`)
  - plus paging: page number, page size
- Service:
  1. resolves origin/destination locations
  2. enumerates valid route patterns:
    - `FLIGHT`
    - `PRE + FLIGHT`
    - `FLIGHT + POST`
    - `PRE + FLIGHT + POST`
  3. enforces date filter via `operatingDays` on each leg
- Returns:
  - `200 OK` with `CustomResponse<CustomPage<RouteResponse>>`

---

## Error Semantics

- `400 Bad Request` — Validation errors (`@Valid`) such as invalid codes, invalid date format, etc.
- `404 Not Found` — Location not found by code, transportation not found, etc.
- `409 Conflict` — Unique constraint violations (e.g., duplicate location code)
- `500 Internal Server Error` — DB access failures or unexpected errors

**Custom Exceptions (examples)**

- `NotFoundException` → `404 NOT_FOUND`
- `AlreadyExistsException` (or `ConflictException`) → `409 CONFLICT`
- `ValidationException` → `400 BAD_REQUEST`

---

## Explore REST APIs

### Endpoints Summary

| Method | URL | Description | Request Body | Headers | Response | Status Codes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| POST | `/api/locations` | Create a location. | `CreateLocationRequest` | `Content-Type: application/json` | `CustomResponse<LocationResponse>` | 200, 400, 409, 500 |
| GET | `/api/locations/{id}` | Get location by id. | - | - | `CustomResponse<LocationResponse>` | 200, 404, 500 |
| PUT | `/api/locations/{id}` | Update location by id. | `UpdateLocationRequest` | `Content-Type: application/json` | `CustomResponse<LocationResponse>` | 200, 400, 404, 409, 500 |
| DELETE | `/api/locations/{id}` | Delete location by id. | - | - | `CustomResponse<Void>` | 200, 404, 500 |
| POST | `/api/locations/list` | List locations (paged). | `CustomPagingRequest` | `Content-Type: application/json` | `CustomResponse<CustomPage<LocationResponse>>` | 200, 400, 500 |
| POST | `/api/transportations` | Create a transportation. | `CreateTransportationRequest` | `Content-Type: application/json` | `CustomResponse<TransportationResponse>` | 200, 400, 404, 500 |
| GET | `/api/transportations/{id}` | Get transportation by id. | - | - | `CustomResponse<TransportationResponse>` | 200, 404, 500 |
| PUT | `/api/transportations/{id}` | Update transportation by id. | `UpdateTransportationRequest` | `Content-Type: application/json` | `CustomResponse<TransportationResponse>` | 200, 400, 404, 500 |
| DELETE | `/api/transportations/{id}` | Delete transportation by id. | - | - | `CustomResponse<Void>` | 200, 404, 500 |
| POST | `/api/transportations/list` | List transportations (paged). | `CustomPagingRequest` | `Content-Type: application/json` | `CustomResponse<CustomPage<TransportationResponse>>` | 200, 400, 500 |
| POST | `/api/routes/search` | Search valid routes (paged) with optional date filtering. | `FindRoutesPagedRequest` | `Content-Type: application/json` | `CustomResponse<CustomPage<RouteResponse>>` | 200, 400, 404, 500 |


-----

### Technologies

* Java 25
* Spring Boot 3.0
* Restful API
* Open Api (Swagger)
* Maven
* Junit5
* Mockito
* Integration Tests
* TestContainer
* Mapstruct
* Docker
* Docker Compose
* CI/CD (Github Actions)
* Postman
* Postgres
* Kubernetes
* JaCoCo (Test Report)
* AOP
* Prometheus
* Grafana
* SonarQube
* React
* Material UI
* Nginx

-----

### Postman

```
Import postman collection under postman_collection folder
```

-----

### Prerequisites

#### For Backend Side

```
$ cd aviation-routes-backend
```
#### Define Variable in .env file
```
AVIATION_ROUTES_DB_IP=localhost
AVIATION_ROUTES_DB_PORT=5432
POSTGRES_USER={your-postgres-user}
POSTGRES_PASSWORD={your-postgres-password}
```

#### For Frontend Side

```
$ cd aviation-ui
```
#### Define Variable in .env file
```
VITE_API_BASE_URL=http://localhost:3141
```

-----

### Open Api (Swagger)

```
http://localhost:3141/swagger-ui/index.html
```

-----

### JaCoCo (Test Report)

After the command named `mvn clean install` completes, the JaCoCo report will be available at:
```
target/site/jacoco/index.html
```
Navigate to the `target/site/jacoco/` directory.

Open the `index.html` file in your browser to view the detailed coverage report.

---

### Maven, Docker and Kubernetes Running Process


### Maven Run
To build and run the application with `Maven`, please follow the directions shown below;

```sh
$ git clone https://github.com/Rapter1990/aviation-routes.git
$ cd aviation-routes-backend
$ mvn clean install
$ mvn spring-boot:run
$ cd aviation-ui
$ npm install --force
$ npm run dev 
```

-----

### Docker Run

The application can be built and run by the `Docker` engine. The `Dockerfile` has multistage build, so you do not need to build and run separately.

Please follow directions shown below in order to build and run the application with Docker Compose file;

```sh
$ cd aviation-routes
$ docker-compose up -d 
```

If you change anything in the project and run it on Docker, you can also use this command shown below

```sh
$ cd aviation-routes
$ docker-compose up -d --build
```

To monitor the application, you can use the following tools:

- **Prometheus**:  
  Open in your browser at [http://localhost:9090](http://localhost:9090)  
  Prometheus collects and stores application metrics.

- **Grafana**:  
  Open in your browser at [http://localhost:3000](http://localhost:3000)  
  Grafana provides a dashboard for visualizing the metrics.  
  **Default credentials**:
  - Username: `admin`
  - Password: `admin`

Define prometheus data source url, use this link shown below

```
http://prometheus:9090
```

-----

### Kubernetes Run
To run the application, please follow the directions shown below;

- Start Minikube

```sh
$ minikube start
```

- Open Minikube Dashboard

```sh
$ minikube dashboard
```

- To deploy the application on Kubernetes, apply the Kubernetes configuration file underneath k8s folder

```sh
$ kubectl apply -f k8s
```

- To learn url to be used for App through Minikube
```sh
minikube service aviation-routes-backend --url
```

It will print something like:

```sh
http://127.0.0.1:xxxxx
```

Then call:
```sh
http://127.0.0.1:xxxxx/api/routes/search
```

---
### Docker Image Location

```
https://hub.docker.com/repository/docker/noyandocker/aviation-routes-backend/general
```

-----

### Sonarqube

- Go to `localhost:9000` for Docker and Go there through `minikube service sonarqube` for Kubernetes
- Enter username and password as `admin`
- Change password
- Click `Create Local Project`
- Choose the baseline for this code for the project as `Use the global setting`
- Click `Locally` in Analyze Method
- Define Token
- Click `Continue`
- Copy `sonar.host.url` and `sonar.token` (`sonar.login`) in the `properties` part in  `pom.xml`
- Run `mvn sonar:sonar` to show code analysis

-----

### 📸 Screenshots

<details>
<summary>Click here to show the screenshots of project</summary>
    <p> Figure 1 </p>
    <img src ="screenshots/jacoco.PNG">
    <p> Figure 2 </p>
    <img src ="screenshots/swagger.PNG">
    <p> Figure 3 </p>
    <img src ="screenshots/docker_info.PNG">
    <p> Figure 4 </p>
    <img src ="screenshots/1.PNG">
    <p> Figure 5 </p>
    <img src ="screenshots/2.PNG">
    <p> Figure 6 </p>
    <img src ="screenshots/3.PNG">
    <p> Figure 7 </p>
    <img src ="screenshots/4.PNG">
    <p> Figure 8 </p>
    <img src ="screenshots/5.PNG">
    <p> Figure 9 </p>
    <img src ="screenshots/6.PNG">
    <p> Figure 10 </p>
    <img src ="screenshots/7.PNG">
    <p> Figure 11 </p>
    <img src ="screenshots/8.PNG">
    <p> Figure 12 </p>
    <img src ="screenshots/9.PNG">
    <p> Figure 13 </p>
    <img src ="screenshots/10.PNG">
    <p> Figure 14 </p>
    <img src ="screenshots/11.PNG">
    <p> Figure 15 </p>
    <img src ="screenshots/12.PNG">
    <p> Figure 16 </p>
    <img src ="screenshots/13.PNG">
    <p> Figure 17 </p>
    <img src ="screenshots/14.PNG">
    <p> Figure 18 </p>
    <img src ="screenshots/15.PNG">
    <p> Figure 19 </p>
    <img src ="screenshots/16.PNG">
    <p> Figure 20 </p>
    <img src ="screenshots/17.PNG">
    <p> Figure 21 </p>
    <img src ="screenshots/18.PNG">
    <p> Figure 22 </p>
    <img src ="screenshots/19.PNG">
    <p> Figure 23 </p>
    <img src ="screenshots/20.PNG">
    <p> Figure 24 </p>
    <img src ="screenshots/21.PNG">
    <p> Figure 25 </p>
    <img src ="screenshots/22.PNG">
    <p> Figure 26 </p>
    <img src ="screenshots/23.PNG">
    <p> Figure 27 </p>
    <img src ="screenshots/24.PNG">
    <p> Figure 28 </p>
    <img src ="screenshots/25.PNG">
    <p> Figure 29 </p>
    <img src ="screenshots/26.PNG">
    <p> Figure 30 </p>
    <img src ="screenshots/27.PNG">
    <p> Figure 31 </p>
    <img src ="screenshots/28.PNG">
    <p> Figure 32 </p>
    <img src ="screenshots/29.PNG">
    <p> Figure 33 </p>
    <img src ="screenshots/30.PNG">
    <p> Figure 34 </p>
    <img src ="screenshots/31.PNG">
</details>

-----

### Contributors

- [Sercan Noyan Germiyanoğlu](https://github.com/Rapter1990)
