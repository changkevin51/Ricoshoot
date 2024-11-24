import pygame

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale=1.0, text_below=False):
        self.image = pygame.image.load(image) if image else None
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_below = text_below

        if self.image is not None:
            # Scale the image based on the provided scale factor
            original_size = self.image.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            self.image = pygame.transform.scale(self.image, new_size)

            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        self.text_rect = self.text.get_rect()
        self.update_text_position()

    def update_text_position(self):
        if self.text_below and self.image is not None:
            # Place text below the image
            self.text_rect.midtop = self.rect.midbottom
        elif self.image is not None:
            # Place text centered on the image
            self.text_rect.center = self.rect.center
        else:
            # If no image, center text at button position
            self.text_rect.center = (self.x_pos, self.y_pos)

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        self.update_text_position()
