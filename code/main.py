import pygame
from colors import *
import random

class Panel:
   def __init__(self, x, y, panel_height, panel_width, border_width, border_color, row_width, row_color):
      self.x = x # top left
      self.y = y # top left
      self.panel_height = panel_height
      self.panel_width = panel_width
      self.border_width = border_width
      self.border_color = border_color
      self.row_width = row_width
      self.row_color = row_color
      self.panel_rects, self.row_rects = self.get_rects()
      
   def get_rects(self):
      panel_rects = []
      row_rects = []

      # go clockwise
      panel_rects.append(pygame.Rect(self.x, self.y, self.panel_width, self.border_width))
      panel_rects.append(pygame.Rect(self.x + self.panel_width - self.border_width, self.y, self.border_width, self.panel_height))
      panel_rects.append(pygame.Rect(self.x, self.y + self.panel_height - self.border_width, self.panel_width, self.border_width))
      panel_rects.append(pygame.Rect(self.x, self.y, self.border_width, self.panel_height))

      y = self.y + self.border_width + self.row_width
      while y + self.border_width + self.row_width <= self.y + self.panel_height:
         gap = random.randint(50, 100)
         left_width = random.randint(0, self.panel_width - 2*self.border_width - gap)
         right_width = self.panel_width - 2*self.border_width - left_width - gap
         left_rect = None if left_width < 10 else pygame.Rect(self.x + self.border_width, y, left_width, self.border_width)
         right_rect = None if right_width < 10 else pygame.Rect(self.x + self.border_width + left_width + gap, y, right_width, self.border_width)
         row_rects.append([left_rect, right_rect])
         y += self.border_width + self.row_width

      return panel_rects, row_rects

   def draw(self, screen):
      # draw panel borders
      # going clockwise
      pygame.draw.rect(screen, self.border_color, self.panel_rects[0])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[1])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[2])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[3])

      # draw rows
      for left, right in self.row_rects:
         if left != None:
            pygame.draw.rect(screen, self.row_color, left)
            
         if right != None:
            pygame.draw.rect(screen, self.row_color, right)

class game:
   def __init__(self) -> None:
      pygame.init()
      displayInfo = pygame.display.Info()
      self.screen_height, self.screen_width = [int(displayInfo.current_h), int(displayInfo.current_w/1.4)]
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
      pygame.display.set_caption("Game")
      self.clock = pygame.time.Clock()
      self.fps = 30

   def run(self):
      panel_width = int(self.screen_width/2)
      panel_height = int(self.screen_height/1.2)
      self.panel = Panel(x=(self.screen_width - panel_width) / 2., 
                         y=(self.screen_height - panel_height) / 2., 
                         panel_height=panel_height, 
                         panel_width=panel_width, 
                         border_width=2, 
                         border_color=WHITE,
                         row_width=50, row_color=WHITE)

      while True:
         self.clock.tick(self.fps)
         self.screen.fill(GRAY)

         # check and handle keyboard and mouse events
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()

         # draw inside panel
         self.panel.draw(self.screen)

         pygame.display.update()

if __name__ == '__main__':
   obj = game()
   obj.run()