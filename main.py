# main.py
import pygame
import sys
import random
from settings import *
from ui import *
from menus import *
from game_screens import *
from tetris_logic import TetrisLogic
from ai import TetrisAI # <--- Kéo AI vào

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Cyberpunk Edition")
pygame.key.set_repeat(200, 50) 

def main():
    clock = pygame.time.Clock()
    current_state = "MAIN_MENU"
    active_input = None 
    
    sys_config = {"volume": "on", "sfx": "on", "brightness": "normal"}
    solo_config = {"level": "1", "grid": "10x20", "ghost": "on", "hold": "on"}
    pvp_config = {
        "level": "1", "grid": "10x20", "ai_diff": "normal",
        "p1_name": "PLAYER 1", "p1_color": "cyan", "p1_type": "human",
        "p2_name": "PLAYER 2", "p2_color": "pink", "p2_type": "human"
    }
    
    # Biến cho Solo
    solo_logic = None
    fall_time = 0; particles = [] 

    # Biến cho PvP
    p1_logic = None; p2_logic = None
    p1_ai = None; p2_ai = None
    p1_fall_time = 0; p2_fall_time = 0
    p1_particles = []; p2_particles = []

    def spawn_particles(logic, particles_list, offset_x=0, block_size=BLOCK_SIZE):
        if logic.cleared_blocks_anim:
            board_w = logic.cols * block_size
            board_x = offset_x + (WIDTH//2 - board_w) // 2 if offset_x != -1 else (WIDTH - board_w) // 2
            board_y = 80 if offset_x != -1 else 60
            for bx, by, color in logic.cleared_blocks_anim:
                px = board_x + bx * block_size
                py = board_y + by * block_size
                for _ in range(5):
                    particles_list.append(Particle(px + random.randint(0, block_size), py + random.randint(0, block_size), color))
            logic.cleared_blocks_anim.clear()

    while True:
        dt = clock.tick(60) 
        mouse_pos = pygame.mouse.get_pos()
        
        # --- CẬP NHẬT LOGIC SOLO ---
        if current_state == "SOLO_GAME" and solo_logic:
            if not solo_logic.game_over:
                fall_time += dt
                if fall_time >= solo_logic.get_fall_speed():
                    fall_time = 0; solo_logic.move(0, 1)

            spawn_particles(solo_logic, particles, -1, 500 // solo_logic.rows)
            for p in particles[:]:
                p.update()
                if p.alpha <= 0: particles.remove(p)

        # --- CẬP NHẬT LOGIC PVP ---
        elif current_state == "PVP_GAME" and p1_logic and p2_logic:
            # 1. Update AI
            if p1_ai: p1_ai.update(p1_logic, dt)
            if p2_ai: p2_ai.update(p2_logic, dt)

            # 2. Rơi gạch tự động
            if not p1_logic.game_over and not p2_logic.game_over:
                p1_fall_time += dt
                if p1_fall_time >= p1_logic.get_fall_speed():
                    p1_fall_time = 0; p1_logic.move(0, 1)

                p2_fall_time += dt
                if p2_fall_time >= p2_logic.get_fall_speed():
                    p2_fall_time = 0; p2_logic.move(0, 1)

            # 3. Kích hoạt dòng rác (Garbage Lines)
            p1_cleared = p1_logic.get_and_reset_cleared_lines()
            if p1_cleared >= 2: p2_logic.add_garbage_lines(p1_cleared - 1)

            p2_cleared = p2_logic.get_and_reset_cleared_lines()
            if p2_cleared >= 2: p1_logic.add_garbage_lines(p2_cleared - 1)

            # 4. Vẽ hạt vụn PVP
            bs = PVP_BLOCK_SIZE
            spawn_particles(p1_logic, p1_particles, 0, bs)
            spawn_particles(p2_logic, p2_particles, 400, bs)
            for p in p1_particles[:]: 
                p.update()
                if p.alpha <= 0: p1_particles.remove(p)
            for p in p2_particles[:]:
                p.update()
                if p.alpha <= 0: p2_particles.remove(p)

        # XỬ LÝ SỰ KIỆN PHÍM BẤM
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if current_state == "SOLO_GAME" and solo_logic and not solo_logic.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: solo_logic.move(-1, 0)
                    elif event.key == pygame.K_RIGHT: solo_logic.move(1, 0)
                    elif event.key == pygame.K_DOWN: solo_logic.move(0, 1); fall_time = 0 
                    elif event.key == pygame.K_UP: solo_logic.rotate()
                    elif event.key == pygame.K_SPACE: solo_logic.hard_drop(); fall_time = 0
                    elif event.key in (pygame.K_z, pygame.K_SLASH): solo_logic.swap_hold()

            elif current_state == "PVP_GAME" and not p1_logic.game_over and not p2_logic.game_over:
                if event.type == pygame.KEYDOWN:
                    # PLAYER 1 (WASD)
                    if pvp_config["p1_type"] == "human":
                        if event.key == pygame.K_a: p1_logic.move(-1, 0)
                        elif event.key == pygame.K_d: p1_logic.move(1, 0)
                        elif event.key == pygame.K_s: p1_logic.move(0, 1); p1_fall_time = 0
                        elif event.key == pygame.K_w: p1_logic.rotate()
                        elif event.key == pygame.K_q: p1_logic.hard_drop(); p1_fall_time = 0
                        elif event.key == pygame.K_z: p1_logic.swap_hold()
                    
                    # PLAYER 2 (ARROWS)
                    if pvp_config["p2_type"] == "human":
                        if event.key == pygame.K_LEFT: p2_logic.move(-1, 0)
                        elif event.key == pygame.K_RIGHT: p2_logic.move(1, 0)
                        elif event.key == pygame.K_DOWN: p2_logic.move(0, 1); p2_fall_time = 0
                        elif event.key == pygame.K_UP: p2_logic.rotate()
                        elif event.key == pygame.K_SPACE: p2_logic.hard_drop(); p2_fall_time = 0
                        elif event.key == pygame.K_SLASH: p2_logic.swap_hold()

            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_BACKSPACE: pvp_config[active_input] = pvp_config[active_input][:-1]
                elif event.key == pygame.K_RETURN: active_input = None
                else:
                    if len(pvp_config[active_input]) < 10: pvp_config[active_input] += event.unicode.upper()

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
                    if btn_back.collidepoint(mouse_pos): current_state = "MAIN_MENU"
                    elif btns["reset"].collidepoint(mouse_pos): sys_config = {"volume": "on", "sfx": "on", "brightness": "normal"}
                    else:
                        for cat in ["volume", "sfx", "brightness"]:
                            for key, rect in btns[cat].items():
                                if rect.collidepoint(mouse_pos): sys_config[cat] = key

                elif current_state == "SOLO_MENU":
                    b_back, b_40l, b_blitz, b_custom = draw_solo_menu(screen, mouse_pos)
                    if b_back.collidepoint(mouse_pos): 
                        current_state = "MAIN_MENU"
                    elif b_40l.collidepoint(mouse_pos) or b_blitz.collidepoint(mouse_pos): 
                        solo_logic = TetrisLogic(solo_config) 
                        fall_time = 0; particles.clear()
                        current_state = "SOLO_GAME"
                    elif b_custom.collidepoint(mouse_pos): 
                        current_state = "SOLO_CUSTOM_MENU"
                
                elif current_state == "SOLO_CUSTOM_MENU":
                    btns = draw_solo_custom_menu(screen, mouse_pos, solo_config)
                    if btns["back"].collidepoint(mouse_pos): current_state = "SOLO_MENU"
                    elif btns["start"].collidepoint(mouse_pos):
                        solo_logic = TetrisLogic(solo_config) 
                        fall_time = 0; particles.clear()
                        current_state = "SOLO_GAME"
                    else:
                        for cat in ["level", "grid", "ghost", "hold"]:
                            for key, rect in btns[cat].items():
                                if rect.collidepoint(mouse_pos): solo_config[cat] = key
                
                elif current_state == "PVP_SETTINGS":
                    btns = draw_pvp_settings(screen, mouse_pos, pvp_config, active_input)
                    if btns["p1_name_box"].collidepoint(mouse_pos) and pvp_config["p1_type"] == "human": active_input = "p1_name"
                    elif btns["p2_name_box"].collidepoint(mouse_pos) and pvp_config["p2_type"] == "human": active_input = "p2_name"
                    else:
                        active_input = None
                        if btns["back"].collidepoint(mouse_pos): current_state = "MAIN_MENU"
                        elif btns["start"].collidepoint(mouse_pos):
                            # KHỞI TẠO VÁN ĐẤU PVP
                            p1_logic = TetrisLogic(pvp_config)
                            p2_logic = TetrisLogic(pvp_config)
                            p1_ai = TetrisAI(pvp_config["ai_diff"]) if pvp_config["p1_type"] == "ai" else None
                            p2_ai = TetrisAI(pvp_config["ai_diff"]) if pvp_config["p2_type"] == "ai" else None
                            p1_fall_time = 0; p2_fall_time = 0
                            p1_particles.clear(); p2_particles.clear()
                            current_state = "PVP_GAME" 
                        else:
                            for cat in ["level", "grid", "p1_color", "p1_type", "p2_color", "p2_type"]:
                                for key, rect in btns[cat].items():
                                    if rect.collidepoint(mouse_pos):
                                        if cat == "p1_type" and key == "ai" and pvp_config["p2_type"] != "ai": pvp_config["p1_name"] = "AI"
                                        elif cat == "p2_type" and key == "ai" and pvp_config["p1_type"] != "ai": pvp_config["p2_name"] = "AI"
                                        elif cat == "p1_type" and key == "human" and pvp_config["p1_type"] == "ai": pvp_config["p1_name"] = "PLAYER 1"
                                        elif cat == "p2_type" and key == "human" and pvp_config["p2_type"] == "ai": pvp_config["p2_name"] = "PLAYER 2"
                                        pvp_config[cat] = key
                            if "ai_diff" in btns:
                                for key, rect in btns["ai_diff"].items():
                                    if rect.collidepoint(mouse_pos): pvp_config["ai_diff"] = key
                                
                elif current_state == "SOLO_GAME":
                    btns = draw_play_screen_solo(screen, mouse_pos, solo_logic, particles)
                    if btns["menu"] and btns["menu"].collidepoint(mouse_pos): current_state = "MAIN_MENU"
                    elif btns["retry"] and btns["retry"].collidepoint(mouse_pos):
                        solo_logic = TetrisLogic(solo_config) 
                        fall_time = 0; particles.clear()
                    
                elif current_state == "PVP_GAME":
                    btns = draw_pvp_screen(screen, mouse_pos, pvp_config, p1_logic, p2_logic, p1_particles, p2_particles)
                    if btns["menu"].collidepoint(mouse_pos): current_state = "MAIN_MENU"
                    elif btns["retry"] and btns["retry"].collidepoint(mouse_pos):
                        # CHƠI LẠI PVP
                        p1_logic = TetrisLogic(pvp_config)
                        p2_logic = TetrisLogic(pvp_config)
                        p1_fall_time = 0; p2_fall_time = 0
                        p1_particles.clear(); p2_particles.clear()

        # RENDER GIAO DIỆN
        if current_state == "MAIN_MENU": draw_main_menu(screen, mouse_pos)
        elif current_state == "ABOUT_MENU": draw_about_menu(screen, mouse_pos)
        elif current_state == "CONFIG_MENU": draw_config_menu(screen, mouse_pos, sys_config)
        elif current_state == "SOLO_MENU": draw_solo_menu(screen, mouse_pos)
        elif current_state == "SOLO_CUSTOM_MENU": draw_solo_custom_menu(screen, mouse_pos, solo_config)
        elif current_state == "PVP_SETTINGS": draw_pvp_settings(screen, mouse_pos, pvp_config, active_input)
        elif current_state == "SOLO_GAME": draw_play_screen_solo(screen, mouse_pos, solo_logic, particles)
        elif current_state == "PVP_GAME": draw_pvp_screen(screen, mouse_pos, pvp_config, p1_logic, p2_logic, p1_particles, p2_particles)
            
        pygame.display.flip()

if __name__ == "__main__":
    main()