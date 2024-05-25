import pygame
from settings import *
from tile import *
from player import *
from debugOnScreen import debug
class LEVEL:
    def __init__(self):

        self.displaySurface = pygame.display.get_surface()

        self.visibleSprites = YSortCameraGroup()
        self.obstacleSprites = pygame.sprite.Group()

        self.createMap()

    def createMap(self):
        for indexR,row in enumerate(WORLD_MAP):
            for indexC, column in enumerate(row):
                x = indexC*TILESIZE
                y = indexR*TILESIZE
                if column == 'x':
                    Tile((x,y),[self.visibleSprites,self.obstacleSprites])
                if column == 'p':
                    self.player = Player((x,y),[self.visibleSprites], self.obstacleSprites)

    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.visibleSprites.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_width()//2
        self.halfHeight = self.displaySurface.get_height()//2
        self.offset = pygame.math.Vector2()

    def customDraw(self,player):

        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        for sprite in sorted(self.sprites(),key=lambda x: x.rect.centery):
            offsetPosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPosition)

