# Humming Tone 🛍️👕

> **A Modern, Full-Stack E-Commerce & Custom Clothing Platform**

Humming Tone is a full-featured apparel e-commerce web application featuring interactive 3D/canvas custom clothing design, dynamic category browsing, secure payments via Razorpay, real-time WhatsApp order tracking, and a powerful administrative dashboard with Cloudinary CDN-powered image delivery.

---

## 🌐 Live Deployments

- **Frontend (Storefront & Admin):** [https://hummingtone.com](https://hummingtone.com) *(Hosted on Vercel)*
- **Backend (API Services):** `https://api.hummingtone.com` / Render Web Service *(Hosted on Render)*
- **Database:** TiDB Cloud (Serverless MySQL)
- **Media & CDN:** Cloudinary Global Edge CDN

---

## 🚀 Key Features

### 🛍️ Customer Storefront (`/usertab`)
- **Dynamic Catalog:** Browse by Gender (Men, Women, Children, Baby, Sports) and dynamic categories.
- **Interactive Product Customizer:** 3D & canvas-based custom apparel builder for custom designs, text, and artwork.
- **Cart & Checkout:** Real-time stock calculation, promotional discounts, and GST handling.
- **Secure Payments:** Full integration with Razorpay checkout & webhook verification.
- **Live Order Tracking:** Multi-stage order status tracking with automated WhatsApp & Email notifications.

### 🛠️ Administrative Control Center (`/admin`)
- **Product Management:** Add/Edit/Archive products with multi-variant pricing, sizing, and colors.
- **Cloudinary Image Pipeline:** Direct buffer streaming with automatic WebP/AVIF compression (`f_auto, q_auto`).
- **Inventory & Orders:** Real-time inventory tracking, order status updates, and returns management.
- **CMS & Site Content:** Live customizer for brand details, social links, gender visibility, and legal policies.
- **Meta WhatsApp Integration:** Automated order confirmations and delivery updates via Meta WhatsApp Cloud API.

---

## 🏗️ Architecture & Tech Stack

```
   ┌─────────────────────────────────────────────────────────────┐
   │                  Vercel (React 19 + Vite)                   │
   │  Storefront, 3D Canvas Customizer, Admin Panel (hummingtone.com) │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ HTTPS REST APIs
   ┌──────────────────────────────▼──────────────────────────────┐
   │                  Render (Node.js + Express)                 │
   │      Authentication, Checkout, Webhooks, Image Streaming    │
   └───────────────┬──────────────────────────────┬──────────────┘
                   │                              │
         SQL Queries (SSL)                Image Stream Buffer
                   │                              │
   ┌───────────────▼──────────────┐   ┌───────────▼──────────────┐
   │      TiDB Cloud (MySQL)      │   │      Cloudinary CDN      │
   │  Products, Orders, Site Data │   │  High-Speed Edge Delivery│
   └──────────────────────────────┘   └──────────────────────────┘
```

### Frontend
- **Framework:** React 19, Vite
- **Routing:** React Router v7
- **3D & Canvas:** Three.js, `@react-three/fiber`, `@react-three/drei`, Valtio, Lucide Icons, Material UI
- **Animations:** Lottie React, Snowfall

### Backend
- **Runtime:** Node.js, Express 5
- **Database:** MySQL2, TiDB Cloud (SSL-enabled)
- **Media Management:** Cloudinary SDK, Multer (`MemoryStorage`)
- **Payments:** Razorpay Node SDK
- **Communications:** Meta WhatsApp Business API, Nodemailer

---

## 🛠️ Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/GowthamCD6/Humming-Tone.git
cd Humming-Tone
```

### 2. Start the Backend API
```bash
cd Server
npm install
npm start
# Server runs on http://localhost:5000
```

### 3. Start the Frontend Application
```bash
cd ../Humming_Tone
npm install
npm run dev
# App runs on http://localhost:5173
```

---

## 🛡️ Health Check & Keep-Alive Endpoints

To prevent the Render free-tier instance from sleeping, configure a periodic ping (every 10-14 minutes) to:

- `GET /health` $\rightarrow$ Lightweight health check (`{ status: "ok", uptime, timestamp }`)
- `GET /ping` $\rightarrow$ Ultra-lightweight string response (`"pong"`)

---

## 📄 License

This project is proprietary and maintained for **Humming Tone**. All rights reserved.
