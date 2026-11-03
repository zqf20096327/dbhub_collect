# PHONE STORE MANAGEMENT SYSTEM

**Hệ thống Quản trị Cơ sở Dữ liệu Quan hệ cho Chuỗi Cửa hàng Điện thoại**

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge&logo=github)](https://github.com/ngockhanh21/store-management-system/releases/tag/v1.0.0)
[![Documentation](https://img.shields.io/badge/Documentation-PDF_Report-red?style=for-the-badge&logo=adobeacrobatreader)](https://github.com/ngockhanh21/store-management-system/releases/tag/v1.0.0)
[![Database](https://img.shields.io/badge/Database-SQL_Server_2022-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/en-us/sql-server)
[![IDE](https://img.shields.io/badge/IDE-SSMS_v22-0078D4?style=for-the-badge&logo=visualstudio)](https://learn.microsoft.com/en-us/sql/ssms/)
[![License](https://img.shields.io/badge/License-Proprietary-green?style=for-the-badge)](./LICENSE.txt)

* **Trường:** Trường Đại học Thủy lợi (TLU)
* **Khoa:** Khoa Công nghệ Thông tin
* **Bộ môn:** Hệ thống Thông tin
* **Môn học:** Cơ sở Dữ liệu
* **Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Quỳnh Châu
* **Lớp:** 67TTNT1

---

##  Mục lục
* [Giới thiệu bài toán](#giới-thiệu-bài-toán)
* [Công nghệ](#công-nghệ)
* [Kiến trúc CSDL](#kiến-trúc-csdl)
* [Quy tắc nghiệp vụ cốt lõi](#quy-tắc-nghiệp-vụ-cốt-lõi)
* [Dạng chuẩn BCNF](#dạng-chuẩn-bcnf)
* [Cấu trúc thư mục](#cấu-trúc-thư-mục)
* [Hướng dẫn cài đặt & Triển khai](#hướng-dẫn-cài-đặt--triển-khai)
* [Đội ngũ thực hiện & Đóng góp](#đội-ngũ-thực-hiện--đóng-góp)
* [Lời cảm ơn](#lời-cảm-ơn)
* [Giấy phép](#giấy-phép)

---

## Giới thiệu bài toán

Trong bối cảnh quy mô của các chuỗi bán lẻ thiết bị di động ngày càng mở rộng, phương thức lưu trữ phân tán bằng sổ sách hoặc bảng tính Excel truyền thống bộc lộ nhiều điểm yếu: tốn thời gian tra cứu, dễ sai lệch tồn kho, khó quản lý lịch sử bảo hành và đối soát dòng tiền.

Hệ thống cơ sở dữ liệu quan hệ này được xây dựng nhằm giải quyết các yêu cầu cốt lõi:
* **Tự động hóa vận hành:** Quản lý tập trung mạng lưới chi nhánh cửa hàng, phân bổ nhân sự và quản lý thông tin khách hàng đa tầng qua chính sách hạng thành viên.
* **Kiểm soát chuỗi cung ứng:** Quản lý toàn diện quy trình nhập kho từ nhà cung cấp và hóa đơn xuất bán thực tế cho khách hàng.
* **Theo dõi dịch vụ sau bán hàng:** Ghi nhận vòng đời bảo hành, tình trạng lỗi thiết bị, nội dung sửa chữa và tiến độ xử lý của kỹ thuật viên.
* **Hỗ trợ ra quyết định:** Cung cấp nguồn dữ liệu chuẩn xác phục vụ báo cáo doanh thu, phân tích mặt hàng bán chạy và hiệu suất kinh doanh.

---

## Công nghệ

| Phân hệ | Công nghệ / Công cụ | Phiên bản / Chi tiết sử dụng |
| :--- | :--- | :--- |
| **Database Engine** | Microsoft SQL Server | T-SQL, Primary/Foreign Keys, Check Constraints |
| **Development IDE** | SQL Server Management Studio | SSMS 22 (Quản lý Solution `.slnx` & Projects) |
| **Modeling & Design** | StarUML | Thiết kế sơ đồ thực thể liên kết (ERD) & file `.mdj` |
| **VCS & Collaboration**| Git & GitHub | Git Flow, Feature Branches, PR Merges, Releases |
| **Documentation** | Microsoft Word / PDF / Markdown | Báo cáo đồ án chi tiết & Thuyết minh kỹ thuật |

---

## Kiến trúc CSDL

### Sơ đồ thực thể liên kết (ERD)

![ERD Architecture](./ER_Entity.png)

Hệ thống bao gồm **11 quan hệ** (tables) được tổ chức theo cấu trúc chuẩn:
* **Thực thể quản trị:** `CuaHang`, `NhanVien`, `KhachHang`, `NhaCungCap`, `SanPham`.
* **Thực thể giao dịch:** `HoaDonNhap`, `HoaDonXuat`.
* **Thực thể kết hợp (N:N):** `ChiTietHDNhap`, `ChiTietHDXuat`.
* **Thực thể kỹ thuật:** `BaoHanh`, `LichSuBaoHanh`.

---

## Quy tắc nghiệp vụ cốt lõi

* **Cửa hàng & Nhân sự:** Mỗi cửa hàng có nhiều nhân viên trực thuộc nhưng chỉ do duy nhất 1 nhân viên quản lý (`MaNVQL`). Mỗi nhân viên thuộc biên chế của một cửa hàng cụ thể.
* **Cung ứng & Kho hàng:** Hóa đơn nhập được tạo từ một nhà cung cấp xác định và quản lý bởi một nhân viên phụ trách. Một hóa đơn nhập ghi nhận nhiều sản phẩm với số lượng nhập chi tiết.
* **Khách hàng & Bán hàng:** Khách hàng được phân hạng thành viên (`Kim Cương`, `Bạch Kim`, `Vàng`, `Bạc`, `Đồng`) để áp dụng chiết khấu. Mỗi hóa đơn xuất ghi nhận khách hàng mua và nhân viên phụ trách giao dịch.
* **Bảo hành khép kín:** Phiếu bảo hành sinh ra phụ thuộc vào hóa đơn xuất thực tế. Mỗi sản phẩm trong thời hạn bảo hành có thể phát sinh nhiều lần sửa chữa (`LichSuBaoHanh`), ghi nhận đầy đủ ngày nhận, tình trạng lỗi, nội dung kỹ thuật xử lý và nhân viên phụ trách.

---

## Dạng chuẩn BCNF

Toàn bộ 11 bảng trong hệ thống đều thỏa mãn **Dạng chuẩn Boyce-Codd (BCNF)**: Mọi phụ thuộc hàm không tầm thường X &rarr; Y đều có vế trái X là một siêu khóa.

| STT | Tên quan hệ | Khóa chính (PK) | Tập phụ thuộc hàm | Đánh giá |
| :-: | :--- | :--- | :--- | :-: |
| 1 | `KhachHang` | `SDTK` | SDTK &rarr; TenKhach, NgaySinh, GioiTinh, HangThanhVien | **BCNF** |
| 2 | `NhanVien` | `MaNV` | MaNV &rarr; TenNV, NgaySinh, DiaChi, GioiTinh, SDTNV, Luong, MaCH | **BCNF** |
| 3 | `CuaHang` | `MaCH` | MaCH &rarr; TenCH, DiaChi, SDT, MaNVQL | **BCNF** |
| 4 | `NhaCungCap` | `MaNhaCC` | MaNhaCC &rarr; TenNhaCC, SDT, DiaChi | **BCNF** |
| 5 | `SanPham` | `MaSP` | MaSP &rarr; TenSP, SoLuongTon, LoaiSP, MoTa, GiaSP | **BCNF** |
| 6 | `HoaDonNhap` | `MaHDNhap` | MaHDNhap &rarr; NgayNhap, MaNhaCC, MaNVQL | **BCNF** |
| 7 | `ChiTietHDNhap` | `(MaHDNhap, MaSP)` | (MaHDNhap, MaSP) &rarr; SoLuong | **BCNF** |
| 8 | `HoaDonXuat` | `MaHDXuat` | MaHDXuat &rarr; NgayXuat, SDTK, MaNV | **BCNF** |
| 9 | `ChiTietHDXuat` | `(MaHDXuat, MaSP)` | (MaHDXuat, MaSP) &rarr; SoLuong | **BCNF** |
| 10 | `BaoHanh` | `MaBH` | MaBH &rarr; MaHDXuat, MaSP, NgayBatDau, NgayKetThuc, TrangThai, ThoiHanBaoHanh | **BCNF** |
| 11 | `LichSuBaoHanh` | `MaLSBH` | MaLSBH &rarr; MaBH, NgayTiepNhan, TinhTrangBanDau, NoiDungSuaChua, NgayHoanThanh, TrangThai, MaNVBH | **BCNF** |

---

## Cấu trúc thư mục

```text
store-management-system/
├── KhoiTaoCSDL/                      # Cấp độ 1: Khởi tạo kiến trúc và dữ liệu
│   ├── CreateDatabase.sql            # Tạo cơ sở dữ liệu và cấu hình ban đầu
│   ├── CreateTable.sql               # DDL: Định nghĩa 11 bảng, Khóa chính, Khóa ngoại
│   └── AddData.sql                   # DML: Bộ dữ liệu mẫu kiểm thử thực tế
├── TruyVanCaNhan/                    # Cấp độ 2: Module truy vấn nghiệp vụ của từng thành viên
│   ├── BuiNgocKhanh.sql              # Module truy vấn phân tích nghiệp vụ
│   ├── DangQuanTri.sql               # Module truy vấn phân tích nghiệp vụ
│   ├── NguyenDangThanhNam.sql        # Module truy vấn phân tích nghiệp vụ
│   ├── NguyenDucHuy.sql              # Module truy vấn phân tích nghiệp vụ
│   └── TruongHongNhatKhanh.sql       # Module truy vấn phân tích nghiệp vụ
├── ER_Entity.png                     # Ảnh sơ đồ quan hệ thực thể (ERD) trực quan
├── ER_Entity.mdj                     # File thiết kế kiến trúc gốc trên StarUML
├── QuanLiCuaHang.slnx                # SSMS Solution File
├── QuanLiCuaHang.ssmssqlproj         # SSMS Project File
└── README.md                         # Tài liệu thuyết minh dự án
```

---

## Hướng dẫn cài đặt & Triển khai

### Yêu cầu môi trường
* **Hệ quản trị CSDL:** Microsoft SQL Server 2019/2022 hoặc SQL Server Express.
* **Công cụ quản trị:** SQL Server Management Studio (SSMS) hoặc các công cụ tương đương
* **Công cụ dòng lệnh:** Git CLI.

### Quy trình triển khai hệ thống

1. **Sao chép kho mã nguồn về máy tính:**
   ```bash
   git clone https://github.com/ngockhanh21/store-management-system.git
   cd store-management-system
   ```

2. **Khởi tạo Database & Cấu hình:**
   * Khởi động SSMS và kết nối vào SQL Server Instance cục bộ.
   * Mở tệp `KhoiTaoCSDL/CreateDatabase.sql`.
   * Nhấn **Execute (F5)** để khởi tạo CSDL `CUAHANG_DT`.

3. **Thiết lập lược đồ quan hệ:**
   * Mở tệp `KhoiTaoCSDL/CreateTable.sql`.
   * Nhấn **Execute (F5)** để tạo toàn bộ 11 bảng.

4. **Nạp bộ dữ liệu mẫu kiểm nghiệm (DML):**
   * Mở tệp `KhoiTaoCSDL/AddData.sql`.
   * Nhấn **Execute (F5)** để nạp dữ liệu danh mục hàng hóa, nhân viên, hóa đơn và bảo hành.

5. **Thực thi phân tích nghiệp vụ:**
   * Truy cập thư mục `TruyVanCaNhan/` và mở file `.sql` tương ứng của từng thành viên để chạy thử các kịch bản báo cáo.

>  Thực thi theo thứ tự lần lượt để không vi phạm ràng buộc khóa ngoại giữa các bảng.

---


## Đội ngũ thực hiện & Đóng góp

Dự án được hoàn thành bởi nhóm sinh viên **Lớp 67TTNT1 - Khoa Công nghệ Thông tin - Trường Đại học Thủy lợi**:

| STT | Họ và tên | Vai trò | GitHub Account |
| :-: | :--- | :--- | :--- |
| **1** | **Bùi Ngọc Khánh** | **Team Leader** | [@ngockhanh21](https://github.com/ngockhanh21) |
| **2** | **Đặng Quang Trí** | Member | [@Tribo288](https://github.com/Tribo288) |
| **3** | **Nguyễn Đăng Thành Nam** | Member | [@AlibabaAhahahahaha](https://github.com/AlibabaAhahahahaha) |
| **4** | **Nguyễn Đức Huy** | Member | [@HotaruYuriw](https://github.com/HotaruYuriw) |
| **5** | **Trương Hồng Nhật Khánh** | Member | [@khanh](https://github.com/khanh-dtr) |

---

## Lời cảm ơn

* **Giảng viên hướng dẫn:** Nhóm xin trân trọng gửi lời cảm ơn sâu sắc đến **ThS. Nguyễn Ngọc Quỳnh Châu** đã tận tình giảng dạy, định hướng mô hình hóa dữ liệu và phản biện chuyên môn trong suốt quá trình thực hiện project.
* **Tài liệu đồ án chi tiết:** Toàn văn thuyết minh đồ án và kịch bản truy vấn: [Bản phát hành v1.0.0 (Release Assets)](https://github.com/ngockhanh21/store-management-system/releases/tag/v1.0.0).

---

## Giấy phép

**Bản quyền © 2026 thuộc về Bùi Ngọc Khánh và các cộng sự. Bảo lưu mọi quyền (All rights reserved).**

Xem đầy đủ điều khoản tại [License](./LICENSE.txt). <br>
Được phép đọc mã nguồn để tham khảo cá nhân/học tập; **không được** sao chép, phát hành lại, hay dùng cho mục đích thương mại nếu chưa có sự cho phép bằng văn bản từ tác giả.
