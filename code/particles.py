import pygame
from support import *
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('../assets/github/graphics/particles/flame/frames'),
            'aura': import_folder('../assets/github/graphics/particles/aura'),
            'heal': import_folder('../assets/github/graphics/particles/heal/frames'),

            # attacks
            'claw': import_folder('../assets/github/graphics/particles/claw'),
            'slash': import_folder('../assets/github/graphics/particles/slash'),
            'sparkle': import_folder('../assets/github/graphics/particles/sparkle'),
            'leaf_attack': import_folder('../assets/github/graphics/particles/leaf_attack'),
            'thunder': import_folder('../assets/github/graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('../assets/github/graphics/particles/smoke_orange'),
            'raccoon': import_folder('../assets/github/graphics/particles/raccoon'),
            'specialRaccoon': import_folder('../assets/github/graphics/particles/raccoon'),
            'spirit': import_folder('../assets/github/graphics/particles/nova'),
            'bamboo': import_folder('../assets/github/graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('../assets/github/graphics/particles/leaf1'),
                import_folder('../assets/github/graphics/particles/leaf2'),
                import_folder('../assets/github/graphics/particles/leaf3'),
                import_folder('../assets/github/graphics/particles/leaf4'),
                import_folder('../assets/github/graphics/particles/leaf5'),
                import_folder('../assets/github/graphics/particles/leaf6'),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf1')),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf2')),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf3')),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf4')),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf5')),
                self.flipFrames(import_folder('../assets/github/graphics/particles/leaf6'))
            )
        }

    def flipFrames(self, frames):
        flippedFramesList = []
        for frame in frames:
            flippedFrame = pygame.transform.flip(frame, True, False)
            flippedFramesList.append(flippedFrame)
        return flippedFramesList

    def createGrassParticles(self,position,groups):
        animationFrames = choice(self.frames['leaf'])
        ParticleEffect(position,animationFrames,groups, 'grass')

    def createParticles(self, animationType, position, groups, spriteType):
        animationFrames = self.frames[animationType]
        ParticleEffect(position,animationFrames,groups, spriteType)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position,animationFrame,groups,spriteType):
        super().__init__(groups)
        self.spriteType = spriteType
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.frames = animationFrame
        self.image = self.frames[int(self.frameIndex)]
        self.rect = self.image.get_rect(center=position)



    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()
