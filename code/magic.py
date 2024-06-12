import pygame
from settings import *
from random import randint
class MagicPlayer:
    def __init__(self, animationPlayer):
        self.animationPlayer = animationPlayer
        self.sounds = {
            'heal': pygame.mixer.Sound('../assets/github/audio/heal.wav'),
            'flame': pygame.mixer.Sound('../assets/github/audio/flame.wav')
        }
        self.sounds['heal'].set_volume(0.2)
        self.sounds['flame'].set_volume(0.2)



    def heal(self, player, strength, cost, groups):
        if player.MP >= cost:
            if player.HP < player.stats['HP']:
                player.HP += strength + (player.stats['magic'] * 0.4)
                player.MP -= cost
            if player.HP >= player.stats['HP']:
                player.HP = player.stats['HP']

            self.animationPlayer.createParticles('aura',player.rect.center, groups, 'magic')
            self.animationPlayer.createParticles('heal', player.rect.center - pygame.math.Vector2(0,30), groups, 'magic')

            self.sounds['heal'].play()


    def flame(self, player, cost, groups):
        if player.MP >= cost:
            player.MP -= cost

            playerMastery = player.stats['MP']//50 + 3

            playerDirection = player.status
            if 'Idle' in playerDirection:
                playerDirection = playerDirection.replace('Idle', '')
            if 'Atk' in playerDirection:
                playerDirection = playerDirection.replace('Atk', '')

            if playerDirection == 'right': direction = pygame.math.Vector2(1,0)
            elif playerDirection == 'left': direction = pygame.math.Vector2(-1,0)
            elif playerDirection == 'down': direction = pygame.math.Vector2(0,1)
            elif playerDirection == 'up': direction = pygame.math.Vector2(0,-1)

            for i in range(1,playerMastery):
                if direction.x:
                    offset = (direction.x * i) * TILESIZE//2
                    x = player.rect.centerx + offset + randint(- TILESIZE//4,TILESIZE//3)
                    y = player.rect.centery + randint(- TILESIZE//4,TILESIZE//4)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')

                    offsetsub = offset // 4
                    x = player.rect.centerx + offset + randint(- TILESIZE // 4, TILESIZE // 3)
                    y = player.rect.centery - offsetsub + randint(- TILESIZE // 4, TILESIZE // 4)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')

                    x = player.rect.centerx + offset + randint(- TILESIZE // 4, TILESIZE // 3)
                    y = player.rect.centery + offsetsub + randint(- TILESIZE // 4, TILESIZE // 4)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')

                else:
                    offset = (direction.y * i) * TILESIZE//2
                    x = player.rect.centerx + randint(- TILESIZE//4,TILESIZE//4)
                    y = player.rect.centery + offset + randint(- TILESIZE//4,TILESIZE//3)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')

                    offsetsub = offset // 4
                    x = player.rect.centerx - offsetsub + randint(- TILESIZE // 4, TILESIZE // 4)
                    y = player.rect.centery + offset + randint(- TILESIZE // 4, TILESIZE // 3)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')

                    x = player.rect.centerx + offsetsub + randint(- TILESIZE // 4, TILESIZE // 4)
                    y = player.rect.centery + offset + randint(- TILESIZE // 4, TILESIZE // 3)
                    self.animationPlayer.createParticles('flame', (x, y), groups, 'magic')



            self.sounds['flame'].play()


