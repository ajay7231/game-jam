import pygame

class Player:
    def __init__(self, x, y, h, w, color) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.direction = [0, 0]
        self.dy = 0.
        self.dx = 0.
        self.net_dy = 0.
        self.jump_power = 0
        self.boost_power = 1
        self.boost = -16.

    def move_x(self):
        self.rect.x += self.dx

    def move_y(self):
        self.rect.y += self.dy
        self.net_dy += abs(self.dy) if self.dy < 0. else 0.

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)