import pygame
import random
import numpy as np
from player import Player
from settings import *

class Panel:
   def __init__(self):
      self.dy = 0.
      self.panel_rects, self.row_rects = self.get_rects()
      self.bullets = []
      self.guns = [
         Gun(x=PANEL_START_X, y =(PANEL_END_Y)//2 , direction=1),
         Gun(x=PANEL_END_X-GUN_WIDTH , y =PANEL_END_Y//2 , direction=-1)
      ]

   def draw_guns(self, screen):
      for gun in self.guns:
         gun.draw(screen)

   def move_guns(self,screen):
      for gun in self.guns:
         new_y = random.randint(PANEL_START_Y, PANEL_END_Y-20)
         gun.rect.y = new_y
         gun.draw(screen)


   def get_rects(self):
      panel_rects = []
      row_rects = []

      panel_rects.append(pygame.Rect(PANEL_START_X, PANEL_START_Y, PANEL_WIDTH, BORDER_WIDTH))
      panel_rects.append(pygame.Rect(PANEL_END_X - BORDER_WIDTH, PANEL_START_Y, BORDER_WIDTH, PANEL_HEIGHT))
      panel_rects.append(pygame.Rect(PANEL_START_X, PANEL_END_Y - BORDER_WIDTH, PANEL_WIDTH, BORDER_WIDTH))
      panel_rects.append(pygame.Rect(PANEL_START_X, PANEL_START_Y, BORDER_WIDTH, PANEL_HEIGHT))

      y = PANEL_START_Y + BORDER_WIDTH + ROW_WIDTH
      while y + BORDER_WIDTH + ROW_WIDTH <= PANEL_END_Y:
         x = random.randint(PANEL_START_X, PANEL_END_X - PLATFORM_WIDTH)
         rect = pygame.Rect(x, y, PLATFORM_WIDTH, BORDER_WIDTH)
         row_rects.append(rect)
         y += BORDER_WIDTH + ROW_WIDTH

      return panel_rects, row_rects

   def move_row_rects(self, dy):
      for i in range(len(self.row_rects)):
         self.row_rects[i].y += dy
   
   def add_rects(self, net_dy):
      if net_dy > BORDER_WIDTH + ROW_WIDTH:
         y = self.row_rects[0].y
         while y - BORDER_WIDTH - ROW_WIDTH >= PANEL_START_Y + BORDER_WIDTH:
            x = random.randint(PANEL_START_X, PANEL_END_X - PLATFORM_WIDTH)
            rect = pygame.Rect(x, y - BORDER_WIDTH - ROW_WIDTH, PLATFORM_WIDTH, BORDER_WIDTH)
            self.row_rects.insert(0, rect)
            y -= BORDER_WIDTH + ROW_WIDTH
      net_dy = 0.
      
   def remove_rects(self):
      for rect in self.row_rects:
         if rect.y < PANEL_START_Y or rect.y > PANEL_END_Y:
            self.row_rects.remove(rect)
         

   def draw_panels(self, screen):
      for rect in self.panel_rects:
         pygame.draw.rect(screen, BORDER_COLOR, rect)


   def draw_rects(self, screen):
      for rect in self.row_rects:
         pygame.draw.rect(screen, ROW_COLOR, rect)


class Bullet:
   def __init__(self, x, y):
      self.rect = pygame.Rect(x, y, 5, 5)
      self.color = BULLET_COLOR
      self.dx = 0

   def draw(self, screen):
      pygame.draw.rect(screen, self.color, self.rect)

   def move(self):
      self.rect.x += self.dx
   

class Gun:
   def __init__(self, x, y,direction):
      self.rect = pygame.Rect(x, y, GUN_WIDTH, GUN_HEIGHT)
      self.color = GUN_COLOR
      self.bullets = []
      self.direction = direction

   def draw(self, screen):
      pygame.draw.rect(screen, self.color, self.rect)

   def shoot(self):
      self.bullets.append(Bullet(x=self.rect.x, y=self.rect.y))
      
   def animate(self,screen,player):
      for bullet in self.bullets:
         if(bullet.rect.colliderect(player.rect)):
            player.health -= 2
            print(player.health)
            self.bullets.remove(bullet)
         bullet.dx = self.direction * 5
         bullet.move()
         bullet.draw(screen)
         if bullet.rect.x < PANEL_START_X or bullet.rect.x > PANEL_END_X:
            self.bullets.remove(bullet)
      


      

      

class game:
   def __init__(self) -> None:
      displayInfo = pygame.display.Info()
      self.screen_height, self.screen_width = [int(displayInfo.current_h), int(displayInfo.current_w/1.4)]
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
      pygame.display.set_caption("Game")
      self.clock = pygame.time.Clock()
      self.fps = 40
      self.bullet_timer = 0
      self.gun_timer = 0
      self.shoot_delay = 1 # seconds
      self.gun_movement_delay = 3
      self.panel = Panel()
       # seconds 
      

   def run(self):
      
      self.player = Player(
         x=0.,
         y=0.,
         h=24,
         w=24,
         color=CYAN
      )

      self.player.rect.center = self.panel.row_rects[int(len(self.panel.row_rects)/2)].center
      self.player.rect.bottom = self.panel.row_rects[int(len(self.panel.row_rects)/2)].top
      
      while True:
         self.clock.tick(self.fps)
         self.screen.fill(GRAY)
         self.bullet_timer += 1
         self.gun_timer += 1

         # check and handle keyboard and mouse events
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()

            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP and self.player.jump_power:
                  self.player.dy = -18.

               if event.key == pygame.K_SPACE and self.player.boost_power:
                  self.player.dy += self.player.boost
                  # self.player.boost_power = 0
      
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


         if self.bullet_timer > self.fps * self.shoot_delay:
            # wait for 2 seconds and then change the rects
            self.bullet_timer = 0
            for gun in self.panel.guns:
               gun.shoot()
               # self.panel.move_guns(self.screen)
         if self.gun_timer > self.fps * self.gun_movement_delay:
            self.gun_timer = 0
            self.panel.move_guns(self.screen)
         
         for gun in self.panel.guns:
            gun.animate(self.screen, self.player)


         # draw inside panel
         self.panel.draw_rects(self.screen)
         self.panel.draw_panels(self.screen)
         self.panel.draw_guns(self.screen)

         # draw player
         self.player.draw(self.screen)

         pygame.display.update()

if __name__ == '__main__':
   obj = game()
   obj.run()