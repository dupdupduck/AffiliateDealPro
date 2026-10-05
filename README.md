# 🔥 AffiliateDealPro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows%20%7C%20macOS-0078D6?style=for-the-badge" alt="Platforms" />
  <img src="https://img.shields.io/badge/Telegram-Bot%20API-24A1DE?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>🤖 Autonomous High-Discount Deal Hunter & Auto-Affiliate Publisher</b><br>
  <i>Tự động săn deal giảm giá sốc trên sàn thương mại, gắn link hoa hồng Affiliate và đăng bài lên Telegram 24/7!</i>
</p>

---

## 🌟 Giới Thiệu (Overview)

**AffiliateDealPro** là công cụ mã nguồn mở giúp bạn xây dựng hệ thống **kiếm tiền thụ động (MMO)** với Tiếp thị liên kết (Affiliate Marketing) hoàn toàn tự động:

- 🔍 **Tự động quét Flash Sale**: Thu thập liên tục các sản phẩm giảm giá khủng (> 30% - 70%), đánh giá cao (⭐ 4.5+), shop uy tín.
- 🔗 **Gắn link Affiliate tự động**: Tự động chuyển đổi link sản phẩm gốc thành link tiếp thị có gắn mã tracking SubID của bạn (Shopee, Lazada,...).
- 📢 **Tự động đăng kênh Telegram**: Soạn tin nhắn với hình ảnh sắc nét, định dạng giá sale, mã voucher và đính kèm **nút bấm MUA NGAY** trực tiếp.
- ⚡ **Chống đăng trùng lặp**: Tích hợp cơ sở dữ liệu SQLite lưu vết, đảm bảo không bao giờ đăng lặp lại 1 deal trong 48 giờ.
- 📱 **Tối ưu cho Termux / Android & Linux**: Chạy nhẹ nhàng 24/7 trên điện thoại cũ hoặc máy chủ VPS siêu rẻ.

---

## 🖥️ Giao Diện Terminal (Preview)

```text
   ___   __  ___ __ _       __       ___             
  / _ | / _/ _/ // /(_)__ _/ /____  / _ \_______    
 / __ |/ _// _/ // // / _ `/ __/ -_) / ___/ __/ _ \   
/_/ |_/_/ /_/ /_//_//_/\_,_/\__/\__/ /_/  /_/  \___/   
   >> Autonomous E-Commerce Deal Hunter & Affiliate Bot <<
         (Shopee / Lazada / Telegram Auto-Publisher)

┌── [ TRẠNG THÁI HỆ THỐNG ] ──────────────────────────────────────────┐
│ 🤖 Telegram Bot:   ĐÃ KẾT NỐI                                      │
│ 📢 Kênh đăng tin:  @kenh_san_deal_hot                               │
│ 🏷️  Affiliate ID:   aff_kiettong                                    │
│ 🎯 Giảm giá tối thiểu: >50%                                         │
├─────────────────────────────────────────────────────────────────────┤
│ 📊 Tổng deal đã quét:     148                                       │
│ ✅ Deal đạt chuẩn (>=50%): 26                                        │
│ 🚀 Đã gửi lên Telegram:   18                                        │
│ ⏱️ Lần quét gần nhất:     14:30:15                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Cài Đặt Nhanh Trong 1 Phút (Quickstart)

### 📲 Chạy trên Termux (Android)
Mở Termux và dán các lệnh sau:

```bash
pkg update -y && pkg install git python -y
git clone https://github.com/dupdupduck/AffiliateDealPro.git
cd AffiliateDealPro
bash install.sh
```

### 💻 Chạy trên Linux / macOS / Windows
```bash
git clone https://github.com/dupdupduck/AffiliateDealPro.git
cd AffiliateDealPro
pip install -r requirements.txt
```

---

## 🛠️ Hướng Dẫn Sử Dụng (Usage)

### 1. Cấu hình Bot & Affiliate (Chỉ mất 2 phút)
Chạy lệnh giao diện thiết lập trực quan:
```bash
python3 main.py --setup
```
Chương trình sẽ hỏi bạn:
1. `Telegram Bot Token`: Lấy miễn phí từ [@BotFather](https://t.me/BotFather).
2. `Telegram Channel ID`: Kênh hoặc nhóm Telegram của bạn (Ví dụ `@kenh_deal` hoặc ID dạng `-100xxxxxxx`).
3. `Affiliate SubID`: Tên định danh tài khoản Affiliate của bạn.
4. `Mức giảm giá tối thiểu (%)`: Mặc định `30` hoặc `50`.

### 2. Kiểm tra dữ liệu deal mẫu (Dry Run)
Chạy thử để xem các deal hot được bóc tách và gắn link affiliate mà chưa gửi đi:
```bash
python3 main.py --test
```

### 3. Gửi 1 tin nhắn test lên Telegram
Kiểm tra xem Bot đã có quyền đăng bài vào kênh chưa:
```bash
python3 main.py --send-test
```

### 4. Bật chế độ săn deal tự động 24/7 (Daemon)
```bash
python3 main.py
```
*(Trên Termux, bạn có thể chạy `termux-wake-lock` để bot duy trì hoạt động ngầm khi tắt màn hình).*

---

## 📖 Hướng Dẫn Chi Tiết Cho Người Mới (Beginner Guide)

<details>
<summary><b>1. Cách tạo Telegram Bot và Kênh nhận tin</b></summary>

1. Mở Telegram, tìm kiếm bot **[@BotFather](https://t.me/BotFather)** và bấm `Start`.
2. Gửi lệnh `/newbot`, sau đó đặt tên và username cho bot (ví dụ: `SanDealVipBot`).
3. Sao chép chuỗi **HTTP API Token** (dạng `7123456789:AAFxxx...`).
4. Tạo một **Kênh (Channel)** hoặc **Nhóm (Group)** mới trên Telegram.
5. Thêm con bot vừa tạo vào kênh với quyền **Administrator (Quản trị viên)** để bot có thể đăng bài.
</details>

<details>
<summary><b>2. Cách lấy link tiếp thị Shopee Affiliate</b></summary>

1. Đăng ký tài khoản tại [Shopee Affiliate Portal](https://affiliate.shopee.vn/).
2. Sau khi được duyệt, lấy mã ID tiếp thị của bạn.
3. Khi người dùng bấm vào nút mua hàng qua bot, hoa hồng sẽ tự động ghi nhận vào tài khoản của bạn!
</details>

---

## ⚙️ Cấu Trúc Dự Án (Project Architecture)

```text
AffiliateDealPro/
├── main.py              # File chạy chính & vòng lặp quét deal
├── deal_hunter.py       # Bộ máy săn Flash Sale & lọc trùng lặp
├── affiliate.py         # Bộ chuyển đổi URL & chèn mã hoa hồng
├── telegram_bot.py      # Module gửi ảnh & nút bấm qua Telegram API
├── tui.py               # Giao diện dòng lệnh Cyberpunk TUI
├── config.py            # Trình quản lý cấu hình
├── config.example.json  # File cấu hình mẫu
├── requirements.txt     # Danh sách thư viện Python
├── install.sh           # Script cài đặt tự động 1-click
└── README.md            # Tài liệu hướng dẫn
```

---

## 🤝 Đóng Góp & Hỗ Trợ (Contributing)

Mọi đóng góp, cải tiến (Pull Request) hoặc báo lỗi (Issue) đều rất được hoan nghênh!
- ⭐️ **Hãy bấm STAR để ủng hộ dự án tiếp tục phát triển thêm các sàn mới (Tiki, TikTok Shop, Amazon)!**

---

## 📄 Bản Quyền (License)

Dự án được phân phối dưới giấy phép **MIT License**. Bạn được toàn quyền sử dụng, chỉnh sửa và triển khai cho mục đích cá nhân hoặc thương mại.
