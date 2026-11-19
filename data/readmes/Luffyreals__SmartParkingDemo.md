# Smart Parking System Demo - Nhóm 10

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Database-TiDB%20Cloud%20%2F%20MySQL-00758F.svg)](https://www.pingcap.com/tidb-cloud/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog-v1.2.0-blue.svg)](CHANGELOG.md)
[![Contributing](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 1. Giới thiệu
Dự án môn Cơ sở dữ liệu xây dựng hệ thống quản lý bãi đỗ xe thông minh trên nền tảng web (Streamlit) kết nối trực tiếp tới cơ sở dữ liệu `dbptit` (hỗ trợ TiDB Cloud Serverless qua SSL và MySQL). Ứng dụng hỗ trợ giám sát sơ đồ vị trí đỗ thời gian thực, xử lý nghiệp vụ xe vào/ra theo transaction, tính phí tự động, quản lý vé tháng và thống kê doanh thu.

## 2. Các tính năng chính
Ứng dụng gồm 6 màn hình nghiệp vụ tiếng Việt (`src/app.py`) với hiệu ứng skeleton loading, bộ nhớ đệm TTL và bảng dữ liệu hiện đại:

1. **Tổng quan & Sơ đồ bãi:** Hiển thị 5 chỉ số KPI (Tổng vị trí, Chỗ trống, Xe đang gửi, Doanh thu hôm nay, Vé tháng hiệu lực), thẻ công suất 3 bãi đỗ kèm địa điểm, tỷ lệ lấp đầy từng khu vực, lưới trực quan trạng thái ô đỗ theo bãi/khu vực và form thêm vị trí đỗ mới.
2. **Vào / Ra bãi xe:** Ghi nhận xe vào bãi (tự động cập nhật `phuongtien`, `luotdo`, trạng thái `vitrido` và `thexe` trong cùng transaction), xem danh sách xe đang gửi, ước tính phí và thực hiện thanh toán check-out.
3. **Lịch sử giao dịch:** Tra cứu và lọc biên lai thanh toán theo khoảng thời gian, loại phương tiện, biển số, mã thẻ hoặc nhân viên trực kèm xuất báo cáo CSV.
4. **Vé tháng & Bảng giá:** Đăng ký vé tháng cho khách hàng/phương tiện kèm ước tính chi phí, theo dõi vé còn hiệu lực và tra cứu bảng giá theo loại phương tiện và đối tượng khách hàng.
5. **Thống kê doanh thu:** Biểu đồ Altair trực quan hóa doanh thu theo ngày, lưu lượng lượt xe, cơ cấu doanh thu theo loại phương tiện và so sánh theo từng bãi đỗ.
6. **Nhân sự & Khách gửi xe:** Gồm 5 tab chuyên sâu — **Nhân sự vận hành** (`nhanvien`), **Giảng viên & Sinh viên** (`khachhang`), **Khách vãng lai**, **Kho thẻ xe RFID** (`thexe`) và **Danh bạ phương tiện** (`phuongtien`).

Ngoài ra, thanh sidebar hỗ trợ **Kiểm tra kết nối DB**, **Làm mới dữ liệu** và **Khởi tạo dữ liệu mẫu** (idempotent) để demo nhanh khi các bảng giao dịch còn trống.

## 3. Cấu trúc dự án
```text
SmartParkingDemo/
├── .streamlit/
│   ├── config.toml           # Cấu hình theme giao diện Streamlit
│   └── secrets.toml          # Cấu hình kết nối TiDB Cloud (không commit lên Git)
├── assets/
│   └── logo.svg              # Logo thương hiệu Smart Parking PTIT
├── docs/                     # Tài liệu dự án
│   ├── IDEA.md               # Ý tưởng & điểm nổi bật
│   ├── LICENSE.md            # Giấy phép MIT
│   ├── MVP.md                # Phạm vi MVP
│   ├── PLAN.md               # Kế hoạch & tiến độ triển khai
│   ├── PROJECT.md            # Thông tin đề tài & thành viên
│   ├── SPEC.md               # Đặc tả kỹ thuật
│   ├── architecture.md       # Kiến trúc phân tầng & schema dbptit
│   └── setup-guide.md        # Hướng dẫn cài đặt chi tiết
├── src/
│   ├── app.py                # Giao diện Streamlit 6 trang
│   ├── models/               # Các dataclass ánh xạ schema dbptit
│   ├── services/
│   │   ├── db_service.py     # Quản lý kết nối TiDB/MySQL, query & transaction
│   │   └── parking_service.py# Logic nghiệp vụ bãi đỗ, tính phí, thống kê, seed data
│   └── ui/
│       ├── icons.py          # Hệ thống icon SVG tối giản
│       └── styles.py         # Design system CSS, skeleton & modern table
├── tests/
│   └── test_app.py           # 20 unit tests cho ParkingService
├── Dump20261118.sql          # Script khởi tạo schema & dữ liệu nền dbptit
├── index.html                # Trang web tĩnh giới thiệu dự án (GitHub Pages)
├── requirements.txt          # Thư viện Python cần thiết
└── README.md                 # Tài liệu tổng quan dự án
```

## 4. Hướng dẫn cài đặt và chạy ứng dụng
1. **Clone repository:**
   ```bash
   git clone https://github.com/Luffyreals/SmartParkingDemo.git
   cd SmartParkingDemo
   ```
2. **Tạo và kích hoạt môi trường ảo:**
   ```powershell
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Linux / macOS:
   # source .venv/bin/activate
   ```
3. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Cấu hình kết nối Database:**
   Tạo file `.streamlit/secrets.toml` với thông tin TiDB Cloud / MySQL:
   ```toml
   [tidb]
   host = "gateway01.ap-northeast-1.prod.aws.tidbcloud.com"
   port = 4000
   database = "dbptit"
   user = "<your_username>"
   password = "<your_password>"
   ```
   Hoặc thiết lập các biến môi trường `TIDB_HOST`, `TIDB_PORT`, `TIDB_DATABASE`, `TIDB_USER`, `TIDB_PASSWORD` (xem thêm [docs/setup-guide.md](docs/setup-guide.md)).
5. **Chạy ứng dụng:**
   ```bash
   streamlit run src/app.py
   ```
   Truy cập `http://localhost:8501`.
6. **Chạy kiểm thử:**
   ```bash
   python -m unittest discover -s tests -v
   ```

## 5. Đóng góp & Lịch sử phiên bản
- Xem hướng dẫn đóng góp tại [CONTRIBUTING.md](CONTRIBUTING.md).
- Theo dõi lịch sử cập nhật chi tiết tại [CHANGELOG.md](CHANGELOG.md).
- Giấy phép mã nguồn mở: [LICENSE](LICENSE) (MIT).

## 6. Thành viên nhóm 10
- Nguyễn Hoàng Tùng (Trưởng nhóm)
- Nguyễn Bá Minh Đức
- Bùi Minh Khang
- Trần Anh Tú
