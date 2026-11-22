# Smart Parking System — Nhóm 10 (PTIT)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20v1%20%2B%20WS-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19%20%2B%20TypeScript-61DAFB.svg)](https://react.dev/)
[![Database](https://img.shields.io/badge/Database-TiDB%20Cloud%20%2F%20MySQL%208-00758F.svg)](https://www.pingcap.com/tidb-cloud/)
[![Version](https://img.shields.io/badge/Changelog-v2.1.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 1. Giới thiệu

Hệ thống quản lý bãi đỗ xe thông minh (**Smart Parking PTIT**) phát triển trên kiến trúc Full-Stack hiện đại: **FastAPI (`/api/v1`) + WebSocket thời gian thực**, giao diện **React 19 + TypeScript + Tailwind CSS v4**, và cơ sở dữ liệu quan hệ **`dbptit`** (16 bảng trên TiDB Cloud / MySQL 8 với migration có phiên bản và khóa giao dịch đồng thời `SELECT ... FOR UPDATE`).

Phiên bản **v2.1.0** tách rõ tầng nghiệp vụ domain, bổ sung xác thực RBAC (`ADMIN` / `ACCOUNTANT` / `OPERATOR`) kèm refresh token rotation, đổi mật khẩu trực tiếp trên giao diện, đối soát ca trực thu ngân, nhật ký kiểm toán nguyên tử, mã thanh toán VietQR chuẩn EMVCo/NAPAS, in phiếu nhiệt 80mm, kiểm thử tự động đa tầng (`pytest` + `vitest`) và GitHub Actions CI.

## 2. Tính năng chính

1. **Cổng Vào / Ra (Gate POS):** Check-in / check-out nguyên tử theo thứ tự khóa chống deadlock, phím tắt vận hành (`F2`, `F3`/`/`, `1–3`, `Enter`, `Esc`), mã QR chuyển khoản chuẩn EMVCo/NAPAS VietQR, xử lý mất thẻ (kèm cấp đổi thẻ cho vé tháng), chuyển vị trí đỗ và in phiếu/biên lai 80mm qua trình duyệt.
2. **Tổng quan & Sơ đồ bãi trực tiếp:** KPI theo thời gian thực (đồng bộ qua WebSocket xác thực bằng single-use ticket), thanh công suất bãi/khu vực, lưới vị trí lọc tại SQL, bật/tắt bảo trì và công cụ đối soát giải phóng ô đỗ & thẻ RFID mồ côi.
3. **Vé tháng & Bảng giá:** Đăng ký, gia hạn nhiều tháng, đổi xe/thẻ, hủy trước hạn và quản lý bảng giá với kiểm tra trùng vé/thẻ trong transaction.
4. **Giao dịch & Ca trực thu ngân:** Tra cứu lịch sử giao dịch có phân trang và lọc từ khóa trực tiếp tại SQL, xuất CSV phía máy chủ, mở/chốt ca bàn giao quỹ tiền mặt – chuyển khoản – hoàn tiền.
5. **Phân tích Doanh thu (Recharts):** Biểu đồ doanh thu & lưu lượng theo ngày (múi giờ Việt Nam UTC+7), cơ cấu theo loại phương tiện và theo bãi đỗ (gộp đầy đủ cả lượt ngày và đăng ký/gia hạn vé tháng).
6. **Quản trị RBAC & Kiểm toán:** Quản lý tài khoản đăng nhập (thu hồi phiên tức thì qua `token_version`, chặn khóa ADMIN cuối cùng), danh bạ nhân sự/khách hàng/phương tiện (ẩn PII đối với `OPERATOR`), kho thẻ RFID, hạ tầng bãi/khu và nhật ký `audit_logs` ghi kèm IP trong cùng transaction.

## 3. Cấu trúc dự án

```text
SmartParkingDemo/
├── .github/workflows/ci.yml      # CI tự động: ruff, mypy, pytest, oxlint, tsc, vitest, vite build
├── pyproject.toml                # Cấu hình đóng gói, pytest, coverage, ruff, mypy
├── .env.example                  # Mẫu biến môi trường (TIDB_*, AUTH_SECRET_KEY, VIETQR_*, CORS_*)
├── Dump20261118.sql              # Lược đồ nền 13 bảng & dữ liệu mẫu dbptit
├── src/
│   ├── core/                     # Settings (pydantic-settings), Exceptions, JSON Logging
│   ├── models/                   # Canonical Pydantic v2 entities (16 bảng) & response DTOs
│   ├── services/
│   │   ├── db_service.py         # Connection pool an toàn, UTC +00:00, TiDB conflict retry
│   │   ├── migration_service.py  # Runner migration có phiên bản (schema_migrations + GET_LOCK)
│   │   ├── auth_service.py       # PBKDF2 600k, JWT HS256, Refresh rotation, WS tickets
│   │   ├── parking_service.py    # Facade tương thích ngược
│   │   └── domain/               # 6 domain service: gate, infra, pass, billing, directory, analytics
│   ├── api/
│   │   ├── main.py               # FastAPI app factory, error envelopes, SPA fallback
│   │   ├── deps.py               # DI, RBAC, lot scoping
│   │   ├── middleware.py         # Request-ID, Security Headers, Sliding-window Rate Limiter
│   │   ├── ws.py                 # WebSocket xác thực ticket, broadcast song song, heartbeat
│   │   └── v1/routers/           # 8 module router REST /api/v1/*
├── frontend/                     # React 19 + TypeScript (strict) + Vite 8 + Tailwind v4 SPA
│   └── src/
│       ├── context/              # AuthContext, ToastContext, ThemeContext (Dark Mode)
│       ├── hooks/                # useLiveSocket (ticket auth + targeted React Query invalidation)
│       ├── lib/                  # API client (refresh interceptor), VietQR EMVCo TLV, CSV
│       ├── components/           # UI primitives (Modal, ConfirmDialog, Pagination) & Gate/Admin modules
│       ├── pages/                # 6 trang nghiệp vụ lazy-loaded + LoginPage
│       └── test/                 # Bộ kiểm thử Vitest + React Testing Library
├── tests/                        # Bộ kiểm thử Pytest (Unit, Security, RBAC, WebSocket)
└── docs/                         # Tài liệu kỹ thuật, hướng dẫn cài đặt & sử dụng (user-guide.md)
```

## 4. Hướng dẫn cài đặt và sử dụng (Windows PowerShell)

> Xem thêm hướng dẫn thao tác chi tiết theo từng phân hệ và vai trò tại **[docs/user-guide.md](docs/user-guide.md)** và hướng dẫn cài đặt đầy đủ tại **[docs/setup-guide.md](docs/setup-guide.md)**.

1. **Cấu hình môi trường:** Sao chép `.env.example` thành `.env` và điền thông tin TiDB Cloud / MySQL cùng `AUTH_SECRET_KEY`.
2. **Cài đặt và chạy Backend FastAPI:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\pip.exe install -r requirements-dev.txt
   .\.venv\Scripts\uvicorn.exe src.api.main:app --reload --port 8000
   ```
   Tài liệu Swagger OpenAPI tại `http://127.0.0.1:8000/docs` (tài khoản dev mặc định sau seed: `admin` / `thungan` / `baove` — mật khẩu `123456`).
3. **Cài đặt và chạy Frontend SPA:**
   ```powershell
   Set-Location frontend
   npm install
   npm run dev
   ```
   Truy cập `http://localhost:5173` (Vite tự proxy `/api`, `/ws`, `/health` về cổng `8000`), hoặc chạy `npm run build` để FastAPI phục vụ trực tiếp bản build tại `http://127.0.0.1:8000`.

## 5. Kiểm thử & Kiểm tra chất lượng mã

```powershell
# Backend lint, typecheck & pytest + coverage
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m mypy src
.\.venv\Scripts\python.exe -m pytest tests --cov=src -v

# Frontend lint, strict typecheck, Vitest & production build
Set-Location frontend
npm run lint
npm run typecheck
npm run test
npm run build
```

## 6. Thành viên nhóm 10 (Lớp D24CQCE04-B — GVHD: Nguyễn Trọng Khánh)
- **Nguyễn Hoàng Tùng** — `B24DCCE284` (Trưởng nhóm)
- **Nguyễn Bá Minh Đức** — `B24DCCE053`
- **Trần Anh Tú** — `B24DCCE277`
- **Bùi Minh Khang** — `B24DCCE137`
