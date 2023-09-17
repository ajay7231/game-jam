import pygame
from panel import Panel
from settings import *
import random

class Game(Panel):
   def __init__(self) -> None:
      super().__init__(WIDTH-2*PADDING, HEIGHT-2*PADDING)
      self.rect.topleft = (PADDING, PADDING)
      self.line_surface = self.surface.copy()
      self.line_surface.fill((0, 255, 0))
      self.line_surface.set_colorkey((0, 255, 0))
      self.line_surface.set_alpha(120)


   def run(self):
      self.surface.fill(GRAY)
      self.draw()
      self.display_surface.blit(self.surface, (PADDING, PADDING))
      pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
   
   def draw(self):
      
        for row in range(1, ROWS):
            y = row * ROW_HEIGHT
            random_width = RANDOM_WIDTHS[row-1]
            display_width = self.surface.get_width()

            
            x1 = pygame.Rect(random_width, y, CANAL_WIDTH, LINE_THICKNESS)
            x2 = pygame.Rect(random_width, y, CANAL_WIDTH, LINE_THICKNESS)

            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (random_width, y), LINE_THICKNESS)
            pygame.draw.line(self.line_surface, LINE_COLOR, (random_width+CANAL_WIDTH, y), (display_width, y), LINE_THICKNESS)


        self.surface.blit(self.line_surface, (0, 0))
   
   
      
      