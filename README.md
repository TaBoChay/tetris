# 🎮 Tetris Cyberpunk Edition

> Một phiên bản Tetris hiện đại với giao diện Cyberpunk/Neon, hỗ trợ chế độ PvP, AI đối kháng và âm nhạc động.

---

## 📸 Giới thiệu

**Tetris Cyberpunk Edition** là trò chơi Tetris được xây dựng bằng Python và Pygame, lấy cảm hứng từ phong cách **Cyberpunk Neon** với hiệu ứng phát sáng, màu sắc rực rỡ và giao diện động. Game hỗ trợ nhiều chế độ chơi khác nhau bao gồm Solo, PvP (Người vs Người) và PvAI (Người vs AI).

---

## ✨ Tính năng nổi bật

- 🕹️ **Nhiều chế độ chơi**: Solo (40 Lines, Blitz, Custom), PvP 2 người, PvAI
- 🤖 **AI thông minh** với 3 kiểu tính cách: Balanced, Aggressive, Defensive
- 🎨 **Giao diện Cyberpunk Neon** với hiệu ứng glow, particle và animation
- 🎵 **Hệ thống âm thanh đầy đủ**: Nhạc nền, hiệu ứng SFX tự sinh
- ⚙️ **Tuỳ chỉnh sâu**: Level, kích thước lưới, ghost piece, hold piece
- ⌨️ **Phím điều khiển tuỳ biến** cho từng người chơi
- 💾 **Lưu cấu hình tự động** vào file JSON
- 📐 **Vật lý NES Tetris** — bảng tốc độ rơi chính xác theo từng level

---

## 🗂️ Cấu trúc dự án

```
Tetris/
├── main.py            # Vòng lặp game chính, xử lý sự kiện và điều hướng màn hình
├── menus.py           # Vẽ tất cả các màn hình menu (Main, Solo, PvP, Config, ...)
├── game_screens.py    # Màn hình gameplay chính (Solo & PvP), vẽ lưới & HUD
├── tetris_logic.py    # Logic cốt lõi của Tetris (di chuyển, xoay, xóa dòng, ...)
├── ai.py              # Trí tuệ nhân tạo AI (thuật toán heuristic đánh giá lưới)
├── audio.py           # Hệ thống âm thanh (sinh file WAV, phát nhạc & SFX)
├── ui.py              # Các component UI tái sử dụng (nút, slider, font, ...)
├── settings.py        # Hằng số, màu sắc, cấu hình mặc định, key mapping
├── tetris_config.json # File lưu cấu hình người dùng (tự động tạo)
├── PressStart2P-Regular.ttf  # Font chữ Pixel game
└── audio_assets/
    ├── music/         # Nhạc nền (background.mp3, ambient.wav, cyberpunk.wav)
    └── sfx/           # Hiệu ứng âm thanh (move, rotate, clear, game_over, ...)
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

### Chế độ Solo

| Phím | Hành động |
|------|-----------|
| `←` / `→` | Di chuyển trái / phải |
| `↓` | Rơi nhanh (Soft Drop) |
| `↑` | Xoay khối |
| `Space` | Thả rơi ngay (Hard Drop) |
| `Z` | Giữ khối (Hold) |
| `P` hoặc `Esc` | Tạm dừng |

### Chế độ PvP — Người chơi 1 (mặc định WASD)

| Phím | Hành động |
|------|-----------|
| `A` / `D` | Di chuyển trái / phải |
| `S` | Soft Drop |
| `W` | Xoay khối |
| `Q` | Hard Drop |
| `Z` | Hold |

### Chế độ PvP — Người chơi 2 (mặc định phím mũi tên)

| Phím | Hành động |
|------|-----------|
| `←` / `→` | Di chuyển trái / phải |
| `↓` | Soft Drop |
| `↑` | Xoay khối |
| `Space` | Hard Drop |
| `/` | Hold |

> 💡 Tất cả phím điều khiển có thể tuỳ chỉnh trong **Settings → Key Bindings**.

---

## 🤖 Chế độ AI

Khi chọn PvP với một bên là AI, bạn có thể chọn:

### Độ khó
| Độ khó | Thời gian phản ứng |
|--------|--------------------|
| Easy | Chậm (~250ms/hành động) |
| Normal | Trung bình (~150ms/hành động) |
| Hard | Nhanh (~85ms/hành động) |

### Kiểu tính cách AI
| Chế độ | Mô tả |
|--------|-------|
| **Balanced** | Cân bằng tấn công và phòng thủ. Ổn định, ít mắc lỗi. Phù hợp để làm quen. |
| **Aggressive** | Ưu tiên xóa nhiều dòng và gửi rác liên tục, bất chấp lưới của chính mình. |
| **Defensive** | Giữ lưới thấp, chơi an toàn, chờ đối thủ mắc lỗi để phản công. |

---

## ⚙️ Cài đặt hệ thống

Truy cập menu **CONFIG** để điều chỉnh:

- 🔊 **Master Volume** — thanh trượt 0–100%
- 🎵 **Sound Effects** — bật/tắt SFX
- ☀️ **Brightness** — Dim / Normal / Bright
- ⌨️ **Key Bindings** — tuỳ chỉnh phím điều khiển

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

Game tự động sinh file âm thanh mặc định nếu không tìm thấy:
- **Nhạc nền**: Đặt file `.mp3`, `.wav`, `.ogg` hoặc `.m4a` vào `audio_assets/music/`
- **SFX**: Tự động sinh sẵn trong `audio_assets/sfx/`

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ |
|-----------|-----------|
| Ngôn ngữ | Python 3.10+ |
| Game Engine | [pygame-ce](https://pyga.me/) 2.5+ |
| Font | Press Start 2P (Google Fonts) |
| Định dạng cấu hình | JSON |
| Âm thanh | WAV tự sinh + MP3 bên ngoài |

---

## 📄 Giấy phép

Dự án được phát triển cho mục đích học tập và cá nhân.  
Tetris® là thương hiệu thuộc sở hữu của **The Tetris Company**.  
Game gốc được sáng tạo bởi **Alexey Pajitnov** năm 1984.
