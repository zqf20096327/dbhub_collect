# TiDB HTAP Demo — Real-time Crypto Analytics

Dự án này là một bản trình diễn (demo) kỹ thuật để so sánh khả năng xử lý **HTAP (Hybrid Transactional and Analytical Processing)** của cơ sở dữ liệu phân tán TiDB so với mô hình cơ sở dữ liệu quan hệ truyền thống (MySQL InnoDB).

Hệ thống giả lập một môi trường giao dịch tiền điện tử (Crypto Exchange) nơi:
- **TiKV (Row Store):** Tiếp nhận dữ liệu giao dịch với tần suất cao (OLTP).
- **TiFlash (Columnar Store):** *(Tuỳ chọn thêm)* Phân tích khối lượng dữ liệu khổng lồ (OLAP) mà không làm phiền đến hoạt động giao dịch.

Dự án sử dụng **Node.js, TypeScript, Prisma ORM, và Docker**.

---

## 🚀 1. Cài đặt và Khởi động

### 1.1 Khởi động Cluster Database
Dự án cung cấp file cấu hình `docker-compose.yml` để dựng cả TiDB Cluster và MySQL.

```bash
# Khởi động toàn bộ các dịch vụ ngầm định (TiDB, TiKV, PD, MySQL, Prisma Studio)
docker compose up -d
```

### 1.2 Cài đặt thư viện Node.js
```bash
npm install
```

### 1.3 Cấu hình Môi trường
Mở file `.env` và thiết lập biến môi trường `PROVIDER` để chọn Database muốn sử dụng:

*   **Để chạy với TiDB (Cổng 4003):** Kho lưu trữ phân tán, có khả năng mở rộng ngang.
    ```env
    PROVIDER="tidb"
    DATABASE_URL="mysql://root:@127.0.0.1:4003/crypto_demo"
    ```
*   **Để chạy với MySQL (Cổng 3307):** Kho lưu trữ tập trung, sử dụng InnoDB truyền thống.
    ```env
    PROVIDER="mysql"
    DATABASE_URL="mysql://root:@127.0.0.1:3307/crypto_demo"
    ```

---

## 🛠️ 2. Hướng dẫn Sử dụng CLI Menu

Hệ thống cung cấp một CLI đa năng để tương tác:

```bash
# Hiển thị Menu trợ giúp
npm start -- --help
```

### Bước 1: Khởi tạo Database
Bạn cần chạy lệnh này lần đầu tiên (hoặc khi đổi `PROVIDER`) để tạo bảng `trade_ticks` theo Prisma Schema.
```bash
npm start -- init
```

### Bước 2: Bơm Dữ Liệu Giao Dịch (OLTP Workload)
Phần này đóng vai trò "máy giả lập" các giao dịch Crypto. Nó sẽ liên tục đẩy các bản ghi về thời gian, giá, khối lượng của các đồng coin vào CSDL.
```bash
# Chạy mặc định (1000 record/batch, mỗi 10ms ném 1 batch)
npm start -- ingest

# Hoặc tùy chỉnh cấu hình tải qua Argument:
npm start -- ingest -b 2000 -i 50
```
> **Lưu ý quan trọng**: Giữ lệnh này chạy trong cửa sổ Terminal riêng (có thể chạy trong khoảng 5-10 phút) để thu thập khoảng 500k đến 1 triệu records trước khi tiến hành bước Phân tích. Có càng nhiều dữ liệu thì CSDL mới thực sự lộ ra bản chất và sức mạnh của nó.

### Bước 3: Phân tích Dữ liệu (OLAP Workload)
Tính toán giá trung bình theo khoảng thời gian, xác định Moving Average (MA), thống kê Volume.
```bash
npm start -- analytics
# Hoặc phân tích riêng một đồng cụ thể:
npm start -- analytics -s SOL/USDT
```

### Bước 4: So Sánh Hiệu Năng
Chạy cùng 1 câu lệnh phân tích hạng nặng (Tổng, Trung bình, Maximum, Window Function..), nhưng so sánh giữa việc chạy thuần túy trên kho lưu trữ Row (TiKV) so với cơ chế Auto-Routing của Hệ thống TiDB (hoặc giữa MySQL InnoDB vs Default).
```bash
npm start -- compare
```

### Xem dữ liệu trực quan:
```bash
npm start -- studio
```

---

## 📊 3. Cách Đo Lường và Đọc Hiểu Các Thông Số

### 3.1. Phân Tích Ingest (Thêm Dữ liệu - OLTP Workload)
**Khi bạn chạy `npm start -- ingest`:**
- **Thông Số Cần Lưu Ý**: **Batch latency (ms)** và **Throughput (rec/s)**.
- **TiDB sẽ biểu hiện**: `Throughput` thường xoay quanh mức `4000 - 8000 rec/s`, `Latency` cho mỗi Batch (1000 records) thường rơi vào `50 - 150ms`.
- **MySQL sẽ biểu hiện**: Ở quy mô chạy Local / Docker, MySQL thường cho tốc độ xử lý nhanh hơn TiDB vì MySQL luân chuyển dữ liệu từ App thẳng vào CPU & RAM nội bộ, không gặp tình trạng Network Hops qua lại giữa `tidb -> pd -> tikv` như TiDB. 
- **Bài học rút ra**: TiDB phải hy sinh chút ít độ trễ ở những giao dịch nhỏ lẻ để giữ cân bằng tổng thể, nhưng bù lại mang cho mình khả năng Mở rộng ngang (Horizontal Scaling) vô hạn bằng cách bổ sung Server khi tập Record chạm mốc vài chục cho đến vài trăm tỷ dòng. 

### 3.2. Phân Tích Truy vấn HTAP (HTAP Compare - OLAP Workload)
Đây là phần cốt lõi chứng minh tính ưu việt của hệ thống phân tán.
**Hãy chạy `npm start -- compare`:**
Mỗi Query sẽ hiển thị 1 cái bảng:
```
┌─────────────────────┬──────────────┬──────────┐
│ Engine              │ Latency (ms) │ Rows     │
├─────────────────────┼──────────────┼──────────┤
│ MySQL (InnoDB)      │        394.9 │        5 │
│ Auto (TiDB chọn)    │        332.8 │        5 │
└─────────────────────┴──────────────┴──────────┘
```
- **Thông Số Cần Lưu Ý**: Tốc độ phản hồi (**Latency**) của **Engine TiKV (Row Store)** so với chức năng **Auto** (nếu bạn tiếp tục nâng cấp dự án và kích hoạt TiFlash, nó sẽ tự Select TiFlash cho các Query Phân Tích nặng).
- **Với Window Function (Query MA5, MA20)**: Các Table dạng Row (TiKV, InnoDB) phải thực hiện một thao tác cực kỳ tốn Resource trên RAM đó là tải toàn bộ các Row (các cột Data thừa thải không cần thiết nằm chung 1 Row) từ Disk lên Memory. Điều này khiến `Latency` tăng mạnh khi bảng Data đạt 1 - 2 Triệu Records.
- **Bài học rút ra**: Auto Mode của TiDB là tính năng *Cost-Based Optimizer (CBO)* rất thông minh. Nó tự xác định xem Query này nên được gửi xuống TiKV (nếu đọc ít dòng) hay TiFlash (nếu lấy Group By, Sum, Avg trên tệp tin hàng triệu phần tử).
