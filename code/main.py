import pygame
from colors import *
import random
import numpy as np
from player import Player

class Panel:
   def __init__(self, x, y, panel_height, panel_width, border_width, border_color, row_width, row_color):
      self.x = x # top left
      self.y = y # top left
      self.dy = 0.
      self.panel_height = panel_height
      self.panel_width = panel_width
      self.border_width = border_width
      self.border_color = border_color
      self.row_width = row_width
      self.row_color = row_color
      self.platform_width = 80
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
   
   # def change_rects(self, screen):
   #    for i in range(len(self.row_rects)):
   #       if random.randint(0, 1) > 0.8:
   #          if self.row_rects[i].x < self.x + self.panel_width - self.platform_width:
   #             new_x = min(max(self.x , abs(np.random.normal(self.x + (self.panel_width - self.platform_width)/2, 100))), self.x + self.panel_width - self.platform_width)
   #             rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
   #             self.row_rects[i] = rect
   #          else:
   #             new_x = min(max(self.x , abs(np.random.normal(self.x + (2*self.panel_width - self.platform_width)/2, 100))), self.x + self.panel_width - self.platform_width)
   #             rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
   #             self.row_rects[i] = rect
   #          # new_x = min(max(self.x , np.random.normal(self.row_rects[i].x, 100)), self.x + self.panel_width - self.platform_width)
   #          # x = random.randint(self.x, self.panel_width - self.platform_width + self.x)
   #          # rect = pygame.Rect(new_x, self.row_rects[i].y, self.platform_width, self.border_width)
   #          # self.row_rects[i] = rect
   #    self.draw_rects(screen)

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
      self.fps = 40
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
      
      self.player = Player(
         x=0.,
         y=0.,
         h=24,
         w=24,
         color=CYAN
      )

      self.player.rect.center = self.panel.row_rects[int(len(self.panel.row_rects)/2)].center
      self.player.rect.bottom = self.panel.row_rects[int(len(self.panel.row_rects)/2)].top
      
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
         # self.timer += 1

         # check and handle keyboard and mouse events
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()

            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP and self.player.jump_power:
                  self.player.dy = -22.
   
               # if event.key == pygame.K_DOWN:
               #    direction[1] = -1
               
               if event.key == pygame.K_RIGHT:
                  self.player.dx = 6.

               if event.key == pygame.K_LEFT:
                  self.player.dx = -6.
            
            if event.type == pygame.KEYUP:
               if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                  self.player.dx = 0.

         # player movements
         # apply gravity on player
         self.player.dy = min(self.player.dy + 1.4, 14.)
         # check collision 
         # first move horizontally
         self.player.move_x()
         for rect in self.panel.row_rects:
            if self.player.rect.colliderect(rect):
               if self.player.dx < 0.:
                  self.player.rect.left = rect.right
               else:
                  self.player.rect.right = rect.left
               self.player.dx = 0.

         # now move vertically
         self.player.move_y()
         # move row_rects
         if self.player.dy < 0.:
            self.panel.move_row_rects(abs(self.player.dy))
         self.player.jump_power = 0
         for rect in self.panel.row_rects:
            if self.player.rect.colliderect(rect):
               if self.player.dy < 0.:
                  self.player.rect.top = rect.bottom
               else:
                  self.player.jump_power = 1
                  self.player.rect.bottom = rect.top
               self.player.dy = 0.


         # add and remove rects
         self.panel.add_rects(self.player.net_dy)
         self.panel.remove_rects()


         # if self.timer > self.fps * self.rectAlterDelay and  direction[1] == 0:
         #    # wait for 2 seconds and then change the rects
         #    self.timer = 0
         #    self.panel.change_rects(self.screen)


         # draw inside panel
         self.panel.draw_rects(self.screen)
         self.panel.draw_panels(self.screen)

         # draw player
         self.player.draw(self.screen)

         pygame.display.update()

if __name__ == '__main__':
   obj = game()
   obj.run()