# Xin chào mọi người.
> Dự án này, tôi build với mục đích là tổng hợp đúc kết các kiến thức, kinh nghiệm thực tế để tạo nên source base hữu ích cho cá nhân tôi và team. Một hệ thống không chỉ chạy được, mà còn phải bảo mật, dễ vận hành và sẵn sàng cho môi trường Production.

## 🛡️ Bảo mật là ưu tiên hàng đầu
Quét lỗ hổng bảo mật dự án là điều không thể thiếu đối với tôi. Tôi sử dụng **Trivy** để quét nhanh các dependency, filesystem và Docker image.

```bash
# Cài đặt Trivy (Arch Linux hoặc Ubuntu)
sudo pacman -S trivy  # Arch
sudo apt-get install trivy  # Ubuntu
```

Lý do tôi chọn Trivy:
- Nhẹ, quét nhanh dependency trong `pom.xml`.
- Hỗ trợ tốt cho CI/CD, có thể chặn pipeline nếu phát hiện lỗi nghiêm trọng.
- Không cần cấu hình phức tạp, phù hợp cho cả local và automation server.

---

## 🏗️ Để chạy Spring Boot cần những gì?
Nhiều người chỉ quan tâm đến việc "source có chạy được hay không", nhưng trong thực tế, độ ổn định phụ thuộc rất nhiều vào môi trường thực thi (runtime environment).

Dưới đây là 4 thành phần nền tảng:

### 1. JDK (Java Development Kit)
Thành phần bắt buộc để compile và chạy Java. Tôi ưu tiên sử dụng **Java 21** (LTS) để tận dụng các tính năng mới nhất như Virtual Threads.

### 2. Biến môi trường (Environment Variables)
Cực kỳ quan trọng để cấu hình hệ thống mà không cần "hard-code". Giúp tách biệt code và cấu hình nhạy cảm (Database, API Keys, JWT Secrets).
- Tham khảo mẫu tại: `.env.example`

### 3. Khả năng tương thích OS
Code phải chạy ổn định trên Linux, Windows và MacOS. Đó là lý do tôi sử dụng **Maven Wrapper (`mvnw`)** để đảm bảo version Maven đồng nhất cho cả team.

### 4. Runtime Dependencies
Hệ thống backend hiện đại không chạy đơn lẻ. Nó cần các service phụ trợ như:
- **PostgreSQL**: Lưu trữ dữ liệu chính.
- **Flyway**: Quản lý version schema database (Nguồn sự thật duy nhất).
- **Redis**: Cache & Session (Nếu cần).

---

## 📂 Tổ chức mã nguồn (Folder Structure)
Thay vì để cả đống file ở root gây rối mắt, tôi tổ chức lại theo cách tường minh nhất:

```
.
├── deployment/          # Chứa cấu hình triển khai
│   └── docker/          # Dockerfile, Docker Compose (Dev/Prod)
├── scripts/             # Bộ kịch bản vận hành (Start, Stop, Backup...)
├── docs/                # Tài liệu chi tiết về kiến trúc, bảo mật
├── src/                 # Source code chính (Clean Architecture)
├── .env                 # Cấu hình môi trường (Bị ignore bởi Git)
└── pom.xml              # Maven dependencies
```

---

## 🏎️ Quick Start - Chạy dự án thần tốc

### Cách 1: Tự động hóa hoàn toàn (Khuyên dùng)
Tôi đã viết sẵn bộ script để bạn không cần nhớ những câu lệnh Docker phức tạp.

```bash
# 1. Cài đặt môi trường (Chỉ làm lần đầu)
cp .env.example .env
chmod +x scripts/*.sh

# 2. Chạy môi trường Development (Có Hot-reload & Postgres)
./scripts/start.sh dev

# 3. Theo dõi log khởi động
./scripts/start.sh logs
```

### Cách 2: Chạy thủ công (Manual)
Dành cho những ông muốn kiểm soát từng bước bằng lệnh Maven truyền thống.

```bash
# 1. Khởi động Database (Bắt buộc)
sg docker -c "docker compose -f docker-compose.yml -f docker-compose.dev.yml up db -d"

# 2. Chạy ứng dụng Spring Boot
./mvnw spring-boot:run
```

---

## 🛠️ Các tính năng & Use Cases đã triển khai
Dự án được xây dựng theo **Clean Architecture + DDD**, đảm bảo mỗi chức năng là một "Atomic Use Case" độc lập.

- ✅ **Authentication**: Sign Up (Đăng ký) & Sign In (Đăng nhập).
- ✅ **Security**: JWT lưu trong HttpOnly Cookie, BCrypt Hashing, CSRF Protection.
- ✅ **Domain Logic**: Rich Domain Model, quản lý Account Status (Active, Disabled, Blacklisted).
- ✅ **Infrastructure**: PostgreSQL 16+, Flyway Migration tự động.
- ✅ **Operational**: Lưu trữ IP, User Agent và sẵn sàng cho Domain Events.

---

## 🚀 Vận hành Production (SRE & DevOps)
Hệ thống này được thiết kế để "vứt lên VPS" và chạy ngay với độ bảo mật cao nhất.

### Quản lý dịch vụ:
```bash
./scripts/start.sh prod    # Chạy Production (Hardened Container)
./scripts/stop.sh prod     # Dừng an toàn
./scripts/healthcheck.sh   # Kiểm tra sức khỏe hệ thống (Actuator)
```

### Sao lưu & Khôi phục (DBA Practices):
- **Backup**: `./scripts/backup.sh` (Nén gzip, bảo mật file 600, giữ 30 ngày).
- **Restore**: `./scripts/restore.sh` (Tự động ngắt kết nối đang active để khôi phục).

### Bảo trì hệ thống:
- **Cleanup**: `./scripts/cleanup.sh` (Dọn dẹp image thừa, xoay vòng log để tránh đầy ổ cứng).

---

## 📚 Tài liệu chuyên sâu (Deep Dive)
Để hiểu sâu hơn về từng mảng, hãy đọc các file trong thư mục `docs/`:
- 🎯 **[DDD Use Cases Guide](docs/DDD_USE_CASES_GUIDE.md)**: Cách thiết kế layer nghiệp vụ.
- 🛡️ **[Security & Hardening](docs/SECURITY.md)**: Cách tôi setup cứng Container & OS.
- 🌐 **[VPS Deployment](docs/VPS_DEPLOYMENT.md)**: Hướng dẫn config Nginx & SSL.

---
**Chúc các ông có trải nghiệm code mượt mà với source base này!**