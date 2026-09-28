# Fullstack Auth System (React + Node.js + MySQL)

**Production-like authentication sample application** showing secure sign-up/login, JWT/Session handling, RBAC and best practices for modern web apps.

---

## ✅ What is this?

- Full-stack demo (React frontend + Node/Express backend + MySQL)
- Focused on **secure user authentication** and **session management**
- Includes **protected routes**, **role-based access**, **token refresh**, **password hashing** and **security headers**

## ⚙️ Tech stack

- **Frontend:** React, React Router, Axios
- **Backend:** Node.js, Express, Passport, JWT
- **Database:** MySQL
- **Security:** bcrypt, helmet, CORS, CSRF protection, secure cookies

## 🚀 Quick start

### 1) Clone
```bash
git clone https://github.com/amariwan/fullstack-auth-system.git
cd fullstack-auth-system
```

### 2) Install dependencies
```bash
cd backend && npm install
cd ../frontend && npm install
```

### 3) Configure environment variables
Copy the template and set your values:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 4) Start (dev)
```bash
# backend
cd backend && npm run dev
# frontend (in a separate terminal)
cd frontend && npm start
```

## 🔒 Security notes

- Uses **bcrypt** to hash passwords
- Uses **HTTP-only cookies** for session tokens
- Includes **CSRF protection** for state-changing requests
- Includes **helmet** + recommended security header defaults

## 📌 Want to extend it?

- Add MFA (TOTP / SMS)
- Add OAuth providers (Google, GitHub)
- Add email confirmation flows
- Add rate limiting / brute force protection

---

## License
MIT
