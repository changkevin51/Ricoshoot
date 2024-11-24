import pygame

class Ball:
    def __init__(self, x, y, vel_x, vel_y, damage, size=20):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.image = pygame.image.load("images/Ballz/projectile.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.count = 0
        self.changed = False
        self.damage = damage
        self.just_collided = False
        self.size = size


    def move(self, screen_width, screen_height):
        self.x += self.vel_x
        self.y += self.vel_y

        # Bounce on collision with screen borders
        if self.x > screen_width - self.rect.width or self.x < 0:
            self.vel_x *= -1
            self.count+=1
        if self.y > screen_height - self.rect.height or self.y < 0:
            self.vel_y *= -1
            self.count+=1
        
        self.rect.topleft = (self.x, self.y)
        self.radius = 10
        ball_rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
    
    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def change_image(self):
        if not self.changed:
            self.image = pygame.image.load("images/Ballz/enemy_projectile.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.changed = True
