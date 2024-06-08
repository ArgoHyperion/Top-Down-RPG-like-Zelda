import pygame
from settings import *
from tile import *
from player import *
from debugOnScreen import debug
from support import *
from random import choice
from weapon import *
from UI import *
from enemy import *

class LEVEL:
    def __init__(self):

        #display surface
        self.displaySurface = pygame.display.get_surface()
        self.gamePaused = False

        #sprite groups
        self.visibleSprites = YSortCameraGroup()
        self.obstacleSprites = pygame.sprite.Group()

        #attack
        self.currentAttack = None
        self.attackSprites = pygame.sprite.Group()
        self.attackableSprites = pygame.sprite.Group()

        self.createMap()

        #user interface
        self.ui = UI()
    def createMap(self):

        layout = {
            'boundary': import_csv_layout('../assets/github/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../assets/github/map/map_Grass.csv'),
            'object': import_csv_layout('../assets/github/map/map_Objects.csv'),
            'entities': import_csv_layout('../assets/github/map/map_Entities.csv'),
        }
        graphics = {
            'grass': import_folder('../assets/github/graphics/grass'),
            'object': import_folder('../assets/github/graphics/objects')
        }


        for type, layout in layout.items():
            for indexR, row in enumerate(layout):
                for indexC, cell in enumerate(row):
                    if cell != '-1':
                        x = indexC*TILESIZE
                        y = indexR*TILESIZE
                        if type == 'boundary':
                            Tile((x,y),
                                 [self.obstacleSprites],
                                 'invisible')

                        if type == 'grass':
                            randomGrassImage = choice(graphics['grass'])
                            Tile((x,y),
                                 [self.visibleSprites,self.obstacleSprites,self.attackableSprites],
                                 'grass',
                                 randomGrassImage)

                        if type == 'object':
                            surface = graphics['object'][int(cell)]
                            Tile((x,y),
                                 [self.visibleSprites,self.obstacleSprites],
                                 'object',surface)

                        if type == 'entities':
                            if cell == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visibleSprites],
                                    self.obstacleSprites,
                                    self.createAttack,
                                    self.removeAttack,
                                    self.createMagic,
                                    self.removeMagic)
                            else:
                                if cell == '390':
                                    monsterName = 'bamboo'
                                elif cell == '391':
                                    monsterName = 'spirit'
                                elif cell == '392':
                                    monsterName = 'raccoon'
                                else:
                                    monsterName = 'squid'
                                Enemy(
                                    monsterName,
                                    (x, y),
                                    [self.visibleSprites, self.attackableSprites],
                                    self.obstacleSprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)



    def createAttack(self):
        self.currentAttack = Weapon(self.player,[self.visibleSprites,self.attackSprites])

    def createMagic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)


    def removeAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None
        # pass

    def removeMagic(self):
        pass

    def playerAttackLogic(self):
        if self.attackSprites:
            for sprite in self.attackSprites:
                collisionSprites = pygame.sprite.spritecollide(sprite,self.attackableSprites, False)
                if collisionSprites:
                    for targetSprite in collisionSprites:
                        if targetSprite.spriteType == 'grass':
                            targetSprite.kill()
                        else:
                            targetSprite.getDamage(self.player,sprite.spriteType)





    def damage_player(self, amount, attack_type):
        # if self.player.vulnerable:
        #     self.player.HP -= amount
        #     self.player.vulnerable = False
        #     self.player.hurt_time = pygame.time.get_ticks()
        #     self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
        pass

    def trigger_death_particles(self):
        pass

    def add_exp(self):
        pass

    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.visibleSprites.update()
        self.visibleSprites.enemyUpdate(self.player)
        self.playerAttackLogic()
        self.ui.display(self.player)



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_width()//2
        self.halfHeight = self.displaySurface.get_height()//2
        self.offset = pygame.math.Vector2()

        #create the floor
        self.floorSurface = pygame.image.load('../assets/github/graphics/tilemap/ground.png').convert_alpha()
        self.floorRect = self.floorSurface.get_rect(topleft = (0,0))

    def customDraw(self,player):


        #getting the offset
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        #drawing floor before sprites with offset
        floorPosition = self.floorRect.topleft - self.offset
        self.displaySurface.blit(self.floorSurface,floorPosition)


        #adding offset to each sprite in group
        for sprite in sorted(self.sprites(),key=lambda x: x.rect.centery):
            offsetPosition = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPosition)

    def enemyUpdate(self,player):
        enemySprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']

        for enemy in enemySprites:
            enemy.enemyUpdate(player)

