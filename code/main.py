import pygame, sys
from settings import *
from debugOnScreen import *
from gameOperator import *

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('TestProject')

        self.clock = pygame.time.Clock()

        self.level = LEVEL()

        self.mainSound = pygame.mixer.Sound('../assets/github/audio/sadtheme.ogg')
        self.mainSound.set_volume(0.05)
        self.mainSound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggleMenu()


            self.screen.fill(WATER_COLOR)
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
