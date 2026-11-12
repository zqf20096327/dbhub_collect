# 🏦 Mini-Bank System

I designed and developed a modular mini-banking application using native Go and MySQL, following the Clean Architecture pattern. The system is built to handle core financial workflows such as fund transfers and balance updates with strict adherence to ACID principles, ensuring data integrity during concurrent transactions. The entire system was constructed without third-party frameworks or ORMs to eliminate hidden abstractions, resulting in optimal native performance and complete source code transparency. Furthermore, I strategically minimized the use of pointers to enforce data immutability and optimize memory management; priority was given to stack allocation over heap allocation, significantly reducing the burden on the Garbage Collector (GC) and preventing latency spikes. This structure also maintains isolated layers, which ensures high test coverage and long-term code readability.



## 🛠️ Tech Stack

This system is built using a modern technology ecosystem:

*   **Primary Programming Language**: **Golang v1.26** (Clean, efficient, and prioritizes pure performance).
*   **API & HTTP Server**: **`net/http`** (Standard Library) for native, high-performance HTTP routing and request handling.
*   **Data Storage (Database)**: **MySQL 8.0** as an ACID-compliant transaction storage.
*   **Database Interface**: **`database/sql`** (Standard Library) for native connection pooling and raw SQL transaction management.
*   **Database Driver**: **`go-sql-driver/mysql`** for interaction with the database engine.
*   **Testing Library**: **`Stretchr/Testify`** (`assert` & `mock`) for the testing architecture.



## 🏗️ System Architecture

This system strictly implements **Clean Architecture** to ensure a decoupled, highly testable, and maintainable codebase. By separating concerns into distinct layers, the core banking logic remains completely independent of external frameworks, databases, and delivery mechanisms.

### 1. Architectural Layers (Inside-Out)

*   **Domain / Entity Layer (Core)**: 
    Contains the fundamental business objects (`Account`, `Transaction`) and core banking rules. This layer is written in pure Golang, has **zero dependencies** on any other layers or libraries, and heavily utilizes *value types* instead of pointers to maximize stack allocation.
*   **Use Case / Service Layer**: 
    Orchestrates the business logic of the mini bank (`CashDeposit`, `CashWithdrawal`, `Transfer`, `BatchSalary`). It interacts with the Domain layer and defines interfaces (ports) for data access. It does not know *how* data is stored, only *what* operations are available.
*   **Repository / Adapter Layer**: 
    This layer implements the interfaces defined by the *Use Case* layer. It is here that **`database/sql`** and **`go-sql-driver/mysql`** reside. This layer executes raw SQL queries and maps rows from the relational database directly into domain value structures using `rows.Scan()`. It also implements an ACID-compliant transaction system via `BeginTx`, ensuring that data remains secure and valid throughout the transaction process.
*   **Delivery / Infrastructure Layer (HTTP)**: 
    The outermost layer handled by **`net/http`**. It acts as the entry point for clients, responsible for parsing JSON payloads from incoming HTTP requests, basic payload validation, invoking the appropriate Use Case, and returning structured JSON responses.

---

### 2. Data Flow & Dependency Rule

The fundamental rule of this architecture is that **dependencies only point inwards**. The inner layers know nothing about the outer layers.

---

<img src="assets/architecture_flow.png" alt="System Architecture Flow" width="600">

---

1.  **Request**: `net/http` receives a transfer request, decodes the body into a plain local struct, and passes the **values** to the Use Case.
2.  **Processing**: The Use Case validates business rules against the Domain entities.
3.  **Persistence**: The Use Case calls the Repository interface. The Repository opens an ACID transaction using `database/sql`, performs raw SQL operations, and returns the results back up the chain as concrete values (avoiding heap escape).

---

### 3. Memory & Performance Design Principles

To achieve optimal performance and minimize Garbage Collector (GC) overhead, the architecture enforces these structural constraints:

*   **Pure Pass-by-Value**: Data structures are passed across layer boundaries as explicit copies (`Account` instead of `*Account`) whenever feasible. This keeps the data scoped to the function execution block, ensuring it stays allocated on the **Stack** and prevents *Escape Analysis* from moving it to the **Heap**.
*   **Boundary Decoupling via Interfaces**: Use Cases rely strictly on interfaces to communicate with Repositories. This decoupling allows **`Stretchr/Testify`** to inject lightweight mocks during unit testing, enabling full test coverage without needing network or database resources.
*   **Explicit Resource Management**: Database rows and HTTP request bodies are closed immediately after consumption using native Go defer statements (`rows.Close()`, `r.Body.Close()`), ensuring deterministic memory cleanup without relying on the GC to release system descriptors.



## 📂 Project Structure

Below is the directory structure of the **mini-bank** application, highlighting the clear separation of concerns aligned with Clean Architecture:

```text
mini-bank/
├── cmd/                # Application entry points (main.go)
├── config/             # Configuration setup, environment loaders, and MySQL connection initialization
├── internal/           # Core application code (protected from external import)
│   ├── delivery/       # Delivery Layer (Infrastructure)
│   │   └── http/       # HTTP network protocol implementation
│   │       ├── handler/# HTTP route handlers and controllers
│   │       └── request/# HTTP payload structures and decoders
│   ├── domain/         # Domain / Entity Layer (Core business rules & structures)
│   │   ├── account.go  # Core structures for bank accounts (strict value types)
│   │   └── transaction.go # Core structures for financial transactions
│   ├── repository/     # Repository Layer (Data persistence & adapters)
│   │   ├── mocks/      # Autogenerated or manual mocks for database testing
│   │   ├── account.go  # Account repository implementations (database/sql)
│   │   └── transaction.go # Transaction repository implementations (database/sql)
│   └── usecase/        # Use Case / Service Layer (Business logic orchestration)
│       ├── account_test.go       # Unit tests for account use cases using testify
│       ├── account.go            # Account use case core business logic
│       ├── transaction_test.go   # Unit tests for banking transaction logic
│       └── transaction.go        # Transaction use case business logic (Transfer, etc.)
├── migration/          # Database schema migrations (SQL files)
├── pkg/                # Shared utilities and reusable standalone packages
│   ├── security/       # Encryption, hashing, or security tools
│   ├── utils/          # General helper functions
│   └── validator/      # Custom validation logic for structs
│
├── report/ # Stack and heap analysis results
├── worker/ # Automated Account Status Maintenance
```



## 🔍 Running tests

Testing is conducted exclusively at the use case layer, as this represents the critical point in the application's program flow and is where the application's business logic is defined.

```text
go test -v internal/usecase/account_test.go
```

```text
go test -v internal/usecase/transaction_test.go
```



## 🔌 API Specification & Postman Payloads

All API request bodies utilize strict JSON formats. Incoming payloads are automatically mapped to value structures inside the `internal/delivery/http/request` layer and validated using structural tags.

### 1. Customer & Account Registration
Used to register a new bank customer and simultaneously initialize their first bank account with an initial deposit.

*   **HTTP Method**: `POST`
*   **Endpoint**: `http://localhost:8080/api/v1/customer/register`
*   **Headers**: `Content-Type: application/json`

#### A. Corporate Customer Payload
For registering corporate entities. This type requires organizational attributes like `tax_id` and `office_address`.

```json
{
  "customer_type": "CORPORATE",
  "name": "PT Teknologi Maju Bersama",
  "phone_number": "0215556677",
  "email": "info@teknologimaju.co.id",
  "pin": "987654",
  "initial_deposit": 10000000,
  "identity_number": "012345678901234",
  "tax_id": "01.234.567.8-012.000",
  "office_address": "Gedung Cyber Lt. 5, Jl. Kuningan Barat, Jakarta Selatan"
}
```

#### B. Individual Customer Payload
For registering single personal accounts. Attributes like `tax_id` and `office_address` are omitted from the request body.

```json
{
  "customer_type": "INDIVIDUAL",
  "name": "John Doe",
  "phone_number": "081234567890",
  "email": "johndoe@email.com",
  "pin": "123456",
  "initial_deposit": 500000,
  "identity_number": "3201234567890001",
  "occupation": "Software Engineer",
  "customer_address": "Jl. Mawar No. 12, Jakarta"
}
```

---

### 2. Transaction Services

#### A. Cash Deposit
Used to add funds to a specific bank account balance securely.

*   **HTTP Method**: `POST`
*   **Endpoint**: `http://localhost:8080/api/v1/transaction/cash-deposit`
*   **Headers**: `Content-Type: application/json`

```json
{
  "account_number": "1101177966",
  "pin": "654321",
  "amount": 100000,
  "description": "Setoran tunai via ATM"
}
```

#### B. Cash Withdrawal
Used to deduct funds from an account balance after verifying the ownership credentials.

*   **HTTP Method**: `POST`
*   **Endpoint**: `http://localhost:8080/api/v1/transaction/cash-withdrawal`
*   **Headers**: `Content-Type: application/json`

```json
{
  "account_number": "1101177966",
  "pin": "654321",
  "amount": 75000,
  "description": "Tarik tunai ATM"
}
```

#### C. Peer-to-Peer Transfer
Used to transfer money between two individual bank accounts under a strict database transaction.

*   **HTTP Method**: `POST`
*   **Endpoint**: `http://localhost:8080/api/v1/transaction/transfer`
*   **Headers**: `Content-Type: application/json`

```json
{
  "sender_account_number": "1101177966",
  "pin": "654321",
  "receiver_account_number": "1101140357",
  "amount": 50000
}
```

#### D. Batch Salary Disbursement
Used by corporate accounts to disburse salaries to multiple employees concurrently within an atomic processing execution block.

*   **HTTP Method**: `POST`
*   **Endpoint**: `http://localhost:8080/api/v1/transaction/batch-salary`
*   **Headers**: `Content-Type: application/json`

```json
{
  "company_account_number": "1101154997",
  "company_name": "PT Teknologi Maju Bersama",
  "company_pin": "987654",
  "employee_list": [
    {
      "employee_account_number": "1101140357",
      "salary_amount": 2000000
    },
    {
      "employee_account_number": "1101177966",
      "salary_amount": 2000000
    }
  ]
}
```


## 🔍 Business Logic Fail-Safe

To ensure transaction security and prevent system failures in banking operations, this application implements the following anticipatory measures:

### 1. Batch Processing Integrity
*   **Anticipation:** Prevents stuck data, unbalanced balances, or partially processed accounts if a disruption occurs during a mass transaction.
*   **Solution:** 
    *   Enforces a strict limit of a maximum of 1,000 mutation entries per single request to avoid system overload.
    *   Applies the *All-or-Nothing* principle. If a single mutation entry fails or is invalid, the entire transaction sequence within the batch is automatically rolled back to maintain balance consistency.

### 2. Regular Code Review & Logic Audit
*   **Anticipation:** Detects and mitigates any hidden loopholes or errors in the business logic and data execution that could lead to miscalculations or fund leaks.
*   **Solution:** Conducts regular visual audits and code reviews on both the **usecase** layer (for business rule validation) and the **repository** layer (for database transaction flow and query validation). This ensures that every banking rule is implemented completely and consistently.

---
**Conclusion:** This anticipatory approach ensures that all business workflows run securely, completely, and free from fatal vulnerabilities that could harm financial circulation.
