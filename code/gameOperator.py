import pygame
from settings import *
from tile import *
from player import *
from debugOnScreen import debug
from support import *
from random import choice, randint
from weapon import *
from UI import *
from enemy import *
from particles import *
from magic import *
from upgrademenu import UpgradeMenu

class LEVEL:
    def __init__(self):

        #display surface
        self.displaySurface = pygame.display.get_surface()
        self.gamePaused = False
        self.ended = False

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
        self.upgradeMenu = UpgradeMenu(self.player)

        #particles
        self.animationPlayer = AnimationPlayer()
        self.magicPlayer = MagicPlayer(self.animationPlayer)
    def createMap(self):

        layout = {
            # 'boundary': import_csv_layout('../assets/github/map/map_FloorBlocks.csv'),
            # 'grass': import_csv_layout('../assets/github/map/map_Grass.csv'),
            # 'object': import_csv_layout('../assets/github/map/map_Objects.csv'),
            # 'entities': import_csv_layout('../assets/github/map/map_Entities.csv'),
            'boundary': import_csv_layout('../assets/maps/map_Blocks.csv'),
            'grass': import_csv_layout('../assets/maps/map_Grass.csv'),
            'object': import_csv_layout('../assets/maps/map_Objects.csv'),
            'entities': import_csv_layout('../assets/maps/map_Entities.csv'),
            'desertHouses': import_csv_layout('../assets/maps/map_DesertHouses.csv'),
            'normalHouses': import_csv_layout('../assets/maps/map_NormalHouses.csv'),


        }
        graphics = {
            'grass': import_folder('../assets/github/graphics/grass'),
            # 'object': import_folder('../assets/github/graphics/objects')
            'object': import_folder('../assets/graphics/objects'),
            'desertHouse': import_folder('../assets/graphics/desertHouses'),
            'normalHouse': import_folder('../assets/graphics/normalHouses'),
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

                        if type == 'desertHouses':
                            surface = graphics['desertHouse'][int(cell)]
                            Tile((x,y),
                                 [self.visibleSprites,self.obstacleSprites],
                                 'object',surface)

                        if type == 'normalHouses':
                            surface = graphics['normalHouse'][int(cell)]
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
                                    self.createMagic)
                            else:
                                if cell == '390':
                                    monsterName = 'bamboo'
                                elif cell == '391':
                                    monsterName = 'spirit'
                                elif cell == '392':
                                    monsterName = 'raccoon'
                                elif cell == '239':
                                    monsterName = 'specialRaccoon'
                                else:
                                    monsterName = 'squid'
                                Enemy(
                                    monsterName,
                                    (x, y),
                                    [self.visibleSprites, self.attackableSprites],
                                    self.obstacleSprites,
                                    self.damagePlayer,
                                    self.triggerDeathParticles,
                                    self.addSP)



    def createAttack(self):
        self.currentAttack = Weapon(self.player,[self.visibleSprites,self.attackSprites])

    def createMagic(self,magic,strength,cost):
        if magic == 'heal':
            self.magicPlayer.heal(self.player, strength, cost, [self.visibleSprites])

        if magic == 'flame':
            self.magicPlayer.flame(self.player, cost, [self.visibleSprites, self.attackSprites])




    def removeAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None
        # pass



    def playerAttackLogic(self):
        if self.attackSprites:
            for sprite in self.attackSprites:
                collisionSprites = pygame.sprite.spritecollide(sprite,self.attackableSprites, False)
                if collisionSprites:
                    for targetSprite in collisionSprites:
                        if targetSprite.spriteType == 'grass':
                            position = targetSprite.rect.center
                            offset = pygame.math.Vector2(0,45)
                            for leaf in range(randint(3,6)):

                                self.animationPlayer.createGrassParticles(position - offset,[self.visibleSprites])
                            targetSprite.kill()
                        else:
                            targetSprite.getDamage(self.player,sprite.spriteType)





    def damagePlayer(self, amount, attackType):
        if not self.player.vulnerable:
            self.player.HP -= amount
            self.player.vulnerable = True
            self.player.hurtTime = pygame.time.get_ticks()
            self.animationPlayer.createParticles(attackType, self.player.rect.center, [self.visibleSprites], 'enemyAttack')
            self.player.speed *= 1.2


    def triggerDeathParticles(self, position, particleType):
        self.animationPlayer.createParticles(particleType,position,self.visibleSprites, 'death')


    def addSP(self, amount):
        self.player.skillPoint += amount

    def toggleMenu(self):
        self.gamePaused = not self.gamePaused

    def checkGoodEnding(self):
        enemySprites = [sprite for sprite in self.attackableSprites.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']
        if len(enemySprites) == 0:
            self.ended = True
            self.gamePaused = True
            self.ui.ending()

    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.ui.display(self.player)
        self.checkGoodEnding()

        if self.gamePaused and not self.ended:
            self.upgradeMenu.display()
        else:

            self.visibleSprites.update()
            self.visibleSprites.enemyUpdate(self.player)
            self.playerAttackLogic()




class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_width()//2
        self.halfHeight = self.displaySurface.get_height()//2
        self.offset = pygame.math.Vector2()

        #create the floor
        # self.floorSurface = pygame.image.load('../assets/github/graphics/tilemap/ground.png').convert_alpha()
        self.floorSurface = pygame.image.load('../assets/maps/ground.png').convert_alpha()
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

