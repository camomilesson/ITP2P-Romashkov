import sys
import pygame
import random
import re

from settings import *
from utils import load_hiscores, save_hiscore, validate_name
from player import Player
from block import Block

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Castle Jumper")
    clock = pygame.time.Clock()

    # --- Fonts ---
    gameover_font = pygame.font.SysFont("Tahoma", 80)
    button_font = pygame.font.SysFont("Tahoma", 45)
    score_font = pygame.font.SysFont("Tahoma", 40)
    hiscore_font = pygame.font.SysFont("Tahoma", 30)

    # --- Background ---
    background_img = pygame.image.load("sprites/background.png").convert_alpha()
    scale_factor = SCREEN_WIDTH / background_img.get_width()
    bg_height = int(background_img.get_height() * scale_factor)
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, bg_height))
    bg_y = -1000
    bg_speed = 0.2

    # --- Groups ---
    all_sprites = pygame.sprite.Group()
    blocks_group = pygame.sprite.Group()

    # --- Player ---
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    all_sprites.add(player)

    # --- Initial Block ---
    first_block = Block(545, 105, 150, 32, 0)
    all_sprites.add(first_block)
    blocks_group.add(first_block)

    # --- Game State ---
    state = "MENU"
    on_ground = False
    score = 0
    player_name = ""
    name_saved = False
    restart_button = pygame.Rect(490, 630, 300, 70)
    terrain_min_size = TERRAIN_MIN_SIZE
    block_vel_x = 0
    menu_rect = pygame.Rect(150, 150, 980, 596)

    SPAWN_RECT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_RECT, 1200)
    INCREASE_DIFFICULTY = pygame.USEREVENT + 2
    pygame.time.set_timer(INCREASE_DIFFICULTY, 5000)

    def reset_game():
        nonlocal player, all_sprites, blocks_group, terrain_min_size, block_vel_x, state, on_ground, score, bg_y
        all_sprites.empty()
        blocks_group.empty()

        player.rect.topleft = (PLAYER_START_X, PLAYER_START_Y)
        player.vel_y = 0
        player.vel_x = 0
        all_sprites.add(player)

        first_block = Block(545, 105, 150, 32, 0)
        all_sprites.add(first_block)
        blocks_group.add(first_block)

        terrain_min_size = TERRAIN_MIN_SIZE
        block_vel_x = 0
        state = "GAME"
        on_ground = False
        score = 0
        bg_y = -1000

    # --- Main Loop ---
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "MENU":
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    state = "GAME"  # start the game
                
            if state == "GAME":
                if event.type == SPAWN_RECT:
                    width = random.randint(terrain_min_size, terrain_min_size * 4)
                    x = random.randint(0, SCREEN_WIDTH - width)
                    y = -50
                    speed = random.randint(-block_vel_x, block_vel_x)
                    block = Block(x, y, width, 32, speed)
                    all_sprites.add(block)
                    blocks_group.add(block)
                    score += max((600 - width) * (speed + 1) // 100 * 5, 5)

                if event.type == INCREASE_DIFFICULTY:
                    terrain_min_size = max(50, terrain_min_size - 30)
                    block_vel_x += 1

            # --- Game Over Name Input ---
            if state == "GAMEOVER":
                if not name_saved:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            if validate_name(player_name):
                                player_name = player_name.upper()
                            else:
                                player_name = "AAA"
                            save_hiscore('hiscores.txt', player_name, score)
                            name_saved = True
                            reset_game()
                        else:
                            if len(player_name) < 3 and event.unicode.isalpha():
                                player_name += event.unicode
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                        save_hiscore('hiscores.txt', player_name, score)
                        reset_game()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        save_hiscore('hiscores.txt', player_name, score)
                        reset_game()

        # --- Game Logic ---
        if state == "GAME":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.rect.x += PLAYER_SPEED
            if keys[pygame.K_SPACE] and on_ground:
                player.vel_y = -10
                player.vel_x = 0
                player.image = player.image_jump

            player.rect.x += int(player.vel_x)

            # Gravity
            player.vel_y += GRAVITY
            if player.vel_y > MAX_FALL_SPEED:
                player.vel_y = MAX_FALL_SPEED
            player.rect.y += int(player.vel_y)

            # Top-only collision
            on_ground = False
            prev_y = player.rect.y - int(player.vel_y)
            for block in blocks_group:
                if player.rect.colliderect(block.rect):
                    is_falling = player.vel_y > 0
                    was_above = prev_y + player.rect.height <= block.rect.top + 5
                    if is_falling and was_above:
                        player.rect.bottom = block.rect.top
                        player.vel_y = BLOCK_VEL_Y
                        player.vel_x = block.speed
                        on_ground = True
                        break
            if on_ground:
                player.image = player.image_idle

            if player.rect.top > SCREEN_HEIGHT:
                state = "GAMEOVER"

            # Move blocks
            for block in blocks_group:
                block.rect.y += BLOCK_VEL_Y
                block.rect.x += block.speed
                if block.rect.x < 0 or block.rect.right > SCREEN_WIDTH:
                    block.speed *= -1
                    if on_ground and player.rect.bottom == block.rect.top:
                        player.vel_x *= -1

            # Remove offscreen blocks
            for block in list(blocks_group):
                if block.rect.top > 2000:
                    block.kill()

        # --- Drawing ---
        if bg_y < 0:
            bg_y += bg_speed
        screen.blit(background_img, (0, bg_y))

        if state == "MENU":
            pygame.draw.rect(screen, GREY, menu_rect)
            pygame.draw.rect(screen, WHITE, menu_rect, 2)
            title_font = pygame.font.SysFont("Tahoma", 125)
            title_text = title_font.render("Castle Jumper", True, GOLD)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH//2, 370)))

            # Controls
            controls_font = pygame.font.SysFont("Tahoma", 30)
            line1 = controls_font.render("Arrows to move", True, WHITE)
            line2 = controls_font.render("Space to jump", True, WHITE)
            line3 = controls_font.render("Any key to start", True, GREEN)
            screen.blit(line1, line1.get_rect(center=(SCREEN_WIDTH//2, 540)))
            screen.blit(line2, line2.get_rect(center=(SCREEN_WIDTH//2, 600)))
            screen.blit(line3, line3.get_rect(center=(SCREEN_WIDTH//2, 660)))

        all_sprites.draw(screen)

        # Score HUD
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

        # Game Over Screen
        if state == "GAMEOVER":
            pygame.draw.rect(screen, GREY, menu_rect)
            pygame.draw.rect(screen, WHITE, menu_rect, 2)

            game_over_text = gameover_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH//2, 250)))

            cur_score_text = hiscore_font.render(f'Your score: {score}!', True, GREEN)
            screen.blit(cur_score_text, cur_score_text.get_rect(center=(SCREEN_WIDTH//2, 320)))

            hiscores = load_hiscores('hiscores.txt')
            for i, (name, hs) in enumerate(hiscores):
                text = hiscore_font.render(f"{i+1}. {name}: {hs}", True, GOLD)
                screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, 385 + i*30)))

            # Name input or congrats
            if not name_saved:
                input_text = hiscore_font.render(f"Enter Name (1-3 chars): {player_name}", True, GOLD)
            else:
                input_text = hiscore_font.render(f"Congratulations, {player_name}!", True, GOLD)
            screen.blit(input_text, (SCREEN_WIDTH // 2 - input_text.get_width() // 2, 570))

            # Restart button
            pygame.draw.rect(screen, GREEN, restart_button)
            pygame.draw.rect(screen, WHITE, restart_button, 2)
            button_text = button_font.render("RESTART", True, GOLD)
            screen.blit(button_text, button_text.get_rect(center=restart_button.center))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
