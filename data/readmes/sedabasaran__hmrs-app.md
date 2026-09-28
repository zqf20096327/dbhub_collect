# HRMS (Human Resource Management System)

##  Mevcut Diller / Available Languages
[🇹🇷 Türkçe](#türkçe) | [🇬🇧 English](#english)

---
## Türkçe 

### Proje Açıklaması
HRMS (İnsan Kaynakları Yönetim Sistemi) projesi, iş ilanlarının, iş başvurularının, işveren ve iş arayan bilgilerinin yönetildiği, Spring Boot tabanlı bir web servis uygulamasıdır.  
Proje, REST API mimarisi ile geliştirilmiş olup, **DTO**, **Request-Response Pattern**, **Validation** ve **Global Exception Handling** gibi modern yazılım geliştirme tekniklerini içermektedir.

---

### Özellikler
- **Şehir Yönetimi**: Şehir ekleme, listeleme.
- **İş Pozisyonu Yönetimi**: Pozisyon ekleme ve listeleme
- **İşveren Yönetimi**: İşveren kaydı ve listeleme.
- **İş arayan Yönetimi**: İş arayan kaydı ve listeleme.
- **İş İlanı Yönetimi**: İş ilanı ekleme, listeleme, filtreleme.
- **İş Başvurusu Yönetimi**: Adayların iş ilanlarına başvuru yapabilmesi.
- **Hata Yönetimi**: `@ControllerAdvice` ile global exception handling.
- **Validasyon**: `@NotBlank`, `@Size` `@Email`, `@Future` gibi anotasyonlarla doğrulama.

---

###  Kullanılan Teknolojiler
| Katman | Teknoloji |
|---|---|
| Dil | Java 17 |
| Framework | Spring Boot 3 |
| ORM | Spring Data JPA / Hibernate |
| Veritabanı | PostgreSQL |
| Test | JUnit 5, MockMvc |
| Yardımcı | Lombok, Jackson, Jakarta Validation |

---
###  Proje Katmanları
- **Entity**: Veritabanı tablolarını temsil eden sınıflar.
- **DTO**: Kullanıcıya döndürülecek veri transfer objeleri.
- **Request**: Kullanıcıdan alınacak verileri temsil eden sınıflar.
- **Service**: İş mantığı katmanı.
- **Repository (DAO)**: Veritabanı erişim katmanı.
- **Controller**: API uç noktalarının bulunduğu katman.
- **Core Utilities**: `Result`, `DataResult`, `SuccessResult`, `ErrorResult` gibi ortak dönüş yapıları.

**Result Yapısı:**
- `Result`: İşlem sonucu (başarılı / başarısız) ve mesaj döner.
- `DataResult<T>`: İşlem sonucu + veri döner.
- `SuccessResult`, `ErrorResult`: Başarılı veya hatalı işlem durumları için hazır sınıflar.

---

###  Örnek API Endpoint'leri
| HTTP | Endpoint | Açıklama |
|------|----------|----------|
| POST | `/api/employers/register` | Yeni işveren kaydı |
| GET  | `/api/employers/getAll` | Tüm işverenleri listele |
| POST | `/api/candidateController/register` | Yeni aday kaydı |
| GET  | `/api/candidateController/getAll` | Tüm adayları listele |
| POST | `/api/jobAdvertisements/add` | Yeni iş ilanı ekle |
| GET  | `/api/jobAdvertisements/getAll` | Tüm iş ilanlarını listele |
| POST | `/api/jobApplications/apply` | Adayın ilana başvurması |

---

### API Endpoint'leri

#### Şehirler
| Metod | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/cities/add` | Yeni şehir ekle |
| GET | `/api/cities/getAll` | Tüm şehirleri listele |

#### İşverenler
| Metod | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/employers/register` | Yeni işveren kaydı |
| GET | `/api/employers/getAll` | Tüm işverenleri listele |

#### İş Arayanlar
| Metod | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/candidateController/register` | Yeni aday kaydı |
| GET | `/api/candidateController/getAll` | Tüm adayları listele |

#### İş İlanları
| Metod | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/jobAdvertisements/add` | Yeni iş ilanı ekle |
| GET | `/api/jobAdvertisements/getAll` | Tüm ilanları listele |

#### İş Başvuruları
| Metod | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/jobApplications/apply` | İlana başvur |

### Örnek İstekler

**İşveren Kaydı**
```json
POST /api/employers/register
{
  "companyName": "Tech Solutions Ltd.",
  "companyWebPage": "https://techsolutions.com",
  "email": "contact@techsolutions.com",
  "phoneNumber": "+90-555-123-4567",
  "password": "password123",
  "confirmPassword": "password123"
}
```

**İş İlanı Ekleme**
```json
POST /api/jobAdvertisements/add
{
  "description": "Spring Boot deneyimli Java Backend Developer arıyoruz.",
  "openPositionCount": 2,
  "minSalary": 30000,
  "maxSalary": 50000,
  "applicationDeadline": "2025-12-31",
  "jobPositionId": 1,
  "cityId": 1,
  "employerId": 1
}
```

### Testler

JUnit 5 ve MockMvc ile yazılmış 27 birim ve entegrasyon testi.

| Test Sınıfı | Tür | Ne Test Ediyor |
|---|---|---|
| `CityDaoTest` | Birim | Kaydetme, duplicate isim kısıtlaması |
| `CityControllerTest` | Entegrasyon | API yanıtları, validasyon |
| `EmployerDaoTest` | Birim | Kaydetme, duplicate email kısıtlaması |
| `JobSeekerDaoTest` | Birim | Kaydetme, duplicate email ve TC kimlik kısıtlaması |
| `JobPositionDaoTest` | Birim | Kaydetme ve listeleme |
| `JobAdvertisementDaoTest` | Birim | İlişkili entity ile kaydetme |
| `JobAdvertisementControllerTest` | Entegrasyon | İlan API yanıtları |
| `JobApplicationDaoTest` | Birim | Başvuru kaydetme ve durum kontrolü |

```bash
mvn test
# Tests run: 27, Failures: 0, Errors: 0
```

### Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/sedabasaran/hmrs-app.git
cd hmrs-app

# 2. Veritabanı oluştur
psql -U postgres -c "CREATE DATABASE hrms;"

# 3. application.properties güncelle
spring.datasource.url=jdbc:postgresql://localhost:5432/hrms
spring.datasource.username=kullanici_adi
spring.datasource.password=sifre

# 4. Çalıştır
mvn spring-boot:run
```

API `http://localhost:8080` adresinde çalışır.

### Yanıt Yapısı

Tüm endpoint'ler tutarlı bir yanıt formatı döndürür:

```json
{
  "message": "İşlem başarılı.",
  "success": true,
  "data": { }
}
```

---

## English

### Project Description

HRMS (Human Resource Management System) is a Spring Boot REST API for managing job postings, employer registrations, candidate applications, and hiring workflows. It implements DTO, Request-Response Pattern, Validation, and Global Exception Handling.

### Features

- **City Management** — Add and list cities with unique name constraint
- **Job Position Management** — Add and list job positions
- **Employer Management** — Register and list employers
- **Candidate Management** — Register and list job seekers
- **Job Advertisement Management** — Add, list, and filter job advertisements
- **Job Application Management** — Candidates can apply for job advertisements
- **Global Exception Handling** — Consistent error responses via `@ControllerAdvice`
- **Field Validation** — Jakarta Validation annotations (`@NotBlank`, `@Size`, `@Email`, `@Future`)

### Tech Stack

| Layer | Technology |
|---|---|
| Language | Java 17 |
| Framework | Spring Boot 3 |
| ORM | Spring Data JPA / Hibernate |
| Database | PostgreSQL |
| Testing | JUnit 5, MockMvc |
| Utilities | Lombok, Jackson, Jakarta Validation |

### Architecture

```
controller/     → REST API endpoints
service/        → Business logic
repository/     → Database access (Spring Data JPA)
entity/         → Database table mappings
dto/            → API response objects
request/        → Incoming request models
core/           → Shared result structures (Result, DataResult, SuccessResult, ErrorResult)
```

### API Endpoints

#### Cities
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/cities/add` | Add a new city |
| GET | `/api/cities/getAll` | List all cities |

#### Employers
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/employers/register` | Register a new employer |
| GET | `/api/employers/getAll` | List all employers |

#### Job Seekers
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/candidateController/register` | Register a new candidate |
| GET | `/api/candidateController/getAll` | List all candidates |

#### Job Advertisements
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/jobAdvertisements/add` | Add a new job advertisement |
| GET | `/api/jobAdvertisements/getAll` | List all job advertisements |

#### Job Applications
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/jobApplications/apply` | Apply for a job advertisement |

### Sample Requests

**Register Employer**
```json
POST /api/employers/register
{
  "companyName": "Tech Solutions Ltd.",
  "companyWebPage": "https://techsolutions.com",
  "email": "contact@techsolutions.com",
  "phoneNumber": "+90-555-123-4567",
  "password": "password123",
  "confirmPassword": "password123"
}
```
**Candidate Registration:**
```json
{
    "name": "Aysu",
    "lastName": "Ay",
    "nationalId": "12345678901",
    "birthDate": 1995,
    "email": "aysu@example.com",
    "password": "password123",
    "confirmPassword": "password123"
}

**Add Job Advertisement**
```json
POST /api/jobAdvertisements/add
{
  "description": "We are looking for a Java Backend Developer with Spring Boot experience.",
  "openPositionCount": 2,
  "minSalary": 30000,
  "maxSalary": 50000,
  "applicationDeadline": "2025-12-31",
  "jobPositionId": 1,
  "cityId": 1,
  "employerId": 1
}
```

### Tests

27 unit and integration tests written with JUnit 5 and MockMvc.

| Test Class | Type | What it tests |
|---|---|---|
| `CityDaoTest` | Unit | Save, duplicate city name constraint |
| `CityControllerTest` | Integration | API responses, validation |
| `EmployerDaoTest` | Unit | Save, duplicate email constraint |
| `JobSeekerDaoTest` | Unit | Save, duplicate email and national ID |
| `JobPositionDaoTest` | Unit | Save and retrieve |
| `JobAdvertisementDaoTest` | Unit | Save with relations |
| `JobAdvertisementControllerTest` | Integration | Advertisement API responses |
| `JobApplicationDaoTest` | Unit | Application save and status |

```bash
mvn test
# Tests run: 27, Failures: 0, Errors: 0
```

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/sedabasaran/hmrs-app.git
cd hmrs-app

# 2. Create database
psql -U postgres -c "CREATE DATABASE hrms;"

# 3. Update application.properties
spring.datasource.url=jdbc:postgresql://localhost:5432/hrms
spring.datasource.username=your_username
spring.datasource.password=your_password

# 4. Run
mvn spring-boot:run
```

API will be available at `http://localhost:8080`

### Response Structure

```json
{
  "message": "Operation successful.",
  "success": true,
  "data": { }
}
```
---
=======
# HMRS-App
Java Human Resource Management System
