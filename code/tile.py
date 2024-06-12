import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, spriteType, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        self.spriteType = spriteType
        self.image = surface

        if spriteType == 'object':
            self.rect = self.image.get_rect(midleft=(position[0], position[1]))
            self.hitbox = self.image.get_rect(topleft=(position[0], position[1]-(TILESIZE//2)+9))
            self.hitbox.height = self.hitbox.height//1.9
            self.hitbox = self.hitbox.inflate(-10,0)

        elif spriteType == 'invisible':
            offset = 16
            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - offset, TILESIZE, TILESIZE + offset//8)
            # print(self.hitbox)
            # self.hitbox = self.rect.inflate(-10, -10)

        else:
            self.rect = self.image.get_rect(topleft=position)
            self.hitbox = self.image.get_rect(topleft=position)
            self.hitbox = self.rect.inflate(-10,-10)
