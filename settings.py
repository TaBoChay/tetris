# settings.py
import json
from pathlib import Path

# --- CÁC THÔNG SỐ CƠ BẢN ---
WIDTH, HEIGHT = 900, 700
BLOCK_SIZE = 28 
PVP_BLOCK_SIZE = 22 

# Bảng màu Neon / Cyberpunk
BG_COLOR = (15, 15, 35)      
CYAN = (0, 255, 255)         
PINK = (255, 107, 157)       
YELLOW = (255, 215, 0)       
GREEN = (0, 255, 0)          
RED = (255, 68, 68)          
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
BLUE = (52, 152, 219)

CONFIG_FILE = Path(__file__).resolve().parent / "tetris_config.json"
DEFAULT_SYS_CONFIG = {"volume": 80, "sfx": "on", "music": "on", "brightness": "normal"}

# Default key mappings for SOLO mode (arrow keys)
DEFAULT_SOLO_KEYS = {
    "move_left": "left",
    "move_right": "right",
    "move_down": "down",
    "rotate": "up",
    "hard_drop": "space",
    "hold": "z"
}

# Default key mappings for PVP P1 (WASD)
DEFAULT_PVP_P1_KEYS = {
    "move_left": "a",
    "move_right": "d",
    "move_down": "s",
    "rotate": "w",
    "hard_drop": "q",
    "hold": "z"
}

# Default key mappings for PVP P2 (arrow keys)
DEFAULT_PVP_P2_KEYS = {
    "move_left": "left",
    "move_right": "right",
    "move_down": "down",
    "rotate": "up",
    "hard_drop": "space",
    "hold": "slash"
}

DEFAULT_SOLO_CONFIG = {"level": "1", "grid": "10x20", "ghost": "on", "hold": "on", "level_up": "on", "keys": DEFAULT_SOLO_KEYS.copy()}
DEFAULT_PVP_CONFIG = {
    "level": "1", "grid": "10x20", "ai_diff": "normal", "ai_mode": "balanced",
    "p1_name": "PLAYER 1", "p1_color": "cyan", "p1_type": "human",
    "p2_name": "PLAYER 2", "p2_color": "pink", "p2_type": "human",
    "p1_keys": DEFAULT_PVP_P1_KEYS.copy(),
    "p2_keys": DEFAULT_PVP_P2_KEYS.copy()
}

COLOR_MAP = {"cyan": CYAN, "lime": GREEN, "gold": YELLOW, "red": RED, "pink": PINK}

# ================= ĐỊNH NGHĨA CÁC KHỐI GẠCH =================
SHAPES = {
    'I': [['.....', '.....', '0000.', '.....', '.....'], 
          ['..0..', '..0..', '..0..', '..0..', '.....'],
          ['.....', '.....', '0000.', '.....', '.....'], 
          ['..0..', '..0..', '..0..', '..0..', '.....']],
    'J': [['.....', '.0...', '.000.', '.....', '.....'], 
          ['.....', '..00.', '..0..', '..0..', '.....'],
          ['.....', '.....', '.000.', '...0.', '.....'],
          ['.....', '..0..', '..0..', '.00..', '.....']],
    'L': [['.....', '...0.', '.000.', '.....', '.....'], 
          ['.....', '..0..', '..0..', '..00.', '.....'],
          ['.....', '.....', '.000.', '.0...', '.....'],
          ['.....', '.00..', '..0..', '..0..', '.....']],
    'O': [['.....', '.....', '.00..', '.00..', '.....'],
          ['.....', '.....', '.00..', '.00..', '.....'],
          ['.....', '.....', '.00..', '.00..', '.....'],
          ['.....', '.....', '.00..', '.00..', '.....']],
    'S': [['.....', '..00.', '.00..', '.....', '.....'], 
          ['.....', '..0..', '..00.', '...0.', '.....'],
          ['.....', '.....', '..00.', '.00..', '.....'],
          ['.....', '.0...', '.00..', '..0..', '.....']],
    'T': [['.....', '..0..', '.000.', '.....', '.....'], 
          ['.....', '..0..', '..00.', '..0..', '.....'],
          ['.....', '.....', '.000.', '..0..', '.....'],
          ['.....', '..0..', '.00..', '..0..', '.....']],
    'Z': [['.....', '.00..', '..00.', '.....', '.....'], 
          ['.....', '..0..', '.00..', '.0...', '.....'],
          ['.....', '.....', '.00..', '..00.', '.....'],
          ['.....', '...0.', '..00.', '..0..', '.....']]
}
SHAPE_COLORS = {'I': CYAN, 'J': BLUE, 'L': ORANGE, 'O': YELLOW, 'S': GREEN, 'T': PURPLE, 'Z': RED}

# ================= BẢNG GRAVITY THEO LEVEL (NES TETRIS) =================
# Mỗi level có số frames khác nhau trước khi khối rơi xuống 1 dòng
# 60 FPS = 1 frame = ~16.67ms
GRAVITY_TABLE = {
    0: 48,    # 0.800s
    1: 43,    # 0.7s
    2: 38,    # 0.633s
    3: 33,    # 0.550s
    4: 28,    # 0.466s
    5: 23,    # 0.383s
    6: 18,    # 0.300s
    7: 13,    # 0.2s
    8: 8,     # 0.133s
    9: 6,     # 0.100s
    10: 5, 11: 5, 12: 5,  # Levels 10-12: 0.083s
    13: 4, 14: 4, 15: 4,  # Levels 13-15: 0.066s
    16: 3, 17: 3, 18: 3,  # Levels 16-18: 0.050s
    19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2, 25: 2, 26: 2, 27: 2, 28: 2,  # Levels 19-28: 0.033s
}

def get_gravity_frames(level):
    """Lấy số frames (60 FPS) cho mỗi drop dựa trên level"""
    if level in GRAVITY_TABLE:
        return GRAVITY_TABLE[level]
    else:
        return 1  # Level 29+: 1 frame (0.016s)


def _merge_config(defaults, loaded):
    merged = defaults.copy()
    if isinstance(loaded, dict):
        for key, value in loaded.items():
            if key in merged:
                merged[key] = value
    return merged


def load_user_config(path=CONFIG_FILE):
    """Đọc cấu hình từ tập tin JSON, nếu không tồn tại thì trả về cấu hình mặc định."""
    if not path.exists():
        return {
            "sys": DEFAULT_SYS_CONFIG.copy(),
            "solo": DEFAULT_SOLO_CONFIG.copy(),
            "pvp": DEFAULT_PVP_CONFIG.copy()
        }

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
        return {
            "sys": _merge_config(DEFAULT_SYS_CONFIG, loaded.get("sys", {})),
            "solo": _merge_config(DEFAULT_SOLO_CONFIG, loaded.get("solo", {})),
            "pvp": _merge_config(DEFAULT_PVP_CONFIG, loaded.get("pvp", {}))
        }
    except Exception:
        return {
            "sys": DEFAULT_SYS_CONFIG.copy(),
            "solo": DEFAULT_SOLO_CONFIG.copy(),
            "pvp": DEFAULT_PVP_CONFIG.copy()
        }


def save_user_config(config, path=CONFIG_FILE):
    """Ghi cấu hình vào tập tin JSON."""
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def apply_brightness(color, brightness):
    if brightness == "dim":
        factor = 0.75
    elif brightness == "bright":
        factor = 1.15
    else:
        return color
    return tuple(max(0, min(255, int(c * factor))) for c in color)


# ================= KEY MAPPING UTILITIES =================
import pygame  # type: ignore

# Map string key names to pygame constants
KEY_MAP = {
    "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN,
    "space": pygame.K_SPACE, "z": pygame.K_z, "x": pygame.K_x, "c": pygame.K_c, "v": pygame.K_v, "b": pygame.K_b, "n": pygame.K_n, "m": pygame.K_m,
    "a": pygame.K_a, "d": pygame.K_d, "s": pygame.K_s, "w": pygame.K_w, "q": pygame.K_q, "e": pygame.K_e, "r": pygame.K_r, "t": pygame.K_t,
    "slash": pygame.K_SLASH, "comma": pygame.K_COMMA, "period": pygame.K_PERIOD,
    "f": pygame.K_f, "g": pygame.K_g, "h": pygame.K_h, "j": pygame.K_j, "k": pygame.K_k, "l": pygame.K_l, "p": pygame.K_p, "i": pygame.K_i, "o": pygame.K_o
}

# Reverse map: pygame constant to string name (for display)
KEY_DISPLAY = {v: k.upper() for k, v in KEY_MAP.items()}
# Override some display names for readability
KEY_DISPLAY.update({
    pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_UP: "UP", pygame.K_DOWN: "DOWN",
    pygame.K_SPACE: "SPACE", pygame.K_SLASH: "SLASH", pygame.K_COMMA: "COMMA", pygame.K_PERIOD: "PERIOD",
    pygame.K_z: "Z", pygame.K_x: "X", pygame.K_c: "C", pygame.K_v: "V", pygame.K_b: "B", pygame.K_n: "N", pygame.K_m: "M",
    pygame.K_a: "A", pygame.K_d: "D", pygame.K_s: "S", pygame.K_w: "W", pygame.K_q: "Q", pygame.K_e: "E", pygame.K_r: "R", pygame.K_t: "T",
    pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L", pygame.K_p: "P", pygame.K_i: "I", pygame.K_o: "O"
})

def get_key_constant(key_name):
    """Convert string key name to pygame constant"""
    return KEY_MAP.get(key_name.lower(), pygame.K_LEFT)

def get_key_display_name(key_constant):
    """Convert pygame constant to display name"""
    return KEY_DISPLAY.get(key_constant, "UNKNOWN")
