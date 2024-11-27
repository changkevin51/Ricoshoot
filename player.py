import pygame
import math
import pygame
import random
from ball import Ball

class Player:
    def __init__(self, x, y, width, height, speed, health, animations):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.flip = False
        self.action = "Idle"
        self.frame = 0
        self.animation_speed = 10
        self.animations = animations
        self.image = self.animations[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Load and scale the orb image
        orb_img = pygame.image.load("images/player_images/Orb.png").convert_alpha()
        self.orb_image = pygame.transform.scale(orb_img, (20, 20))  # Shrink to appropriate size
        self.orb_offset = 35

    def move(self, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        moving = False
        dx, dy = 0, 0  # Change in x and y directions
        
        if keys[pygame.K_w]:
            dy -= self.speed
            moving = True
        if keys[pygame.K_s]:
            dy += self.speed
            moving = True
        if keys[pygame.K_a]:
            dx -= self.speed
            self.flip = True  # Flip image when moving left
            moving = True
        if keys[pygame.K_d]:
            dx += self.speed
            self.flip = False  # Reset flip when moving right
            moving = True

        # Normalize speed for diagonal movement
        if dx != 0 or dy != 0:  # Check if the player is moving
            length = math.hypot(dx, dy)  # Calculate diagonal length
            dx, dy = dx / length * self.speed, dy / length * self.speed
        
        if self.x + dx < 0 or self.x + dx > screen_width - 100:
            dx = 0
        if self.y + dy < 0 or self.y + dy > screen_height - 100:
            dy = 0

        # for wall in walls:
        #     if new_rect.colliderect(wall):  # Collision detected
        #         if dx > 0:  # Moving right
        #             new_rect.right = wall.left
        #             dx = 0
        #         if dx < 0:  # Moving left
        #             new_rect.left = wall.right
        #             dx = 0
        #         if dy > 0:  # Moving down
        #             new_rect.bottom = wall.top
        #             dy = 0
        #         if dy < 0:  # Moving up
        #             new_rect.top = wall.bottom
        #             dy = 0
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

        if moving:
            self.change_action("Running")
        else:
            self.change_action("Idle")

    def update(self, screen_width, screen_height):
        self.move(screen_width, screen_height)
        self.animate()

    def animate(self):
        if self.action == 'Idle':
            self.animation_speed = 6
        if self.action == 'Running':
            self.animation_speed = 4
        self.frame += 1
        if self.frame >= len(self.animations[self.action]) * self.animation_speed:
            self.frame = 0

        self.image = self.animations[self.action][self.frame // self.animation_speed]

        self.orb_offset = 35 + math.sin(pygame.time.get_ticks()*0.007)*7  # Distance above the player

    def draw(self, surface):
        # Draw the player
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)

        # Calculate orb position relative to the player
        orb_x = self.rect.centerx - (self.orb_image.get_width() // 2)
        orb_y = self.rect.top - self.orb_offset
        flipped_orb_image = pygame.transform.flip(self.orb_image, self.flip, False)

        # Draw the orb
        surface.blit(flipped_orb_image, (orb_x, orb_y))

    def change_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame = 0
    
class Enemy:
    def __init__(self, x, y, width, height, speed, health, animations, player):
        self.x = random.randint(0, 800)
        self.y = 200
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.rect = pygame.Rect(x, y, 30, 30)
        self.shoot_cooldown = 0
        self.balls = []
        self.flip = False
        self.health = health
        self.frame = 0
        self.animation_speed = 10
        self.speed = speed
        self.animations = animations
        self.action = "Walking"
        self.image = self.animations[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_shot = pygame.time.get_ticks()
        self.balls = []
        self.bullet_image = pygame.image.load("images/Ballz/projectile.png").convert_alpha()
        self.player = player
        self.bigballzhitby = []

    def move(self):
        # Check direction to flip the image
        if self.player.x < self.x:
            self.flip = True
        else:
            self.flip = False

        # Calculate distance vector (dx, dy) toward the player
        dx = self.player.x - self.x
        dy = self.player.y - self.y

        # Calculate the distance
        distance = math.hypot(dx, dy)

        # Ensure the distance is non-zero to avoid division errors
        if distance > 0:
            # Normalize the direction vector
            dx /= distance
            dy /= distance

            # Update position
            self.x += dx * self.speed
            self.y += dy * self.speed

            # Update rect position to match
            self.rect.topleft = (self.x, self.y)




    def shoot(self, player_rect):
        # angle = math.atan2(player_rect.centery - self.rect.centery, player_rect.centerx - self.rect.centerx)
        angle = 30
        x_vel = math.cos(angle) * 4
        y_vel = math.sin(angle) * 4
        self.balls.append(Ball(self.rect.centerx, self.rect.centery, x_vel, y_vel, 2, 3))
        self.shoot_cooldown = 60
    
    def take_damage(self, a):
        self.health -= a

    def upd(self):
        self.shoot_cooldown -= 1
        
        if self.shoot_cooldown < 0:
            self.shoot(self.player.rect)
        
        self.move()
        self.animate()

    def animate(self):
        self.animation_speed = 4
        self.frame += 1
        if self.frame >= len(self.animations[self.action]) * self.animation_speed:
            self.frame = 0

        self.image = self.animations[self.action][self.frame // self.animation_speed]

    def draw(self, surface):
        # Draw the player
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)

    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.balls:
            bullet.move(screen.get_width(), screen.get_height(), [])
            bullet.render(screen)