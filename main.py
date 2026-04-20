# main.py
import pygame  # type: ignore
import sys
import random
from settings import *
from ui import *
from menus import *
from game_screens import *
from tetris_logic import TetrisLogic
from audio import init_audio, play_sfx, play_music, stop_music, update_audio_settings, set_master_volume
from ai import TetrisAI

# Helper: Check if key matches configured key
def key_matches(event_key, config_key_name, key_config):
    """
    Kiểm tra xem phím bấm (event_key) có khớp với cấu hình phím đã thiết lập hay không.
    Trả về True nếu khớp.
    """
    return event_key == get_key_constant(key_config.get(config_key_name, "left"))

# Config menu slider geometry (phải khớp với menus.py)
CONFIG_PANEL_W = 460
CONFIG_PANEL_X = (WIDTH - CONFIG_PANEL_W) // 2  # 220
VOL_SLIDER_TRACK_X = CONFIG_PANEL_X + 60      # 280
VOL_SLIDER_TRACK_Y = 130 + 55                 # 185
VOL_SLIDER_TRACK_W = CONFIG_PANEL_W - 120     # 340
VOL_SLIDER_TRACK_H = 12

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Cyberpunk Edition")
pygame.key.set_repeat(200, 50)

def main():
    """
    Hàm chính của chương trình.
    Khởi tạo game loop, xử lý sự kiện, cập nhật logic và vẽ giao diện
    tuỳ theo trạng thái hiện tại (Menu, Settings, Solo Game, PvP Game, v.v.).
    """
    clock = pygame.time.Clock()
    current_state = "MAIN_MENU"
    active_input = None
    volume_dragging = None
    keys_held = set()
    is_paused = False

    config_data = load_user_config()
    sys_config = config_data["sys"]
    solo_config = config_data["solo"]
    pvp_config = config_data["pvp"]
    config_dirty = False
    init_audio()
    update_audio_settings(sys_config)

    solo_logic = None
    fall_time = 0; particles = []
    game_mode = None
    blitz_time = 0
    solo_clear_played = False
    solo_game_over_sounded = False
    
    # Key rebinding state
    rebinding_key_mode = None  # "solo", "pvp_p1", or "pvp_p2"
    rebinding_key_action = None  # The action being rebound
    rebinding_key_from = None  # "config" or "pvp_settings" - where we came from

    p1_logic = None; p2_logic = None
    p1_ai = None; p2_ai = None
    p1_fall_time = 0; p2_fall_time = 0
    p1_particles = []; p2_particles = []
    p1_game_over_sounded = False
    p2_game_over_sounded = False

    def spawn_particles(logic, particles_list, offset_x=0, block_size=BLOCK_SIZE):
        # Tạo hiệu ứng hạt (particles) khi một dòng gạch bị phá huỷ.
        # Tính toán vị trí phát sinh hạt dưa trên toạ độ của các khối gạch đã bị xoá.
        if logic.cleared_blocks_anim:
            board_w = logic.cols * block_size
            board_x = offset_x + (WIDTH//2 - board_w) // 2 if offset_x != -1 else (WIDTH - board_w) // 2
            board_y = (HEIGHT - logic.rows * block_size) // 2
            for bx, by, color in logic.cleared_blocks_anim:
                px = board_x + bx * block_size
                py = board_y + by * block_size
                for _ in range(5):
                    particles_list.append(Particle(px + random.randint(0, block_size), py + random.randint(0, block_size), color))
            logic.cleared_blocks_anim.clear()

    while True:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        if current_state == "SOLO_GAME" and solo_logic:
            if not is_paused:
                if not solo_logic.game_over:
                    if game_mode == "BLITZ":
                        blitz_time -= dt
                        if blitz_time <= 0:
                            blitz_time = 0
                            solo_logic.game_over = True

                    if game_mode == "40L":
                        blitz_time += dt

                    fall_time += dt
                    if fall_time >= solo_logic.get_fall_speed():
                        fall_time = 0; solo_logic.move(0, 1)

                    if solo_logic.lines_cleared_this_turn > 0 and not solo_clear_played:
                        play_sfx("clear")
                        solo_clear_played = True
                    elif solo_logic.lines_cleared_this_turn == 0:
                        solo_clear_played = False

                if solo_logic.game_over and not solo_game_over_sounded:
                    play_sfx("game_over")
                    solo_game_over_sounded = True

                spawn_particles(solo_logic, particles, -1, 540 // solo_logic.rows)
                for p in particles[:]:
                    p.update()
                    if p.alpha <= 0: particles.remove(p)

        elif current_state == "PVP_GAME" and p1_logic and p2_logic:
            if not is_paused:
                game_ended = p1_logic.game_over or p2_logic.game_over

                if not game_ended:
                    if p1_ai: p1_ai.update(p1_logic, dt)
                    if p2_ai: p2_ai.update(p2_logic, dt)

                if not game_ended:
                    p1_fall_time += dt
                    if p1_fall_time >= p1_logic.get_fall_speed():
                        p1_fall_time = 0; p1_logic.move(0, 1)

                    p2_fall_time += dt
                    if p2_fall_time >= p2_logic.get_fall_speed():
                        p2_fall_time = 0; p2_logic.move(0, 1)

                p1_garbage = p1_logic.get_garbage_amount()
                p1_logic.get_and_reset_cleared_lines()
                if p1_garbage > 0: p2_logic.add_garbage_lines(p1_garbage)

                p2_garbage = p2_logic.get_garbage_amount()
                p2_logic.get_and_reset_cleared_lines()
                if p2_garbage > 0: p1_logic.add_garbage_lines(p2_garbage)

                if p1_garbage > 0 or p2_garbage > 0:
                    play_sfx("clear")

                if game_ended and not p2_game_over_sounded:
                    play_sfx("game_over")
                    p2_game_over_sounded = True

        for event in pygame.event.get():
            is_repeat = False
            if event.type == pygame.KEYDOWN:
                is_repeat = event.key in keys_held
                keys_held.add(event.key)
                
                if not is_repeat and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    if current_state in ("SOLO_GAME", "PVP_GAME"):
                        is_paused = not is_paused
                        play_sfx("button")
            elif event.type == pygame.KEYUP:
                keys_held.discard(event.key)

            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Handle key rebinding
            if current_state == "KEYCONFIG_MENU" and event.type == pygame.KEYDOWN and rebinding_key_action:
                if event.key == pygame.K_ESCAPE:
                    rebinding_key_action = None
                    play_sfx("button")
                else:
                    new_key_name = get_key_display_name(event.key).lower()
                    if new_key_name == "unknown" and event.unicode and event.unicode.isprintable() and len(event.unicode.strip()) > 0:
                        new_key_name = event.unicode.lower()
                        
                    if new_key_name != "unknown":
                        if rebinding_key_mode == "solo":
                            solo_config.setdefault("keys", DEFAULT_SOLO_KEYS.copy())[rebinding_key_action] = new_key_name
                        elif rebinding_key_mode == "pvp_p1":
                            pvp_config.setdefault("p1_keys", DEFAULT_PVP_P1_KEYS.copy())[rebinding_key_action] = new_key_name
                        elif rebinding_key_mode == "pvp_p2":
                            pvp_config.setdefault("p2_keys", DEFAULT_PVP_P2_KEYS.copy())[rebinding_key_action] = new_key_name
                        config_dirty = True
                        
                    rebinding_key_action = None
                    play_sfx("button")

            if current_state == "SOLO_GAME" and solo_logic and not solo_logic.game_over and not is_paused:
                if event.type == pygame.KEYDOWN:
                    keys = solo_config.get("keys", DEFAULT_SOLO_KEYS)
                    if key_matches(event.key, "move_left", keys):
                        solo_logic.move(-1, 0)
                        play_sfx("move")
                    elif key_matches(event.key, "move_right", keys):
                        solo_logic.move(1, 0)
                        play_sfx("move")
                    elif key_matches(event.key, "move_down", keys):
                        solo_logic.move(0, 1); fall_time = 0
                        play_sfx("move")
                    elif key_matches(event.key, "rotate", keys):
                        if not is_repeat:
                            solo_logic.rotate()
                            play_sfx("rotate")
                    elif key_matches(event.key, "hard_drop", keys):
                        if not is_repeat:
                            solo_logic.hard_drop(); fall_time = 0
                            play_sfx("hard_drop")
                    elif key_matches(event.key, "hold", keys):
                        if not is_repeat:
                            solo_logic.swap_hold()
                            play_sfx("hold")

            elif current_state == "PVP_GAME" and not p1_logic.game_over and not p2_logic.game_over and not is_paused:
                if event.type == pygame.KEYDOWN:
                    p1_keys = pvp_config.get("p1_keys", DEFAULT_PVP_P1_KEYS)
                    p2_keys = pvp_config.get("p2_keys", DEFAULT_PVP_P2_KEYS)
                    
                    if pvp_config["p1_type"] == "human":
                        if key_matches(event.key, "move_left", p1_keys):
                            p1_logic.move(-1, 0)
                            play_sfx("move")
                        elif key_matches(event.key, "move_right", p1_keys):
                            p1_logic.move(1, 0)
                            play_sfx("move")
                        elif key_matches(event.key, "move_down", p1_keys):
                            p1_logic.move(0, 1); p1_fall_time = 0
                            play_sfx("move")
                        elif key_matches(event.key, "rotate", p1_keys):
                            if not is_repeat:
                                p1_logic.rotate()
                                play_sfx("rotate")
                        elif key_matches(event.key, "hard_drop", p1_keys):
                            if not is_repeat:
                                p1_logic.hard_drop(); p1_fall_time = 0
                                play_sfx("hard_drop")
                        elif key_matches(event.key, "hold", p1_keys):
                            if not is_repeat:
                                p1_logic.swap_hold()
                                play_sfx("hold")

                    if pvp_config["p2_type"] == "human":
                        if key_matches(event.key, "move_left", p2_keys):
                            p2_logic.move(-1, 0)
                            play_sfx("move")
                        elif key_matches(event.key, "move_right", p2_keys):
                            p2_logic.move(1, 0)
                            play_sfx("move")
                        elif key_matches(event.key, "move_down", p2_keys):
                            p2_logic.move(0, 1); p2_fall_time = 0
                            play_sfx("move")
                        elif key_matches(event.key, "rotate", p2_keys):
                            if not is_repeat:
                                p2_logic.rotate()
                                play_sfx("rotate")
                        elif key_matches(event.key, "hard_drop", p2_keys):
                            if not is_repeat:
                                p2_logic.hard_drop(); p2_fall_time = 0
                                play_sfx("hard_drop")
                        elif key_matches(event.key, "hold", p2_keys):
                            if not is_repeat:
                                p2_logic.swap_hold()
                                play_sfx("hold")

            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE:
                    pvp_config[active_input] = pvp_config[active_input][:-1]
                    config_dirty = True
                elif event.key == pygame.K_RETURN:
                    active_input = None
                else:
                    if len(pvp_config[active_input]) < 10:
                        pvp_config[active_input] += event.unicode.upper()
                        config_dirty = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "MAIN_MENU":
                    b_solo, b_multi, b_conf, b_about, b_exit = draw_main_menu(screen, mouse_pos)
                    if b_solo.collidepoint(mouse_pos): current_state = "SOLO_MENU"
                    elif b_multi.collidepoint(mouse_pos): current_state = "PVP_SETTINGS"
                    elif b_conf.collidepoint(mouse_pos): current_state = "CONFIG_MENU"
                    elif b_about.collidepoint(mouse_pos): current_state = "ABOUT_MENU"
                    elif b_exit.collidepoint(mouse_pos): pygame.quit(); sys.exit()

                elif current_state == "ABOUT_MENU":
                    if draw_about_menu(screen, mouse_pos).collidepoint(mouse_pos): current_state = "MAIN_MENU"

                elif current_state == "CONFIG_MENU":
                    btn_back, btns = draw_config_menu(screen, mouse_pos, sys_config)
                    if btn_back.collidepoint(mouse_pos):
                        current_state = "MAIN_MENU"
                    elif btns["reset"].collidepoint(mouse_pos):
                        sys_config = DEFAULT_SYS_CONFIG.copy()
                        config_dirty = True
                        update_audio_settings(sys_config)
                        play_sfx("button")
                    else:
                        # Xử lý volume slider click (bắt đầu kéo)
                        if btns["volume_slider"]:
                            track_rect, thumb_rect = btns["volume_slider"]
                            if track_rect.collidepoint(mouse_pos) or thumb_rect.collidepoint(mouse_pos):
                                volume_dragging = track_rect
                                rel_x = mouse_pos[0] - track_rect.x
                                ratio = max(0.0, min(1.0, rel_x / track_rect.width))
                                new_vol = int(ratio * 100)
                                sys_config["volume"] = new_vol
                                config_dirty = True
                                set_master_volume(new_vol)
                        # Xử lý các toggle còn lại
                        for cat in ["sfx", "brightness"]:
                            for key, rect in btns[cat].items():
                                if rect.collidepoint(mouse_pos):
                                    sys_config[cat] = key
                                    config_dirty = True
                                    update_audio_settings(sys_config)
                                    play_sfx("button")
                        # Key config menu
                        if "keys" in btns and btns["keys"].collidepoint(mouse_pos):
                            current_state = "KEYCONFIG_MENU"
                            rebinding_key_mode = "solo"
                            rebinding_key_action = None
                            rebinding_key_from = "config"
                            play_sfx("button")

                elif current_state == "KEYCONFIG_MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Compute button positions WITHOUT rendering
                        key_y = 140
                        key_actions = ["move_left", "move_right", "move_down", "rotate", "hard_drop", "hold"]
                        btns = {}
                        # Back button position
                        btns["back"] = pygame.Rect(WIDTH//2 - 100, 620, 200, 50)
                        
                        panel_w = 700
                        panel_x = (WIDTH - panel_w) // 2
                        for i, action in enumerate(key_actions):
                            btns[action] = pygame.Rect(panel_x + 280, key_y + i*50 - 12, 350, 35)
                        
                        if "back" in btns and btns["back"].collidepoint(mouse_pos):
                            rebinding_key_action = None
                            rebinding_key_mode = None
                            # Map return state correctly
                            state_map = {
                                "config": "CONFIG_MENU",
                                "pvp_settings": "PVP_SETTINGS",
                                "pause_solo": "SOLO_GAME",
                                "pause_pvp": "PVP_GAME"
                            }
                            ret_state = state_map.get(rebinding_key_from, "CONFIG_MENU")
                            rebinding_key_from = None
                            current_state = ret_state
                            active_input = None
                            config_dirty = True
                            play_sfx("button")
                        else:
                            # Check which key action was clicked
                            for action in key_actions:
                                if action in btns and btns[action].collidepoint(mouse_pos):
                                    rebinding_key_action = action
                                    play_sfx("button")
                                    break

                elif current_state == "SOLO_MENU":
                    b_back, b_40l, b_blitz, b_custom = draw_solo_menu(screen, mouse_pos)
                    if b_back.collidepoint(mouse_pos):
                        current_state = "MAIN_MENU"
                    elif b_40l.collidepoint(mouse_pos):
                        config_40l = solo_config.copy()
                        config_40l["level_up"] = "off"  # Khóa level ở 1
                        solo_logic = TetrisLogic(config_40l)
                        fall_time = 0; particles.clear()
                        game_mode = "40L"
                        blitz_time = 0
                        solo_clear_played = False
                        solo_game_over_sounded = False
                        current_state = "SOLO_GAME"
                        play_sfx("button")
                    elif b_blitz.collidepoint(mouse_pos):
                        solo_logic = TetrisLogic(solo_config)
                        fall_time = 0; particles.clear()
                        game_mode = "BLITZ"
                        blitz_time = 120000
                        solo_clear_played = False
                        solo_game_over_sounded = False
                        current_state = "SOLO_GAME"
                        play_sfx("button")
                    elif b_custom.collidepoint(mouse_pos):
                        current_state = "SOLO_CUSTOM_MENU"
                        play_sfx("button")

                elif current_state == "SOLO_CUSTOM_MENU":
                    btns = draw_solo_custom_menu(screen, mouse_pos, solo_config)
                    if btns["back"].collidepoint(mouse_pos):
                        current_state = "SOLO_MENU"
                        play_sfx("button")
                    elif btns["start"].collidepoint(mouse_pos):
                        solo_logic = TetrisLogic(solo_config)
                        fall_time = 0; particles.clear()
                        solo_clear_played = False
                        solo_game_over_sounded = False
                        current_state = "SOLO_GAME"
                        play_sfx("button")
                    else:
                        for cat in ["level", "level_up", "grid", "ghost", "hold"]:
                            for key, rect in btns[cat].items():
                                if rect.collidepoint(mouse_pos):
                                    solo_config[cat] = key
                                    config_dirty = True

                elif current_state == "PVP_SETTINGS":
                    btns = draw_pvp_settings(screen, mouse_pos, pvp_config, active_input)
                    if btns["p1_name_box"].collidepoint(mouse_pos) and pvp_config["p1_type"] == "human": active_input = "p1_name"
                    elif btns["p2_name_box"].collidepoint(mouse_pos) and pvp_config["p2_type"] == "human": active_input = "p2_name"
                    else:
                        active_input = None
                        if btns["back"].collidepoint(mouse_pos): current_state = "MAIN_MENU"
                        elif btns["start"].collidepoint(mouse_pos):
                            p1_logic = TetrisLogic(pvp_config)
                            p2_logic = TetrisLogic(pvp_config)
                            p1_ai = TetrisAI(pvp_config["ai_diff"], pvp_config["ai_mode"]) if pvp_config["p1_type"] == "ai" else None
                            p2_ai = TetrisAI(pvp_config["ai_diff"], pvp_config["ai_mode"]) if pvp_config["p2_type"] == "ai" else None
                            p1_fall_time = 0; p2_fall_time = 0
                            p1_particles.clear(); p2_particles.clear()
                            p1_game_over_sounded = False
                            p2_game_over_sounded = False
                            current_state = "PVP_GAME"
                            play_sfx("button")
                        else:
                            for cat in ["level", "grid", "p1_color", "p1_type", "p2_color", "p2_type"]:
                                for key, rect in btns[cat].items():
                                    if rect.collidepoint(mouse_pos):
                                        if cat == "p1_type" and key == "ai" and pvp_config["p2_type"] != "ai": pvp_config["p1_name"] = "AI"
                                        elif cat == "p2_type" and key == "ai" and pvp_config["p1_type"] != "ai": pvp_config["p2_name"] = "AI"
                                        elif cat == "p1_type" and key == "human" and pvp_config["p1_type"] == "ai": pvp_config["p1_name"] = "PLAYER 1"
                                        elif cat == "p2_type" and key == "human" and pvp_config["p2_type"] == "ai": pvp_config["p2_name"] = "PLAYER 2"
                                        pvp_config[cat] = key
                                        config_dirty = True
                            if "ai_diff" in btns:
                                for key, rect in btns["ai_diff"].items():
                                    if rect.collidepoint(mouse_pos):
                                        pvp_config["ai_diff"] = key
                                        config_dirty = True
                            if "ai_mode" in btns:
                                for key, rect in btns["ai_mode"].items():
                                    if rect.collidepoint(mouse_pos):
                                        pvp_config["ai_mode"] = key
                                        config_dirty = True
                            # Key binding buttons
                            if "p1_keys" in btns and btns["p1_keys"].collidepoint(mouse_pos):
                                current_state = "KEYCONFIG_MENU"
                                rebinding_key_mode = "pvp_p1"
                                rebinding_key_action = None
                                rebinding_key_from = "pvp_settings"
                                play_sfx("button")
                            elif "p2_keys" in btns and btns["p2_keys"].collidepoint(mouse_pos):
                                current_state = "KEYCONFIG_MENU"
                                rebinding_key_mode = "pvp_p2"
                                rebinding_key_action = None
                                rebinding_key_from = "pvp_settings"
                                play_sfx("button")

                elif current_state in ("SOLO_GAME", "PVP_GAME") and is_paused:
                    btns = draw_pause_menu(screen, mouse_pos, sys_config, current_state)
                    if btns["resume"] and btns["resume"].collidepoint(mouse_pos):
                        is_paused = False
                        play_sfx("button")
                    elif btns["quit"] and btns["quit"].collidepoint(mouse_pos):
                        is_paused = False
                        current_state = "MAIN_MENU"
                        play_sfx("button")
                    elif btns["keys_solo"] and btns["keys_solo"].collidepoint(mouse_pos):
                        current_state = "KEYCONFIG_MENU"
                        rebinding_key_mode = "solo"
                        rebinding_key_action = None
                        rebinding_key_from = "pause_solo"
                        play_sfx("button")
                    elif btns["keys_p1"] and btns["keys_p1"].collidepoint(mouse_pos):
                        current_state = "KEYCONFIG_MENU"
                        rebinding_key_mode = "pvp_p1"
                        rebinding_key_action = None
                        rebinding_key_from = "pause_pvp"
                        play_sfx("button")
                    elif btns["keys_p2"] and btns["keys_p2"].collidepoint(mouse_pos):
                        current_state = "KEYCONFIG_MENU"
                        rebinding_key_mode = "pvp_p2"
                        rebinding_key_action = None
                        rebinding_key_from = "pause_pvp"
                        play_sfx("button")
                    elif btns["volume_slider"]:
                        track_rect, thumb_rect = btns["volume_slider"]
                        if track_rect.collidepoint(mouse_pos) or thumb_rect.collidepoint(mouse_pos):
                            volume_dragging = track_rect
                            rel_x = mouse_pos[0] - track_rect.x
                            ratio = max(0.0, min(1.0, rel_x / track_rect.width))
                            new_vol = int(ratio * 100)
                            sys_config["volume"] = new_vol
                            config_dirty = True
                            set_master_volume(new_vol)
                            
                elif current_state == "SOLO_GAME" and not is_paused:
                    btns = draw_play_screen_solo(screen, mouse_pos, solo_logic, particles, game_mode, blitz_time)
                    if btns["menu"] and btns["menu"].collidepoint(mouse_pos):
                        game_mode = None
                        current_state = "MAIN_MENU"
                        play_sfx("button")
                    elif btns.get("pause") and btns["pause"].collidepoint(mouse_pos):
                        is_paused = True
                        play_sfx("button")
                    elif btns["retry"] and btns["retry"].collidepoint(mouse_pos):
                        solo_logic = TetrisLogic(solo_config)
                        fall_time = 0; particles.clear()
                        if game_mode == "BLITZ": blitz_time = 120000

                elif current_state == "PVP_GAME" and not is_paused:
                    btns = draw_pvp_screen(screen, mouse_pos, pvp_config, p1_logic, p2_logic, p1_particles, p2_particles)
                    if btns["menu"] and btns["menu"].collidepoint(mouse_pos): 
                        current_state = "MAIN_MENU"
                        play_sfx("button")
                    elif btns.get("pause") and btns["pause"].collidepoint(mouse_pos):
                        is_paused = True
                        play_sfx("button")
                    elif btns["retry"] and btns["retry"].collidepoint(mouse_pos):
                        p1_logic = TetrisLogic(pvp_config)
                        p2_logic = TetrisLogic(pvp_config)
                        p1_fall_time = 0; p2_fall_time = 0
                        p1_particles.clear(); p2_particles.clear()

            if event.type == pygame.MOUSEMOTION:
                if volume_dragging is not None:
                    track_rect = volume_dragging
                    rel_x = mouse_pos[0] - track_rect.x
                    ratio = max(0.0, min(1.0, rel_x / track_rect.width))
                    new_vol = int(ratio * 100)
                    if sys_config["volume"] != new_vol:
                        sys_config["volume"] = new_vol
                        config_dirty = True
                        set_master_volume(new_vol)
            if event.type == pygame.MOUSEBUTTONUP:
                volume_dragging = None

        if current_state == "MAIN_MENU": draw_main_menu(screen, mouse_pos)
        elif current_state == "ABOUT_MENU": draw_about_menu(screen, mouse_pos)
        elif current_state == "CONFIG_MENU": draw_config_menu(screen, mouse_pos, sys_config)
        elif current_state == "KEYCONFIG_MENU":
            # ALWAYS render to prevent freeze
            if rebinding_key_mode:
                draw_keyconfig_menu(screen, mouse_pos, rebinding_key_mode, 
                                    solo_config if rebinding_key_mode == "solo" else pvp_config,
                                    rebinding_key_action)
            else:
                # Fallback if mode lost
                current_state = "CONFIG_MENU"
        elif current_state == "SOLO_MENU": draw_solo_menu(screen, mouse_pos)
        elif current_state == "SOLO_CUSTOM_MENU": draw_solo_custom_menu(screen, mouse_pos, solo_config)
        elif current_state == "PVP_SETTINGS": draw_pvp_settings(screen, mouse_pos, pvp_config, active_input)
        elif current_state == "SOLO_GAME": draw_play_screen_solo(screen, mouse_pos, solo_logic, particles, game_mode, blitz_time)
        elif current_state == "PVP_GAME": draw_pvp_screen(screen, mouse_pos, pvp_config, p1_logic, p2_logic, p1_particles, p2_particles)

        if current_state in ("SOLO_GAME", "PVP_GAME") and is_paused:
            draw_pause_menu(screen, mouse_pos, sys_config, current_state)

        if config_dirty:
            save_user_config({"sys": sys_config, "solo": solo_config, "pvp": pvp_config})
            config_dirty = False

        if sys_config["brightness"] == "dim":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))
            screen.blit(overlay, (0, 0))
        elif sys_config["brightness"] == "bright":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 40))
            screen.blit(overlay, (0, 0))

        pygame.display.flip()

if __name__ == "__main__":
    main()
