# tetris_logic.py
import random
from settings import *

class Piece:
    def __init__(self, x, y, shape):
        self.x = x; self.y = y; self.shape = shape
        self.color = SHAPE_COLORS[shape]; self.rotation = 0
    def get_format(self):
        """Trả về cấu trúc mảng 2D của viên gạch tại góc xoay hiện tại."""
        return SHAPES[self.shape][self.rotation % len(SHAPES[self.shape])]

class TetrisLogic:
    def __init__(self, config):
        cols, rows = map(int, config['grid'].split('x'))
        self.cols = cols; self.rows = rows
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.level = int(config.get('level', 1))
        self.start_level = self.level
        self.score = 0; self.lines = 0
        self.level_up_enabled = config.get('level_up', 'on') == 'on'
        
        self.ghost_enabled = config.get('ghost', 'on') == 'on'
        self.hold_enabled = config.get('hold', 'on') == 'on'
        
        self.bag = []
        
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.hold_piece = None
        self.can_hold = True
        self.game_over = False
        
        self.cleared_blocks_anim = []
        self.lines_cleared_this_turn = 0 # Ghi nhận số dòng vừa ăn để đánh đối thủ
        self.combo = 0  # Combo counter cho garbage multiplier

    def get_new_piece(self):
        """
        Lấy một viên gạch mới từ túi gạch (7-bag algorithm).
        Nếu túi trống, tạo túi mới gồm 7 loại gạch và xáo trộn.
        """
        if not hasattr(self, 'bag') or not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        shape = self.bag.pop()
        return Piece(self.cols // 2 - 2, 0, shape)

    def valid_space(self, piece):
        """
        Kiểm tra xem vị trí hiện tại của viên gạch có hợp lệ không.
        (Không bị ra ngoài lưới và không bị đè lên các viên gạch đã khoá).
        """
        format = piece.get_format()
        for i, line in enumerate(format):
            for j, cell in enumerate(line):
                if cell == '0':
                    px, py = piece.x + j, piece.y + i
                    if px < 0 or px >= self.cols or py >= self.rows: return False
                    if py >= 0 and self.grid[py][px] is not None: return False
        return True

    def lock_piece(self):
        """
        Khoá viên gạch hiện tại vào lưới (khi nó không thể rơi xuống thêm được nữa).
        Kiểm tra xoá dòng và tự động tạo viên gạch mới. Đánh dấu game_over nếu đầy lưới.
        """
        format = self.current_piece.get_format()
        for i, line in enumerate(format):
            for j, cell in enumerate(line):
                if cell == '0':
                    py, px = self.current_piece.y + i, self.current_piece.x + j
                    if py >= 0: self.grid[py][px] = self.current_piece.color
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.can_hold = True 
        if not self.valid_space(self.current_piece): self.game_over = True

    def clear_lines(self):
        """
        Xoá các dòng đã được lấp đầy trên lưới.
        Tính toán điểm số, số dòng đã xoá, hệ số combo và tăng cấp độ (level).
        """
        lines_cleared = 0
        new_grid = []
        for i in range(self.rows):
            if None not in self.grid[i]:
                for j in range(self.cols):
                    self.cleared_blocks_anim.append((j, i, self.grid[i][j]))
                lines_cleared += 1
            else:
                new_grid.append(self.grid[i])
                
        if lines_cleared > 0:
            for _ in range(lines_cleared): new_grid.insert(0, [None for _ in range(self.cols)])
            self.grid = new_grid
            self.lines += lines_cleared
            pts = {1: 100, 2: 300, 3: 500, 4: 800}.get(lines_cleared, 800)
            self.score += pts * self.level
            if self.level_up_enabled:
                new_level = self.start_level + (self.lines // 10)
                if new_level > self.level:
                    self.level = new_level
            self.combo += 1  # Tăng combo
        else:
            self.combo = 0  # Reset combo nếu không xóa dòng
            
        self.lines_cleared_this_turn = lines_cleared

    def get_and_reset_cleared_lines(self):
        # """
        # Lấy số lượng dòng đã xoá trong lượt vừa rồi và tự động reset về 0.
        # Được sử dụng trong chế độ PvP để tính toán lượng rác sẽ ném sang đối thủ.
        # """
        res = self.lines_cleared_this_turn
        self.lines_cleared_this_turn = 0
        return res
    
    def get_garbage_amount(self):
        # """Calculate garbage to send with combo multiplier
        # 1 line = 1 garbage, but multiplier increases with combo
        # Combo 5+ = 2x garbage"""
        if self.lines_cleared_this_turn == 0:
            return 0
        garbage = self.lines_cleared_this_turn
        if self.combo >= 5:
            garbage *= 2
        return garbage

    def add_garbage_lines(self, amount):
        
        # Thêm các dòng rác từ dưới đáy lưới lên (nhận rác từ đối thủ).
        # Dòng rác có màu xám đậm và luôn chừa lại 1 ô trống ngẫu nhiên.
        
        if amount <= 0 or self.game_over: return
        self.grid = self.grid[amount:] # Đẩy lưới lên
        for _ in range(amount):
            hole_x = random.randint(0, self.cols - 1)
            # Khối rác màu xám đậm (GRAY), chừa 1 lỗ ngẫu nhiên
            garbage_row = [(50, 50, 50) if x != hole_x else None for x in range(self.cols)]
            self.grid.append(garbage_row)
            
        while not self.valid_space(self.current_piece) and self.current_piece.y > -2:
            self.current_piece.y -= 1

    def move(self, dx, dy):
        # Di chuyển viên gạch theo trục x (ngang) và y (dọc).
        # Nếu di chuyển xuống (dy > 0) mà bị kẹt thì sẽ tự động khoá viên gạch.
        # Trả về True nếu di chuyển thành công, False nếu bị chặn.
        if self.game_over: return False
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.valid_space(self.current_piece):
            self.current_piece.x -= dx; self.current_piece.y -= dy
            if dy > 0: self.lock_piece()
            return False
        return True

    def rotate(self):
        # Xoay viên gạch theo chiều kim đồng hồ.
        # Nếu vị trí sau khi xoay bị chặn, thử dịch chuyển sang trái/phải/lên (Wall Kick).
        # Nếu vẫn không được, sẽ huỷ việc xoay.
        if self.game_over: return
        self.current_piece.rotation += 1
        if self.valid_space(self.current_piece):
            return
            
        # Wall kick logic (try shifting left, right, up, double left, double right)
        kick_offsets = [(-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0), (-1, -1), (1, -1)]
        for dx, dy in kick_offsets:
            self.current_piece.x += dx
            self.current_piece.y += dy
            if self.valid_space(self.current_piece):
                return
            # Revert shift if invalid
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            
        # Revert rotation if all kicks fail
        self.current_piece.rotation -= 1

    def hard_drop(self):
        # Cho viên gạch rơi thẳng lập tức xuống vị trí thấp nhất có thể.
        if self.game_over: return
        while self.move(0, 1): pass 

    def swap_hold(self):
        """
        Đổi viên gạch hiện tại với viên gạch đang được giữ (Hold).
        Mỗi lượt rơi chỉ được phép sử dụng chức năng Hold một lần.
        """
        if self.game_over or not self.hold_enabled or not self.can_hold: return
        if self.hold_piece is None:
            self.hold_piece = Piece(self.cols // 2 - 2, 0, self.current_piece.shape)
            self.current_piece = self.next_piece
            self.next_piece = self.get_new_piece()
        else:
            temp_shape = self.current_piece.shape
            self.current_piece = Piece(self.cols // 2 - 2, 0, self.hold_piece.shape)
            self.hold_piece = Piece(self.cols // 2 - 2, 0, temp_shape)
        self.can_hold = False 

    def get_ghost_piece(self):
        # Tính toán và trả về vị trí ảnh ảo (Ghost Piece) của viên gạch hiện tại.
        # Ảnh ảo hiển thị nơi viên gạch sẽ rơi xuống nếu thực hiện thả mạnh (hard drop).
        if not self.ghost_enabled or self.game_over: return None
        ghost = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape)
        ghost.rotation = self.current_piece.rotation
        while self.valid_space(ghost): ghost.y += 1
        ghost.y -= 1
        return ghost

    def get_fall_speed(self):
        """Trả về thời gian (ms) giữa các lần khối rơi xuống dựa trên level
        Sử dụng bảng gravity NES Tetris: frames (60 FPS) -> ms"""
        gravity_frames = get_gravity_frames(self.level)
        # Chuyển đổi frames (60 FPS) sang milliseconds
        return int(gravity_frames * 1000 / 60)