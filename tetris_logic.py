# tetris_logic.py
import random
from settings import *

class Piece:
    def __init__(self, x, y, shape):
        self.x = x; self.y = y; self.shape = shape
        self.color = SHAPE_COLORS[shape]; self.rotation = 0
    def get_format(self):
        return SHAPES[self.shape][self.rotation % len(SHAPES[self.shape])]

class TetrisLogic:
    def __init__(self, config):
        cols, rows = map(int, config['grid'].split('x'))
        self.cols = cols; self.rows = rows
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.level = int(config.get('level', 1))
        self.score = 0; self.lines = 0
        
        self.ghost_enabled = config.get('ghost', 'on') == 'on'
        self.hold_enabled = config.get('hold', 'on') == 'on'
        
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.hold_piece = None
        self.can_hold = True
        self.game_over = False
        
        self.cleared_blocks_anim = []
        self.lines_cleared_this_turn = 0 # Ghi nhận số dòng vừa ăn để đánh đối thủ

    def get_new_piece(self):
        return Piece(self.cols // 2 - 2, 0, random.choice(list(SHAPES.keys())))

    def valid_space(self, piece):
        format = piece.get_format()
        for i, line in enumerate(format):
            for j, cell in enumerate(line):
                if cell == '0':
                    px, py = piece.x + j, piece.y + i
                    if px < 0 or px >= self.cols or py >= self.rows: return False
                    if py >= 0 and self.grid[py][px] is not None: return False
        return True

    def lock_piece(self):
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
            if self.lines >= self.level * 10: self.level += 1
            
        self.lines_cleared_this_turn = lines_cleared

    def get_and_reset_cleared_lines(self):
        res = self.lines_cleared_this_turn
        self.lines_cleared_this_turn = 0
        return res

    def add_garbage_lines(self, amount):
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
        if self.game_over: return False
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.valid_space(self.current_piece):
            self.current_piece.x -= dx; self.current_piece.y -= dy
            if dy > 0: self.lock_piece()
            return False
        return True

    def rotate(self):
        if self.game_over: return
        self.current_piece.rotation += 1
        if not self.valid_space(self.current_piece): self.current_piece.rotation -= 1 

    def hard_drop(self):
        if self.game_over: return
        while self.move(0, 1): pass 

    def swap_hold(self):
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
        if not self.ghost_enabled or self.game_over: return None
        ghost = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape)
        ghost.rotation = self.current_piece.rotation
        while self.valid_space(ghost): ghost.y += 1
        ghost.y -= 1
        return ghost

    def get_fall_speed(self):
        return max(50, 1000 - (self.level - 1) * 80)