import pygame
from settings import *
from entity import Entity
from support import *
from debugOnScreen import *


class Enemy(Entity):
    def __init__(self, monsterName, position, groups, obstacleSprites, damagePlayer, triggerDeathParticles, addExp):

        # general setup
        super().__init__(groups)
        self.spriteType = 'enemy'

        # graphics setup
        self.import_graphics(monsterName)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frameIndex]

        # movement
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacleSprites = obstacleSprites

        # stats
        self.monsterName = monsterName
        monsterInfo = monsterData[self.monsterName]
        self.HP = monsterInfo['HP']
        self.exp = monsterInfo['exp']
        self.speed = monsterInfo['speed']
        self.attackDamage = monsterInfo['damage']
        self.resistance = monsterInfo['resistance']
        self.attackRadius = monsterInfo['attackRadius']
        self.noticeRadius = monsterInfo['noticeRadius']
        self.attackType = monsterInfo['attackType']

        # player interaction
        self.attackStatus = False
        self.attackTimeRecord = None
        self.attackCooldown = 1000
        self.damagePlayer = damagePlayer
        self.triggerDeathParticles = triggerDeathParticles
        self.addExp = addExp

        # invincibility timer
        self.vulnerable = False
        self.hitTime = None
        self.invincibilityDuration = 350

        #sound
        self.deathSound = pygame.mixer.Sound('../assets/github/audio/death.wav')
        self.hitSound = pygame.mixer.Sound('../assets/github/audio/hit.wav')
        self.attackSound = pygame.mixer.Sound(monsterInfo['attackSound'])
        self.deathSound.set_volume(0.2)
        self.hitSound.set_volume(0.2)
        self.attackSound.set_volume(0.2)

    def import_graphics(self, name):
        if name == 'specialRaccoon':
            name = 'raccoon'
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../assets/github/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def setDistanceDirection(self, player):
        enemyVector = pygame.math.Vector2(self.rect.center)
        playerVector = pygame.math.Vector2(player.rect.center)
        distance = (playerVector - enemyVector).magnitude()

        if distance > 0:
            direction = (playerVector - enemyVector).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def getStatus(self, player):
        distance = self.setDistanceDirection(player)[0]
        # print(distance)

        if distance <= self.attackRadius and (not self.attackStatus):
            if self.status != 'attack':
                self.frameIndex = 0
            self.status = 'attack'

        elif distance <= self.noticeRadius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            self.attackTimeRecord = pygame.time.get_ticks()
            self.damagePlayer(self.attackDamage, self.attackType)
            self.attackSound.play()
        elif self.status == 'move':
            self.direction = self.setDistanceDirection(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed

        if self.frameIndex >= len(animation):
            if self.status == 'attack':
                self.attackStatus = True
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        #flickering effect
        if self.vulnerable:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attackStatus:
            if current_time - self.attackTimeRecord >= self.attackCooldown:
                self.attackStatus = False

        if self.vulnerable:
            if current_time - self.hitTime >= self.invincibilityDuration:
                self.vulnerable = False

    def getDamage(self, player, attackType):
        if not self.vulnerable:
            self.hitSound.play()
            self.direction = self.setDistanceDirection(player)[1]
            if attackType == 'weapon':
                self.HP -= player.getWeaponDamage()
            else:
                self.HP -= player.getMagicDamage()
                pass
            self.hitTime = pygame.time.get_ticks()
            self.vulnerable = True


    def checkDeath(self):
        if self.HP <= 0:
            self.kill()
            self.triggerDeathParticles(self.rect.center, self.monsterName)
            self.addExp(self.exp)
            self.deathSound.play()

    def hitReaction(self):
        if self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hitReaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.checkDeath()


    def enemyUpdate(self, player):
        self.getStatus(player)
        self.action(player)
