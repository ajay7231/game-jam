import pygame
from settings import *
from game import Game

class Main:
   def __init__(self) -> None:
      pygame.init()
      self.screen = pygame.display.set_mode(GAME_SIZE)
      pygame.display.set_caption("Game")
      self.clock = pygame.time.Clock()
      self.game = Game()

   def run(self):
      while True:
         self.clock.tick(FPS)
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               exit()
         self.screen.fill(GRAY)
         self.game.run()

         pygame.display.update()

if __name__ == '__main__':
   main = Main()
   main.run()