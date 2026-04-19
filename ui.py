# ui.py
import pygame  # type: ignore
import random
from settings import *

pygame.init()

# --- HỆ THỐNG FONT CHỮ ---
try:
    title_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
    main_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    small_font = pygame.font.Font("PressStart2P-Regular.ttf", 10)
    tiny_font = pygame.font.Font("PressStart2P-Regular.ttf", 8)
except:
    title_font = pygame.font.SysFont("Courier", 50, bold=True)
    main_font = pygame.font.SysFont("Courier", 20, bold=True)
    small_font = pygame.font.SysFont("Courier", 14)
    tiny_font = pygame.font.SysFont("Courier", 10)

def draw_shape_preview(surface, shape_key, x, y, block_size=15):
    if not shape_key: return
    shape_matrix = SHAPES[shape_key][0]
    color = SHAPE_COLORS[shape_key]
    for i, line in enumerate(shape_matrix):
        for j, col in enumerate(line):
            if col == '0':
                rect = pygame.Rect(x + j*block_size, y + i*block_size, block_size, block_size)
                # Thu nhỏ 2 pixel để tạo khe hở, bo tròn góc
                inner_rect = rect.inflate(-2, -2)
                pygame.draw.rect(surface, color, inner_rect, border_radius=2)

# --- CLASS HIỆU ỨNG VỤN VỠ (PARTICLE) ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-7, -2) 
        self.alpha = 255
        self.size = random.randint(3, 8)
        self.gravity = 0.5

    def update(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy
        self.alpha -= 8 

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(s, (*self.color, self.alpha), s.get_rect(), border_radius=2)
            surface.blit(s, (self.x, self.y))

class FloatingBlock:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(20, 50)
        self.color = random.choice([CYAN, PINK, YELLOW, GREEN, RED])
        self.alpha = random.randint(20, 60)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT + 50:
            self.y = -50
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(s, (*self.color, self.alpha), s.get_rect(), border_radius=4)
        pygame.draw.rect(s, (*self.color, self.alpha + 40), s.get_rect(), width=2, border_radius=4)
        surface.blit(s, (self.x, self.y))

floating_blocks = [FloatingBlock() for _ in range(15)]

def render_bold_text(surface, text, font, color, center_x, center_y, align="center"):
    text_surf = font.render(text, False, color)
    if align == "center": rect = text_surf.get_rect(center=(center_x, center_y))
    else: rect = text_surf.get_rect(midleft=(center_x, center_y))
    surface.blit(text_surf, rect)
    surface.blit(text_surf, (rect.x + 1, rect.y)) 

def draw_neon_button(surface, text, x, y, w, h, neon_color, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse_pos)
    border_thickness = 3 if is_hover else 2
    bg_alpha = 80 if is_hover else 15
    
    if is_hover:
        for i in range(1, 5): 
            glow_rect = rect.inflate(i*4, i*4)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*neon_color, max(0, 60 - i*12)), glow_surf.get_rect(), width=2, border_radius=8)
            surface.blit(glow_surf, (glow_rect.x, glow_rect.y))
            
    bg_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (*neon_color, bg_alpha), bg_surface.get_rect(), border_radius=8)
    surface.blit(bg_surface, (x, y))
    pygame.draw.rect(surface, neon_color, rect, border_thickness, border_radius=8)
    
    text_color = WHITE if is_hover else neon_color
    render_bold_text(surface, text, main_font, text_color, x + w//2, y + h//2, "center")
    return rect

def draw_toggle_button(surface, text, x, y, w, h, neon_color, mouse_pos, is_active):
    rect = pygame.Rect(x, y, w, h)
    is_hover = rect.collidepoint(mouse_pos)
    border_thickness = 3 if is_hover or is_active else 1
    bg_alpha = 90 if is_active else (40 if is_hover else 10)
    
    if is_active or is_hover:
        for i in range(1, 4): 
            glow_rect = rect.inflate(i*3, i*3)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*neon_color, max(0, 40 - i*10)), glow_surf.get_rect(), width=2, border_radius=6)
            surface.blit(glow_surf, (glow_rect.x, glow_rect.y))
            
    bg_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (*neon_color, bg_alpha), bg_surface.get_rect(), border_radius=6)
    surface.blit(bg_surface, (x, y))
    pygame.draw.rect(surface, neon_color, rect, border_thickness, border_radius=6)
    
    text_color = WHITE if is_active or is_hover else neon_color
    render_bold_text(surface, text, small_font, text_color, rect.centerx, rect.centery, "center")
    return rect

def draw_slider(surface, x, y, w, h, min_val, max_val, current_val, track_color, thumb_color, mouse_pos):
     track_rect = pygame.Rect(x, y, w, h)
     is_hover = track_rect.collidepoint(mouse_pos)
     
     # Draw track
     track_surf = pygame.Surface((w, h), pygame.SRCALPHA)
     pygame.draw.rect(track_surf, (*track_color, 120), track_surf.get_rect(), border_radius=h//2)
     surface.blit(track_surf, (x, y))
     
     # Calculate thumb position
     ratio = (current_val - min_val) / (max_val - min_val)
     thumb_x = x + int(ratio * w)
     thumb_radius = h + 4
     thumb_rect = pygame.Rect(thumb_x - thumb_radius, y - 2, thumb_radius * 2, h + 4)
     
     # Draw thumb glow
     if is_hover or thumb_rect.collidepoint(mouse_pos):
         for i in range(1, 4):
             glow_rect = thumb_rect.inflate(i*4, i*4)
             glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
             pygame.draw.circle(glow_surf, (*thumb_color, max(0, 80 - i*20)), (glow_rect.width//2, glow_rect.height//2), glow_rect.width//2)
             surface.blit(glow_surf, (glow_rect.x, glow_rect.y))
     
     # Draw thumb
     pygame.draw.circle(surface, thumb_color, (thumb_x, y + h//2), thumb_radius)
     pygame.draw.circle(surface, WHITE, (thumb_x, y + h//2), thumb_radius - 3)
     
     return track_rect, thumb_rect

def draw_glow_text(surface, text, font, color, center_x, center_y, align="center"):
     if font == title_font:
         shadow_surf = font.render(text, False, (0, 100, 100))
         if align == "center": shadow_rect = shadow_surf.get_rect(center=(center_x + 4, center_y + 4))
         else: shadow_rect = shadow_surf.get_rect(midleft=(center_x + 4, center_y + 4))
         surface.blit(shadow_surf, shadow_rect)
     
     core_color = WHITE if font == title_font else color
     render_bold_text(surface, text, font, core_color, center_x, center_y, align)