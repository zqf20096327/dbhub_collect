# Quiz Platform (Backend & Frontend)

Full-stack quiz va bilim baholash platformasi. Ushbu tizim foydalanuvchilarga turli kategoriyalar bo'yicha testlar ishlash, o'z natijalarini kuzatish va peshqadamlar jadvalida (`Leaderboard`) o'z o'rinlarini ko'rish imkonini beradi.

## 🚀 Texnologiyalar (Tech Stack)

### Backend:
* **Java 17+** / **Spring Boot**
* **Spring Security** (Authentication & Authorization)
* **Spring Data JPA** (Hibernate)
* **PostgreSQL / MySQL**
* **Gradle** (Build tool)

### Frontend:
* **React** / **TypeScript**
* **Tailwind CSS** (Styling)
* **Framer Motion** (Animations)
* **Recharts** (Statistika va grafiklar)
* **Axios** (API requests)

---

## 📊 Asosiy Imkoniyatlar

* **Shaxsiy Dashboard:** Foydalanuvchining umumiy natijalari, aniqlik ko'rsatkichi (Accuracy), sarflangan vaqt va dinamik grafiklar.
* **Peshqadamlar Jadvali (Leaderboard):** Barcha vaqtlar, haftalik va kunlik reytinglar.
* **Testlar va Kategoriyalar:** Turli qiyinlikdagi va yo'nalishlardagi testlarni ishlash va natijalarni saqlash.
* **Xavfsizlik:** JWT yoki Spring Security orqali himoyalangan REST API endpointlari.

---

## ⚙️ O'rnatish va Ishga Tushirish

### 1. Backend qismini ishga tushirish

Loyihaning backend papkasiga o'ting va quyidagi buyruqni bajaring:

```bash
# Gradle yordamida loyihani ishga tushirish
./gradlew bootRun

# Bog'liqliklarni o'rnatish
npm install

# Development serverni ishga tushirish
npm run dev
```
```text
quiz-platform/
├── backend/                  # Spring Boot Backend
│   ├── src/main/java/com/quizplatform/backend/
│   │   ├── modules/
│   │   │   ├── auth/         # Autentifikatsiya
│   │   │   ├── leaderboard/  # Reyting va Statistika
│   │   │   ├── quiz/         # Testlar boshqaruvi
│   │   │   └── user/         # Foydalanuvchi profili
│   │   └── BackendApplication.java
│   └── build.gradle
│
└── frontend/                 # React & TypeScript Frontend
    ├── src/
    │   ├── api/              # Axios sozlamalari
    │   ├── components/       # Umumiy komponentlar
    │   └── pages/            # Dashboard, Leaderboard, Quiz sahifalari
    └── package.json
```

