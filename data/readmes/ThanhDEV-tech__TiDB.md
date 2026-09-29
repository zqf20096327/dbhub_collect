# Hệ Thống Triển Khai TiDB HA Cluster Với Ansible

Tài liệu này hướng dẫn triển khai, cấu hình, kiểm tra, sao lưu và phục hồi cho cụm TiDB HA Cluster sử dụng Ansible và TiUP.

Hạ tầng AWS EC2 được chuẩn bị sẵn. Project tập trung vào việc tự động hóa quá trình triển khai, quản lý và vận hành TiDB Cluster bằng Ansible.

---

## Kiến Trúc Hệ Thống

Hệ thống được triển khai trên AWS EC2 với mô hình phân tán gồm các nhóm máy chủ sau:

1. **Control Node (1 Node)**
   - Chạy Ansible.
   - Cài đặt TiUP.
   - Sinh file `topology.yaml`.
   - Triển khai và quản lý TiDB Cluster.
   - Thực hiện Backup và Restore.
   - Cấu hình NFS Shared Storage.

2. **PD Cluster (3 Nodes)**
   - Quản lý metadata của toàn bộ cluster.
   - Thực hiện Leader Election.
   - Điều phối TiKV và TiDB.

3. **TiDB Server (3 Nodes)**
   - Tiếp nhận kết nối từ ứng dụng.
   - Xử lý câu lệnh SQL.
   - Phân phối truy vấn xuống TiKV.

4. **TiKV Cluster (3 Nodes)**
   - Lưu trữ dữ liệu phân tán.
   - Sao chép dữ liệu theo cơ chế Raft.

5. **TiCDC Cluster (3 Nodes)**
   - Đồng bộ dữ liệu theo thời gian thực.
   - Hỗ trợ Change Data Capture.

6. **TiProxy (2 Nodes)**
   - Điểm truy cập duy nhất cho Client.
   - Cân bằng kết nối tới các TiDB Server.

Tổng số máy chủ triển khai: **15 EC2 Instances**

---

## Cấu Trúc Thư Mục Dự Án

```text
TiDB/
│
├── ansible/
│   ├── ansible.cfg
│   │
│   ├── inventory/
│   │   ├── hosts.ini.example
│   │   └── group_vars/
│   │       ├── all.yml
│   │       ├── vault.yml
│   │       ├── control.yml
│   │       ├── pd.yml
│   │       ├── tidb_server.yml
│   │       ├── tikv.yml
│   │       ├── ticdc.yml
│   │       └── tiproxy.yml
│   │
│   ├── playbooks/
│   │   ├── install.yml
│   │   ├── nfs.yml
│   │   ├── backup.yml
│   │   └── restore.yml
│   │
│   └── roles/
│       ├── os_baseline/
│       ├── tiup_deploy/
│       ├── verify/
│       ├── nfs/
│       ├── backup/
│       └── restore/
│
├── README.md
└── .gitignore
```

---

## Các Tham Số Cấu Hình Chính

### 1. Cấu hình chung (`inventory/group_vars/all.yml`)

- `tidb_version`: `8.5.5`
- `tidb_cluster_name`: `tidb-prod`
- `deploy_user`: `tidb`
- `deploy_dir`: `/data/tidb-deploy`
- `data_dir`: `/data/tidb-data`
- `log_dir`: `/data/tidb-logs`
- `backup_base_dir`: `/data/tidb-backup`

### 2. Cấu hình theo từng nhóm máy chủ

- `control.yml`: Prometheus, Grafana, Alertmanager.
- `pd.yml`: Cấu hình PD.
- `tidb_server.yml`: Cấu hình TiDB Server.
- `tikv.yml`: Cấu hình TiKV và ổ đĩa dữ liệu.
- `ticdc.yml`: Cấu hình TiCDC.
- `tiproxy.yml`: Cấu hình TiProxy.

### 3. Biến bảo mật

Các thông tin nhạy cảm như mật khẩu root của TiDB được mã hóa bằng **Ansible Vault**.

Ví dụ:

```text
inventory/group_vars/vault.yml
```

---

## Điều Kiện Tiên Quyết

1. Đã chuẩn bị các EC2 Instance.
2. Các máy chủ có thể SSH với nhau bằng Private IP.
3. Đã cài đặt Ansible trên Control Node.
4. Đã copy SSH Private Key lên Control Node.
5. Đã cập nhật đúng IP vào file `hosts.ini`.

---

## Chuẩn Bị Inventory

```bash
cd ansible

cp inventory/hosts.ini.example inventory/hosts.ini
```

Sau đó cập nhật Private IP của các máy chủ vào `hosts.ini`.

---

## Copy SSH Private Key

Private Key không được đưa lên Git.

```bash
scp -i your-key.pem your-key.pem \
ubuntu@<CONTROL_PUBLIC_IP>:~/.ssh/id_ed25519
```

---

## Triển Khai TiDB Cluster

```bash
ansible-playbook playbooks/install.yml
```

Playbook sẽ thực hiện:

- Chuẩn hóa hệ điều hành.
- Tạo User triển khai.
- Cấu hình System Limits.
- Disable Swap.
- Disable Transparent Huge Pages.
- Cài đặt TiUP.
- Sinh file topology.yaml.
- Kiểm tra Cluster.
- Deploy TiDB Cluster.
- Khởi động Cluster.
- Kiểm tra trạng thái Cluster.

---

## Kiểm Tra Cluster

Hiển thị trạng thái Cluster:

```bash
tiup cluster display tidb-prod
```

Kết nối TiDB thông qua TiProxy:

```bash
mysql -h <TIPROXY_IP> -P 6000 -u root -p
```

Ví dụ kiểm tra dữ liệu:

```sql
CREATE DATABASE lab_test;

USE lab_test;

CREATE TABLE users(
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO users VALUES (1,'Thanh');

SELECT * FROM users;
```

---

## Cấu Hình NFS Shared Storage

Project sử dụng **NFS Shared Storage** để phục vụ Backup và Restore.

### Vì Sao Sử Dụng NFS

TiDB BR thực hiện Backup trực tiếp từ các TiKV Node.

Nếu sử dụng Local Storage, mỗi TiKV sẽ ghi dữ liệu vào ổ đĩa cục bộ của chính nó. Khi đó Control Node không thể truy cập đầy đủ dữ liệu Backup.

Để giải quyết vấn đề này, Control Node được cấu hình làm **NFS Server** và export thư mục:

```text
/data/tidb-backup
```

Các TiKV Node mount cùng thư mục này về:

```text
/data/tidb-backup
```

Nhờ đó tất cả TiKV Node và Control Node cùng sử dụng chung một vùng lưu trữ, đáp ứng yêu cầu của TiDB BR khi thực hiện Backup và Restore.

---

## Thiết Lập NFS

```bash
ansible-playbook playbooks/nfs.yml
```

Playbook sẽ thực hiện:

- Cài đặt NFS Server trên Control Node.
- Export thư mục Backup.
- Cài đặt NFS Client trên các TiKV Node.
- Mount Shared Storage.
- Kiểm tra trạng thái Mount.

---

## Backup

Project sử dụng **TiDB BR** để sao lưu dữ liệu.

```bash
ansible-playbook playbooks/backup.yml
```

Dữ liệu Backup sẽ được lưu tại:

```text
/data/tidb-backup/<backup_version>
```

Phiên bản Backup mới nhất được lưu tại:

```text
/home/ubuntu/tidb-deploy/latest_backup_version
```

---

## Restore

Khôi phục dữ liệu từ bản Backup:

```bash
ansible-playbook playbooks/restore.yml \
-e backup_version=<backup_version>
```

Ví dụ:

```bash
ansible-playbook playbooks/restore.yml \
-e backup_version=20260706-142206
```

---

## High Availability Test

Đã kiểm tra thành công các tình huống sau:

### TC01 - Mất 1 TiKV Node

- Dừng một TiKV Node.
- Cluster vẫn đọc và ghi dữ liệu bình thường.
- Sau khi khởi động lại, TiKV tự động tham gia lại Cluster.

### TC02 - Mất PD Leader

- Dừng PD Leader.
- PD tự động bầu Leader mới.
- Cluster vẫn hoạt động bình thường.

### TC03 - Mất 1 TiDB Server

- Dừng một TiDB Server.
- TiProxy tự động chuyển kết nối sang TiDB còn lại.
- Ứng dụng không bị gián đoạn.

### TC04 - Mất 1 TiProxy

- Dừng một TiProxy.
- Client kết nối thông qua TiProxy còn lại.
- SQL vẫn thực hiện bình thường.

### TC05 - Mất 1 TiCDC

- Dừng một TiCDC Node.
- Cluster vẫn xử lý SQL bình thường.

### TC06 - Ghi Dữ Liệu Khi Mất TiKV

- Thực hiện ghi dữ liệu liên tục.
- Dừng một TiKV trong quá trình ghi.
- Toàn bộ dữ liệu vẫn được ghi thành công.

---

## Kết Quả

Đã triển khai và kiểm tra thành công các chức năng sau:

- Triển khai TiDB HA Cluster bằng Ansible và TiUP.
- Kiểm tra trạng thái Cluster.
- Kết nối SQL thông qua TiProxy.
- Cấu hình NFS Shared Storage.
- Backup dữ liệu bằng TiDB BR.
- Restore dữ liệu từ bản Backup.
- Kiểm tra khả năng chịu lỗi của Cluster:
  - Mất 1 TiKV Node.
  - Mất PD Leader.
  - Mất 1 TiDB Server.
  - Mất 1 TiProxy.
  - Mất 1 TiCDC.
  - Ghi dữ liệu liên tục khi mất TiKV.