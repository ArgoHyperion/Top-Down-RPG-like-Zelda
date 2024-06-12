import pygame
from settings import *
from debugOnScreen import *
class UI:
    def __init__(self):

        #general
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.endingFont = pygame.font.SysFont(UI_FONT, 54)

        #bar setup
        self.HPBarRect = pygame.Rect(94,15,HP_BAR_WIDTH,BAR_HEIGHT)
        self.MPBarRect = pygame.Rect(94,49,MP_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dict
        self.weaponGraphics = []

        #image
        self.avatar = pygame.image.load(avatarPath)
        for weapon in weaponData.values():
            path = weapon['graphic']
            weaponImage = pygame.image.load(path).convert_alpha()
            self.weaponGraphics.append(weaponImage)

        #convert magic dict
        self.magicGraphics = []
        for magic in magicData.values():
            path = magic['graphic']
            magicImage = pygame.image.load(path).convert_alpha()
            self.magicGraphics.append(magicImage)

    def showBar(self,currentAmount,maxAmount,bgRect,color):
        #draw background
        pygame.draw.rect(self.displaySurface,UI_BG_COLOR,bgRect)

        #convert current stat to pixel
        ratio = currentAmount/maxAmount
        currentWidth = bgRect.width * ratio
        currentRect = bgRect.copy()
        currentRect.width = currentWidth
        #font
        textSurface = self.font.render(f'{int(currentAmount)}/{int(maxAmount)}',False,'white')
        textRect = textSurface.get_rect(center = bgRect.center)
        #draw the bar
        pygame.draw.rect(self.displaySurface,color,currentRect)
        pygame.draw.rect(self.displaySurface,UI_BORDER_COLOR,bgRect,3)
        self.displaySurface.blit(textSurface, textRect)

    def showExp(self,SP):
        textSurface = self.font.render(f'SP: {(int(SP))}',False,TEXT_COLOR)
        x = self.displaySurface.get_size()[0]//2-60
        y = self.displaySurface.get_size()[1]   -40
        textRect = textSurface.get_rect(topleft = (x,y))

        pygame.draw.rect(self.displaySurface,UI_BG_COLOR,textRect.inflate(20,20))
        self.displaySurface.blit(textSurface,textRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, textRect.inflate(20, 20),3)



    def showSelectionBox(self,left,top, weaponSwitch=False):
        bgRect = pygame.Rect(left,top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.displaySurface,UI_BG_COLOR,bgRect)
        if weaponSwitch:
            pygame.draw.rect(self.displaySurface,UI_BORDER_COLOR_ACTIVE,bgRect,3)
        else:
            pygame.draw.rect(self.displaySurface,UI_BORDER_COLOR,bgRect,3)
        return bgRect

    def showWeaponBox(self, weaponIndex,weaponSwitch):
        bgRect = self.showSelectionBox(10, 630,weaponSwitch)
        weapon = list(weaponData.keys())[weaponIndex]
        weaponSurface = self.weaponGraphics[weaponIndex]
        weaponRect = weaponSurface.get_rect(center = bgRect.center)

        self.displaySurface.blit(weaponSurface,weaponRect)

    def showMagicBox(self, magicIndex,magicSwitch):
        bgRect = self.showSelectionBox(90, 630,magicSwitch)
        magic = list(magicData.keys())[magicIndex]
        magicSurface = self.magicGraphics[magicIndex]
        magicRect = magicSurface.get_rect(center = bgRect.center)

        self.displaySurface.blit(magicSurface,magicRect)

    def showAvatar(self):
        avatarRect = self.avatar.get_rect(topleft = (10,10))
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, avatarRect)
        self.displaySurface.blit(self.avatar,avatarRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, avatarRect, 3)

    def display(self,player):
        self.showBar(player.HP, player.stats['HP'], self.HPBarRect, HP_COLOR)
        self.showBar(player.MP, player.stats['MP'], self.MPBarRect, MP_COLOR)

        self.showExp(player.skillPoint)
        self.showAvatar()

        self.showWeaponBox(player.weaponIndex, not player.weaponSwitch) #weapon
        self.showMagicBox(player.magicIndex, not player.magicSwitch) #magic

    def ending(self,ending):
        self.displaySurface.fill((0,0,0))
        if ending == True:
            textSurface = self.font.render('YOU HAVE FINISHED THE CLEARING QUEST',False,TEXT_COLOR)
        else:
            textSurface = self.font.render('YOUR NAME HAS BEEN WRITTEN IN THE HALL OF FAILURES', False, TEXT_COLOR)
        displayRect = self.displaySurface.get_rect()
        textRect = textSurface.get_rect(center = displayRect.center)
        self.displaySurface.blit(textSurface,textRect)
