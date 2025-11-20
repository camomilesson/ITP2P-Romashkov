import sys
import pygame
import random
import re
import os

# --- Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
HISCORE_FILE = "hiscores.txt"
TOP_N = 5

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)

# --- Sprite Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_idle = pygame.image.load("player_idle.png").convert_alpha()
        self.image_idle = pygame.transform.scale(image_idle, (40, 60))
        image_jumping = pygame.image.load("player_jumping.png").convert_alpha()
        self.image_jump = pygame.transform.scale(image_jumping, (40, 60))
        self.image = self.image_idle  # default
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0.0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        try:
            img = pygame.image.load("block.png").convert_alpha()
            self.image = pygame.transform.scale(img, (width, height))
        except:
            # fallback if no image
            self.image = pygame.Surface((width, height))
            self.image.fill(GREY)
        self.rect = self.image.get_rect(topleft=(x, y))

def main():
    # --- Pygame Initialization ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame HS ITP2P")
    clock = pygame.time.Clock()

    # --- Fonts ---
    gameover_font = pygame.font.SysFont("Apple Chancery", 80)
    button_font = pygame.font.SysFont("Apple Chancery", 50)
    score_font = pygame.font.SysFont("Apple Chancery", 40)
    hiscore_font = pygame.font.SysFont("Apple Chancery", 30)

    # --- Background ---
    background_img = pygame.image.load("background.png").convert_alpha()
    scale_factor = SCREEN_WIDTH / background_img.get_width()
    bg_height = int(background_img.get_height() * scale_factor)
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, bg_height))
    bg_y = -1200          # initial vertical position
    bg_speed = 0.3    # very slow scroll

    # --- Game Variables ---
    player_start_x, player_start_y = 600, 0
    player_speed = 10
    gravity = 0.225
    max_fall_speed = 15
    terrain_speed = 2
    terrain_min_size = 150

    SPAWN_RECT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_RECT, 1200)
    SHRINK_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SHRINK_EVENT, 5000)

    # --- Groups ---
    all_sprites = pygame.sprite.Group()
    blocks_group = pygame.sprite.Group()

    # --- Player ---
    player = Player(player_start_x, player_start_y)
    all_sprites.add(player)

    # --- Initial Block ---
    first_block = Block(150, 100, 1000, 333)
    all_sprites.add(first_block)
    blocks_group.add(first_block)

    # --- Game State ---
    state = "GAME"
    on_ground = False
    score = 0
    player_name = ""
    enter_name = False
    restart_button = pygame.Rect(490, 500, 300, 60)

    # --- Functions ---
    def reset_game():
        nonlocal player, all_sprites, blocks_group, terrain_min_size, state, on_ground, score, player_name, enter_name, bg_y
        all_sprites.empty()
        blocks_group.empty()

        player.rect.topleft = (player_start_x, player_start_y)
        player.vel_y = 0
        all_sprites.add(player)

        first_block = Block(150, 100, 1000, 50)
        all_sprites.add(first_block)
        blocks_group.add(first_block)

        terrain_min_size = 150
        state = "GAME"
        on_ground = False
        score = 0
        player_name = ""
        enter_name = False
        bg_y = -1200

    def load_hiscores():
        if not os.path.exists(HISCORE_FILE):
            return []
        hiscores = []
        with open(HISCORE_FILE, "r") as f:
            for line in f:
                try:
                    n, s = line.strip().split(",")
                    hiscores.append((n, int(s)))
                except:
                    continue
        hiscores.sort(key=lambda hs: hs[1], reverse=True)
        return hiscores[:TOP_N]

    def save_hiscore(name, score):
        with open(HISCORE_FILE, "a") as f:
            f.write(f"{name},{score}\n")

    # --- Main Game Loop ---
    running = True
    while running:
        clock.tick(FPS)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "GAME":
                if event.type == SPAWN_RECT:
                    width = random.randint(terrain_min_size, terrain_min_size * 4)
                    x = random.randint(- width // 2, SCREEN_WIDTH - width // 2)
                    y = -50
                    block = Block(x, y, width, 50)
                    all_sprites.add(block)
                    blocks_group.add(block)
                    score += max((600 - width) // 100 * 5, 5)

                if event.type == SHRINK_EVENT:
                    terrain_min_size = max(50, terrain_min_size - 30)

            if state == "GAMEOVER" and enter_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        pattern = r"^[A-Za-z]{1,3}$"
                        if re.match(pattern, player_name):
                            save_hiscore(player_name.upper(), score)
                            enter_name = False
                        else:
                            player_name = ""
                    else:
                        if len(player_name) < 10:
                            player_name += event.unicode

            if state == "GAMEOVER" and not enter_name:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        reset_game()

        if state == "GAME":
            # --- Player Movement ---
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.rect.x -= player_speed
            if keys[pygame.K_d]:
                player.rect.x += player_speed
            if keys[pygame.K_SPACE] and on_ground:
                player.vel_y = -10
                player.image = player.image_jump

            # --- Gravity ---
            player.vel_y += gravity
            if player.vel_y > max_fall_speed:
                player.vel_y = max_fall_speed
            player.rect.y += int(player.vel_y)

            # --- Top-only Collision ---
            on_ground = False
            prev_y = player.rect.y - int(player.vel_y)
            for block in blocks_group:
                if player.rect.colliderect(block.rect):
                    is_falling = player.vel_y > 0
                    was_above = prev_y + player.rect.height <= block.rect.top + 5
                    if is_falling and was_above:
                        player.rect.bottom = block.rect.top
                        player.vel_y = terrain_speed
                        on_ground = True
                        break
            
            if on_ground:
                player.image = player.image_idle                

            if player.rect.top > SCREEN_HEIGHT:
                state = "GAMEOVER"
                enter_name = True

            # --- Move blocks ---
            for block in blocks_group:
                block.rect.y += terrain_speed

            # Remove far below blocks
            for block in list(blocks_group):
                if block.rect.top > 2000:
                    block.kill()

        # --- Drawing background---
        if bg_y < 0:
            bg_y += bg_speed

        screen.blit(background_img, (0, bg_y))

        # --- Drawing blocks and player ---
        all_sprites.draw(screen)

        # --- Drawing score ---
        score_text = score_font.render(f"Score: {score}", True, GOLD)
        text_rect = score_text.get_rect(topleft=(20, 10))
        padding_x, padding_y = 10, 5
        box_rect = pygame.Rect(
            text_rect.left - padding_x,
            text_rect.top - padding_y,
            text_rect.width + 2*padding_x,
            text_rect.height + 2*padding_y
        )
        pygame.draw.rect(screen, GREY, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)

        screen.blit(score_text, text_rect)

        if state == "GAMEOVER":
            game_over_text = gameover_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH//2, 150)))

            # Display high scores
            hiscores = load_hiscores()
            for i, (name, hs) in enumerate(hiscores):
                text = hiscore_font.render(f"{i+1}. {name}: {hs}", True, GOLD)
                screen.blit(text, (540, 250 + i*30))

            if enter_name:
                input_text = hiscore_font.render(f"Enter Name (1-3 chars): {player_name}", True, GOLD)
                screen.blit(input_text, (400, 500))
            else:
                pygame.draw.rect(screen, GREEN, restart_button)
                button_text = button_font.render("RESTART", True, WHITE)
                screen.blit(button_text, button_text.get_rect(center=restart_button.center))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
