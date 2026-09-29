# 🤖 InterviewMate - AI Job Interview Simulator

**InterviewMate** adalah aplikasi web modern yang membantu kandidat pelamar kerja melatih kemampuan wawancara mereka. Aplikasi ini menggunakan kecerdasan buatan (**Google Gemini AI**) yang berperan sebagai HRD profesional untuk memberikan pertanyaan yang relevan sesuai posisi dan CV, serta memberikan feedback instan.

![Project Status](https://img.shields.io/badge/Status-Development-green)
![Tech Stack](https://img.shields.io/badge/Stack-Next.js_14-black)

## 🚀 Fitur Utama

*   **🎯 Role-Based Interview:** AI menyesuaikan pertanyaan berdasarkan posisi yang dilamar (misal: Frontend Dev, Admin, Marketing).
*   **📄 CV Analysis:** AI membaca ringkasan CV pengguna untuk mengajukan pertanyaan yang personal.
*   **💬 Interactive Chat:** Antarmuka chat yang intuitif dan responsif (Real-time feeling).
*   **💡 Instant Feedback:** AI memberikan kritik dan saran setelah pengguna menjawab pertanyaan.
*   **☁️ Cloud Database:** Data tersimpan aman menggunakan TiDB (Serverless MySQL).

## 🛠️ Teknologi yang Digunakan (Tech Stack)

Aplikasi ini dibangun dengan arsitektur **Clean Code** dan teknologi terbaru:

*   **Framework:** [Next.js 14](https://nextjs.org/) (App Router & TypeScript)
*   **Styling:** [Tailwind CSS](https://tailwindcss.com/) & Lucide React Icons
*   **Database:** [MySQL](https://www.mysql.com/) (via TiDB Cloud Serverless)
*   **ORM:** [Prisma](https://www.prisma.io/) (Type-safe database access)
*   **AI Engine:** [Google Gemini API](https://ai.google.dev/) (`gemini-pro` model)
*   **Deploy:** [Vercel](https://vercel.com/)

## 📦 Cara Menjalankan di Lokal

Ikuti langkah ini untuk mencoba project di komputermu:

1.  **Clone Repository**
    ```bash
    git clone https://github.com/username-kamu/interview-mate.git
    cd interview-mate
    ```

2.  **Install Dependencies**
    Pastikan kamu menggunakan `yarn`:
    ```bash
    yarn install
    ```

3.  **Setup Environment Variables**
    Buat file `.env` dan isi dengan kredensial kamu:
    ```env
    # Database Connection (TiDB / Local MySQL)
    DATABASE_URL="mysql://username:password@host:port/database?sslaccept=strict"

    # Google Gemini AI Key
    GEMINI_API_KEY="isi_api_key_kamu_disini"
    ```

4.  **Setup Database**
    ```bash
    yarn prisma generate
    yarn prisma db push
    ```

5.  **Jalankan Server**
    ```bash
    yarn dev
    ```
    Buka [http://localhost:3000](http://localhost:3000) di browser.

## 🤝 Kontribusi

Project ini terbuka untuk kontribusi! Silakan buat *Pull Request* jika ingin menambahkan fitur baru seperti:
*   Voice-to-Text (Wawancara suara).
*   Sistem penilaian (Scoring).
*   Login User (Auth).

---
Dibuat dengan ❤️ menggunakan Next.js dan Gemini AI.