# menus.py
import pygame  # type: ignore
from settings import *
from ui import *

def draw_main_menu(screen, mouse_pos):
    """Vẽ màn hình menu chính với các lựa chọn: Solo, Multiplayer, Config, About, Exit."""
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    draw_glow_text(screen, "TETRIS", title_font, CYAN, WIDTH//2, 100)
    
    btn_w, btn_h = 350, 55; start_x = (WIDTH - btn_w) // 2
    b_solo = draw_neon_button(screen, "SOLO", start_x, 190, btn_w, btn_h, GREEN, mouse_pos)
    b_multi = draw_neon_button(screen, "MULTIPLAYER", start_x, 260, btn_w, btn_h, PINK, mouse_pos)
    b_conf = draw_neon_button(screen, "CONFIG", start_x, 330, btn_w, btn_h, YELLOW, mouse_pos)
    b_about = draw_neon_button(screen, "ABOUT", start_x, 400, btn_w, btn_h, CYAN, mouse_pos)
    b_exit = draw_neon_button(screen, "EXIT", start_x, 470, btn_w, btn_h, RED, mouse_pos)
    
    draw_glow_text(screen, "© 1984 Created by Alexey Pajitnov", small_font, GRAY, WIDTH//2, HEIGHT - 30)
    
    return b_solo, b_multi, b_conf, b_about, b_exit

def draw_about_menu(screen, mouse_pos):
    """Vẽ màn hình thông tin (About), hướng dẫn luật chơi, cách điều khiển và cách tính điểm."""
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    
    draw_glow_text(screen, "ABOUT THE GAME", title_font, CYAN, WIDTH//2, 50)
    
    # Center panels - RULES and CONTROLS side by side
    panel_w1 = 330
    gap_between = 30
    total_w_row1 = panel_w1 * 2 + gap_between
    start_x_row1 = (WIDTH - total_w_row1) // 2
    
    p1_x = start_x_row1
    p1_y, p1_w, p1_h = 110, 330, 200
    p1_surf = pygame.Surface((p1_w, p1_h), pygame.SRCALPHA)
    pygame.draw.rect(p1_surf, (*CYAN, 30), p1_surf.get_rect(), border_radius=8)
    screen.blit(p1_surf, (p1_x, p1_y))
    pygame.draw.rect(screen, CYAN, (p1_x, p1_y, p1_w, p1_h), 2, border_radius=8)
    draw_glow_text(screen, "RULES", main_font, CYAN, p1_x + p1_w//2, p1_y + 25)
    rules = ["• Fill horizontal lines", "  with blocks to clear.", "", "• Speed increases as", "  the Level goes up.", "", "• Game Over when blocks", "  reach the top."]
    for i, line in enumerate(rules):
        render_bold_text(screen, line, small_font, WHITE, p1_x + 20, p1_y + 70 + i*16, "left")

    p2_x = p1_x + p1_w + gap_between
    p2_y, p2_w, p2_h = 110, 330, 200
    p2_surf = pygame.Surface((p2_w, p2_h), pygame.SRCALPHA)
    pygame.draw.rect(p2_surf, (*PINK, 30), p2_surf.get_rect(), border_radius=8)
    screen.blit(p2_surf, (p2_x, p2_y))
    pygame.draw.rect(screen, PINK, (p2_x, p2_y, p2_w, p2_h), 2, border_radius=8)
    draw_glow_text(screen, "CONTROLS", main_font, PINK, p2_x + p2_w//2, p2_y + 25)
    controls = ["[ SOLO & PLAYER 2 ]", "• Arrows: Move", "• Up: Rotate", "• / or Space: Hold", "", "[ PLAYER 1 PVP ]", "• W/A/S/D: Move", "• Z: Hold piece"]
    for i, line in enumerate(controls):
        render_bold_text(screen, line, small_font, WHITE, p2_x + 20, p2_y + 60 + i*16, "left")

    # Center SCORING panel
    p3_w, p3_h = 680, 160
    p3_x = (WIDTH - p3_w) // 2
    p3_y = 330
    p3_surf = pygame.Surface((p3_w, p3_h), pygame.SRCALPHA)
    pygame.draw.rect(p3_surf, (*YELLOW, 30), p3_surf.get_rect(), border_radius=8)
    screen.blit(p3_surf, (p3_x, p3_y))
    pygame.draw.rect(screen, YELLOW, (p3_x, p3_y, p3_w, p3_h), 2, border_radius=8)
    draw_glow_text(screen, "SCORING", main_font, YELLOW, p3_x + p3_w//2, p3_y + 25)
    render_bold_text(screen, "1 Line : 100 PTS", small_font, WHITE, p3_x + 100, p3_y + 70, "left")
    render_bold_text(screen, "2 Lines: 300 PTS", small_font, WHITE, p3_x + 100, p3_y + 110, "left")
    render_bold_text(screen, "3 Lines: 500 PTS", small_font, WHITE, p3_x + 380, p3_y + 70, "left")
    render_bold_text(screen, "4 Lines: 800 PTS (TETRIS)", small_font, RED, p3_x + 380, p3_y + 110, "left")

    btn_back = draw_neon_button(screen, "< BACK", WIDTH//2 - 100, 520, 200, 50, GRAY, mouse_pos)
    return btn_back

def draw_solo_menu(screen, mouse_pos):
    """Vẽ màn hình chọn chế độ chơi đơn (Solo): 40 Lines, Blitz, Custom."""
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    btn_back = draw_neon_button(screen, "< BACK", 30, 30, 120, 40, PINK, mouse_pos)
    draw_glow_text(screen, "SOLO MODE", title_font, CYAN, WIDTH//2, 100)
    
    btn_w, btn_h = 400, 75; start_x = (WIDTH - btn_w) // 2
    b_40l = draw_neon_button(screen, "40 LINES", start_x, 200, btn_w, btn_h, GREEN, mouse_pos)
    b_blitz = draw_neon_button(screen, "BLITZ", start_x, 295, btn_w, btn_h, YELLOW, mouse_pos)
    b_custom = draw_neon_button(screen, "CUSTOM", start_x, 390, btn_w, btn_h, CYAN, mouse_pos)
    return btn_back, b_40l, b_blitz, b_custom

def draw_solo_custom_menu(screen, mouse_pos, config):
    """Vẽ màn hình tuỳ chỉnh cấu hình cho chế độ Solo Custom (Level, Grid, Ghost, Hold)."""
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    draw_glow_text(screen, "SOLO CUSTOM", title_font, CYAN, WIDTH//2, 50)
    buttons = {"level": {}, "grid": {}, "ghost": {}, "hold": {}}
    panel_w = 600; panel_x = (WIDTH - panel_w) // 2

    l_y = 110
    l_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(l_surf, (*CYAN, 30), l_surf.get_rect(), border_radius=8)
    screen.blit(l_surf, (panel_x, l_y))
    pygame.draw.rect(screen, CYAN, (panel_x, l_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "> START LEVEL", main_font, CYAN, panel_x + 20, l_y + 40, align="left")
    buttons["level"]["1"] = draw_toggle_button(screen, "LV 1", panel_x + 220, l_y + 20, 80, 35, GREEN, mouse_pos, config["level"] == "1")
    buttons["level"]["5"] = draw_toggle_button(screen, "LV 5", panel_x + 310, l_y + 20, 80, 35, YELLOW, mouse_pos, config["level"] == "5")
    buttons["level"]["10"] = draw_toggle_button(screen, "LV 10", panel_x + 400, l_y + 20, 80, 35, ORANGE, mouse_pos, config["level"] == "10")
    buttons["level"]["15"] = draw_toggle_button(screen, "LV 15", panel_x + 490, l_y + 20, 80, 35, RED, mouse_pos, config["level"] == "15")

    g_y = 205
    g_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(g_surf, (*PINK, 30), g_surf.get_rect(), border_radius=8)
    screen.blit(g_surf, (panel_x, g_y))
    pygame.draw.rect(screen, PINK, (panel_x, g_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "> GRID SIZE", main_font, PINK, panel_x + 20, g_y + 40, align="left")
    buttons["grid"]["8x15"] = draw_toggle_button(screen, "8x15", panel_x + 220, g_y + 20, 100, 35, GREEN, mouse_pos, config["grid"] == "8x15")
    buttons["grid"]["10x20"] = draw_toggle_button(screen, "10x20", panel_x + 330, g_y + 20, 120, 35, YELLOW, mouse_pos, config["grid"] == "10x20")
    buttons["grid"]["12x25"] = draw_toggle_button(screen, "12x25", panel_x + 460, g_y + 20, 100, 35, RED, mouse_pos, config["grid"] == "12x25")

    gh_y = 300
    gh_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(gh_surf, (*GREEN, 30), gh_surf.get_rect(), border_radius=8)
    screen.blit(gh_surf, (panel_x, gh_y))
    pygame.draw.rect(screen, GREEN, (panel_x, gh_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "> GHOST PIECE", main_font, GREEN, panel_x + 20, gh_y + 40, align="left")
    buttons["ghost"]["off"] = draw_toggle_button(screen, "OFF", panel_x + 260, gh_y + 20, 80, 35, RED, mouse_pos, config["ghost"] == "off")
    buttons["ghost"]["on"] = draw_toggle_button(screen, "ON", panel_x + 350, gh_y + 20, 80, 35, GREEN, mouse_pos, config["ghost"] == "on")

    h_y = 395
    h_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(h_surf, (*YELLOW, 30), h_surf.get_rect(), border_radius=8)
    screen.blit(h_surf, (panel_x, h_y))
    pygame.draw.rect(screen, YELLOW, (panel_x, h_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "> HOLD PIECE", main_font, YELLOW, panel_x + 20, h_y + 40, align="left")
    buttons["hold"]["off"] = draw_toggle_button(screen, "OFF", panel_x + 260, h_y + 20, 80, 35, RED, mouse_pos, config["hold"] == "off")
    buttons["hold"]["on"] = draw_toggle_button(screen, "ON", panel_x + 350, h_y + 20, 80, 35, GREEN, mouse_pos, config["hold"] == "on")

    buttons["back"] = draw_neon_button(screen, "< BACK", 120, 500, 220, 50, RED, mouse_pos)
    buttons["start"] = draw_neon_button(screen, "START GAME >", 460, 500, 220, 50, GREEN, mouse_pos)
    return buttons

def draw_config_menu(screen, mouse_pos, sys_config):
    """Vẽ màn hình cài đặt hệ thống (Volume, Music, SFX, Brightness)."""
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    btn_back = draw_neon_button(screen, "< BACK", 30, 30, 120, 40, PINK, mouse_pos)
    draw_glow_text(screen, "SETTINGS", title_font, CYAN, WIDTH//2, 50)
    draw_glow_text(screen, "System Configuration", small_font, PINK, WIDTH//2, 90)

    buttons = {"volume_slider": None, "music_slider": None, "sfx_slider": None, "brightness": {}}
    panel_w = 460; panel_x = (WIDTH - panel_w) // 2

    # MASTER VOLUME SLIDER
    vol_y = 115
    vol_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(vol_surf, (*CYAN, 30), vol_surf.get_rect(), border_radius=8)
    screen.blit(vol_surf, (panel_x, vol_y))
    pygame.draw.rect(screen, CYAN, (panel_x, vol_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "MASTER VOLUME", main_font, CYAN, WIDTH//2, vol_y + 20, align="center")
    vol_value = sys_config.get("volume", 80)
    if isinstance(vol_value, str):
        vol_value = 100 if vol_value == "on" else 0
    buttons["volume_slider"] = draw_slider(screen, panel_x + 60, vol_y + 45, panel_w - 120, 12, 0, 100, vol_value, CYAN, WHITE, mouse_pos)
    draw_glow_text(screen, f"{vol_value}%", small_font, WHITE, panel_x + panel_w - 45, vol_y + 45, align="center")

    # MUSIC SLIDER
    music_y = vol_y + 95
    music_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(music_surf, (*PURPLE, 30), music_surf.get_rect(), border_radius=8)
    screen.blit(music_surf, (panel_x, music_y))
    pygame.draw.rect(screen, PURPLE, (panel_x, music_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "MUSIC", main_font, PURPLE, WIDTH//2, music_y + 20, align="center")
    music_value = sys_config.get("music_volume", 70)
    if isinstance(music_value, str):
        music_value = 70
    buttons["music_slider"] = draw_slider(screen, panel_x + 60, music_y + 45, panel_w - 120, 12, 0, 100, music_value, PURPLE, WHITE, mouse_pos)
    draw_glow_text(screen, f"{music_value}%", small_font, WHITE, panel_x + panel_w - 45, music_y + 45, align="center")

    # SFX SLIDER
    sfx_y = music_y + 95
    sfx_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(sfx_surf, (*PINK, 30), sfx_surf.get_rect(), border_radius=8)
    screen.blit(sfx_surf, (panel_x, sfx_y))
    pygame.draw.rect(screen, PINK, (panel_x, sfx_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "SOUND EFFECTS", main_font, PINK, WIDTH//2, sfx_y + 20, align="center")
    sfx_value = sys_config.get("sfx_volume", 80)
    if isinstance(sfx_value, str):
        sfx_value = 0 if sfx_value == "off" else 80
    buttons["sfx_slider"] = draw_slider(screen, panel_x + 60, sfx_y + 45, panel_w - 120, 12, 0, 100, sfx_value, PINK, WHITE, mouse_pos)
    draw_glow_text(screen, f"{sfx_value}%", small_font, WHITE, panel_x + panel_w - 45, sfx_y + 45, align="center")

    # BRIGHTNESS
    bri_y = sfx_y + 95
    bri_surf = pygame.Surface((panel_w, 80), pygame.SRCALPHA)
    pygame.draw.rect(bri_surf, (*YELLOW, 30), bri_surf.get_rect(), border_radius=8)
    screen.blit(bri_surf, (panel_x, bri_y))
    pygame.draw.rect(screen, YELLOW, (panel_x, bri_y, panel_w, 80), 2, border_radius=8)
    draw_glow_text(screen, "BRIGHTNESS", main_font, YELLOW, WIDTH//2, bri_y + 20, align="center")
    buttons["brightness"]["dim"] = draw_toggle_button(screen, "DIM", WIDTH//2 - 165, bri_y + 38, 100, 30, PURPLE, mouse_pos, sys_config["brightness"] == "dim")
    buttons["brightness"]["normal"] = draw_toggle_button(screen, "NORMAL", WIDTH//2 - 50, bri_y + 38, 100, 30, YELLOW, mouse_pos, sys_config["brightness"] == "normal")
    buttons["brightness"]["bright"] = draw_toggle_button(screen, "BRIGHT", WIDTH//2 + 65, bri_y + 38, 100, 30, CYAN, mouse_pos, sys_config["brightness"] == "bright")

    buttons["reset"] = draw_neon_button(screen, "RESET DEFAULTS", WIDTH//2 - 150, bri_y + 100, 300, 45, GRAY, mouse_pos)
    buttons["keys"] = draw_neon_button(screen, "KEY BINDINGS >", WIDTH//2 - 150, bri_y + 155, 300, 45, CYAN, mouse_pos)
    return btn_back, buttons

def draw_ai_mode_tooltip(screen, mouse_pos):
    tooltip_w = 530
    tooltip_h = 430
    tt_x = mouse_pos[0] + 15
    tt_y = mouse_pos[1] + 15
    if tt_x + tooltip_w > WIDTH:
        tt_x = mouse_pos[0] - tooltip_w - 15
    if tt_y + tooltip_h > HEIGHT:
        tt_y = HEIGHT - tooltip_h - 10

    tt_surf = pygame.Surface((tooltip_w, tooltip_h), pygame.SRCALPHA)
    pygame.draw.rect(tt_surf, (15, 15, 30, 245), tt_surf.get_rect(), border_radius=10)
    screen.blit(tt_surf, (tt_x, tt_y))
    pygame.draw.rect(screen, CYAN, (tt_x, tt_y, tooltip_w, tooltip_h), 2, border_radius=10)

    lines = [
        ("1. BALANCED", main_font, CYAN),
        ("Style: Safe & Steady.", small_font, (180, 220, 255)),
        ("Info: Balances attack and defense.", small_font, WHITE),
        ("      Rarely makes mistakes.", small_font, WHITE),
        ("Tip: Great for warm-ups.", small_font, YELLOW),
        ("", small_font, WHITE),
        ("2. AGGRESSIVE", main_font, ORANGE),
        ("Style: High Pressure!", small_font, (255, 210, 180)),
        ("Info: Spams garbage lines at all costs,", small_font, WHITE),
        ("      ignoring its own board.", small_font, WHITE),
        ("Tip: Don't build high. Clear lines fast!", small_font, YELLOW),
        ("", small_font, WHITE),
        ("3. DEFENSIVE", main_font, BLUE),
        ("Style: Survival Focus.", small_font, (180, 200, 255)),
        ("Info: Keeps board low, plays safe,", small_font, WHITE),
        ("      and waits for your mistakes.", small_font, WHITE),
        ("Tip: Take time to set up massive", small_font, YELLOW),
        ("      combos to break its defense.", small_font, YELLOW),
    ]

    y_offset = tt_y + 16
    for text, f, color in lines:
        if text == "":
            y_offset += 8
            continue
        render_bold_text(screen, text, f, color, tt_x + 16, y_offset + f.get_height() // 2, align="left")
        y_offset += f.get_height() + 6

def draw_pvp_settings(screen, mouse_pos, config, active_input):
    """
    Vẽ màn hình cài đặt cho chế độ PvP (Player vs Player / Player vs AI).
    Cấu hình bao gồm: Level, Grid, Cài đặt AI (nếu có), Tên, Màu sắc và Phím điều khiển của 2 người chơi.
    """
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    draw_glow_text(screen, "PVP SETTINGS", title_font, CYAN, WIDTH//2, 40)
    buttons = {"level": {}, "grid": {}, "ai_diff": {}, "ai_mode": {}, "p1_color": {}, "p1_type": {}, "p2_color": {}, "p2_type": {}}
    
    # ===== Panel-based layout =====
    panel_w = 720
    panel_x = (WIDTH - panel_w) // 2
    opt_y = 70
    opt_h = 55
    opt_spacing = 62
    
    # LEVEL PANEL
    level_surf = pygame.Surface((panel_w, opt_h), pygame.SRCALPHA)
    pygame.draw.rect(level_surf, (*CYAN, 30), level_surf.get_rect(), border_radius=8)
    screen.blit(level_surf, (panel_x, opt_y))
    pygame.draw.rect(screen, CYAN, (panel_x, opt_y, panel_w, opt_h), 2, border_radius=8)
    draw_glow_text(screen, "> START LEVEL", main_font, CYAN, panel_x + 20, opt_y + 26, align="left")
    buttons["level"]["1"] = draw_toggle_button(screen, "LV 1", panel_x + 250, opt_y + 5, 65, 32, GREEN, mouse_pos, config["level"] == "1")
    buttons["level"]["5"] = draw_toggle_button(screen, "LV 5", panel_x + 325, opt_y + 5, 65, 32, YELLOW, mouse_pos, config["level"] == "5")
    buttons["level"]["10"] = draw_toggle_button(screen, "LV 10", panel_x + 400, opt_y + 5, 65, 32, ORANGE, mouse_pos, config["level"] == "10")
    buttons["level"]["15"] = draw_toggle_button(screen, "LV 15", panel_x + 475, opt_y + 5, 65, 32, RED, mouse_pos, config["level"] == "15")
    
    # GRID PANEL
    opt_y += opt_spacing
    grid_surf = pygame.Surface((panel_w, opt_h), pygame.SRCALPHA)
    pygame.draw.rect(grid_surf, (*PINK, 30), grid_surf.get_rect(), border_radius=8)
    screen.blit(grid_surf, (panel_x, opt_y))
    pygame.draw.rect(screen, PINK, (panel_x, opt_y, panel_w, opt_h), 2, border_radius=8)
    draw_glow_text(screen, "> GRID SIZE", main_font, PINK, panel_x + 20, opt_y + 26, align="left")
    buttons["grid"]["8x15"] = draw_toggle_button(screen, "8x15", panel_x + 250, opt_y + 5, 70, 32, GREEN, mouse_pos, config["grid"] == "8x15")
    buttons["grid"]["10x20"] = draw_toggle_button(screen, "10x20", panel_x + 340, opt_y + 5, 80, 32, YELLOW, mouse_pos, config["grid"] == "10x20")
    buttons["grid"]["12x25"] = draw_toggle_button(screen, "12x25", panel_x + 440, opt_y + 5, 70, 32, RED, mouse_pos, config["grid"] == "12x25")
    
    # AI SETTINGS
    show_ai_settings = config["p1_type"] == "ai" or config["p2_type"] == "ai"
    panel_y = opt_y + opt_spacing
    if show_ai_settings:
        # AI DIFFICULTY PANEL
        ai_diff_surf = pygame.Surface((panel_w, opt_h), pygame.SRCALPHA)
        pygame.draw.rect(ai_diff_surf, (*RED, 30), ai_diff_surf.get_rect(), border_radius=8)
        screen.blit(ai_diff_surf, (panel_x, panel_y))
        pygame.draw.rect(screen, RED, (panel_x, panel_y, panel_w, opt_h), 2, border_radius=8)
        draw_glow_text(screen, "> AI DIFFICULTY", main_font, RED, panel_x + 20, panel_y + 26, align="left")
        buttons["ai_diff"]["easy"] = draw_toggle_button(screen, "EASY", panel_x + 250, panel_y + 5, 70, 32, GREEN, mouse_pos, config["ai_diff"] == "easy")
        buttons["ai_diff"]["normal"] = draw_toggle_button(screen, "NORMAL", panel_x + 340, panel_y + 5, 95, 32, YELLOW, mouse_pos, config["ai_diff"] == "normal")
        buttons["ai_diff"]["hard"] = draw_toggle_button(screen, "HARD", panel_x + 455, panel_y + 5, 70, 32, RED, mouse_pos, config["ai_diff"] == "hard")
        
        # AI MODE PANEL
        panel_y += opt_spacing
        ai_mode_surf = pygame.Surface((panel_w, opt_h), pygame.SRCALPHA)
        pygame.draw.rect(ai_mode_surf, (*PURPLE, 30), ai_mode_surf.get_rect(), border_radius=8)
        screen.blit(ai_mode_surf, (panel_x, panel_y))
        pygame.draw.rect(screen, PURPLE, (panel_x, panel_y, panel_w, opt_h), 2, border_radius=8)
        draw_glow_text(screen, "> AI MODE", main_font, PURPLE, panel_x + 20, panel_y + 26, align="left")
        buttons["ai_mode"]["balanced"] = draw_toggle_button(screen, "BALANCED", panel_x + 250, panel_y + 5, 90, 32, CYAN, mouse_pos, config["ai_mode"] == "balanced")
        buttons["ai_mode"]["aggressive"] = draw_toggle_button(screen, "AGGRESSIVE", panel_x + 360, panel_y + 5, 100, 32, ORANGE, mouse_pos, config["ai_mode"] == "aggressive")
        buttons["ai_mode"]["defensive"] = draw_toggle_button(screen, "DEFENSIVE", panel_x + 480, panel_y + 5, 90, 32, BLUE, mouse_pos, config["ai_mode"] == "defensive")
        
        buttons["ai_mode_info"] = draw_neon_button(screen, "!", panel_x + 600, panel_y + 5, 32, 32, YELLOW, mouse_pos)
        
        panel_y += opt_spacing
    
    # PLAYER PANELS
    p1_w, p2_w = 360, 360
    p1_x = (WIDTH // 2) - p1_w - 15
    p2_x = (WIDTH // 2) + 15
    p_h = 220
    
    p1_surf = pygame.Surface((p1_w, p_h), pygame.SRCALPHA)
    pygame.draw.rect(p1_surf, (*CYAN, 30), p1_surf.get_rect(), border_radius=8)
    screen.blit(p1_surf, (p1_x, panel_y))
    pygame.draw.rect(screen, CYAN, (p1_x, panel_y, p1_w, p_h), 2, border_radius=8)
    
    p2_surf = pygame.Surface((p2_w, p_h), pygame.SRCALPHA)
    pygame.draw.rect(p2_surf, (*PINK, 30), p2_surf.get_rect(), border_radius=8)
    screen.blit(p2_surf, (p2_x, panel_y))
    pygame.draw.rect(screen, PINK, (p2_x, panel_y, p2_w, p_h), 2, border_radius=8)
    
    draw_glow_text(screen, "PLAYER 1", main_font, CYAN, p1_x + p1_w//2, panel_y + 15)
    draw_glow_text(screen, "PLAYER 2", main_font, PINK, p2_x + p2_w//2, panel_y + 15)
    
    draw_glow_text(screen, "NAME", small_font, WHITE, p1_x + p1_w//2, panel_y + 30)
    buttons["p1_name_box"] = pygame.Rect(p1_x + 15, panel_y + 42, 300, 25)
    pygame.draw.rect(screen, CYAN if active_input == "p1_name" else (*CYAN, 80), buttons["p1_name_box"], 2, border_radius=4)
    cursor = "_" if (pygame.time.get_ticks() % 1000 < 500) else ""
    p1_display = config["p1_name"] + (cursor if active_input == "p1_name" else "")
    render_bold_text(screen, p1_display, small_font, CYAN, buttons["p1_name_box"].centerx, buttons["p1_name_box"].centery, "center")
    
    draw_glow_text(screen, "NAME", small_font, WHITE, p2_x + p2_w//2, panel_y + 30)
    buttons["p2_name_box"] = pygame.Rect(p2_x + 15, panel_y + 42, 300, 25)
    pygame.draw.rect(screen, PINK if active_input == "p2_name" else (*PINK, 80), buttons["p2_name_box"], 2, border_radius=4)
    p2_display = config["p2_name"] + (cursor if active_input == "p2_name" else "")
    render_bold_text(screen, p2_display, small_font, PINK, buttons["p2_name_box"].centerx, buttons["p2_name_box"].centery, "center")
    
    draw_glow_text(screen, "COLOR", small_font, WHITE, p1_x + p1_w//2, panel_y + 75)
    buttons["p1_color"]["cyan"] = draw_toggle_button(screen, "C", p1_x + 10, panel_y + 85, 60, 24, CYAN, mouse_pos, config["p1_color"] == "cyan")
    buttons["p1_color"]["lime"] = draw_toggle_button(screen, "L", p1_x + 75, panel_y + 85, 60, 24, GREEN, mouse_pos, config["p1_color"] == "lime")
    buttons["p1_color"]["gold"] = draw_toggle_button(screen, "G", p1_x + 140, panel_y + 85, 60, 24, YELLOW, mouse_pos, config["p1_color"] == "gold")
    buttons["p1_color"]["red"] = draw_toggle_button(screen, "R", p1_x + 205, panel_y + 85, 60, 24, RED, mouse_pos, config["p1_color"] == "red")
    
    draw_glow_text(screen, "COLOR", small_font, WHITE, p2_x + p2_w//2, panel_y + 75)
    buttons["p2_color"]["pink"] = draw_toggle_button(screen, "P", p2_x + 10, panel_y + 85, 60, 24, PINK, mouse_pos, config["p2_color"] == "pink")
    buttons["p2_color"]["lime"] = draw_toggle_button(screen, "L", p2_x + 75, panel_y + 85, 60, 24, GREEN, mouse_pos, config["p2_color"] == "lime")
    buttons["p2_color"]["gold"] = draw_toggle_button(screen, "G", p2_x + 140, panel_y + 85, 60, 24, YELLOW, mouse_pos, config["p2_color"] == "gold")
    buttons["p2_color"]["cyan"] = draw_toggle_button(screen, "C", p2_x + 205, panel_y + 85, 60, 24, CYAN, mouse_pos, config["p2_color"] == "cyan")
    
    p1_ai_color = GRAY if config["p2_type"] == "ai" else RED
    p2_ai_color = GRAY if config["p1_type"] == "ai" else RED
    
    draw_glow_text(screen, "OPP", small_font, WHITE, p1_x + p1_w//2, panel_y + 125)
    buttons["p1_type"]["human"] = draw_toggle_button(screen, "HUM", p1_x + 30, panel_y + 135, 120, 24, GREEN, mouse_pos, config["p1_type"] == "human")
    buttons["p1_type"]["ai"] = draw_toggle_button(screen, "AI", p1_x + 160, panel_y + 135, 120, 24, p1_ai_color, mouse_pos, config["p1_type"] == "ai")
    
    draw_glow_text(screen, "OPP", small_font, WHITE, p2_x + p2_w//2, panel_y + 125)
    buttons["p2_type"]["human"] = draw_toggle_button(screen, "HUM", p2_x + 30, panel_y + 135, 120, 24, GREEN, mouse_pos, config["p2_type"] == "human")
    buttons["p2_type"]["ai"] = draw_toggle_button(screen, "AI", p2_x + 160, panel_y + 135, 120, 24, p2_ai_color, mouse_pos, config["p2_type"] == "ai")
    
    # KEY BINDING BUTTONS - ALIGN WITH PLAYER PANELS
    p1_key_x = p1_x  # Left align with P1 panel
    p2_key_x = p2_x  # Left align with P2 panel (same as P1)
    if config["p1_type"] == "human":
        buttons["p1_keys"] = draw_neon_button(screen, "P1 KEYS", p1_key_x, 555, 150, 35, GREEN, mouse_pos)
    if config["p2_type"] == "human":
        buttons["p2_keys"] = draw_neon_button(screen, "P2 KEYS", p2_key_x, 555, 150, 35, PINK, mouse_pos)
    
    buttons["back"] = draw_neon_button(screen, "< BACK", 120, 610, 220, 50, RED, mouse_pos)
    buttons["start"] = draw_neon_button(screen, "START PVP >", 460, 610, 220, 50, GREEN, mouse_pos)
    
    if "ai_mode_info" in buttons and buttons["ai_mode_info"].collidepoint(mouse_pos):
        draw_ai_mode_tooltip(screen, mouse_pos)
        
    return buttons

def draw_keyconfig_menu(screen, mouse_pos, mode, config, rebinding_key=None):
    """
    Vẽ màn hình thiết lập phím điều khiển (Key bindings) cho cả chế độ Solo và PvP.
    Hiển thị thông báo khi đang chờ người dùng nhập phím mới (rebinding_key).
    """
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    
    # Safe default if mode is None
    if mode is None:
        mode = "solo"
    
    # Safe default if mode is None
    if mode is None:
        mode = "solo"
    
    if mode == "solo":
        title = "SOLO KEY CONFIG"
        keys_dict = config.get("keys", DEFAULT_SOLO_KEYS)
        key_actions = ["move_left", "move_right", "move_down", "rotate", "hard_drop", "hold"]
        action_labels = ["MOVE LEFT", "MOVE RIGHT", "MOVE DOWN", "ROTATE", "HARD DROP", "HOLD"]
        color = CYAN
    elif mode == "pvp_p1":
        title = "PVP P1 KEY CONFIG"
        keys_dict = config.get("p1_keys", DEFAULT_PVP_P1_KEYS)
        key_actions = ["move_left", "move_right", "move_down", "rotate", "hard_drop", "hold"]
        action_labels = ["MOVE LEFT", "MOVE RIGHT", "MOVE DOWN", "ROTATE", "HARD DROP", "HOLD"]
        color = GREEN
    else:  # pvp_p2
        title = "PVP P2 KEY CONFIG"
        keys_dict = config.get("p2_keys", DEFAULT_PVP_P2_KEYS)
        key_actions = ["move_left", "move_right", "move_down", "rotate", "hard_drop", "hold"]
        action_labels = ["MOVE LEFT", "MOVE RIGHT", "MOVE DOWN", "ROTATE", "HARD DROP", "HOLD"]
        color = PINK
    
    draw_glow_text(screen, title, title_font, color, WIDTH//2, 40)
    if rebinding_key:
        draw_glow_text(screen, f"PRESS KEY FOR: {rebinding_key.upper()}", main_font, YELLOW, WIDTH//2, 100)
    
    buttons = {}
    panel_w = 700
    panel_x = (WIDTH - panel_w) // 2
    key_y = 140
    
    for i, (action, label) in enumerate(zip(key_actions, action_labels)):
        current_key_str = keys_dict.get(action, "left")
        key_display = get_key_display_name(get_key_constant(current_key_str))
        
        # Label
        render_bold_text(screen, f"{label}:", small_font, color, panel_x + 30, key_y + i*50, "left")
        
        # Button to click to rebind
        btn = draw_neon_button(screen, f"[{key_display}]", panel_x + 280, key_y + i*50 - 12, 350, 35, 
                               YELLOW if rebinding_key == action else GRAY, mouse_pos)
        buttons[action] = btn
    
    btn_back = draw_neon_button(screen, "< BACK", WIDTH//2 - 100, 620, 200, 50, RED, mouse_pos)
    buttons["back"] = btn_back
    
    return buttons

def draw_pause_menu(screen, mouse_pos, sys_config, game_state):
    """
    Vẽ màn hình Pause gọn — chỉ có các nút điều hướng.
    Âm thanh tách sang màn hình PAUSE_SOUND_MENU riêng.
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    draw_glow_text(screen, "PAUSED", title_font, CYAN, WIDTH//2, 130)

    buttons = {"sound": None, "keys_solo": None, "keys_p1": None, "keys_p2": None,
               "resume": None, "mode_select": None, "quit": None}

    btn_w, btn_h = 300, 52
    btn_x = WIDTH // 2 - btn_w // 2
    btn_y = 220
    gap = 62

    buttons["sound"] = draw_neon_button(screen, "SFX SETTINGS", btn_x, btn_y, btn_w, btn_h, PURPLE, mouse_pos)

    if game_state == "SOLO_GAME":
        buttons["keys_solo"] = draw_neon_button(screen, "KEY BINDINGS", btn_x, btn_y + gap, btn_w, btn_h, GREEN, mouse_pos)
    else:
        buttons["keys_p1"] = draw_neon_button(screen, "P1 KEYS", btn_x, btn_y + gap, btn_w // 2 - 5, btn_h, GREEN, mouse_pos)
        buttons["keys_p2"] = draw_neon_button(screen, "P2 KEYS", WIDTH // 2 + 5, btn_y + gap, btn_w // 2 - 5, btn_h, PINK, mouse_pos)

    buttons["resume"]      = draw_neon_button(screen, ">> RESUME",      btn_x, btn_y + gap * 2, btn_w, btn_h, YELLOW, mouse_pos)
    buttons["mode_select"] = draw_neon_button(screen, "<< MODE SELECT", btn_x, btn_y + gap * 3, btn_w, btn_h, CYAN,   mouse_pos)
    buttons["quit"]        = draw_neon_button(screen, "X  QUIT TO MENU", btn_x, btn_y + gap * 4, btn_w, btn_h, RED,    mouse_pos)

    return buttons


def draw_pause_sound_menu(screen, mouse_pos, sys_config):
    """
    Màn hình chỉnh âm thanh riêng khi game đang pause.
    Hiển thị 3 thanh trượt: Master Volume, Music, SFX.
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    draw_glow_text(screen, "SOUND SETTINGS", title_font, PURPLE, WIDTH // 2, 70)

    buttons = {"volume_slider": None, "music_slider": None, "sfx_slider": None, "back": None}
    panel_w = 500
    panel_x = (WIDTH - panel_w) // 2

    # MASTER VOLUME
    vol_y = 145
    vol_surf = pygame.Surface((panel_w, 90), pygame.SRCALPHA)
    pygame.draw.rect(vol_surf, (*CYAN, 35), vol_surf.get_rect(), border_radius=10)
    screen.blit(vol_surf, (panel_x, vol_y))
    pygame.draw.rect(screen, CYAN, (panel_x, vol_y, panel_w, 90), 2, border_radius=10)
    draw_glow_text(screen, "MASTER VOLUME", main_font, CYAN, WIDTH // 2, vol_y + 22, align="center")
    vol_value = sys_config.get("volume", 80)
    if isinstance(vol_value, str): vol_value = 100 if vol_value == "on" else 0
    buttons["volume_slider"] = draw_slider(screen, panel_x + 60, vol_y + 58, panel_w - 120, 14, 0, 100, vol_value, CYAN, WHITE, mouse_pos)
    draw_glow_text(screen, f"{vol_value}%", small_font, WHITE, panel_x + panel_w - 40, vol_y + 58, align="center")

    # MUSIC
    music_y = vol_y + 110
    music_surf = pygame.Surface((panel_w, 90), pygame.SRCALPHA)
    pygame.draw.rect(music_surf, (*PURPLE, 35), music_surf.get_rect(), border_radius=10)
    screen.blit(music_surf, (panel_x, music_y))
    pygame.draw.rect(screen, PURPLE, (panel_x, music_y, panel_w, 90), 2, border_radius=10)
    draw_glow_text(screen, "MUSIC", main_font, PURPLE, WIDTH // 2, music_y + 22, align="center")
    music_value = sys_config.get("music_volume", 70)
    if isinstance(music_value, str): music_value = 70
    buttons["music_slider"] = draw_slider(screen, panel_x + 60, music_y + 58, panel_w - 120, 14, 0, 100, music_value, PURPLE, WHITE, mouse_pos)
    draw_glow_text(screen, f"{music_value}%", small_font, WHITE, panel_x + panel_w - 40, music_y + 58, align="center")

    # SFX
    sfx_y = music_y + 110
    sfx_surf = pygame.Surface((panel_w, 90), pygame.SRCALPHA)
    pygame.draw.rect(sfx_surf, (*PINK, 35), sfx_surf.get_rect(), border_radius=10)
    screen.blit(sfx_surf, (panel_x, sfx_y))
    pygame.draw.rect(screen, PINK, (panel_x, sfx_y, panel_w, 90), 2, border_radius=10)
    draw_glow_text(screen, "SOUND EFFECTS", main_font, PINK, WIDTH // 2, sfx_y + 22, align="center")
    sfx_value = sys_config.get("sfx_volume", 80)
    if isinstance(sfx_value, str): sfx_value = 0 if sfx_value == "off" else 80
    buttons["sfx_slider"] = draw_slider(screen, panel_x + 60, sfx_y + 58, panel_w - 120, 14, 0, 100, sfx_value, PINK, WHITE, mouse_pos)
    draw_glow_text(screen, f"{sfx_value}%", small_font, WHITE, panel_x + panel_w - 40, sfx_y + 58, align="center")

    buttons["back"] = draw_neon_button(screen, "<< BACK", WIDTH // 2 - 100, sfx_y + 115, 200, 50, GRAY, mouse_pos)
    return buttons