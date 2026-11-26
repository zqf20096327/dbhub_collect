# Smart Parking System — Nhóm 10 (PTIT)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20v1%20%2B%20WS-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19%20%2B%20TypeScript-61DAFB.svg)](https://react.dev/)
[![Database](https://img.shields.io/badge/Database-TiDB%20Cloud%20%2F%20MySQL%208%20(13%20tables)-00758F.svg)](https://www.pingcap.com/tidb-cloud/)
[![Version](https://img.shields.io/badge/Changelog-v2.2.0-blue.svg)](docs/CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 1. Giới thiệu

**Smart Parking PTIT** là hệ thống quản lý bãi đỗ xe thông minh phục vụ học phần **Cơ sở dữ liệu (PTIT)**, phát triển trên kiến trúc Full-Stack gồm **FastAPI (`/api/v1`) + WebSocket `/ws/live`**, giao diện **React 19 + TypeScript + Tailwind CSS v4**, và cơ sở dữ liệu quan hệ **`dbptit`** gồm đúng **13 bảng chuẩn ERD** trên TiDB Cloud / MySQL 8.

Phiên bản **v2.2.0** tinh gọn toàn bộ mô hình vận hành dành cho **một người quản lý duy nhất** trên máy trạm hoặc mạng LAN nội bộ: bỏ lớp đăng nhập, phân quyền và bảng ca làm việc thừa để vào thẳng bàn điều hành, đồng thời giữ nguyên cơ chế **ghi nhận nhân viên thực hiện (`nhanvien.id`)** trên từng thao tác tại cổng (tự động chọn sẵn *Bảo vệ* phụ trách bãi khi check-in, *Thu ngân* phụ trách bãi khi check-out / đăng ký / gia hạn vé tháng, kèm tùy chọn đổi tay khi cần) và bổ sung bộ khởi chạy **1-click `Mo_SmartParking.bat`** cho Windows.

## 2. Cơ sở dữ liệu `dbptit` (13 bảng ERD)

![Sơ đồ thực thể quan hệ CSDL dbptit](docs/assets/so_do.png)

Lược đồ hoàn chỉnh lưu tại [`database/Dump20261118.sql`](database/Dump20261118.sql) với đúng **13 bảng nghiệp vụ**, không sinh thêm bảng phụ lúc khởi động:

| Nhóm bảng | Các bảng trong `dbptit` | Vai trò nghiệp vụ |
| --- | --- | --- |
| **Hạ tầng & Biểu giá (6)** | `baidoxe`, `khuvucdo`, `vitrido`, `loaiphuongtien`, `loaikhachhang`, `banggia` | Bãi đỗ, khu vực, trạng thái từng ô đỗ và ma trận đơn giá vé ngày / vé tháng |
| **Nhân sự, Khách, Xe & Thẻ (5)** | `nhanvien`, `khachhang`, `phuongtien`, `thexe`, `vethang` | Danh bạ nhân sự phụ trách bãi, chủ xe, phương tiện, kho thẻ RFID và vé tháng |
| **Vận hành & Hóa đơn (2)** | `luotdo`, `thanhtoan` | Lượt gửi xe vào/ra (`luotdo.idnv`) và hóa đơn thanh toán lượt ngày / vé tháng (`thanhtoan.idnv`) |

**Kỹ thuật CSDL áp dụng trong `src/services/`:**
- **Chống tranh chấp & Deadlock:** Mọi giao dịch đa bảng chạy trong `DBService.transaction()` với `SELECT ... FOR UPDATE` theo thứ tự khóa cố định `phuongtien -> vitrido -> thexe -> luotdo`, tự động retry các mã xung đột TiDB/MySQL (`1205`, `1213`, `8028`, `9007`).
- **Chống nhân bản JOIN & Cấp phát ID an toàn:** Dùng `ROW_NUMBER()` tách đúng 1 vé tháng còn hạn mới nhất cho mỗi thẻ/xe và cấp phát `nhanvien.id` bằng `COALESCE(MAX(id), 0) + 1` dưới khóa `FOR UPDATE`.
- **Chuẩn hóa UTC & Sargable Index:** Mọi cột `DATETIME` lưu ở UTC (`+00:00`); thống kê và lọc ngày kinh doanh Việt Nam (`Asia/Ho_Chi_Minh`, UTC+7) quy đổi bằng ranh giới `vn_day_utc_bounds()` (`>= start_utc AND < end_utc`) để tận dụng index thay vì bọc `DATE()` lên cột.

## 3. Tính năng chính (6 phân hệ SPA)

1. **Cổng Vào / Ra — Gate POS (`/gate`):** Check-in / check-out nguyên tử; tự nhận diện biển số vé tháng còn hạn và gắn đúng thẻ RFID; tự chọn *Bảo vệ* (check-in) hoặc *Thu ngân* (check-out) theo bãi đỗ nhưng vẫn đổi tay được; phím tắt vận hành (`F2`, `F3`/`/`, `1–3`, `Ctrl+Enter`, `Esc`); mã chuyển khoản **VietQR chuẩn EMVCo/NAPAS**; xử lý mất thẻ (hỗ trợ cấp đổi thẻ mới cho vé tháng); chuyển ô đỗ; hủy lượt nhập nhầm; và in phiếu/biên lai khổ nhiệt **80mm**.
2. **Tổng quan & Sơ đồ bãi trực tiếp (`/overview`):** KPI thời gian thực qua WebSocket `/ws/live`, thanh công suất theo bãi/khu vực, lưới ô đỗ lọc trực tiếp tại SQL, bật/tắt bảo trì, thêm ô đỗ hàng loạt (1–50 ô) và công cụ đối soát giải phóng ô đỗ hoặc thẻ RFID bị kẹt mồ côi.
3. **Vé tháng & Bảng giá (`/passes`):** Đăng ký mới, gia hạn nhiều tháng (cộng dồn từ `max(ngày hết hạn, hôm nay)`), hủy trước hạn, chọn nhân viên thu ngân thực hiện (`employee_id`) và chỉnh sửa trực tiếp ma trận đơn giá vé ngày / vé tháng.
4. **Lịch sử Giao dịch (`/transactions`):** Lọc đa tiêu chí tại SQL theo khoảng ngày kinh doanh UTC+7, từ khóa, **nhân viên thu ngân (`employee_id`)**, **phương thức thanh toán** (`Tiền mặt` / `Chuyển khoản`); cập nhật trạng thái (`Thành công`, `Hoàn tiền`, `Thất bại`); in lại biên lai; và xuất file CSV UTF-8 BOM trực tiếp từ backend (`/api/v1/transactions/export`).
5. **Phân tích Doanh thu (`/analytics`):** Biểu đồ Recharts doanh thu và lưu lượng theo ngày (UTC+7), cơ cấu theo loại phương tiện và theo bãi đỗ (gộp đủ cả hóa đơn lượt ngày và đăng ký/gia hạn vé tháng).
6. **Quản trị Danh mục & Hạ tầng (`/admin` — 3 tab):** Quản lý **Nhân sự & Danh bạ** (nhân viên, khách hàng, phương tiện), **Kho thẻ RFID** (phát hành, theo dõi thẻ đang gắn lượt/vé tháng, chuyển `Sẵn sàng` / `Mất - Hỏng`), và **Hạ tầng bãi/khu** (tạo bãi đỗ, thêm khu vực đỗ).

## 4. Cấu trúc dự án

```text
SmartParkingDemo/
├── .github/
│   ├── CONTRIBUTING.md           # Quy chuẩn kiến trúc, kiểm thử và commit
│   └── workflows/ci.yml          # CI tự động: ruff, mypy, pytest --cov>=80%, Prettier, oxlint, tsc, vitest, vite build
├── database/
│   └── Dump20261118.sql          # Lược đồ chuẩn 13 bảng & dữ liệu mẫu dbptit
├── scripts/
│   ├── launch_app.py             # Launcher Python (probe /health/live, auto npm run build, mở http://127.0.0.1:8000)
│   └── Tao_Shortcut_Desktop.bat  # Tùy chọn tạo shortcut "Smart Parking PTIT" trên Desktop Windows
├── docs/
│   ├── assets/                   # Logo & sơ đồ thực thể quan hệ (so_do.png)
│   ├── index.html & 404.html     # Trang giới thiệu tĩnh cho GitHub Pages
│   ├── architecture.md           # Kiến trúc phân tầng & quy ước giao dịch CSDL
│   ├── setup-guide.md            # Hướng dẫn cài đặt cục bộ & mạng LAN
│   ├── user-guide.md             # Hướng dẫn vận hành 6 phân hệ SPA
│   ├── CHANGELOG.md              # Lịch sử phiên bản dự án
│   └── Bao_cao_du_an.pdf, ...    # Báo cáo bài tập lớn & slide thuyết trình PTIT
├── Mo_SmartParking.bat           # File chạy 1-click trên Windows: tự kiểm tra build, mở server & trình duyệt
├── pyproject.toml                # Cấu hình đóng gói v2.2.0, pytest, coverage, ruff, mypy
├── .env.example                  # Mẫu biến môi trường (TIDB_*, CORS_ALLOWED_ORIGINS, VIETQR_*)
├── src/
│   ├── core/                     # Settings (pydantic-settings), Domain Exceptions, JSON Logging
│   ├── models/                   # Pydantic v2 entities cho 13 bảng dbptit & response DTOs
│   ├── services/
│   │   ├── db_service.py         # MySQLConnectionPool, cleanup an toàn, UTC +00:00, TiDB conflict retry
│   │   ├── parking_service.py    # Facade tương thích ngược
│   │   └── domain/               # 6 domain service: gate, infrastructure, pass, billing, directory, analytics
│   └── api/
│       ├── main.py               # FastAPI factory (/api/v1 + alias /api), error envelopes, SPA fallback
│       ├── deps.py               # DI wiring cho DBService & ParkingService
│       ├── middleware.py         # Request-ID & Security Headers
│       ├── ws.py                 # WebSocket /ws/live (origin check, heartbeat, concurrent broadcast)
│       ├── schemas.py            # Request schemas (/api/v1/*)
│       └── v1/routers/           # 7 router REST: health, infrastructure, turns, billing, passes, directory, analytics
├── frontend/                     # React 19 + TypeScript (strict) + Vite 8 + Tailwind v4 SPA
│   └── src/
│       ├── context/              # ToastContext, ThemeContext (Light / Dark Mode)
│       ├── hooks/                # useLiveSocket (WebSocket -> targeted React Query invalidation)
│       ├── lib/                  # API client, employee default selector, VietQR EMVCo TLV, CSV
│       ├── components/           # UI primitives, TicketPrintModal 80mm, Gate POS, Passes, Admin tabs
│       ├── pages/                # 6 trang vận hành lazy-loaded
│       └── test/                 # Bộ kiểm thử Vitest + React Testing Library
└── tests/                        # Bộ kiểm thử Pytest (Domain, API v1, Security headers, WebSocket, MySQL integration)
```

## 5. Khởi chạy nhanh & Cài đặt (Windows PowerShell)

> Xem thêm hướng dẫn chi tiết từng bước tại [`docs/setup-guide.md`](docs/setup-guide.md) và hướng dẫn vận hành giao diện tại [`docs/user-guide.md`](docs/user-guide.md).

### Cách 1 — Chạy 1-click trên Windows (Khuyến nghị cho Demo & Vận hành)

1. Chuẩn bị môi trường một lần duy nhất:
   ```powershell
   copy .env.example .env   # Điền TIDB_HOST, TIDB_USER, TIDB_PASSWORD
   python -m venv .venv
   .\.venv\Scripts\pip.exe install -r requirements-dev.txt
   ```
2. Nhấp đúp **`Mo_SmartParking.bat`**: script tự động kiểm tra (hoặc build `frontend/dist/` nếu chưa có), khởi động FastAPI ở `http://127.0.0.1:8000` và mở thẳng trình duyệt vào hệ thống.
3. *(Tùy chọn)* Nhấp đúp **`scripts\Tao_Shortcut_Desktop.bat`** để tạo lối tắt **Smart Parking PTIT** ngoài Desktop.

### Cách 2 — Chạy tách Backend / Frontend khi phát triển hoặc qua mạng LAN

```powershell
# Terminal 1: Backend FastAPI + Swagger UI tại http://127.0.0.1:8000/docs
.\.venv\Scripts\uvicorn.exe src.api.main:app --reload --port 8000

# Terminal 2: Frontend Vite dev server tại http://localhost:5173 (proxy /api, /ws, /health -> 8000)
Set-Location frontend
npm install
npm run dev
```

Để mở cho máy trạm / điện thoại trong cùng mạng LAN truy cập:
```powershell
Set-Location frontend; npm run build; Set-Location ..
.\.venv\Scripts\uvicorn.exe src.api.main:app --host 0.0.0.0 --port 8000
```

## 6. Kiểm thử & Kiểm tra chất lượng mã

```powershell
# Backend: Ruff lint, Mypy typecheck & Pytest + coverage (>= 80%)
.\.venv\Scripts\python.exe -m ruff check src tests scripts
.\.venv\Scripts\python.exe -m mypy src scripts
.\.venv\Scripts\python.exe -m pytest tests -m "not integration" --cov=src --cov-report=term-missing --cov-fail-under=80 -v

# Frontend: Prettier format check, Oxlint (0 warnings), TypeScript strict, Vitest & Vite build
Set-Location frontend
npm run format:check
npm run lint
npm run typecheck
npm run test
npm run build
```

## 7. Tài liệu & Thành viên Nhóm 10

- **Tài liệu kỹ thuật:** [`docs/architecture.md`](docs/architecture.md) · [`docs/setup-guide.md`](docs/setup-guide.md) · [`docs/user-guide.md`](docs/user-guide.md) · [`docs/CHANGELOG.md`](docs/CHANGELOG.md) · [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md)
- **Tài liệu đồ án:** [`docs/Bao_cao_du_an.pdf`](docs/Bao_cao_du_an.pdf) · [`docs/Cơ sở dữ liệu (final).pptx`](docs/Cơ%20sở%20dữ%20liệu%20(final).pptx)

**Thành viên Nhóm 10 (Lớp D24CQCE04-B — GVHD: Nguyễn Trọng Khánh):**
- **Nguyễn Hoàng Tùng** — `B24DCCE284` (Trưởng nhóm)
- **Nguyễn Bá Minh Đức** — `B24DCCE053`
- **Trần Anh Tú** — `B24DCCE277`
- **Bùi Minh Khang** — `B24DCCE137`
