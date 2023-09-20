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
      self.platform_width = 100
      self.panel_rects, self.row_rects = self.get_rects()
      
   def get_rects(self):
      panel_rects = []
      row_rects = []

      panel_rects.append(pygame.Rect(self.x, self.y, self.panel_width, self.border_width))
      panel_rects.append(pygame.Rect(self.x + self.panel_width - self.border_width, self.y, self.border_width, self.panel_height))
      panel_rects.append(pygame.Rect(self.x, self.y + self.panel_height - self.border_width, self.panel_width, self.border_width))
      panel_rects.append(pygame.Rect(self.x, self.y, self.border_width, self.panel_height))

      y = self.y + self.border_width + self.row_width
      while y + self.border_width + self.row_width <= self.y + self.panel_height:
         x = random.randint(self.x, self.panel_width - self.platform_width + self.x)
         rect = pygame.Rect(x, y, self.platform_width, self.border_width)
         row_rects.append(rect)
         y += self.border_width + self.row_width

      return panel_rects, row_rects
   
   def change_rects(self, screen):
      y = self.y + self.border_width + self.row_width
      rectindex = 0
      while y + self.border_width + self.row_width <= self.y + self.panel_height: 
         if random.randint(0, 1) > 0.5: # checking if the row should be changed or not
            x = random.randint(self.x, self.panel_width - self.platform_width + self.x)
            rect = pygame.Rect(x, y, self.platform_width, self.border_width)
            self.row_rects[rectindex] = rect
         rectindex += 1
         y += self.border_width + self.row_width
      self.draw_rects(screen)


   def draw_panels(self, screen):
      pygame.draw.rect(screen, self.border_color, self.panel_rects[0])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[1])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[2])
      pygame.draw.rect(screen, self.border_color, self.panel_rects[3])


   def draw_rects(self, screen):
      for rect in self.row_rects:
         pygame.draw.rect(screen, self.row_color, rect)

class game:
   def __init__(self) -> None:
      pygame.init()
      displayInfo = pygame.display.Info()
      self.screen_height, self.screen_width = [int(displayInfo.current_h), int(displayInfo.current_w/1.4)]
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
      pygame.display.set_caption("Game")
      self.clock = pygame.time.Clock()
      self.fps = 30
      self.timer = 0
      self.rectAlterDelay = 2 # seconds 

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
         self.timer += 1
         if self.timer == self.fps * self.rectAlterDelay:
            self.timer = 0
            self.panel.change_rects(self.screen)

         # check and handle keyboard and mouse events
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()

         # draw inside panel
         self.panel.draw_rects(self.screen)
         self.panel.draw_panels(self.screen)

         pygame.display.update()

if __name__ == '__main__':
   obj = game()
   obj.run()