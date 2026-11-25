# Corelens

**Tiếng Việt** · [English](README.en.md)

[![Giấy phép: MIT và AGPL-3.0](https://img.shields.io/badge/Gi%E1%BA%A5y%20ph%C3%A9p-MIT%20%2B%20AGPL--3.0-blue.svg)](LICENSES.md)
[![Bản phát hành mới nhất](https://img.shields.io/github/v/release/AlaVox-lab/corelens)](https://github.com/AlaVox-lab/corelens/releases)
[![Tích hợp liên tục trên pull request](https://github.com/AlaVox-lab/corelens/actions/workflows/ci.yml/badge.svg?event=pull_request)](https://github.com/AlaVox-lab/corelens/actions/workflows/ci.yml)
[![Trang tài liệu](https://github.com/AlaVox-lab/corelens/actions/workflows/trang-tai-lieu.yml/badge.svg?branch=main)](https://alavox-lab.github.io/corelens/)

Corelens là cổng vận hành yêu cầu nội bộ nguồn mở cho doanh nghiệp. Báo máy hỏng, xin cấp phần mềm, xin
giấy xác nhận, đề xuất mua sắm đều gửi về một chỗ, đi theo một quy trình khai trong dữ liệu chứ không viết
cứng trong mã. Bên dưới cổng là một nền tảng lõi chỉ có API (`/core/v1`) để ứng dụng khác dùng lại.

Tài liệu: **https://alavox-lab.github.io/corelens/** · Dự án dự thi Phần mềm nguồn mở, Olympic Tin học
Sinh viên Việt Nam 2026.

![Trang chủ của điều phối viên: việc cần làm ngay, xếp theo độ gấp](docs-site/src/assets/anh/trang-chu-dieu-phoi.png)

## Corelens làm gì

- **Điều phối từng hồ sơ.** Điều phối viên phân loại, đặt mức ưu tiên và chọn phòng; phòng nhận sai
  chuyên môn thì trả lại kèm lý do.
- **Quy trình là dữ liệu.** Trạng thái, bước đi, vai trò, ràng buộc chống sai và mọi con số nằm trong
  bảng; đổi quy trình là sửa dữ liệu, không sửa mã.
- **Hạn tính theo giờ làm việc.** Hạn đếm theo lịch làm việc và ngày lễ, nhân hệ số theo mức ưu tiên;
  quá hạn thì tự leo thang.
- **Nhật ký sự kiện và khai phá quy trình.** Mỗi lần chuyển trạng thái ghi một dòng chỉ ghi thêm; từ đó hệ
  thống dựng lại quy trình đang chạy thật và chỉ ra điểm nghẽn.
- **AI chỉ gợi ý.** Mô hình ngôn ngữ cục bộ (tùy chọn) gợi ý loại, mức ưu tiên, phòng; người bấm xác nhận
  mới thành quyết định.
- **Nền tảng lõi `/core/v1`.** Ứng dụng khác gọi qua cổng API bằng tài khoản dịch vụ — ví dụ chạy được ở
  [`examples/goi-loi/`](examples/goi-loi/).

Lõi lắp ghép Keycloak, Apache APISIX, PostgreSQL, SeaweedFS và Apache Superset quanh một engine quy trình
nhóm tự viết: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Đáp ứng từng yêu cầu của đề thi:
[`docs/doi-chieu-de-thi.md`](docs/doi-chieu-de-thi.md).

## Chạy thử

Cần Git và Docker kèm Compose v2 (Docker Desktop, hoặc Docker Engine 24 trở lên).

```bash
git clone https://github.com/AlaVox-lab/corelens.git
cd corelens/infra
cp .env.example .env
docker compose --env-file .env up -d --build
```

Trên PowerShell thay `cp` bằng `Copy-Item`. Lần dựng đầu mất khoảng 10–20 phút.

Mở `http://localhost:3000`, bấm **Đăng nhập bằng tài khoản công ty**, đăng nhập `binh.tran` / `matkhau123`
(điều phối viên). Tài khoản của các vai khác:
[Tài khoản mẫu](https://alavox-lab.github.io/corelens/huong-dan/tai-khoan-mau/).

Đây là cụm trình diễn: mật khẩu và tài khoản mẫu đều công khai. Cài từ tệp nén của bản phát hành, yêu cầu
máy, các dịch vụ tùy chọn và việc cần làm trước khi dùng thật:
[Cài đặt](https://alavox-lab.github.io/corelens/cai-dat/cai-dat/).

## Tài liệu

| Trang | Nội dung |
|---|---|
| [Bắt đầu nhanh](https://alavox-lab.github.io/corelens/bat-dau/bat-dau-nhanh/) | Dựng cụm và đi trọn một hồ sơ qua bốn vai |
| [Cài đặt và vận hành](https://alavox-lab.github.io/corelens/cai-dat/cai-dat/) | Yêu cầu máy, cấu hình, mô hình ngôn ngữ, thư, kho tri thức, nâng cấp, sao lưu |
| [Hướng dẫn sử dụng](https://alavox-lab.github.io/corelens/huong-dan/nguoi-gui/) | Người gửi, điều phối viên, trưởng phòng, người xử lý |
| [API của nền tảng lõi](https://alavox-lab.github.io/corelens/tham-khao/api/) | `/core/v1`, token của tài khoản dịch vụ, quy trình dạng BPMN, gọi lặp an toàn |
| [Kiến trúc](https://alavox-lab.github.io/corelens/phat-trien/kien-truc/) | Các dịch vụ trong cụm, engine quy trình, nhật ký sự kiện |

Mã nguồn trang tài liệu ở [`docs-site/`](docs-site/). Tài liệu kỹ thuật đi cùng mã ở [`docs/`](docs/): trạng
thái dự án, quyết định kiến trúc ([`docs/adr/`](docs/adr/)), luồng nghiệp vụ, phụ thuộc và giấy phép.
Thay đổi theo từng bản: [`CHANGELOG.md`](CHANGELOG.md).

## Đóng góp

Đọc [`CONTRIBUTING.md`](CONTRIBUTING.md) trước khi gửi thay đổi: mô hình nhánh, Conventional Commits, header
giấy phép SPDX. Báo lỗi và đề xuất ở [Issues](https://github.com/AlaVox-lab/corelens/issues); lỗ hổng bảo mật
báo riêng theo [`SECURITY.md`](SECURITY.md). Tham gia dự án là đồng ý với
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Đội ngũ

| Vai trò | Thành viên | Tài khoản |
|---|---|---|
| Giảng viên hướng dẫn | ThS. Trần Phước Đức | [`@tranphuocduc1998`](https://github.com/tranphuocduc1998) |
| Điều phối kho mã | Nguyễn Thanh Sơn | [`@AlaVox-lab`](https://github.com/AlaVox-lab) |
| Thành viên | Nguyễn Thanh Nguyên | [`@NguyentimAnh`](https://github.com/NguyentimAnh) |

Công việc chia theo từng [issue](https://github.com/AlaVox-lab/corelens/issues), không cố định ai phụ
trách không gian nào.

## Giấy phép

Kho theo mô hình nhiều giấy phép: mã theo [MIT](LICENSE), riêng dịch vụ khai phá quy trình
[`services/khai-pha/`](services/khai-pha/) theo [AGPL-3.0-or-later](services/khai-pha/LICENSE) vì dùng thư
viện PM4Py — phần còn lại chỉ trao đổi với nó qua HTTP. Bảng theo thư mục ở [`LICENSES.md`](LICENSES.md),
thông báo bên thứ ba ở [`NOTICE`](NOTICE).
