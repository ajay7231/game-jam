import pygame
from colors import *
import random
import numpy as np

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
      for i in range(len(self.row_rects)):
         if random.randint(0, 1) > 0.8:
            if self.row_rects[i].x < self.x + self.panel_width - self.platform_width:
               new_x = min(max(self.x , abs(np.random.normal(self.x + (self.panel_width - self.platform_width)/2, 100))), self.x + self.panel_width - self.platform_width)
               rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
               self.row_rects[i] = rect
            else:
               new_x = min(max(self.x , abs(np.random.normal(self.x + (2*self.panel_width - self.platform_width)/2, 100))), self.x + self.panel_width - self.platform_width)
               rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
               self.row_rects[i] = rect
            # new_x = min(max(self.x , np.random.normal(self.row_rects[i].x, 100)), self.x + self.panel_width - self.platform_width)
            # x = random.randint(self.x, self.panel_width - self.platform_width + self.x)
            # rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
            # self.row_rects[i] = rect
      self.draw_rects(screen)

   def move_row_rects(self, dy):
      for i in range(len(self.row_rects)):
         self.row_rects[i].y += dy
   
   def add_rects(self, net_dy):
      if net_dy > self.border_width + self.row_width:
         y = self.row_rects[0].y
         while y - self.border_width - self.row_width >= self.y + self.border_width:
            x = random.randint(self.x, self.panel_width - self.platform_width + self.x)
            rect = pygame.Rect(x, y - self.border_width - self.row_width, self.platform_width, self.border_width)
            self.row_rects.insert(0, rect)
            y -= self.border_width + self.row_width
      net_dy = 0.
      
   def remove_rects(self):
      for rect in self.row_rects:
         if rect.y < self.y or rect.y > self.y + self.panel_height:
            self.row_rects.remove(rect)
         

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
                         row_width=100, row_color=WHITE)
      
      dy = 0.
      net_dy = 0.
      direction = [0, 0]
      '''
      Steps to be followed in a loop:
      1. check for inputs
      2. update entities w.r.t received inputs
      3. draw entities
      4. update screen
      '''
      while True:
         self.clock.tick(self.fps)
         self.screen.fill(GRAY)
         self.timer += 1

         # check and handle keyboard and mouse events
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()

            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                  direction[1] = 1
   
               if event.key == pygame.K_DOWN:
                  direction[1] = -1
            
            if event.type == pygame.KEYUP:
               direction[1] = 0
                  
         # checking y displacement
         if direction[1] != 0:
            dy = -5. if direction[1] == -1 else 5.
         else:
            dy = 0.

         # net displacment in y direction
         net_dy += dy
         self.panel.move_row_rects(dy)

         # add and remove rects
         self.panel.add_rects(net_dy)
         self.panel.remove_rects()


         if self.timer > self.fps * self.rectAlterDelay and  direction[1] == 0:
            # wait for 2 seconds and then change the rects
            self.timer = 0
            self.panel.change_rects(self.screen)

         # move row_rects

         # draw inside panel
         self.panel.draw_rects(self.screen)
         self.panel.draw_panels(self.screen)

         pygame.display.update()

if __name__ == '__main__':
   obj = game()
   obj.run()