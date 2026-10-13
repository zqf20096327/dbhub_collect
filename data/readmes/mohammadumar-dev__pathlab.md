# PathLab - Pathology Laboratory Management System

A comprehensive full-stack application for managing pathology laboratory operations, including patient management, test bookings, sample tracking, test results, payment processing, and administrative dashboards.

## 📋 Project Overview

PathLab is an enterprise-grade laboratory information management system (LIMS) that digitally transforms pathology laboratory operations. The system provides end-to-end workflow automation from test booking through result generation and delivery, serving patients, healthcare providers, laboratory staff, and administrators through intuitive web interfaces backed by a robust REST API.

### Who It's For

- **Patients**: Book tests online, view and download results securely, manage appointments, and track payment history
- **Laboratory Technicians**: Manage sample collection and tracking, record test results, and handle specimen workflows
- **Doctors**: Monitor patient test results and access comprehensive medical data
- **Administrative Personnel**: Oversee laboratory operations, manage users and tests, track financial metrics, and generate analytics
- **Pathology Laboratories**: Modern diagnostic centers seeking to streamline operations and improve patient experience

### Core Objectives

- Automate manual laboratory processes and reduce turnaround time
- Minimize human errors in result reporting and data management
- Improve patient experience through digital accessibility and transparency
- Enhance data security with JWT authentication and role-based access control
- Enable real-time tracking of samples and test status
- Provide comprehensive analytics and business intelligence
- Ensure scalability and maintainability through modern architecture

## ✨ Key Features

### Patient Portal
- User registration with email verification
- Secure JWT-based authentication and authorization
- Appointment scheduling and test booking
- Browse comprehensive test catalog with pricing information
- Payment tracking and invoice generation (offline payments)
- Secure digital report access with PDF download
- Historical test results and booking history
- Real-time notifications via email

### Laboratory Management
- Multi-status sample lifecycle tracking (collection pending, collected, in transit, received, tested, discarded)
- Sample collection assignment to lab technicians
- Parametric test result entry and updates
- Quality control measures and validation
- Barcode generation for sample identification
- Centralized test catalog with parameter definitions

### Administrative Dashboard
- Comprehensive user and staff management
- Business analytics with monthly booking trends
- Test distribution analysis
- Recent activity logs and audit trails
- Role-based access control (ADMIN, LAB_TECH, DOCTOR, PATIENT)
- System-wide statistics and KPIs

### Reporting & Documents
- PDF report generation with Freemarker templates
- Customizable report layouts
- Invoice PDF generation for payments
- Digital signature support (planned)
- Export and sharing functionality
- Bulk report processing capabilities

### Additional Features
- Cloudinary integration for image storage
- Email notifications for verification, password recovery, and test results
- Caffeine caching for performance optimization
- Database version control with Flyway migrations
- Comprehensive input validation with error handling
- CORS configuration for secure frontend-backend integration

## 🏗️ Architecture Overview

PathLab follows a modern full-stack architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                       │
│         (TypeScript, Vite, Tailwind CSS)                │
│    Components → Pages → API Services → Hooks            │
└────────────────────┬────────────────────────────────────┘
                     │ REST API (JSON)
                     │ JWT Authentication
┌────────────────────┴────────────────────────────────────┐
│              Spring Boot Backend                        │
│    Controller → Service → Repository → Entity           │
│         (Java 21, Spring Security, JPA)                 │
└────────────────────┬────────────────────────────────────┘
                     │ JDBC
┌────────────────────┴────────────────────────────────────┐
│              PostgreSQL Database                        │
│         (Relational data storage)                       │
└─────────────────────────────────────────────────────────┘

External Integrations:
├── Cloudinary (Image storage)
├── Email Service (SMTP notifications)
└── PDF Generation (OpenHTML2PDF + Freemarker)
```

### Backend Architecture (Spring Boot)

The backend follows a layered architecture pattern:

```
Controller Layer (REST endpoints)
     ↓
Service Layer (Business logic)
     ↓
Repository Layer (Data access with Spring Data JPA)
     ↓
Entity/Domain Models
     ↓
PostgreSQL Database
```

**Functional Modules:**
- Authentication & Authorization
- Patient Management
- Test Catalog Management
- Booking & Appointment System
- Sample Collection & Tracking
- Test Results Recording
- Payment Processing
- Dashboard & Analytics
- PDF Generation & Email Services

### Frontend Architecture (React)

The frontend uses a component-based architecture:

```
Pages (Route-based screens)
  ↓
Components (Reusable UI with Radix UI)
  ↓
API Services (Backend integration)
  ↓
Hooks (Custom React logic)
  ↓
Contexts (Global state management)
```

## 🛠️ Tech Stack

### Backend Technologies
- **Runtime**: Java 21 (Eclipse Temurin)
- **Framework**: Spring Boot 3.5.5
- **Security**: Spring Security with JWT authentication (JJWT 0.11.5)
- **Database**: PostgreSQL (primary) + Spring Data JPA (Hibernate ORM)
- **Migration**: Flyway (database version control)
- **Email**: Spring Mail (SMTP)
- **Caching**: Caffeine 3.1.8 (in-memory)
- **PDF Generation**: OpenHTML2PDF with PDFBox
- **Templates**: Freemarker (PDF and email templates)
- **Storage**: Cloudinary HTTP5 (cloud image storage)
- **Build Tool**: Apache Maven 3.9.9
- **Utilities**: Lombok (boilerplate reduction)

### Frontend Technologies
- **Framework**: React 18.3.1 with TypeScript 5.5.3
- **Build Tool**: Vite 7.1.2 (fast HMR and optimized builds)
- **UI Components**: Radix UI (accessible primitives)
- **Styling**: Tailwind CSS 3.4.13 with custom animations
- **Routing**: React Router DOM 7.8.0
- **Forms**: React Hook Form 7.53.0 + Zod 3.23.8 (validation)
- **State Management**: React Context API
- **HTTP Client**: Fetch API with custom ApiClient wrapper
- **Charts**: Recharts 3.1.2
- **Date Handling**: date-fns 3.6.0 + react-datepicker 8.7.0
- **PDF Export**: jsPDF 3.0.2 + html2canvas 1.4.1
- **Animations**: Framer Motion 12.23.12
- **Icons**: Lucide React 0.539.0 + Radix UI Icons
- **Notifications**: Sonner 1.5.0 (toast notifications)
- **Code Quality**: ESLint 9.11.1 with TypeScript support

### DevOps & Tooling
- **Containerization**: Docker (multi-stage builds)
- **Version Control**: Git
- **API Documentation**: Swagger/OpenAPI (if configured)
- **Package Management**: Maven (backend), npm (frontend)
- **Deployment**: Netlify (frontend), Render/Cloud providers (backend)

## 📁 Project Structure

```
pathlab/
├── app/
│   ├── pathlab-backend/                    # Spring Boot backend application
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/com/pathlab/
│   │   │   │   │   ├── config/             # Security & app configuration
│   │   │   │   │   │   ├── SecurityConfig.java
│   │   │   │   │   │   ├── CorsConfig.java
│   │   │   │   │   │   └── FreemarkerConfig.java
│   │   │   │   │   │
│   │   │   │   │   ├── controller/         # REST API endpoints
│   │   │   │   │   │   ├── AuthController.java
│   │   │   │   │   │   ├── PatientController.java
│   │   │   │   │   │   ├── BookingsController.java
│   │   │   │   │   │   ├── SampleController.java
│   │   │   │   │   │   ├── PaymentController.java
│   │   │   │   │   │   ├── BookingResultsController.java
│   │   │   │   │   │   └── DashboardController.java
│   │   │   │   │   │
│   │   │   │   │   ├── dto/                # Request/response models
│   │   │   │   │   │   ├── auth/
│   │   │   │   │   │   ├── booking/
│   │   │   │   │   │   ├── patient/
│   │   │   │   │   │   ├── payment/
│   │   │   │   │   │   ├── result/
│   │   │   │   │   │   └── dashboard/
│   │   │   │   │   │
│   │   │   │   │   ├── entity/             # JPA domain entities
│   │   │   │   │   │   ├── User.java
│   │   │   │   │   │   ├── Patient.java
│   │   │   │   │   │   ├── Booking.java
│   │   │   │   │   │   ├── Sample.java
│   │   │   │   │   │   ├── TestEntity.java
│   │   │   │   │   │   ├── TestResult.java
│   │   │   │   │   │   ├── Payment.java
│   │   │   │   │   │   └── enums/          # Domain enumerations
│   │   │   │   │   │
│   │   │   │   │   ├── repository/         # Spring Data JPA repositories
│   │   │   │   │   │   ├── UserRepository.java
│   │   │   │   │   │   ├── PatientRepository.java
│   │   │   │   │   │   ├── BookingRepository.java
│   │   │   │   │   │   ├── SampleRepository.java
│   │   │   │   │   │   ├── TestEntityRepository.java
│   │   │   │   │   │   └── PaymentRepository.java
│   │   │   │   │   │
│   │   │   │   │   ├── service/            # Business logic layer
│   │   │   │   │   │   ├── AuthService.java
│   │   │   │   │   │   ├── PatientService.java
│   │   │   │   │   │   ├── BookingService.java
│   │   │   │   │   │   ├── SampleService.java
│   │   │   │   │   │   ├── TestService.java
│   │   │   │   │   │   ├── TestResultService.java
│   │   │   │   │   │   ├── PaymentService.java
│   │   │   │   │   │   ├── DashboardService.java
│   │   │   │   │   │   ├── EmailService.java
│   │   │   │   │   │   └── PdfService.java
│   │   │   │   │   │
│   │   │   │   │   ├── security/           # JWT filters & handlers
│   │   │   │   │   │   └── JwtAuthenticationFilter.java
│   │   │   │   │   │
│   │   │   │   │   ├── exception/          # Global exception handling
│   │   │   │   │   │   └── GlobalExceptionHandler.java
│   │   │   │   │   │
│   │   │   │   │   ├── util/               # Utility helpers
│   │   │   │   │   │   ├── JwtUtil.java
│   │   │   │   │   │   └── DateUtils.java
│   │   │   │   │   │
│   │   │   │   │   └── PathLabApplication.java  # Spring Boot entry
│   │   │   │   │
│   │   │   │   └── resources/
│   │   │   │       ├── application.properties  # App configuration
│   │   │   │       ├── db/migration/           # Flyway migrations
│   │   │   │       │   └── V1__init.sql
│   │   │   │       └── templates/              # Freemarker templates
│   │   │   │           ├── email/
│   │   │   │           │   ├── verification.html
│   │   │   │           │   └── report-template.html
│   │   │   │           ├── invoice.ftl
│   │   │   │           └── report.ftl
│   │   │   │
│   │   │   └── test/                           # Unit & integration tests
│   │   │
│   │   ├── Dockerfile                          # Backend containerization
│   │   ├── pom.xml                             # Maven dependencies
│   │   ├── mvnw / mvnw.cmd                     # Maven wrapper
│   │   └── .gitignore
│   │
│   └── pathlab-frontend/                       # React frontend application
│       ├── src/
│       │   ├── pages/                          # Route-based page components
│       │   │   ├── HomePage.tsx
│       │   │   ├── LoginPage.tsx
│       │   │   ├── PatientDashboard.tsx
│       │   │   ├── AdminDashboard.tsx
│       │   │   ├── BookingPage.tsx
│       │   │   ├── ResultsPage.tsx
│       │   │   └── ...
│       │   │
│       │   ├── components/                     # Reusable UI components
│       │   │   ├── ui/                         # Radix UI primitives
│       │   │   ├── layout/                     # Layout components
│       │   │   ├── forms/                      # Form components
│       │   │   └── ...
│       │   │
│       │   ├── api/                            # Backend integration
│       │   │   ├── index.ts                    # Base API client
│       │   │   ├── auth.ts                     # Auth endpoints
│       │   │   ├── tests.ts                    # Test management
│       │   │   ├── bookings.ts                 # Booking endpoints
│       │   │   └── ...
│       │   │
│       │   ├── hooks/                          # Custom React hooks
│       │   │   ├── useAuth.ts
│       │   │   ├── useForm.ts
│       │   │   └── ...
│       │   │
│       │   ├── contexts/                       # Global state management
│       │   │   ├── AuthContext.tsx
│       │   │   └── UserContext.tsx
│       │   │
│       │   ├── lib/                            # Utility functions
│       │   │   └── utils.ts
│       │   │
│       │   ├── App.tsx                         # Root component
│       │   ├── main.tsx                        # Entry point
│       │   ├── index.css                       # Global styles
│       │   └── vite-env.d.ts                   # Type definitions
│       │
│       ├── public/                             # Static assets
│       ├── index.html                          # HTML entry point
│       ├── vite.config.ts                      # Vite configuration
│       ├── tailwind.config.js                  # Tailwind CSS config
│       ├── tsconfig.json                       # TypeScript config
│       ├── package.json                        # Dependencies & scripts
│       ├── eslint.config.js                    # ESLint configuration
│       ├── netlify.toml                        # Deployment config
│       └── .gitignore
│
├── README.md                                   # This file
├── CONTRIBUTING.md                             # Contribution guidelines
└── .git/                                       # Git version control
```

## 🚀 Getting Started

### Prerequisites

**Backend:**
- Java 21 or later (Eclipse Temurin recommended)
- Maven 3.9.9 or later
- PostgreSQL 12 or later
- Git

**Frontend:**
- Node.js 18.x or higher
- npm 9.x or higher (or yarn)

### Environment Setup

#### Backend Configuration

1. **Install PostgreSQL and create a database:**
   ```bash
   createdb pathlab
   ```

2. **Navigate to backend directory:**
   ```bash
   cd app/pathlab-backend
   ```

3. **Configure environment variables in `application.properties` or as system environment variables:**

   ```properties
   # Database Configuration
   DB_URL=jdbc:postgresql://localhost:5432/pathlab
   DB_USERNAME=postgres
   DB_PASSWORD=your_password
   
   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   
   # Email Configuration
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   
   # Security & JWT
   JWT_SECRET_BASE64=your-base64-encoded-secret
   
   # Application URLs
   PUBLIC_BASE_URL=http://localhost:5173
   ```

#### Frontend Configuration

1. **Navigate to frontend directory:**
   ```bash
   cd app/pathlab-frontend
   ```

2. **Create `.env.local` file in the frontend root:**
   ```env
   # Backend API Configuration
   VITE_API_BASE_URL=http://localhost:8080/api
   
   # Authentication
   VITE_AUTH_TIMEOUT=3600000
   
   # Feature Flags
   VITE_ENABLE_DEMO_MODE=false
   
   # Notification Settings
   VITE_TOAST_DURATION=3000
   
   # Application Name
   VITE_APP_NAME=Pathology Lab Management System
   ```

### Installation Steps

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd app/pathlab-backend
   ```

2. **Build the application using Maven:**
   ```bash
   ./mvnw clean package
   ```
   *On Windows:*
   ```bash
   mvnw.cmd clean package
   ```

3. **Run the application:**
   ```bash
   ./mvnw spring-boot:run
   ```
   *Or after packaging:*
   ```bash
   java -jar target/pathlab-0.0.1-SNAPSHOT.jar
   ```

4. **Verify backend is running:**
   - Backend API available at: `http://localhost:8080`
   - API documentation (if Swagger configured): `http://localhost:8080/swagger-ui.html`

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd app/pathlab-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   - Frontend available at: `http://localhost:5173` (default Vite port)

### Running the Full Stack

For development, run both applications simultaneously:

**Terminal 1 (Backend):**
```bash
cd app/pathlab-backend
./mvnw spring-boot:run
```

**Terminal 2 (Frontend):**
```bash
cd app/pathlab-frontend
npm run dev
```

The frontend will proxy API requests to the backend automatically.

## 💻 Development Workflow

### Backend Development

**Running Tests:**
```bash
cd app/pathlab-backend
./mvnw test
```

**Building the Application:**
```bash
./mvnw clean package -DskipTests
```

**Useful Maven Commands:**
```bash
# Clean build
./mvnw clean

# Compile only
./mvnw compile

# Run tests
./mvnw test

# Package without tests
./mvnw package -DskipTests

# View dependency tree
./mvnw dependency:tree

# Format code (if spotless configured)
./mvnw spotless:apply
```

**Available API Endpoints:**

***Authentication:***
```bash
POST /api/auth/register/patient
POST /api/auth/register/user
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/verify-email?token=...
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

***Patient Management:***
```bash
GET    /api/patients
GET    /api/patients/{id}
POST   /api/patients
PUT    /api/patients/{id}
DELETE /api/patients/{id}
```

***Bookings:***
```bash
GET    /api/bookings
GET    /api/bookings/{id}
POST   /api/bookings
PUT    /api/bookings/{id}
DELETE /api/bookings/{id}
```

***Test Results & PDF Generation:***
```bash
POST /api/bookings/{bookingId}/tests/{testId}/results
GET  /api/bookings/{bookingId}/results
GET  /api/bookings/{bookingId}/results/pdf
GET  /api/payments/{id}/invoice/pdf
```

### Frontend Development

**Available Scripts:**
```bash
# Start development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run ESLint checks
npm run lint
```

**Script Details:**
- **dev**: Starts Vite development server with fast refresh at `http://localhost:5173`
- **build**: Compiles TypeScript and builds optimized production bundle to `dist/`
- **lint**: Analyzes code for errors and style issues using ESLint
- **preview**: Serves the built application locally for testing

### Code Quality Standards

**Backend:**
- Follow Java naming conventions (PascalCase for classes, camelCase for methods)
- Use Lombok annotations for boilerplate reduction
- Add validation to all DTOs using Jakarta validation annotations
- Include appropriate error handling with custom exceptions
- Write meaningful commit messages
- Document complex business logic
- Test your changes before submitting

**Frontend:**
- Use TypeScript strict mode for all components
- Follow React Hooks conventions and best practices
- Write self-documenting, readable code
- Use Tailwind CSS utility classes (avoid inline styles)
- Create reusable components following single responsibility principle
- Ensure all components are properly typed
- Document complex logic with comments
- Test changes thoroughly in browser

## 🚢 Deployment

### Backend Deployment (Docker)

The backend includes a multi-stage Dockerfile for containerization:

1. **Build the Docker image:**
   ```bash
   cd app/pathlab-backend
   docker build -t pathlab-backend:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -p 8080:8080 \
     -e DB_URL=jdbc:postgresql://postgres:5432/pathlab \
     -e DB_USERNAME=postgres \
     -e DB_PASSWORD=your_password \
     -e MAIL_USERNAME=your-email@gmail.com \
     -e MAIL_PASSWORD=your-app-password \
     -e JWT_SECRET_BASE64=your-secret \
     -e CLOUDINARY_CLOUD_NAME=your-cloud-name \
     -e CLOUDINARY_API_KEY=your-api-key \
     -e CLOUDINARY_API_SECRET=your-api-secret \
     pathlab-backend:latest
   ```

### Frontend Deployment (Netlify)

The frontend is configured for Netlify deployment (see `netlify.toml`):

1. **Build Command:** `npm run build`
2. **Publish Directory:** `dist/`
3. **Node Version:** 18.x or higher

**Environment Configuration for Deployment:**
- Development: `http://localhost:8080/api`
- Production: `https://pathology-lab-backend-new.onrender.com/api`

### Production Deployment Checklist

**Backend:**
- [ ] Environment variables securely configured
- [ ] PostgreSQL connection pooling optimized
- [ ] HTTPS/TLS enabled for all endpoints
- [ ] Logging and monitoring configured
- [ ] Rate limiting implemented for API endpoints
- [ ] Reverse proxy (Nginx/Apache) configured
- [ ] CORS settings updated for production frontend URL
- [ ] Secrets management system implemented
- [ ] Audit logging enabled for sensitive operations
- [ ] Database backups configured
- [ ] Health check endpoints verified

**Frontend:**
- [ ] Production API URL configured in environment variables
- [ ] Backend API accessibility verified
- [ ] Production build tested locally
- [ ] TypeScript compilation successful
- [ ] ESLint checks passing
- [ ] Static assets optimized
- [ ] Error tracking configured (e.g., Sentry)
- [ ] Analytics implemented (if required)
- [ ] Browser compatibility tested
- [ ] Performance metrics verified

### Production Considerations

- Use environment variables for all sensitive configuration
- Enable comprehensive logging and monitoring
- Implement proper error tracking and alerting
- Configure database connection pooling appropriately
- Use a CDN for static assets (frontend)
- Enable compression for API responses
- Implement proper CORS policies
- Set up automated backups for database
- Configure SSL/TLS certificates
- Implement rate limiting and DDoS protection
- Use a reverse proxy for the backend
- Enable API response caching where appropriate
- Monitor application performance and resource usage

## 🗺️ Roadmap & Future Improvements

### Planned Features

1. **Enhanced Notifications**
   - SMS notifications for booking confirmations and results
   - Push notifications via Progressive Web App (PWA)
   - WhatsApp integration for report delivery
   - Configurable notification preferences

2. **Payment Integration**
   - Online payment gateway integration (Stripe, PayPal, Razorpay)
   - Automated invoice generation
   - Payment reminders and receipts
   - Multi-currency support

3. **Advanced Analytics**
   - Comprehensive business intelligence dashboards
   - Revenue forecasting and trend analysis
   - Patient demographics and test distribution insights
   - Exportable reports in multiple formats

4. **Mobile Experience**
   - Progressive Web App (PWA) implementation
   - Offline functionality with service workers
   - Mobile-optimized dashboards and workflows
   - Native mobile app (React Native)

5. **Internationalization**
   - Multi-language support (i18n)
   - Localized date and currency formats
   - Regional compliance features

6. **Enhanced Features**
   - Document storage for patient records and consents
   - Automated scheduling for sample collection
   - Integration with external lab equipment APIs
   - Real-time booking notifications via WebSockets
   - Advanced search and filtering capabilities
   - Batch processing for multiple samples/tests
   - Digital signature for authorized personnel
   - Audit trail with detailed logging

7. **UI/UX Improvements**
   - Dark mode full implementation
   - Interactive tutorials and onboarding
   - Customizable user preferences
   - Accessibility enhancements (WCAG 2.1 AA compliance)
   - Advanced data visualization

8. **Performance Optimization**
   - Redis caching for improved performance
   - Code splitting and lazy loading (frontend)
   - Image optimization and CDN integration
   - API response caching strategies
   - Database query optimization
   - Background job processing

9. **Testing & Quality**
   - Comprehensive unit test coverage
   - Integration tests for critical workflows
   - End-to-end testing with Playwright/Cypress
   - Load testing and performance benchmarks
   - Security auditing and penetration testing

10. **DevOps & Infrastructure**
    - CI/CD pipeline automation
    - Kubernetes deployment configuration
    - Monitoring and alerting with Prometheus/Grafana
    - Automated database backups and recovery
    - Infrastructure as Code (Terraform)

## 📝 License

This project is proprietary software. All rights reserved.

## 👥 Team & Support

For questions, issues, or contributions, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

**Project Maintainers:**
- Backend: [Mohammad Umar](https://github.com/mohammadumar-dev)
- Frontend: [Mohammad Umar](https://github.com/mohammadumar-dev)

**Repository Links:**
- Monorepo: `https://github.com/mohammadumar-dev/pathlab`
---

**Built with ❤️ for modern pathology laboratories**
