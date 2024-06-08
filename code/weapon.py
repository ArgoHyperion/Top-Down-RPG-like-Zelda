import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)

        self.spriteType = 'weapon'

        #get direction of player
        direction = player.status
        if 'Idle' in direction:
            direction = direction.replace('Idle','')
        if 'Atk' in direction:
            direction = direction.replace('Atk','')

        fullPath = f'../assets/github/graphics/weapons/{player.weapon}/{direction}.png'
        #graphic
        self.image = pygame.image.load(fullPath).convert_alpha()



        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-8,0))

