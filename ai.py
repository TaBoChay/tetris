# ai.py
import copy
from settings import *

class TetrisAI:
    def __init__(self, difficulty, ai_mode="balanced"):
        self.difficulty = difficulty
        self.ai_mode = ai_mode  # "balanced", "aggressive", "defensive"
        
        # ĐÃ CÂN BẰNG LẠI TỐC ĐỘ ĐỂ PHÙ HỢP VỚI NGƯỜI CHƠI
        if difficulty == "easy": 
            self.action_delay = 250  
            self.drop_delay = 600
        elif difficulty == "normal": 
            self.action_delay = 150   
            self.drop_delay = 250
        else: 
            self.action_delay = 85   # Hard: Nhanh nhưng con người vẫn bắt kịp
            self.drop_delay = 85
        
        self.timer = 0
        self.target_x = 0
        self.target_r = 0
        self.should_hold = False
        self.current_piece_id = None
        
        self.state = "THINK" 

    def update(self, logic, dt):
        if logic.game_over: return
        
        if id(logic.current_piece) != self.current_piece_id:
            self.state = "THINK"
            self.current_piece_id = id(logic.current_piece)
            
        self.timer += dt
        
        if self.state == "THINK":
            self.calculate_best_move(logic)
            self.state = "MOVE"
            self.timer = 0
            
        elif self.state == "MOVE":
            if self.timer >= self.action_delay:
                self.timer = 0
                self.execute_move_step(logic)
                
        elif self.state == "DROP":
            if self.timer >= self.drop_delay:
                self.timer = 0
                if self.difficulty == "hard":
                    logic.hard_drop()
                elif self.difficulty == "normal":
                    logic.move(0, 1) 
                else:
                    pass 

    def execute_move_step(self, logic):
        if self.should_hold and logic.can_hold:
            logic.swap_hold()
            self.should_hold = False
            self.state = "THINK" 
            return

        if logic.current_piece.rotation != self.target_r:
            logic.rotate()
            return

        if logic.current_piece.x > self.target_x:
            if not logic.move(-1, 0): self.state = "DROP" 
        elif logic.current_piece.x < self.target_x:
            if not logic.move(1, 0): self.state = "DROP"
        else:
            self.state = "DROP" 

    def calculate_best_move(self, logic):
        best_score = -999999
        best_x = logic.current_piece.x
        best_r = logic.current_piece.rotation
        best_hold = False

        score, x, r = self.get_best_for_piece(logic, logic.current_piece)
        if score > best_score:
            best_score = score; best_x = x; best_r = r; best_hold = False

        if logic.hold_enabled and logic.can_hold:
            hold_piece = logic.hold_piece if logic.hold_piece else logic.next_piece
            h_score, h_x, h_r = self.get_best_for_piece(logic, hold_piece)
            if h_score > best_score:
                best_score = h_score; best_x = h_x; best_r = h_r; best_hold = True

        self.target_x = best_x
        self.target_r = best_r
        self.should_hold = best_hold

    def get_best_for_piece(self, logic, piece):
        best_score = -999999
        best_x = piece.x
        best_r = piece.rotation

        for r in range(4):
            for x in range(-2, logic.cols + 2):
                score = self.simulate_drop(logic, piece, x, r)
                if score > best_score:
                    best_score = score; best_x = x; best_r = r
        return best_score, best_x, best_r

    def simulate_drop(self, logic, piece, x, r):
        dummy_y = piece.y
        shape_format = SHAPES[piece.shape][r % len(SHAPES[piece.shape])]
        
        def valid(dx, dy):
            for i, line in enumerate(shape_format):
                for j, cell in enumerate(line):
                    if cell == '0':
                        px, py = dx + j, dy + i
                        if px < 0 or px >= logic.cols or py >= logic.rows: return False
                        if py >= 0 and logic.grid[py][px] is not None: return False
            return True

        if not valid(x, dummy_y): return -999999

        while valid(x, dummy_y + 1): dummy_y += 1
            
        temp_grid = [row[:] for row in logic.grid]
        for i, line in enumerate(shape_format):
            for j, cell in enumerate(line):
                if cell == '0':
                    py, px = dummy_y + i, x + j
                    if 0 <= py < logic.rows and 0 <= px < logic.cols:
                        temp_grid[py][px] = piece.color
                        
        lines_cleared = 0
        new_grid = []
        for row in temp_grid:
            if None not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(logic.cols)])
            
        return self.evaluate_grid(new_grid, logic.cols, logic.rows, lines_cleared)

    def evaluate_grid(self, grid, cols, rows, lines_cleared):
        heights = [0] * cols
        holes = 0

        for y in range(rows):
            for x in range(cols):
                if grid[y][x] is not None:
                    if heights[x] == 0: heights[x] = rows - y
                else:
                    if heights[x] > 0: holes += 1 

        agg_height = sum(heights)
        bumpiness = sum(abs(heights[i] - heights[i+1]) for i in range(cols - 1))

        # Chọn weights dựa trên ai_mode
        if self.ai_mode == "aggressive":
            # 🔥 Ưu tiên xóa dòng/gửi rác, ignore holes
            a, b, c, d = -0.4, 1.2, -0.2, -0.05
        elif self.ai_mode == "defensive":
            # 🛡️ Ưu tiên an toàn, tránh cao/lỗ
            a, b, c, d = -0.8, 0.5, -0.8, -0.3
        else:  # balanced (default)
            # Cân bằng
            a, b, c, d = -0.510066, 0.760666, -0.35663, -0.184483
            
        return (a * agg_height) + (b * lines_cleared) + (c * holes) + (d * bumpiness)