# 🎮 Tetris Cyberpunk Edition

> Một phiên bản Tetris hiện đại với giao diện Cyberpunk/Neon, hỗ trợ chế độ PvP, AI đối kháng, nhạc nền và âm thanh đầy đủ.

---

## 📸 Giới thiệu

**Tetris Cyberpunk Edition** là trò chơi Tetris được xây dựng bằng Python và Pygame, lấy cảm hứng từ phong cách **Cyberpunk Neon** với hiệu ứng phát sáng, màu sắc rực rỡ và giao diện động. Game hỗ trợ nhiều chế độ chơi: Solo (40 Lines, Blitz, Custom), PvP (Người vs Người) và PvAI (Người vs AI).

---

## ✨ Tính năng nổi bật

- 🕹️ **Nhiều chế độ chơi**: Solo (40 Lines, Blitz, Custom), PvP 2 người, PvAI
- 🤖 **AI thông minh** với 3 kiểu tính cách: Balanced, Aggressive, Defensive
- 🎨 **Giao diện Cyberpunk Neon** với hiệu ứng glow, particle và animation
- 🎵 **Hệ thống âm thanh 3 kênh**: Master Volume · Music · Sound Effects — mỗi kênh có thanh trượt riêng
- 🎶 **Nhạc nền tự động**: phát `background.mp3` (hoặc WAV/OGG) ngay khi khởi động, dừng/tiếp khi Pause
- ⚙️ **Tuỳ chỉnh sâu**: Level khởi đầu, kích thước lưới, ghost piece, hold piece
- ⌨️ **Phím điều khiển tuỳ biến** cho từng người chơi
- 💾 **Lưu cấu hình tự động** vào `tetris_config.json`
- 📐 **Vật lý NES Tetris** — bảng tốc độ rơi (gravity) chính xác theo từng level
- ⚡ **DAS / ARR** — xử lý giữ phím di chuyển chuyên nghiệp, tốc độ tỉ lệ thuận với level

---

## 🗂️ Cấu trúc dự án

```
Tetris/
├── main.py              # Vòng lặp game chính, xử lý sự kiện và điều hướng màn hình
├── menus.py             # Vẽ tất cả các màn hình menu (Main, Solo, PvP, Config, Pause, Sound...)
├── game_screens.py      # Màn hình gameplay (Solo & PvP), vẽ lưới & HUD
├── tetris_logic.py      # Logic cốt lõi của Tetris (di chuyển, xoay, xóa dòng, garbage...)
├── ai.py                # Trí tuệ nhân tạo (heuristic đánh giá lưới)
├── audio.py             # Hệ thống âm thanh 3 kênh (Master/Music/SFX), sinh file WAV
├── ui.py                # Component UI tái sử dụng (nút neon, slider, font, particle...)
├── settings.py          # Hằng số, màu sắc, config mặc định, key mapping
├── tetris_config.json   # Cấu hình người dùng (tự động tạo & lưu)
├── PressStart2P-Regular.ttf  # Font chữ Pixel game
└── audio_assets/
    ├── music/           # Nhạc nền — đặt background.mp3/wav/ogg vào đây
    └── sfx/             # Hiệu ứng âm thanh (tự sinh nếu thiếu)
```

---

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống

- Python **3.10+**
- `pygame-ce` (Community Edition) **2.5+**

### Cài đặt

```bash
# Clone hoặc tải project về
git clone <repository-url>
cd Tetris

# Tạo môi trường ảo (tuỳ chọn nhưng khuyến khích)
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS

# Cài thư viện
pip install pygame-ce
```

### Chạy game

```bash
python main.py
```

---

## 🕹️ Điều khiển

### Chế độ Solo (mặc định)

| Phím | Hành động |
|------|-----------|
| `←` / `→` | Di chuyển trái / phải |
| `↓` | Rơi nhanh (Soft Drop) |
| `↑` | Xoay khối |
| `Space` | Thả rơi ngay (Hard Drop) |
| `Z` | Giữ khối (Hold) |
| `P` hoặc `Esc` | Tạm dừng / Mở Pause Menu |

### Chế độ PvP — Người chơi 1 (mặc định WASD)

| Phím | Hành động |
|------|-----------|
| `A` / `D` | Di chuyển trái / phải |
| `S` | Soft Drop |
| `W` | Xoay khối |
| `Q` | Hard Drop |
| `C` | Hold |

### Chế độ PvP — Người chơi 2 (mặc định phím mũi tên)

| Phím | Hành động |
|------|-----------|
| `←` / `→` | Di chuyển trái / phải |
| `↓` | Soft Drop |
| `↑` | Xoay khối |
| `Space` | Hard Drop |
| `1` | Hold |

> 💡 Tất cả phím điều khiển có thể tuỳ chỉnh trong **Settings → Key Bindings** hoặc ngay trong **Pause Menu**.

---

## ⏸️ Pause Menu

Nhấn `P` hoặc `Esc` trong lúc chơi để mở menu tạm dừng:

| Nút | Chức năng |
|-----|-----------|
| ♪ **SOUND SETTINGS** | Mở trang chỉnh âm thanh riêng (3 slider) |
| **KEY BINDINGS** | Tuỳ chỉnh phím điều khiển ngay lập tức |
| ▶ **RESUME** | Tiếp tục chơi (nhạc tự unpause) |
| ◀ **MODE SELECT** | Quay về màn hình chọn chế độ |
| ✕ **QUIT TO MENU** | Thoát về Main Menu |

### Sound Settings (từ Pause)

Điều chỉnh 3 thanh trượt âm thanh mà không cần thoát game:

- 🔵 **Master Volume** — âm lượng tổng thể
- 🟣 **Music** — âm lượng nhạc nền riêng
- 🔴 **Sound Effects** — âm lượng hiệu ứng âm thanh riêng

Nhấn `◀ BACK` hoặc `Esc` để quay về Pause Menu.

---

## 🤖 Chế độ AI

Khi chọn PvP với một bên là AI:

### Độ khó
| Độ khó | Tốc độ phản ứng |
|--------|-----------------|
| Easy   | Chậm (~250ms/hành động) |
| Normal | Trung bình (~150ms/hành động) |
| Hard   | Nhanh (~85ms/hành động) |

### Kiểu tính cách AI
| Chế độ | Mô tả |
|--------|-------|
| **Balanced** | Cân bằng tấn công và phòng thủ. Ổn định, ít mắc lỗi. |
| **Aggressive** | Liên tục gửi rác, bất chấp lưới của chính mình. |
| **Defensive** | Giữ lưới thấp, chờ đối thủ mắc lỗi. |

> 💡 Hover vào nút `!` bên cạnh AI Mode để xem tooltip mô tả chi tiết từng kiểu.

---

## ⚙️ Cài đặt hệ thống (CONFIG)

Truy cập menu **CONFIG** từ Main Menu để điều chỉnh:

| Mục | Loại | Mô tả |
|-----|------|-------|
| 🔵 Master Volume | Thanh trượt 0–100% | Âm lượng tổng |
| 🟣 Music | Thanh trượt 0–100% | Âm lượng nhạc nền |
| 🔴 Sound Effects | Thanh trượt 0–100% | Âm lượng hiệu ứng |
| ☀️ Brightness | Toggle | Dim / Normal / Bright |
| ⌨️ Key Bindings | Button | Tuỳ chỉnh phím Solo |

Cấu hình được lưu tự động vào `tetris_config.json`.

---

## 📊 Tính điểm

| Số dòng xóa | Điểm thưởng |
|-------------|-------------|
| 1 dòng | 100 điểm |
| 2 dòng | 300 điểm |
| 3 dòng | 500 điểm |
| 4 dòng (TETRIS) | 800 điểm 🏆 |

---

## 🎵 Âm thanh

### Nhạc nền
Đặt file nhạc vào `audio_assets/music/` với tên `background` và đuôi:

```
audio_assets/music/background.mp3   ← ưu tiên nhất
audio_assets/music/background.wav
audio_assets/music/background.ogg
```

Game tự tìm theo thứ tự `.mp4 → .mp3 → .wav → .ogg → .m4a`. Nếu không có file nào, nhạc mặc định (WAV tổng hợp) sẽ được tạo tự động.

### Hiệu ứng âm thanh (SFX)
SFX được **tự động sinh** vào `audio_assets/sfx/` khi lần đầu chạy game:

| File | Khi nào phát |
|------|-------------|
| `button.wav` | Nhấn nút menu |
| `move.wav` | Di chuyển khối |
| `rotate.wav` | Xoay khối |
| `hard_drop.wav` | Hard Drop |
| `hold.wav` | Hold piece |
| `clear.wav` | Xóa dòng |
| `game_over.wav` | Game Over |

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| Ngôn ngữ | Python 3.10+ |
| Game Engine | [pygame-ce](https://pyga.me/) 2.5+ |
| Font | Press Start 2P (Google Fonts) |
| Cấu hình | JSON |
| Âm thanh | WAV tự sinh + file nhạc bên ngoài (MP3/WAV/OGG) |

---

## 📄 Giấy phép

Dự án được phát triển cho mục đích học tập và cá nhân.  
Tetris® là thương hiệu thuộc sở hữu của **The Tetris Company**.  
Game gốc được sáng tạo bởi **Alexey Pajitnov** năm 1984.
