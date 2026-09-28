# ZStyle Shop - Cửa hàng Thương mại Điện tử về Thời trang Áo

<p align="center">
  <img src="screenshot/logo_zstyle_resized.png" alt="ZStyle Shop Logo" height="50px"/> <!-- Cập nhật đường dẫn logo của bạn tại đây -->
</p>

Chào mừng bạn đến với ZStyle Shop, một nền tảng thương mại điện tử được xây dựng để mang đến những sản phẩm áo thun và thời trang chất lượng cho mọi người. Dự án này là một ứng dụng web full-stack được xây dựng bằng PHP, được thiết kế để sử dụng với XAMPP, và có đầy đủ các chức năng cho cả khách hàng và quản trị viên.

README này có sẵn bằng tiếng Anh và tiếng Việt. Vui lòng mở rộng phần ngôn ngữ bạn muốn xem.

**Project Link:** [https://github.com/TranHuuDat2004/zstyle](https://github.com/TranHuuDat2004/zstyle) <!-- Cập nhật link repo của bạn tại đây -->

---

<details>
<summary><strong>English Version (Click to Expand)</strong></summary>

## 🌟 Project Overview

ZStyle Shop is designed to provide a seamless and modern online shopping experience for fashion enthusiasts. From browsing a curated collection of apparel to a secure checkout process and order tracking, ZStyle Shop aims to be a go-to destination for quality clothing. The platform also includes a robust administration system for efficient business management.


## ✨ Key Features

### For Customers:
*   **Intuitive Product Browsing:** Homepage featuring new arrivals and featured items, product categories, and advanced search functionality.
*   **Detailed Product Pages:** High-quality product images, detailed descriptions, size and color options, and customer reviews.
*   **Shopping Cart:** A clear and simple cart for adding items, updating quantities, and applying discount vouchers.
*   **Secure Checkout Process:** A multi-step, easy-to-follow checkout process for entering shipping information and completing the order.
*   **User Accounts:** Easy registration and login, personal profile management, and access to order history.
*   **Engagement & Information:** A news/blog section for updates, an "About Us" page, a contact form, and company policy information.

### 🛍️ Customer Interface (Screenshots)


|                 Home Page                 |                  Product Page                  |                Product Detail Page                |
| :---------------------------------------: | :--------------------------------------------: | :-----------------------------------------------: |
| ![Home Page](screenshot/home.png)         | ![Product Page](screenshot/product.png)        | ![Product Detail](screenshot/product-detail.png)  |
|              **Shopping Cart**              |               **Checkout Process**               |                  **Order History**                  |
| ![Shopping Cart](screenshot/cart.png)     | ![Checkout](screenshot/checkout.png)           | ![Order History](screenshot/history.png)          |
|                **Login Page**                 |              **Registration Page**               |                  **User Profile**                   |
| ![Login Page](screenshot/login.png)       | ![Sign-up Page](screenshot/sign-up.png)        | ![Profile Page](screenshot/profile.png)           |
|                 **News Page**                 |                 **About Us Page**                |                  **Contact Page**                   |
| ![News Page](screenshot/news.png)         | ![About Page](screenshot/about.png)            | ![Contact Page](screenshot/contact.png)           |

### For Administrators (Admin Dashboard):
*   **Dashboard Overview:** Key statistics on revenue, orders, and users at a glance.
*   **Product Management:** Easily add, view, edit, and delete clothing products and manage their images.
*   **Order Management:** View and manage all customer orders.
*   **User Management:** View and manage registered customer accounts.
*   **Voucher Management:** Create and manage promotional discount codes.
*   **Content Management:** Manage news articles and user comments.

### ⚙️ Admin Interface (Screenshots)


|               Admin Dashboard                |                   Manage Products                    |                     Manage Orders                     |
| :------------------------------------------: | :--------------------------------------------------: | :---------------------------------------------------: |
| ![Admin Dashboard](screenshot/admin-dashboard.png) | ![Manage Products](screenshot/manager-product.png) | ![Manage Orders](screenshot/manager-order.png)        |
|                  **Manage Users**                  |                 **Manage Vouchers**                  |                  **Manage Comments**                  |
| ![Manage Users](screenshot/manager-user.png)   | ![Manage Vouchers](screenshot/manager-voucher.png) | ![Manage Comments](screenshot/manager-comment.png)    |

## 🛠️ Technology Stack

*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
*   **Backend:** PHP (Procedural or with a custom structure)
*   **Database:** MySQL (Managed via phpMyAdmin in XAMPP)
*   **Web Server:** Apache (via XAMPP)

## 🚀 Getting Started

### Prerequisites

*   **XAMPP:** Installed and running (Apache, PHP, MySQL).
*   **Git:** For cloning the repository.

### Installation & Setup

1.  **Start XAMPP:** Ensure Apache and MySQL services are running from the XAMPP Control Panel.
2.  **Clone Repository into `htdocs`:**
    *   Navigate to your XAMPP `htdocs` directory (e.g., `C:\xampp\htdocs`).
    *   Run: `git clone https://github.com/TranHuuDat2004/zstyle.git`
    *   This will create a folder (e.g., `C:\xampp\htdocs\zstyle`).

3.  **Database Setup:**
    *   Go to `http://localhost/phpmyadmin` in your web browser.
    *   Create a new database. It's recommended to use a name like `Zstyle` (with collation `utf8mb4_general_ci`).
    *   Select the newly created database, go to the "Import" tab, choose your project's `.sql` file (e.g., `Zstyle.sql`), and click "Go" to import the structure and data.


5.  **Accessing the Application:**
    *   **Customer Site:** `http://localhost/zstyle/`

## 📝 License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/). You are free to Share and Adapt the material, under the terms of Attribution and NonCommercial use.
[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

## 👤 Contributors

*   **Team Engineering**
    *   **Phan Trung Trực** - Team Leader | Project Visionary & Lead Ideator
    *   **Trần Hữu Đạt** - Full-Stack Web Developer - [@TranHuuDat2004](https://github.com/TranHuuDat2004)
    *   **Lê Nguyễn Minh Kha** - Member
    *   **Dương Thị Thùy Linh** - Member

</details>

---

<details>
<summary><strong>Phiên bản Tiếng Việt (Nhấn để Mở rộng)</strong></summary>

## 🌟 Tổng quan Dự án

ZStyle Shop được thiết kế để cung cấp trải nghiệm mua sắm trực tuyến liền mạch và hiện đại cho những người yêu thích thời trang. Từ việc duyệt qua bộ sưu tập áo quần được tuyển chọn kỹ lưỡng đến quy trình thanh toán an toàn và theo dõi đơn hàng, ZStyle Shop đặt mục tiêu trở thành điểm đến tin cậy cho các sản phẩm thời trang chất lượng. Nền tảng này cũng bao gồm một hệ thống quản trị mạnh mẽ để quản lý kinh doanh hiệu quả.



## ✨ Các Tính năng Chính

### Dành cho Khách hàng:
*   **Duyệt Sản phẩm Trực quan:** Trang chủ hiển thị các sản phẩm mới và nổi bật, danh mục sản phẩm và chức năng tìm kiếm nâng cao.
*   **Trang Chi tiết Sản phẩm:** Hình ảnh sản phẩm chất lượng cao, mô tả chi tiết, tùy chọn kích cỡ và màu sắc, cùng với đánh giá của khách hàng.
*   **Giỏ hàng:** Giỏ hàng đơn giản, rõ ràng để thêm sản phẩm, cập nhật số lượng và áp dụng mã giảm giá.
*   **Quy trình Thanh toán An toàn:** Quy trình thanh toán gồm nhiều bước, dễ thực hiện để nhập thông tin vận chuyển và hoàn tất đơn hàng.
*   **Tài khoản Người dùng:** Đăng ký và đăng nhập dễ dàng, quản lý hồ sơ cá nhân và truy cập lịch sử đơn hàng.
*   **Tương tác & Thông tin:** Mục tin tức/blog để cập nhật thông tin, trang "Giới thiệu", biểu mẫu liên hệ và thông tin chính sách của công ty.

### 🛍️ Giao diện Khách hàng (Ảnh chụp màn hình)


|                 Trang Chủ                 |                Trang Sản Phẩm                 |              Trang Chi Tiết Sản Phẩm              |
| :---------------------------------------: | :-------------------------------------------: | :-----------------------------------------------: |
| ![Trang Chủ](screenshot/home.png)         | ![Trang Sản Phẩm](screenshot/product.png)     | ![Chi Tiết SP](screenshot/product-detail.png)     |
|                **Giỏ hàng**                 |            **Quy trình Thanh toán**             |                **Lịch sử Đơn hàng**                 |
| ![Giỏ hàng](screenshot/cart.png)          | ![Thanh toán](screenshot/checkout.png)        | ![Lịch sử Đơn hàng](screenshot/history.png)       |
|              **Trang Đăng nhập**              |                **Trang Đăng ký**                |                **Hồ sơ Người dùng**                 |
| ![Trang Đăng nhập](screenshot/login.png)   | ![Trang Đăng ký](screenshot/sign-up.png)      | ![Trang Hồ sơ](screenshot/profile.png)            |
|               **Trang Tin tức**               |               **Trang Giới thiệu**               |                 **Trang Liên hệ**                   |
| ![Trang Tin tức](screenshot/news.png)      | ![Trang Giới thiệu](screenshot/about.png)    | ![Trang Liên hệ](screenshot/contact.png)          |

### Dành cho Quản trị viên (Bảng điều khiển Admin):
*   **Tổng quan Dashboard:** Thống kê nhanh các chỉ số quan trọng về doanh thu, đơn hàng và người dùng.
*   **Quản lý Sản phẩm:** Dễ dàng thêm, xem, sửa, xóa sản phẩm quần áo và quản lý hình ảnh của chúng.
*   **Quản lý Đơn hàng:** Xem và quản lý tất cả các đơn hàng của khách.
*   **Quản lý Người dùng:** Xem và quản lý tài khoản của khách hàng đã đăng ký.
*   **Quản lý Voucher:** Tạo và quản lý các mã giảm giá khuyến mãi.
*   **Quản lý Nội dung:** Quản lý các bài viết tin tức và bình luận của người dùng.

### ⚙️ Giao diện Quản trị (Ảnh chụp màn hình)


|             Bảng điều khiển Admin             |                 Quản lý Sản phẩm                 |                   Quản lý Đơn hàng                    |
| :------------------------------------------: | :-----------------------------------------------: | :---------------------------------------------------: |
| ![Dashboard Admin](screenshot/admin-dashboard.png) | ![Quản lý SP](screenshot/manager-product.png) | ![Quản lý Đơn hàng](screenshot/manager-order.png)     |
|               **Quản lý Người dùng**               |                 **Quản lý Voucher**                 |                  **Quản lý Bình luận**                  |
| ![Quản lý User](screenshot/manager-user.png)   | ![Quản lý Voucher](screenshot/manager-voucher.png) | ![Quản lý Comment](screenshot/manager-comment.png)    |

## 🛠️ Công nghệ sử dụng

*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
*   **Backend:** PHP (Lập trình thủ tục hoặc theo cấu trúc tùy chỉnh)
*   **Cơ sở dữ liệu:** MySQL (Quản lý qua phpMyAdmin trong XAMPP)
*   **Web Server:** Apache (thông qua XAMPP)

## 🚀 Bắt đầu

### Điều kiện Tiên quyết

*   **XAMPP:** Đã được cài đặt và đang chạy (Apache, PHP, MySQL).
*   **Git:** Để sao chép kho lưu trữ.

### Cài đặt & Thiết lập

1.  **Khởi động XAMPP:** Mở XAMPP Control Panel và đảm bảo các dịch vụ **Apache** và **MySQL** đang chạy.
2.  **Sao chép kho lưu trữ vào `htdocs`:**
    *   Điều hướng đến thư mục `htdocs` của XAMPP (ví dụ: `C:\xampp\htdocs`).
    *   Chạy lệnh: `git clone https://github.com/TranHuuDat2004/zstyle.git`
    *   Lệnh này sẽ tạo một thư mục dự án (ví dụ: `C:\xampp\htdocs\zstyle`).

3.  **Thiết lập Cơ sở dữ liệu:**
    *   Mở trình duyệt và truy cập `http://localhost/phpmyadmin`.
    *   Tạo một cơ sở dữ liệu mới. Khuyến khích đặt tên là `Zstyle` (với đối chiếu là `utf8mb4_general_ci`).
    *   Chọn cơ sở dữ liệu vừa tạo, chuyển đến tab "Import", chọn tệp `.sql` của dự án (ví dụ: `Zstyle.sql`), và nhấn "Go" để nhập cấu trúc và dữ liệu.

4.  **Cấu hình Kết nối Cơ sở dữ liệu (nếu cần):**
    *   Tìm tệp PHP trong dự án của bạn chịu trách nhiệm kết nối cơ sở dữ liệu (ví dụ: `config.php`, `db_connect.php`).
    *   Đảm bảo các thông tin kết nối khớp với cài đặt XAMPP của bạn. Thông tin mặc định thường là:
        *   Host: `localhost`
        *   User: `root`
        *   Password: `(để trống)`
        *   Tên cơ sở dữ liệu: `Zstyle` (hoặc tên bạn đã đặt ở bước trước).

5.  **Truy cập Ứng dụng:**
    *   **Trang Khách hàng:** `http://localhost/zstyle/`


## 📝 Giấy phép

Công trình này được cấp phép theo [Giấy phép Quốc tế Creative Commons Ghi công-Phi thương mại 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Bạn được tự do Chia sẻ và Phỏng theo tài liệu, theo các điều khoản Ghi công và Phi thương mại.
[![Giấy phép: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

## 👤 Thành viên Đóng góp

*   **Nhóm Kỹ thuật**
    *   **Phan Trung Trực** - Trưởng nhóm | Định hướng & Lên ý tưởng chính cho Dự án
    *   **Trần Hữu Đạt** - Lập trình viên Web - [@TranHuuDat2004](https://github.com/TranHuuDat2004)
    *   **Lê Nguyễn Minh Kha** - Thành viên
    *   **Dương Thị Thùy Linh** - Thành viên

</details>