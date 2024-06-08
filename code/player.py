import pygame
from pygame import Vector2
from debugOnScreen import *
from settings import *
from support import *
from entity import *
class Player(Entity):
    def __init__(self, position, groups, obstacleSprites, createAttack, removeAttack, createMagic, removeMagic):
        super().__init__(groups)
        self.image = pygame.image.load('../assets/graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0,-20)

        #graphic setup
        self.import_player_assets()
        self.status = 'down'


        #movement

        # self.speed = 5
        self.obstacleSprites = obstacleSprites

        #weapon
        self.createAttack = createAttack
        self.removeAttack = removeAttack
        self.weaponIndex = 0
        self.weapon = list(weaponData.keys())[self.weaponIndex]
        self.weaponSwitch = True
        self.weaponSwitchTimeRecord = None


        #magic
        self.createMagic = createMagic
        self.magicIndex = 0
        self.magic = list(magicData.keys())[self.magicIndex]
        self.magicSwitch = True
        self.magicSwitchTimeRecord = None

        #switch cooldown
        self.switchCooldown = 200

        #normal attack
        self.attackStatus = False
        self.attackCooldown = 100
        self.attackTimeRecord = 0

        #stat
        self.stats = {'HP': 100, 'MP': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.HP = self.stats['HP']*0.5
        self.MP = self.stats['MP']
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assets(self):
        characterPath = '../assets/graphics/player/'
        self.animations = {'up': [],
                           'down': [],
                           'left': [],
                           'right': [],
                           'upIdle': [],
                           'downIdle': [],
                           'leftIdle': [],
                           'rightIdle': [],
                           'upAtk': [],
                           'downAtk': [],
                           'leftAtk': [],
                           'rightAtk': [],
        }

        for animation in self.animations:
            self.animations[animation] = import_folder(characterPath + animation)

    def input(self):
        if not self.attackStatus:
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attackStatus = True
                self.attackTimeRecord = pygame.time.get_ticks()
                self.createAttack()

            #magic input
            if keys[pygame.K_e]:
                self.attackStatus = True
                self.attackTimeRecord = pygame.time.get_ticks()
                style = self.magic
                strength = magicData[style]['strength'] + self.stats['magic']
                cost = magicData[style]['cost']


                self.createMagic(style,strength,cost)

            if keys[pygame.K_q] and self.weaponSwitch:
                self.weaponSwitch = False
                self.weaponSwitchTimeRecord = pygame.time.get_ticks()

                if self.weaponIndex < len(list(weaponData.keys()))-1:
                    self.weaponIndex += 1
                else:
                    self.weaponIndex = 0

                self.weapon = list(weaponData.keys())[self.weaponIndex]
                # self.attackCooldown = (weaponData[f'{self.weapon}'])['cooldown']

            if keys[pygame.K_r] and self.magicSwitch:
                self.magicSwitch = False
                self.magicSwitchTimeRecord = pygame.time.get_ticks()

                if self.magicIndex < len(list(magicData.keys()))-1:
                    self.magicIndex += 1
                else:
                    self.magicIndex = 0

                self.magic = list(magicData.keys())[self.magicIndex]

    def getStatus(self):
        if self.direction == Vector2(0, 0) and not ('Idle' in self.status or 'Atk' in self.status):
            self.status = self.status + 'Idle'

        if self.attackStatus:
            self.direction = Vector2(0, 0)
            if 'Atk' not in self.status:
                if 'Idle' in self.status:
                    self.status = self.status.replace('Idle','Atk')
                else:
                    self.status = self.status + 'Atk'
        else:
            if 'Atk' in self.status:
                self.status = self.status.replace('Atk','')



    def cooldown(self):
        currentTime = pygame.time.get_ticks()
        if self.attackStatus:
            if currentTime - self.attackTimeRecord >= self.attackCooldown + weaponData[f'{self.weapon}']['cooldown']:
                self.attackStatus = False
                self.removeAttack()

        if not self.weaponSwitch:
            if currentTime - self.weaponSwitchTimeRecord >= self.switchCooldown:
                self.weaponSwitch = True

        if not self.magicSwitch:
            if currentTime - self.magicSwitchTimeRecord >= self.switchCooldown:
                self.magicSwitch = True

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        #set image
        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def getWeaponDamage(self):
        baseDamage = self.stats['attack']
        weaponDamage = weaponData[f'{self.weapon}']['damage']

        return baseDamage + weaponDamage

    def update(self):
        self.input()
        self.getStatus()
        self.cooldown()
        self.animate()
        self.move(self.speed)
        # debug(self.magicIndex,10,500)
