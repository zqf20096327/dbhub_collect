# 🔐 Authentication Form

A full-stack authentication form built with Next.js, Prisma, SQLite, bcrypt, and Playwright.

This project provides a simple and secure authentication flow with user registration, login, form validation, password hashing, error handling, and end-to-end testing.

## 🚀 Features

- 🔑 User Login
- 📝 User Sign Up
- 🔒 Password hashing with bcrypt
- 🗄️ SQLite database with Prisma ORM
- ✅ Client-side form validation
- ⚠️ Error handling
- 👁️ Show / Hide password
- ⏳ Loading states
- 🧪 End-to-End testing with Playwright
- 📱 Responsive UI
- ⚡ Next.js App Router
- 🔌 API Routes for authentication

## 🛠️ Technologies

- Next.js
- React
- Prisma
- SQLite
- bcryptjs
- Playwright
- CSS

## 📁 Project Structure

```text
authentication-form/
│
├── app/
│   ├── Components/
│   │   ├── LoginForm.js
│   │   └── Navbar.js
│   │
│   ├── api/
│   │   ├── login/
│   │   │   └── route.js
│   │   └── register/
│   │       └── route.js
│   │
│   ├── lib/
│   │   └── prisma.js
│   │
│   ├── login/
│   │   └── page.js
│   │
│   ├── register/
│   │   └── page.js
│   │
│   ├── globals.css
│   ├── layout.js
│   └── page.js
│
├── prisma/
│   ├── migrations/
│   └── schema.prisma
│
├── tests/
│   └── auth.spec.js
│
├── playwright.config.js
├── package.json
└── README.md
````

## 🔐 Authentication Flow

### Sign Up

Users can create an account by providing:

* Email
* Password

The password is hashed using `bcrypt` before being stored in the database.

### Login

Users can log in using their registered email and password.

The server verifies the user and compares the entered password with the hashed password stored in the database.

Invalid credentials return an appropriate error message.

## 🧪 Testing

The authentication flow is tested using Playwright.

The project includes tests for:

```text
✓ User can sign up successfully
✓ User can login successfully
✓ Login fails with wrong password
```

Run the tests with:

```bash
npx playwright test
```

To run tests with the browser visible:

```bash
npx playwright test --headed
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/authentication-form.git
```

Navigate to the project:

```bash
cd authentication-form
```

Install dependencies:

```bash
npm install
```

Generate Prisma Client:

```bash
npx prisma generate
```

Run database migrations:

```bash
npx prisma migrate dev
```

Start the development server:

```bash
npm run dev
```

The application will be available at:

```text
http://localhost:3000
```

## 📌 Future Improvements

* 🔐 Session-based authentication
* 🍪 Secure authentication cookies
* 🚪 Logout functionality
* 🔄 Password reset
* 📧 Email verification
* 🛡️ Authentication middleware
* 👤 User profile
* 🔒 Improved security with rate limiting

## 👩‍💻 Author

**Mahdis**

Frontend Developer | React & Next.js

---

⭐ If you found this project useful, feel free to star the repository.
