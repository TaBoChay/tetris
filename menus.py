# menus.py
import pygame
from settings import *
from ui import *

def draw_main_menu(screen, mouse_pos):
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    draw_glow_text(screen, "TETRIS", title_font, CYAN, WIDTH//2, 100)
    
    btn_w, btn_h = 350, 55; start_x = (WIDTH - btn_w) // 2
    b_solo = draw_neon_button(screen, "SOLO", start_x, 190, btn_w, btn_h, GREEN, mouse_pos)
    b_multi = draw_neon_button(screen, "MULTIPLAYER", start_x, 260, btn_w, btn_h, PINK, mouse_pos)
    b_conf = draw_neon_button(screen, "CONFIG", start_x, 330, btn_w, btn_h, YELLOW, mouse_pos)
    b_about = draw_neon_button(screen, "ABOUT", start_x, 400, btn_w, btn_h, CYAN, mouse_pos)
    b_exit = draw_neon_button(screen, "EXIT", start_x, 470, btn_w, btn_h, RED, mouse_pos)
    
    return b_solo, b_multi, b_conf, b_about, b_exit

def draw_about_menu(screen, mouse_pos):
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    
    draw_glow_text(screen, "ABOUT THE GAME", title_font, CYAN, WIDTH//2, 50)
    
    p1_x, p1_y, p1_w, p1_h = 60, 110, 330, 200
    p1_surf = pygame.Surface((p1_w, p1_h), pygame.SRCALPHA)
    pygame.draw.rect(p1_surf, (*CYAN, 30), p1_surf.get_rect(), border_radius=8)
    screen.blit(p1_surf, (p1_x, p1_y))
    pygame.draw.rect(screen, CYAN, (p1_x, p1_y, p1_w, p1_h), 2, border_radius=8)
    draw_glow_text(screen, "RULES", main_font, CYAN, p1_x + p1_w//2, p1_y + 25)
    rules = ["• Fill horizontal lines", "  with blocks to clear.", "", "• Speed increases as", "  the Level goes up.", "", "• Game Over when blocks", "  reach the top."]
    for i, line in enumerate(rules):
        render_bold_text(screen, line, small_font, WHITE, p1_x + 20, p1_y + 70 + i*16, "left")

    p2_x, p2_y, p2_w, p2_h = 410, 110, 330, 200
    p2_surf = pygame.Surface((p2_w, p2_h), pygame.SRCALPHA)
    pygame.draw.rect(p2_surf, (*PINK, 30), p2_surf.get_rect(), border_radius=8)
    screen.blit(p2_surf, (p2_x, p2_y))
    pygame.draw.rect(screen, PINK, (p2_x, p2_y, p2_w, p2_h), 2, border_radius=8)
    draw_glow_text(screen, "CONTROLS", main_font, PINK, p2_x + p2_w//2, p2_y + 25)
    controls = ["[ SOLO & PLAYER 2 ]", "• Arrows: Move", "• Up: Rotate", "• / or Space: Hold", "", "[ PLAYER 1 PVP ]", "• W/A/S/D: Move", "• Z: Hold piece"]
    for i, line in enumerate(controls):
        render_bold_text(screen, line, small_font, WHITE, p2_x + 20, p2_y + 60 + i*16, "left")

    p3_x, p3_y, p3_w, p3_h = 60, 330, 680, 160
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
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    btn_back = draw_neon_button(screen, "< BACK", 30, 30, 120, 40, PINK, mouse_pos)
    draw_glow_text(screen, "SETTINGS", title_font, CYAN, WIDTH//2, 50)
    draw_glow_text(screen, "System Configuration", small_font, PINK, WIDTH//2, 90)

    buttons = {"volume": {}, "sfx": {}, "brightness": {}}
    panel_w = 460; panel_x = (WIDTH - panel_w) // 2

    vol_y = 130
    vol_surf = pygame.Surface((panel_w, 100), pygame.SRCALPHA)
    pygame.draw.rect(vol_surf, (*CYAN, 30), vol_surf.get_rect(), border_radius=8)
    screen.blit(vol_surf, (panel_x, vol_y))
    pygame.draw.rect(screen, CYAN, (panel_x, vol_y, panel_w, 100), 2, border_radius=8)
    draw_glow_text(screen, "VOLUME", main_font, CYAN, WIDTH//2, vol_y + 25, align="center")
    buttons["volume"]["on"] = draw_toggle_button(screen, "ON", WIDTH//2 - 90, vol_y + 50, 80, 35, GREEN, mouse_pos, sys_config["volume"] == "on")
    buttons["volume"]["off"] = draw_toggle_button(screen, "OFF", WIDTH//2 + 10, vol_y + 50, 80, 35, RED, mouse_pos, sys_config["volume"] == "off")

    sfx_y = 250
    sfx_surf = pygame.Surface((panel_w, 100), pygame.SRCALPHA)
    pygame.draw.rect(sfx_surf, (*PINK, 30), sfx_surf.get_rect(), border_radius=8)
    screen.blit(sfx_surf, (panel_x, sfx_y))
    pygame.draw.rect(screen, PINK, (panel_x, sfx_y, panel_w, 100), 2, border_radius=8)
    draw_glow_text(screen, "SOUND EFFECTS", main_font, PINK, WIDTH//2, sfx_y + 25, align="center")
    buttons["sfx"]["on"] = draw_toggle_button(screen, "ON", WIDTH//2 - 90, sfx_y + 50, 80, 35, GREEN, mouse_pos, sys_config["sfx"] == "on")
    buttons["sfx"]["off"] = draw_toggle_button(screen, "OFF", WIDTH//2 + 10, sfx_y + 50, 80, 35, RED, mouse_pos, sys_config["sfx"] == "off")

    bri_y = 370
    bri_surf = pygame.Surface((panel_w, 100), pygame.SRCALPHA)
    pygame.draw.rect(bri_surf, (*YELLOW, 30), bri_surf.get_rect(), border_radius=8)
    screen.blit(bri_surf, (panel_x, bri_y))
    pygame.draw.rect(screen, YELLOW, (panel_x, bri_y, panel_w, 100), 2, border_radius=8)
    draw_glow_text(screen, "BRIGHTNESS", main_font, YELLOW, WIDTH//2, bri_y + 25, align="center")
    buttons["brightness"]["dim"] = draw_toggle_button(screen, "DIM", WIDTH//2 - 165, bri_y + 50, 100, 35, PURPLE, mouse_pos, sys_config["brightness"] == "dim")
    buttons["brightness"]["normal"] = draw_toggle_button(screen, "NORMAL", WIDTH//2 - 50, bri_y + 50, 100, 35, YELLOW, mouse_pos, sys_config["brightness"] == "normal")
    buttons["brightness"]["bright"] = draw_toggle_button(screen, "BRIGHT", WIDTH//2 + 65, bri_y + 50, 100, 35, CYAN, mouse_pos, sys_config["brightness"] == "bright")

    buttons["reset"] = draw_neon_button(screen, "RESET DEFAULTS", WIDTH//2 - 150, 500, 300, 50, GRAY, mouse_pos)
    return btn_back, buttons

def draw_pvp_settings(screen, mouse_pos, config, active_input):
    screen.fill(BG_COLOR)
    for block in floating_blocks: block.update(); block.draw(screen)
    draw_glow_text(screen, "PVP SETTINGS", title_font, CYAN, WIDTH//2, 40)
    buttons = {"level": {}, "grid": {}, "ai_diff": {}, "p1_color": {}, "p1_type": {}, "p2_color": {}, "p2_type": {}}
    
    draw_glow_text(screen, "> START LEVEL", main_font, CYAN, 80, 90, align="left")
    buttons["level"]["1"] = draw_toggle_button(screen, "LV 1", 280, 75, 80, 35, GREEN, mouse_pos, config["level"] == "1")
    buttons["level"]["5"] = draw_toggle_button(screen, "LV 5", 370, 75, 80, 35, YELLOW, mouse_pos, config["level"] == "5")
    buttons["level"]["10"] = draw_toggle_button(screen, "LV 10", 460, 75, 80, 35, ORANGE, mouse_pos, config["level"] == "10")
    buttons["level"]["15"] = draw_toggle_button(screen, "LV 15", 550, 75, 80, 35, RED, mouse_pos, config["level"] == "15")

    draw_glow_text(screen, "> GRID SIZE", main_font, PINK, 80, 140, align="left")
    buttons["grid"]["8x15"] = draw_toggle_button(screen, "8x15", 280, 125, 100, 35, GREEN, mouse_pos, config["grid"] == "8x15")
    buttons["grid"]["10x20"] = draw_toggle_button(screen, "10x20", 390, 125, 120, 35, YELLOW, mouse_pos, config["grid"] == "10x20")
    buttons["grid"]["12x25"] = draw_toggle_button(screen, "12x25", 520, 125, 100, 35, RED, mouse_pos, config["grid"] == "12x25")

    show_ai_settings = config["p1_type"] == "ai" or config["p2_type"] == "ai"
    if show_ai_settings:
        draw_glow_text(screen, "> AI DIFFICULTY", main_font, RED, 80, 190, align="left")
        buttons["ai_diff"]["easy"] = draw_toggle_button(screen, "EASY", 280, 175, 100, 35, GREEN, mouse_pos, config["ai_diff"] == "easy")
        buttons["ai_diff"]["normal"] = draw_toggle_button(screen, "NORMAL", 390, 175, 120, 35, YELLOW, mouse_pos, config["ai_diff"] == "normal")
        buttons["ai_diff"]["hard"] = draw_toggle_button(screen, "HARD", 520, 175, 100, 35, RED, mouse_pos, config["ai_diff"] == "hard")

    panel_y = 230
    p1_x, p1_w, p1_h = 60, 320, 230
    p2_x, p2_w, p2_h = 420, 320, 230

    p1_surf = pygame.Surface((p1_w, p1_h), pygame.SRCALPHA)
    pygame.draw.rect(p1_surf, (*CYAN, 30), p1_surf.get_rect(), border_radius=8)
    screen.blit(p1_surf, (p1_x, panel_y))
    pygame.draw.rect(screen, CYAN, (p1_x, panel_y, p1_w, p1_h), 2, border_radius=8)
    
    p2_surf = pygame.Surface((p2_w, p2_h), pygame.SRCALPHA)
    pygame.draw.rect(p2_surf, (*PINK, 30), p2_surf.get_rect(), border_radius=8)
    screen.blit(p2_surf, (p2_x, panel_y))
    pygame.draw.rect(screen, PINK, (p2_x, panel_y, p2_w, p2_h), 2, border_radius=8)

    draw_glow_text(screen, "PLAYER 1", main_font, CYAN, p1_x + p1_w//2, panel_y + 20)
    draw_glow_text(screen, "PLAYER 2", main_font, PINK, p2_x + p2_w//2, panel_y + 20)

    draw_glow_text(screen, "NAME", small_font, WHITE, p1_x + p1_w//2, panel_y + 50)
    draw_glow_text(screen, "NAME", small_font, WHITE, p2_x + p2_w//2, panel_y + 50)
    
    buttons["p1_name_box"] = pygame.Rect(p1_x + 30, panel_y + 65, 260, 35)
    buttons["p2_name_box"] = pygame.Rect(p2_x + 30, panel_y + 65, 260, 35)
    
    pygame.draw.rect(screen, CYAN if active_input == "p1_name" else (*CYAN, 80), buttons["p1_name_box"], 2, border_radius=4)
    pygame.draw.rect(screen, PINK if active_input == "p2_name" else (*PINK, 80), buttons["p2_name_box"], 2, border_radius=4)
    
    cursor = "_" if (pygame.time.get_ticks() % 1000 < 500) else ""
    p1_display = config["p1_name"] + (cursor if active_input == "p1_name" else "")
    p2_display = config["p2_name"] + (cursor if active_input == "p2_name" else "")
    render_bold_text(screen, p1_display, small_font, CYAN, buttons["p1_name_box"].centerx, buttons["p1_name_box"].centery, "center")
    render_bold_text(screen, p2_display, small_font, PINK, buttons["p2_name_box"].centerx, buttons["p2_name_box"].centery, "center")

    draw_glow_text(screen, "COLOR", small_font, WHITE, p1_x + p1_w//2, panel_y + 115)
    buttons["p1_color"]["cyan"] = draw_toggle_button(screen, "CYN", p1_x + 30, panel_y + 130, 60, 30, CYAN, mouse_pos, config["p1_color"] == "cyan")
    buttons["p1_color"]["lime"] = draw_toggle_button(screen, "LIM", p1_x + 100, panel_y + 130, 60, 30, GREEN, mouse_pos, config["p1_color"] == "lime")
    buttons["p1_color"]["gold"] = draw_toggle_button(screen, "GLD", p1_x + 170, panel_y + 130, 60, 30, YELLOW, mouse_pos, config["p1_color"] == "gold")
    buttons["p1_color"]["red"] = draw_toggle_button(screen, "RED", p1_x + 240, panel_y + 130, 60, 30, RED, mouse_pos, config["p1_color"] == "red")

    draw_glow_text(screen, "COLOR", small_font, WHITE, p2_x + p2_w//2, panel_y + 115)
    buttons["p2_color"]["pink"] = draw_toggle_button(screen, "PNK", p2_x + 30, panel_y + 130, 60, 30, PINK, mouse_pos, config["p2_color"] == "pink")
    buttons["p2_color"]["lime"] = draw_toggle_button(screen, "LIM", p2_x + 100, panel_y + 130, 60, 30, GREEN, mouse_pos, config["p2_color"] == "lime")
    buttons["p2_color"]["gold"] = draw_toggle_button(screen, "GLD", p2_x + 170, panel_y + 130, 60, 30, YELLOW, mouse_pos, config["p2_color"] == "gold")
    buttons["p2_color"]["cyan"] = draw_toggle_button(screen, "CYN", p2_x + 240, panel_y + 130, 60, 30, CYAN, mouse_pos, config["p2_color"] == "cyan")

    p1_ai_color = GRAY if config["p2_type"] == "ai" else RED
    p2_ai_color = GRAY if config["p1_type"] == "ai" else RED

    draw_glow_text(screen, "OPPONENT TYPE", small_font, WHITE, p1_x + p1_w//2, panel_y + 175)
    buttons["p1_type"]["human"] = draw_toggle_button(screen, "HUMAN", p1_x + 50, panel_y + 190, 100, 30, GREEN, mouse_pos, config["p1_type"] == "human")
    buttons["p1_type"]["ai"] = draw_toggle_button(screen, "AI", p1_x + 170, panel_y + 190, 100, 30, p1_ai_color, mouse_pos, config["p1_type"] == "ai")

    draw_glow_text(screen, "OPPONENT TYPE", small_font, WHITE, p2_x + p2_w//2, panel_y + 175)
    buttons["p2_type"]["human"] = draw_toggle_button(screen, "HUMAN", p2_x + 50, panel_y + 190, 100, 30, GREEN, mouse_pos, config["p2_type"] == "human")
    buttons["p2_type"]["ai"] = draw_toggle_button(screen, "AI", p2_x + 170, panel_y + 190, 100, 30, p2_ai_color, mouse_pos, config["p2_type"] == "ai")

    buttons["back"] = draw_neon_button(screen, "< BACK", 120, 485, 220, 50, RED, mouse_pos)
    buttons["start"] = draw_neon_button(screen, "START PVP >", 460, 485, 220, 50, GREEN, mouse_pos)

    return buttons