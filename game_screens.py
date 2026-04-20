# game_screens.py
import pygame
from settings import *
from ui import *

def _key_label(keys_config, action, fallback="?"):
    """Trả về tên hiển thị của phím được bind cho action."""
    key_name = keys_config.get(action, fallback)
    return get_key_display_name(get_key_constant(key_name))

def draw_play_screen_solo(screen, mouse_pos, logic, particles, game_mode=None, blitz_time=0, keys_config=None):
    # Vẽ màn hình chơi game
    screen.fill(BG_COLOR)
    if game_mode == "40L":
        draw_glow_text(screen, "40 LINES", title_font, GREEN, WIDTH//2, 40, align="center")
    elif game_mode == "BLITZ":
        draw_glow_text(screen, "BLITZ", title_font, YELLOW, WIDTH//2, 40, align="center")
    else:
        draw_glow_text(screen, "SOLO", title_font, CYAN, WIDTH//2, 40, align="center")

    board_h_max = 540
    block_size = board_h_max // logic.rows
    board_w = logic.cols * block_size
    board_h = logic.rows * block_size
    board_x = (WIDTH - board_w) // 2
    board_y = (HEIGHT - board_h) // 2

    bg_surface = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (10, 15, 25, 200), bg_surface.get_rect())
    for x in range(logic.cols):
        pygame.draw.line(bg_surface, (255, 255, 255, 15), (x * block_size, 0), (x * block_size, board_h))
    for y in range(logic.rows):
        pygame.draw.line(bg_surface, (255, 255, 255, 15), (0, y * block_size), (board_w, y * block_size))

    screen.blit(bg_surface, (board_x, board_y))
    pygame.draw.rect(screen, (*CYAN, 120), (board_x, board_y, board_w, board_h), 2)

    for y in range(logic.rows):
        for x in range(logic.cols):
            if logic.grid[y][x]:
                rect = pygame.Rect(board_x + x*block_size, board_y + y*block_size, block_size, block_size)
                inner_rect = rect.inflate(-2, -2)
                pygame.draw.rect(screen, logic.grid[y][x], inner_rect, border_radius=2)

    ghost = logic.get_ghost_piece()
    if ghost:
        for i, line in enumerate(ghost.get_format()):
            for j, cell in enumerate(line):
                if cell == '0':
                    px = board_x + (ghost.x + j) * block_size
                    py = board_y + (ghost.y + i) * block_size
                    if py >= board_y:
                        s = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
                        inner_rect = s.get_rect().inflate(-2, -2)
                        pygame.draw.rect(s, (*ghost.color, 30), inner_rect, border_radius=2)
                        pygame.draw.rect(s, (*ghost.color, 180), inner_rect, 1, border_radius=2)
                        screen.blit(s, (px, py))

    if not logic.game_over:
        piece = logic.current_piece
        for i, line in enumerate(piece.get_format()):
            for j, cell in enumerate(line):
                if cell == '0':
                    px = board_x + (piece.x + j) * block_size
                    py = board_y + (piece.y + i) * block_size
                    if py >= board_y:
                        rect = pygame.Rect(px, py, block_size, block_size)
                        inner_rect = rect.inflate(-2, -2)
                        pygame.draw.rect(screen, piece.color, inner_rect, border_radius=2)

    for p in particles:
        p.draw(screen)

    ctrl_y = board_y + board_h + 20
    if keys_config:
        k = keys_config
        rot   = _key_label(k, "rotate")
        left  = _key_label(k, "move_left")
        right = _key_label(k, "move_right")
        down  = _key_label(k, "move_down")
        hard  = _key_label(k, "hard_drop")
        hold  = _key_label(k, "hold")
        line1 = f"[{rot}] ROTATE   [{left}/{right}] MOVE   [{down}] DROP"
        line2 = f"[{hard}] HARD DROP   [{hold}] HOLD"
    else:
        line1 = "[UP] ROTATE   [L/R] MOVE   [DOWN] DROP"
        line2 = "[SPACE] HARD DROP   [Z] HOLD"
    draw_glow_text(screen, line1, small_font, CYAN, WIDTH//2, ctrl_y, align="center")
    draw_glow_text(screen, line2, small_font, YELLOW, WIDTH//2, ctrl_y + 22, align="center")

    left_x = 60
    if logic.hold_enabled:
        draw_glow_text(screen, "HOLD", main_font, CYAN, left_x, 80, align="left")
        pygame.draw.rect(screen, (*CYAN, 120), (left_x, 100, 120, 100), 1, border_radius=4)
        if logic.hold_piece:
            draw_shape_preview(screen, logic.hold_piece.shape, left_x + 30, 125, block_size=15)

    stats = [
        ("POINTS", str(logic.score), GREEN),
        ("LINES", str(logic.lines), YELLOW),
        ("LEVEL", str(logic.level), CYAN)
    ]
    stat_y = 100 if not logic.hold_enabled else 230
    for label, val, color in stats:
        draw_glow_text(screen, label, small_font, color, left_x, stat_y, align="left")
        draw_glow_text(screen, val, main_font, WHITE, left_x, stat_y + 25, align="left")
        stat_y += 60

    if game_mode == "BLITZ" or game_mode == "40L":
        if game_mode == "BLITZ":
            seconds = blitz_time // 1000
        else:
            seconds = blitz_time // 1000
        mins = seconds // 60
        secs = seconds % 60
        timer_text = f"{mins:02}:{secs:02}"
        timer_color = YELLOW
        draw_glow_text(screen, "TIME", small_font, timer_color, left_x, stat_y, align="left")
        draw_glow_text(screen, timer_text, main_font, timer_color, left_x, stat_y + 25, align="left")

    right_x = WIDTH - 180
    draw_glow_text(screen, "NEXT", main_font, CYAN, right_x, 80, align="left")
    pygame.draw.rect(screen, (*CYAN, 120), (right_x, 100, 120, 140), 1, border_radius=4)
    draw_shape_preview(screen, logic.next_piece.shape, right_x + 30, 130, block_size=15)

    draw_glow_text(screen, "STATUS", small_font, RED, right_x, 260, align="left")
    status_text = "GAME OVER" if logic.game_over else "PLAYING"
    status_color = RED if logic.game_over else WHITE
    draw_glow_text(screen, status_text, main_font, status_color, right_x, 285, align="left")

    buttons = {"menu": None, "retry": None, "pause": None, "mode_select": None}

    if logic.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        if game_mode == "BLITZ" and blitz_time <= 0:
            draw_glow_text(screen, "TIME'S UP!", title_font, YELLOW, WIDTH//2, HEIGHT//2 - 110)
        elif game_mode == "40L":
            if logic.lines >= 40:
                draw_glow_text(screen, "YOU WIN!", title_font, GREEN, WIDTH//2, HEIGHT//2 - 110)
                draw_glow_text(screen, f"TIME: {blitz_time // 1000 // 60:02}:{blitz_time // 1000 % 60:02}", main_font, CYAN, WIDTH//2, HEIGHT//2 - 65, align="center")
            else:
                draw_glow_text(screen, "GAME OVER", title_font, RED, WIDTH//2, HEIGHT//2 - 110)
                draw_glow_text(screen, f"LINES: {logic.lines}/40", main_font, CYAN, WIDTH//2, HEIGHT//2 - 65, align="center")
        else:
            draw_glow_text(screen, "GAME OVER", title_font, RED, WIDTH//2, HEIGHT//2 - 90)
        draw_glow_text(screen, f"FINAL SCORE: {logic.score}", main_font, YELLOW, WIDTH//2, HEIGHT//2 - 25)

        btn_w, btn_h = 180, 48
        total_w = btn_w * 3 + 20 * 2
        start_x = WIDTH//2 - total_w//2
        buttons["retry"] = draw_neon_button(screen, "RETRY", start_x, HEIGHT//2 + 35, btn_w, btn_h, GREEN, mouse_pos)
        buttons["mode_select"] = draw_neon_button(screen, "MODE SELECT", start_x + btn_w + 20, HEIGHT//2 + 35, btn_w, btn_h, CYAN, mouse_pos)
        buttons["menu"] = draw_neon_button(screen, "MAIN MENU", start_x + (btn_w + 20)*2, HEIGHT//2 + 35, btn_w, btn_h, PINK, mouse_pos)
    else:
        buttons["pause"] = draw_neon_button(screen, "PAUSE", WIDTH - 140, 20, 100, 40, PINK, mouse_pos)

    return buttons


def draw_pvp_screen(screen, mouse_pos, pvp_config, logic1, logic2, particles1, particles2, p1_keys=None, p2_keys=None):
    # Vẽ màn hình chơi game cho chế độ PvP (2 người chơi cạnh nhau).
    # Hiển thị hai bảng lưới riêng biệt, thông tin điểm số, combo và phần hướng dẫn phím.
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, (*CYAN, 100), (WIDTH//2, 60), (WIDTH//2, HEIGHT - 20), 2)

    c1 = COLOR_MAP.get(pvp_config["p1_color"], CYAN)
    c2 = COLOR_MAP.get(pvp_config["p2_color"], PINK)

    def draw_player_side(offset_x, player_name, color, logic, controls_lines, particles_list):
        # Vẽ riêng một nửa màn hình (trái/phải) cho từng người chơi.
        # Bao gồm lưới, gạch Hold, gạch Next và trạng thái Thắng/Thua.
        center_x = offset_x + 200
        if offset_x > 200:
            center_x += 40

        board_w = logic.cols * PVP_BLOCK_SIZE
        board_h = logic.rows * PVP_BLOCK_SIZE
        board_x = center_x - board_w // 2
        board_y = (HEIGHT - board_h) // 2

        render_bold_text(screen, player_name, main_font, color, center_x, 60, "center")

        bg_surface = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (10, 15, 25, 200), bg_surface.get_rect())
        for x in range(logic.cols):
            pygame.draw.line(bg_surface, (255, 255, 255, 15), (x * PVP_BLOCK_SIZE, 0), (x * PVP_BLOCK_SIZE, board_h))
        for y in range(logic.rows):
            pygame.draw.line(bg_surface, (255, 255, 255, 15), (0, y * PVP_BLOCK_SIZE), (board_w, y * PVP_BLOCK_SIZE))
        screen.blit(bg_surface, (board_x, board_y))
        pygame.draw.rect(screen, (*color, 150), (board_x, board_y, board_w, board_h), 2)

        for y in range(logic.rows):
            for x in range(logic.cols):
                if logic.grid[y][x]:
                    rect = pygame.Rect(board_x + x*PVP_BLOCK_SIZE, board_y + y*PVP_BLOCK_SIZE, PVP_BLOCK_SIZE, PVP_BLOCK_SIZE)
                    inner_rect = rect.inflate(-1, -1)
                    pygame.draw.rect(screen, logic.grid[y][x], inner_rect, border_radius=2)

        ghost = logic.get_ghost_piece()
        if ghost:
            for i, line in enumerate(ghost.get_format()):
                for j, cell in enumerate(line):
                    if cell == '0':
                        px = board_x + (ghost.x + j) * PVP_BLOCK_SIZE
                        py = board_y + (ghost.y + i) * PVP_BLOCK_SIZE
                        if py >= board_y:
                            s = pygame.Surface((PVP_BLOCK_SIZE, PVP_BLOCK_SIZE), pygame.SRCALPHA)
                            inner_rect = s.get_rect().inflate(-1, -1)
                            pygame.draw.rect(s, (*ghost.color, 30), inner_rect, border_radius=2)
                            pygame.draw.rect(s, (*ghost.color, 180), inner_rect, 1, border_radius=2)
                            screen.blit(s, (px, py))

        if not logic.game_over:
            piece = logic.current_piece
            for i, line in enumerate(piece.get_format()):
                for j, cell in enumerate(line):
                    if cell == '0':
                        px = board_x + (piece.x + j) * PVP_BLOCK_SIZE
                        py = board_y + (piece.y + i) * PVP_BLOCK_SIZE
                        if py >= board_y:
                            rect = pygame.Rect(px, py, PVP_BLOCK_SIZE, PVP_BLOCK_SIZE)
                            pygame.draw.rect(screen, piece.color, rect.inflate(-1, -1), border_radius=2)

        for p in particles_list:
            p.draw(screen)

        hold_x = board_x - 65
        render_bold_text(screen, "HOLD", small_font, color, hold_x + 25, board_y - 15, "center")
        pygame.draw.rect(screen, (*color, 150), (hold_x, board_y, 50, 50), 2, border_radius=4)
        if logic.hold_piece:
            draw_shape_preview(screen, logic.hold_piece.shape, hold_x + 5, board_y + 10, block_size=10)

        next_x = board_x + board_w + 15
        render_bold_text(screen, "NEXT", small_font, color, next_x + 25, board_y - 15, "center")
        pygame.draw.rect(screen, (*color, 150), (next_x, board_y, 50, 110), 2, border_radius=4)
        draw_shape_preview(screen, logic.next_piece.shape, next_x + 5, board_y + 10, block_size=10)

        stat_y = board_y + board_h + 15
        render_bold_text(screen, f"PTS: {logic.score}", small_font, GREEN, center_x - 60, stat_y, "center")
        render_bold_text(screen, f"LIN: {logic.lines}", small_font, YELLOW, center_x + 5, stat_y, "center")
        render_bold_text(screen, f"LVL: {logic.level}", small_font, RED, center_x + 70, stat_y, "center")

        ctrl_y = stat_y + 25
        for i, line in enumerate(controls_lines):
            c = GRAY if "AI" in line else (CYAN if i == 0 else YELLOW)
            draw_glow_text(screen, line, small_font, c, center_x, ctrl_y + i*20, "center")

        if logic.game_over:
            overlay = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (board_x, board_y))
            # draw_glow_text(screen, "LOSER!", title_font, RED, center_x, board_y + board_h//2)

    if pvp_config["p1_type"] == "human":
        if p1_keys:
            k = p1_keys
            rot  = _key_label(k, "rotate")
            left = _key_label(k, "move_left")
            right= _key_label(k, "move_right")
            down = _key_label(k, "move_down")
            hard = _key_label(k, "hard_drop")
            hold = _key_label(k, "hold")
            p1_controls = [f"[{rot}] ROTA   [{left}/{right}] MOVE",
                           f"[{down}] DROP   [{hard}] HARD   [{hold}] HOLD"]
        else:
            p1_controls = ["[W] ROTA   [A/D] MOVE", "[S] DROP   [Q] HARD   [Z] HOLD"]
    else:
        p1_controls = ["", "AI IS PLAYING...", ""]

    if pvp_config["p2_type"] == "human":
        if p2_keys:
            k = p2_keys
            rot  = _key_label(k, "rotate")
            left = _key_label(k, "move_left")
            right= _key_label(k, "move_right")
            down = _key_label(k, "move_down")
            hard = _key_label(k, "hard_drop")
            hold = _key_label(k, "hold")
            p2_controls = [f"[{rot}] ROTA   [{left}/{right}] MOVE",
                           f"[{down}] DROP   [{hard}] HARD   [{hold}] HOLD"]
        else:
            p2_controls = ["[UP] ROTA   [L/R] MOVE", "[DOWN] DROP   [SPACE] HARD   [/] HOLD"]
    else:
        p2_controls = ["", "AI IS PLAYING...", ""]

    draw_player_side(0, pvp_config["p1_name"], c1, logic1, p1_controls, particles1)
    draw_player_side(400, pvp_config["p2_name"], c2, logic2, p2_controls, particles2)

    buttons = {"menu": None, "retry": None, "pause": None, "mode_select": None}

    if logic1.game_over or logic2.game_over:
        win_text = pvp_config["p2_name"] + " WINS!" if logic1.game_over else pvp_config["p1_name"] + " WINS!"
        draw_glow_text(screen, win_text, title_font, YELLOW, WIDTH//2, HEIGHT//2 - 30)
        btn_w, btn_h = 180, 48
        total_w = btn_w * 3 + 20 * 2
        start_x = WIDTH//2 - total_w//2
        buttons["retry"] = draw_neon_button(screen, "RETRY PVP", start_x, HEIGHT//2 + 30, btn_w, btn_h, GREEN, mouse_pos)
        buttons["mode_select"] = draw_neon_button(screen, "MODE SELECT", start_x + btn_w + 20, HEIGHT//2 + 30, btn_w, btn_h, CYAN, mouse_pos)
        buttons["menu"] = draw_neon_button(screen, "MAIN MENU", start_x + (btn_w + 20)*2, HEIGHT//2 + 30, btn_w, btn_h, PINK, mouse_pos)
    else:
        buttons["pause"] = draw_neon_button(screen, "PAUSE", WIDTH//2 - 50, 10, 100, 35, PINK, mouse_pos)

    return buttons
