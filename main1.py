import pygame
import sys
import time
import random
import math
import os
from Buttons import Button
from ball import Ball
from player import Player, Enemy

from pygame.locals import (
    K_a,
    K_w,
    K_s,
    K_d,
    QUIT,
    K_z,
    K_x,
    K_c,
    K_ESCAPE,
    K_1,
    K_2,
    K_3,
    K_SPACE,
)

pygame.init()

COINS = 10000
FREEZE = False
EXPLODE = False
DOUBLE_ATTACK_SPEED = False
LARGER_BULLETS = False
FLAMETHROWER = False


death_sound = pygame.mixer.Sound('sounds/death.wav')
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
shot_sound = pygame.mixer.Sound('sounds/sounds_hurt.mp3')
win_sound = pygame.mixer.Sound('sounds/win_music.wav')
menu_sound = pygame.mixer.Sound('sounds/background.mp3')
main_sound = pygame.mixer.Sound('sounds/background.mp3')

main_sound.set_volume(0.4)

menu_sound.play()

display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h - 60

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



TILE_SIZE = 16

def get_tile_surface(x_coord, y_coord):
    tileset = pygame.image.load("images/Dungeon_Tileset.png")
    tile = tileset.subsurface((x_coord * 16, y_coord * 16, 16, 16))
    tile = pygame.transform.scale(tile, (32, 32))
    return tile

# Initialize tiles
top = get_tile_surface(1,0)
bottom = get_tile_surface(1,4)
left = get_tile_surface(0,2)
right = get_tile_surface(5,2)
middle = get_tile_surface(2,2)

tileset = [
    [left] + [top] * (SCREEN_WIDTH // 32 - 2) + [right]
]

for a in range(SCREEN_HEIGHT // 32 - 2):
    tileset.append([left] + [middle] * (SCREEN_WIDTH // 32 - 2) + [right])
tileset.append([left] + [bottom] * (SCREEN_WIDTH // 32 - 2) + [right])

# Create a Surface for the tilemap
tilemap_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tilemap_surface = tilemap_surface.convert()

def render_tilemap():
    for y in range(len(tileset)):
        for x in range(len(tileset[0])):
            tilemap_surface.blit(tileset[y][x], (x * 32, y * 32))

render_tilemap()


######## Image loading ########

# Load the shop icon

# Load the image
shop_image = pygame.image.load("images/Backgrounds/shop.png").convert_alpha()
shop_image = pygame.transform.scale(shop_image, (100, 100))
# Get image dimensions
image_width, image_height = shop_image.get_size()

# Position the image near the top-right corner (e.g., 20 pixels away from the edges)
x_position = SCREEN_WIDTH - image_width - 20
y_position = 20

#Background for options
option_bg = pygame.image.load("images/Backgrounds/background.png")
option_bg = pygame.transform.scale(option_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))



level_select_bg = pygame.image.load("images/Backgrounds/background2.png")
level_select_bg = pygame.transform.scale(level_select_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG = pygame.image.load("images/Backgrounds/menu.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to screen dimensions
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

gun_img = pygame.image.load('images/guns/gun-basic.png').convert_alpha()

projectile_img = pygame.image.load('images/ballz/projectile.png').convert()
projectile_img.set_colorkey((0, 0, 0))

enemy_projectile_img = pygame.image.load('images/ballz/enemy_projectile.png').convert()
enemy_projectile_img.set_colorkey((0, 0, 0))



def load_animations(actions, folder_name):
    animation_database = {}
    for action in actions:
        image_path = 'images/' + folder_name + '/' + action
        animation_database.update({action:[]})
        for image in os.listdir(image_path):
            image_id = pygame.image.load(image_path + '/' + image).convert_alpha()
            animation_database[action].append(pygame.transform.scale(image_id, (90, 90)))
    return animation_database

player_animations = load_animations(['Idle', 'Running'], 'player_images')

enemy_animations = load_animations(['Walking'], 'enemy_images')

#####################



def get_font(size):
    return pygame.font.Font("images/Textboxes/font.ttf", size)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        global COINS
        COINS_TEXT = get_font(30).render(f"COINS: {COINS}🔶", True, "#b68f40")
        COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH - SCREEN_WIDTH/8, SCREEN_HEIGHT//11))
        SCREEN.blit(COINS_TEXT, COINS_RECT)
        
        OPTIONS_BUTTON = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        for button in [OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                #if event.type == pygame.TUTORIAL:
                #    
                #    pass
                    
        pygame.display.update()



def level_select():
    while True:
        
        screen.blit(level_select_bg, (0, 0))
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()
        LEVEL_TEXT = get_font(75).render("LEVEL SELECT", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT/6))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        level1 = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
                            text_input= "LEVEL 1", font=get_font(45), base_color="White", hovering_color="Green")
        

        level2 = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6), 
                            text_input="LEVEL 2", font=get_font(45), base_color="White", hovering_color="Green")
        
        
        back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT/6), 
                            text_input="BACK", font=get_font(45), base_color="White", hovering_color="Green")
        for button in [level1, level2, back]:    
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.checkForInput(LEVEL_MOUSE_POS):
                    map1()
                if level2.checkForInput(LEVEL_MOUSE_POS):
                    comingsoon()
                if back.checkForInput(LEVEL_MOUSE_POS):
                    main_menu()

        pygame.display.update()  

def comingsoon():
    while True:
        SCREEN.fill("lightblue")
        SOON = pygame.mouse.get_pos()


        SOON_TEXT = get_font(75).render("COMING SOON", True, "Black")
        SOON_RECT = SOON_TEXT.get_rect(center=(SCREEN_WIDTH//3, SCREEN_HEIGHT/2))
        SCREEN.blit(SOON_TEXT, SOON_RECT)


        back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT/6), 
                            text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Green")
        back.changeColor(SOON)
        back.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.checkForInput(SOON):
                    main_menu()

        pygame.display.update()  


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(option_bg, (0, 0))


        OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT/6))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT/6), 
                            text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Green")
        

        OPTIONS_SHOP = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6), 
                            text_input="SHOP", font=get_font(45), base_color="Black", hovering_color="Green")

        
            
        
        OPTIONS_LEVELS = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
                            text_input="LEVELS", font=get_font(45), base_color="Black", hovering_color="Green")
        for button in [OPTIONS_LEVELS, OPTIONS_SHOP, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif OPTIONS_SHOP.checkForInput(OPTIONS_MOUSE_POS):
                    print("shop")
                    shop()
                elif OPTIONS_LEVELS.checkForInput(OPTIONS_MOUSE_POS):
                    print("levels")
                    level_select()

        pygame.display.update()    

def pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 50))
    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(overlay, (0, 0))


        mouse_pos = pygame.mouse.get_pos()
        resume = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6), 
                            text_input="RESUME", font=get_font(45), base_color="Black", hovering_color="Green")
        menu = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - SCREEN_HEIGHT/6), 
                            text_input="MAIN MENU", font=get_font(45), base_color="Black", hovering_color="Green")
        for button in [resume, menu]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume.checkForInput(mouse_pos):
                    return 
                elif menu.checkForInput(mouse_pos):
                    main_menu()
        pygame.display.update()
        clock.tick(20)



def map1():
    """
    what to do:
    - make bullets ricochet
    - make bullets shoot in mouse's direction
    
    """
    player = Player(100, 100, 50, 50, 5, 100, player_animations)
    enemies_defeated = 0
    enemies = []
    gun = 1

    balls = []
    frame_count = 13


    #font = pygame.font.Font(None, 36)
    freeze_cooldown_start = 0
    freeze_cooldown = 5000
    freeze_used = False
    last_time = pygame.time.get_ticks()
    speed_used = False
    speed_on = False
    starttime = pygame.time.get_ticks()
    starttime2 = pygame.time.get_ticks()
    larger_on = False

    while True:
        
        if pygame.time.get_ticks() - last_time >= 1000 - ((pygame.time.get_ticks()-starttime2)/1000):
            last_time = pygame.time.get_ticks()
            enemies.append(Enemy(random.randint(10, 1000), random.randint(10, 600), 50, 50, random.randint(150, 400)//100, 50, enemy_animations, player))
        SCREEN.blit(BG, (0, 0))
        #draw_tilemap(SCREEN)
        #ball.render(SCREEN)
        SCREEN.blit(tilemap_surface, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        #back = Button(image="images/Buttons/Back.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/16, SCREEN_HEIGHT/10), 
        #                    text_input="", font=get_font(1), base_color="Black", hovering_color="Green", scale=0.2)
        pause = Button(image="images/Buttons/Pause.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/10, SCREEN_HEIGHT/10), 
                                text_input="", font=get_font(1), base_color="Black", hovering_color="Green",scale=0.05)
        
        """if larger_on:
            for ball in balls:
                for wall in walls:
                    if player.rect.colliderect(wall):
                        ball.rect = ball.image.get_rect(topleft=(ball.x, ball.y))
            big = False
            pass
            #ball gotta get bigger hitbox"""
        global FREEZE
        time_left = 0
        if FREEZE:
            current_time = pygame.time.get_ticks()
            time_gone = current_time - freeze_cooldown_start
            time_left = max(0, (freeze_cooldown - time_left)/1000)
            if time_left <= 0:
                freeze_used = False
            if not freeze_used and (time_gone >= freeze_cooldown):
                freeze = Button(image="images/Buttons/Ice.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/8, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="X", font=get_font(25), base_color="GREEN", hovering_color="Green",scale=0.2)
            else:
                freeze = Button(image="images/Buttons/Ice.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/8, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="X", font=get_font(25), base_color="RED", hovering_color="RED",scale=0.2)
        global EXPLODE
        if EXPLODE:
            if player.health > 50:
                explode = Button(image="images/Buttons/bomb.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/14, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="C", font=get_font(25), base_color="GREEN", hovering_color="Green",scale=0.2)
            else:
                explode = Button(image="images/Buttons/bomb.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH/14, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="C", font=get_font(25), base_color="RED", hovering_color="RED",scale=0.2)
        global DOUBLE_ATTACK_SPEED
        if DOUBLE_ATTACK_SPEED and gun != 3:
            if not speed_used:
                speed = Button(image="images/Buttons/double_speed.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH//5, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="Z", font=get_font(25), base_color="GREEN", hovering_color="Green",scale=0.2)
                speed_used = True
            else:
                speed = Button(image="images/Buttons/double_speed.png", pos=(SCREEN_WIDTH - SCREEN_WIDTH//5, SCREEN_HEIGHT - SCREEN_HEIGHT/16), 
                                    text_input="Z", font=get_font(25), base_color="RED", hovering_color="RED",scale=0.15)


        pause.changeColor(mouse_pos)
        pause.update(SCREEN)
        if FREEZE:
            freeze.changeColor(mouse_pos)
            freeze.update(SCREEN)
        if EXPLODE:
            explode.changeColor(mouse_pos)
            explode.update(SCREEN)
        if DOUBLE_ATTACK_SPEED:
            speed.changeColor(mouse_pos)
            speed.update(SCREEN)
            
        
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if gun == 1:
                        gun = 2
                    elif gun == 2:
                        gun = 3
                    elif gun == 3:
                        gun = 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                if FREEZE:
                    if not freeze_used and (current_time - freeze_cooldown_start >= freeze_cooldown):
                        balls = []
                        for enemy in enemies:
                            enemy.bullets = []
                        time.sleep(3)
                        freeze_used = True
                        freeze_cooldown_start = pygame.time.get_ticks()
                if pause.checkForInput(mouse_pos):
                    pause_menu()
                if EXPLODE:
                    if explode.checkForInput(mouse_pos):
                        if player.health > 50:
                            player.health -= 50
                            shot_sound.play()
                            enemies = []
                if DOUBLE_ATTACK_SPEED:
                    if speed.checkForInput(mouse_pos):
                        speed_on = True

        
        keys = pygame.key.get_pressed()
        global LARGER_BULLETS
        global FLAMETHROWER
        if FLAMETHROWER:
            if gun == 3:
                if frame_count > 0.01:
                    frame_count = 0
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = math.atan2((player.rect.centery - mouse_y), (player.rect.centerx - mouse_x))

                    x_vel = math.cos(angle) * -10
                    y_vel = math.sin(angle) * -10
                    
                    ball = Ball(player.rect.centerx, player.rect.top - 40, x_vel, y_vel, 2, 20)
                    balls.append(ball)

                frame_count += 1
        if FREEZE:
            if keys[K_x]:
                balls = []
                for enemy in enemies:
                    enemy.bullets = []
                time.sleep(3)
                freeze_used = True
                freeze_cooldown_start = pygame.time.get_ticks()
        if EXPLODE:
            if keys[K_c]:
                if player.health > 50:
                    player.health -= 50
                    shot_sound.play()
                    enemies.pop(0)
        if DOUBLE_ATTACK_SPEED:
            if keys[K_z]:
                speed_on = True

        if speed_on:
            if frame_count > 12:
                frame_count = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2((player.rect.centery - mouse_y), (player.rect.centerx - mouse_x))

                x_vel = math.cos(angle) * -10
                y_vel = math.sin(angle) * -10
                
                ball = Ball(player.rect.centerx, player.rect.top - 40, x_vel, y_vel, 15, 20)
                balls.append(ball)
            frame_count += 1
        else:
            if frame_count > 24:
                frame_count = 0
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2((player.rect.centery - mouse_y), (player.rect.centerx - mouse_x))

                x_vel = math.cos(angle) * -10
                y_vel = math.sin(angle) * -10
                if gun == 2 and LARGER_BULLETS:
                    ball = Ball(player.rect.centerx, player.rect.top - 40, x_vel, y_vel, 30, 60)
                else:
                    ball = Ball(player.rect.centerx, player.rect.top - 40, x_vel, y_vel, 15, 20)
                balls.append(ball)
            frame_count += 1
        
        if pygame.time.get_ticks() - starttime > 10000:
            starttime = pygame.time.get_ticks()
            speed_on = False
        #hi
        print(enemies)
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                player.health -= 0.1
                shot_sound.play()
                
            enemy.upd()
        
        if player.health <= 0:
            victory(enemies_defeated * 5)

        #hi
        
        """for enemy in enemies:
            for ball in enemy.balls[:]:
                if ball.changed and ball.rect.colliderect(player.rect):
                    player. ball.damage
                    if player.health <= 0:
                        enemy.balls.remove(ball)
                        choice = game_over()
                        if choice == "restart":
                            map1()
                        elif choice == "main":
                            main_menu()
                        else:
                            pygame.quit()
                            sys.exit()
                if ball.count >= 1:
                    enemy.balls.remove(ball)"""
        
        
        player.update(SCREEN_WIDTH, SCREEN_HEIGHT)  # Update player state
        player.draw(SCREEN)  # Draw player on top of the background

        for ball in balls:
            if ball.changed and ball.rect.colliderect(player.rect):
                player.health -= ball.damage
                shoot_sound.play()
                balls.remove(ball)
                if player.health <= 0:
                    victory(enemies_defeated * 5)
            for enemy in enemies:
                if enemy.rect.colliderect(ball.rect):
                    if ball not in enemy.bigballzhitby:
                        enemy.bigballzhitby.append(ball)
                        enemy.take_damage(ball.damage)
                        shoot_sound.play()
                    if ball.size != 60:
                        if ball in balls:
                            balls.remove(ball)
                    if enemy.health <= 0:
                        enemies_defeated += 1
                        player.health += 5
                        enemies.remove(enemy)
                        del enemy
                else:
                    if ball in enemy.bigballzhitby:
                        enemy.bigballzhitby.remove(ball)
            if ball.count >= 1:
                ball.change_image()
            if ball.count > 2:
                balls.remove(ball)
            ball.move(SCREEN_WIDTH, SCREEN_HEIGHT)
            ball.render(SCREEN)
        for enemy in enemies:
            enemy.draw(SCREEN)
            pygame.draw.rect(SCREEN, (0, 255, 0), (enemy.x, enemy.y, enemy.health, 5))

        pygame.draw.rect(SCREEN, (0, 255, 0), (100, SCREEN_HEIGHT - 100, player.health * 5, 20))

        pygame.display.update()
        
        clock.tick(60)

def victory(coins):
    win_sound.play()
    global COINS
    COINS += coins
    while True:
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("red")
        VICTORY_TEXT = get_font(150).render("VICTORY", True, "BLACK")
        VICTORY_RECT = VICTORY_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        SCREEN.blit(VICTORY_TEXT, VICTORY_RECT)
        COINS_TEXT = get_font(75).render(f"Coins Gained: {coins}", True, "BLACK")
        COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        SCREEN.blit(COINS_TEXT, COINS_RECT)
        
        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(45), base_color="Black", hovering_color="Green")


        
        BACK_BUTTON.changeColor(LEVEL_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    main_menu()
        pygame.display.flip()


def game_over():
    win_sound.play()
    while True:
        GO_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("red")
        GAMEOVER_TEXT = get_font(150).render("GAME OVER", True, "BLACK")
        GAMEOVER_RECT = GAMEOVER_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
        SCREEN.blit(GAMEOVER_TEXT, GAMEOVER_RECT)

        
        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="QUIT", font=get_font(45), base_color="Black", hovering_color="Green")
        RESTART_BUTTON = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2),
                                text_input="RESTART", font=get_font(45), base_color="Black", hovering_color="Green")
        MAINMENU_BUTTON= Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(45), base_color="Black", hovering_color="Green")


        
        for button in [BACK_BUTTON, RESTART_BUTTON, MAINMENU_BUTTON]:
            button.changeColor(GO_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(GO_MOUSE_POS):
                    return "restart"
                elif MAINMENU_BUTTON.checkForInput(GO_MOUSE_POS):
                    return "main"
                elif BACK_BUTTON.checkForInput(GO_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

def shop():
    
    while True:
        # Shop image
        screen.blit(shop_image, (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//6))
        
        SHOP_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("lightblue")

        SHOP_TEXT = get_font(75).render("SHOP", True, "Black")
        SHOP_RECT = SHOP_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
        SCREEN.blit(SHOP_TEXT, SHOP_RECT)
        global FREEZE, EXPLODE, DOUBLE_ATTACK_SPEED, FLAMETHROWER, LARGER_BULLETS
        if not FREEZE:
            ITEM1_BUTTON = Button(
                image=None, 
                pos=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2), 
                text_input="FREEZE: 250🔶", 
                font=get_font(25), 
                base_color="Black", 
                hovering_color="Green"
            )
            ITEM1_BUTTON.changeColor(SHOP_MOUSE_POS)
            ITEM1_BUTTON.update(SCREEN)
        if not EXPLODE:
            ITEM2_BUTTON = Button(
                image=None, 
                pos=(3*SCREEN_WIDTH/4, SCREEN_HEIGHT//2), 
                text_input="EXPLODE: 100🔶", 
                font=get_font(25), 
                base_color="Black", 
                hovering_color="Green"
            )
            ITEM2_BUTTON.changeColor(SHOP_MOUSE_POS)
            ITEM2_BUTTON.update(SCREEN)
        if not DOUBLE_ATTACK_SPEED:
            ITEM3_BUTTON = Button(
                image=None, 
                pos=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2 + SCREEN_HEIGHT//6), 
                text_input="ATTACK SPEED: 200🔶", 
                font=get_font(25), 
                base_color="Black", 
                hovering_color="Green"
            )
            ITEM3_BUTTON.changeColor(SHOP_MOUSE_POS)
            ITEM3_BUTTON.update(SCREEN)
        if not LARGER_BULLETS:
            ITEM4_BUTTON = Button(
                    image=None, 
                    pos=(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2 + SCREEN_HEIGHT//6), 
                    text_input="LARGER BULLETS: 500🔶", 
                    font=get_font(25), 
                    base_color="Black", 
                    hovering_color="Green"
                )
            ITEM4_BUTTON.changeColor(SHOP_MOUSE_POS)
            ITEM4_BUTTON.update(SCREEN)
        
        if not FLAMETHROWER:
            ITEM5_BUTTON = Button(
                    image=None, 
                    pos=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6), 
                    text_input="FLAMETHROWER: 1000", 
                    font=get_font(25), 
                    base_color="Black", 
                    hovering_color="Green"
            )
            ITEM5_BUTTON.changeColor(SHOP_MOUSE_POS)
            ITEM5_BUTTON.update(SCREEN)
        
        BACK_BUTTON = Button(
            image=None, 
            pos=(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6), 
            text_input="BACK", 
            font=get_font(25), 
            base_color="Black", 
            hovering_color="Green"
        )

        BACK_BUTTON.changeColor(SHOP_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not FREEZE:
                    if ITEM1_BUTTON.checkForInput(SHOP_MOUSE_POS):
                        freeze()
                if not EXPLODE:
                    if ITEM2_BUTTON.checkForInput(SHOP_MOUSE_POS):
                        explode()
                if not DOUBLE_ATTACK_SPEED:
                    if ITEM3_BUTTON.checkForInput(SHOP_MOUSE_POS):
                        speed()
                if not LARGER_BULLETS:
                    if ITEM4_BUTTON.checkForInput(SHOP_MOUSE_POS):
                        larger_bullets()
                if not FLAMETHROWER:
                    if ITEM5_BUTTON.checkForInput(SHOP_MOUSE_POS):
                        flamethrower()
                if BACK_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def flamethrower():
    while True:
        FLAME = pygame.mouse.get_pos()
        global COINS
        SCREEN.fill("lightblue")

        if COINS < 1000:
            FLAME_TEXT = get_font(40).render("INSUFFICIENT FUNDS", True, "Black")
            FLAME_RECT = LARGER_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(FLAME_TEXT, FLAME_RECT)
            COINS_TEXT = get_font(25).render(f"COINS REQUIRED: {1000-COINS}🔶", True, "Black")
            COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(COINS_TEXT, COINS_RECT)
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            back.changeColor(FLAME)
            back.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(FLAME):
                        main_menu()
        else:
            FLAME_TEXT = get_font(40).render("PURCHASE FLAMETHROWER: 1000🔶?", True, "Black")
            FLAME_RECT = FLAME_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(FLAME_TEXT, FLAME_RECT)
            purchase = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6),
                                text_input="FLAMETHROWER: 1000🔶", font=get_font(25), base_color="Black", hovering_color="Green")
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            for button in [purchase, back]:
                button.changeColor(FLAME)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purchase.checkForInput(FLAME):
                        COINS -= 1000
                        global FLAMETHROWER
                        FLAMETHROWER = True
                        return
                    if back.checkForInput(FLAME):
                        main_menu()

        pygame.display.update()

def larger_bullets():
    while True:
        LARGER = pygame.mouse.get_pos()
        global COINS
        SCREEN.fill("lightblue")

        if COINS < 500:
            LARGER_TEXT = get_font(40).render("INSUFFICIENT FUNDS", True, "Black")
            LARGER_RECT = LARGER_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(LARGER_TEXT, LARGER_RECT)
            COINS_TEXT = get_font(25).render(f"COINS REQUIRED: {500-COINS}🔶", True, "Black")
            COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(COINS_TEXT, COINS_RECT)
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            back.changeColor(LARGER)
            back.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(LARGER):
                        main_menu()
        else:
            LARGER_TEXT = get_font(40).render("PURCHASE LARGER BULLETS: 500🔶?", True, "Black")
            LARGER_RECT = LARGER_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(LARGER_TEXT, LARGER_RECT)
            purchase = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6),
                                text_input="LARGER BULLETS: 500🔶", font=get_font(25), base_color="Black", hovering_color="Green")
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            for button in [purchase, back]:
                button.changeColor(LARGER)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purchase.checkForInput(LARGER):
                        COINS -= 500
                        global LARGER_BULLETS
                        LARGER_BULLETS = True
                        return
                    if back.checkForInput(LARGER):
                        main_menu()

        pygame.display.update()


def speed():
    while True:
        SPEED_MOUSE_POS = pygame.mouse.get_pos()
        global COINS
        SCREEN.fill("lightblue")

        if COINS < 200:
            SPEED_TEXT = get_font(40).render("INSUFFICIENT FUNDS", True, "Black")
            SPEED_RECT = SPEED_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(SPEED_TEXT, SPEED_RECT)
            COINS_TEXT = get_font(25).render(f"COINS REQUIRED: {200-COINS}🔶", True, "Black")
            COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(COINS_TEXT, COINS_RECT)
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            back.changeColor(SPEED_MOUSE_POS)
            back.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(SPEED_MOUSE_POS):
                        main_menu()
        else:
            SPEED_TEXT = get_font(40).render("PURCHASE SPEED ABILITY: 200🔶?", True, "Black")
            SPEED_RECT = SPEED_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(SPEED_TEXT, SPEED_RECT)
            purchase = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6),
                                text_input="2X RELOAD SPEED: 200🔶", font=get_font(25), base_color="Black", hovering_color="Green")
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            for button in [purchase, back]:
                button.changeColor(SPEED_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purchase.checkForInput(SPEED_MOUSE_POS):
                        COINS -= 200
                        global DOUBLE_ATTACK_SPEED
                        DOUBLE_ATTACK_SPEED = True
                        return
                    if back.checkForInput(SPEED_MOUSE_POS):
                        main_menu()

        pygame.display.update()


def explode():
    while True:
        EXPLODE_MOUSE_POS = pygame.mouse.get_pos()
        global COINS
        SCREEN.fill("lightblue")

        if COINS < 100:
            EXPLODE_TEXT = get_font(40).render("INSUFFICIENT FUNDS", True, "Black")
            EXPLODE_RECT = EXPLODE_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(EXPLODE_TEXT, EXPLODE_RECT)
            COINS_TEXT = get_font(25).render(f"COINS REQUIRED: {100-COINS}🔶", True, "Black")
            COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(COINS_TEXT, COINS_RECT)
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            back.changeColor(EXPLODE_MOUSE_POS)
            back.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(EXPLODE_MOUSE_POS):
                        main_menu()
        else:
            EXPLODE_TEXT = get_font(40).render("PURCHASE EXPLODE ABILITY: 100🔶?", True, "Black")
            EXPLODE_RECT = EXPLODE_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(EXPLODE_TEXT, EXPLODE_RECT)
            purchase = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6),
                                text_input="EXPLODE: 100🔶", font=get_font(25), base_color="Black", hovering_color="Green")
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            for button in [purchase, back]:
                button.changeColor(EXPLODE_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purchase.checkForInput(EXPLODE_MOUSE_POS):
                        
                        COINS -= 100
                        global EXPLODE
                        EXPLODE = True
                        return
                    if back.checkForInput(EXPLODE_MOUSE_POS):
                        main_menu()

        pygame.display.update()
def freeze():
    """🔶"""
    while True:
        FREEZE_MOUSE_POS = pygame.mouse.get_pos()
        global COINS
        SCREEN.fill("lightblue")
        if COINS < 250:
            FREEZE_TEXT = get_font(40).render("INSUFFICIENT FUNDS", True, "Black")
            FREEZE_RECT = FREEZE_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(FREEZE_TEXT, FREEZE_RECT)
            COINS_TEXT = get_font(25).render(f"COINS REQUIRED: {250-COINS}🔶", True, "Black")
            COINS_RECT = COINS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            SCREEN.blit(COINS_TEXT, COINS_RECT)
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            back.changeColor(FREEZE_MOUSE_POS)
            back.update(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(FREEZE_MOUSE_POS):
                        main_menu()



        else:
            FREEZE_TEXT = get_font(40).render("PURCHASE FREEZE ABILITY: 250🔶?", True, "Black")
            FREEZE_RECT = FREEZE_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//6))
            SCREEN.blit(FREEZE_TEXT, FREEZE_RECT)
            purchase = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + SCREEN_HEIGHT/6),
                                text_input="FREEZE: 100🔶", font=get_font(25), base_color="Black", hovering_color="Green")
            back = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 2*SCREEN_HEIGHT//6),
                                text_input="MAIN MENU", font=get_font(30), base_color="Black", hovering_color="Green")
            for button in [purchase, back]:
                button.changeColor(FREEZE_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if purchase.checkForInput(FREEZE_MOUSE_POS):
                        COINS -= 250
                        global FREEZE
                        FREEZE = True
                        return
                    if back.checkForInput(FREEZE_MOUSE_POS):
                        main_menu()

        pygame.display.update()

    


######## Tilemap ########



#######################
main_menu()
