

import pygame
from settings import *

class UpgradeMenu():
    def __init__(self,player):

        #general setup
        self.displaySurface = pygame.display.get_surface()
        self.player = player
        self.attributeNumber = len(self.player.stats)
        self.attributeName = list(self.player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.maxValue = list(self.player.maxStats.values())
        self.upgradeCost = list(self.player.upgradeCost.values())

        #item demenstions
        self.height = (HEIGHT//9)* 7
        self.width =  (WIDTH//9) * 7

        self.itemHeight = (HEIGHT//9)* 7*0.85
        self.itemWidth = ((WIDTH//9) * 7)//6

        #item creation
        self.createItem()

        #selection system
        self.selectionIndex = 0
        self.selectionTime = None
        self.canMove = True

    def input(self):
        keys = pygame.key.get_pressed()
        if self.canMove:
            if keys[pygame.K_RIGHT]:
                self.selectionIndex +=1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT]:
                self.selectionIndex -=1
                self.canMove = False
                self.selectionTime = pygame.time.get_ticks()

            if self.selectionIndex >= self.attributeNumber:
                self.selectionIndex = 0
            elif self.selectionIndex < 0:
                self.selectionIndex = self.attributeNumber - 1


        if keys[pygame.K_SPACE]:
            self.canMove = False
            self.selectionTime = pygame.time.get_ticks()
            self.itemList[self.selectionIndex].trigger(self.player)

    def selectionCooldown(self):
        if not self.canMove:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.selectionTime >= 175:
                self.canMove = True

    def createItem(self):
        self.itemList = []
        for idx in range(self.attributeNumber):
            increment = self.width//self.attributeNumber
            x = (idx * increment) + ((WIDTH//9)) + 19
            y = self.height//7*1.5




            item = Item(x,y,self.itemWidth, self.itemHeight, idx, self.font)
            self.itemList.append(item)


    def display(self):
        self.input()

        for i in self.itemList:
            i.triggerCooldown()
        self.selectionCooldown()


        bgRect = pygame.Rect(WIDTH//9, HEIGHT//9, self.width, self.height)
        bgSurface = pygame.Surface((self.width,self.height))
        pygame.draw.rect(self.displaySurface, 'black', bgRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, bgRect, 3)

        for idx, item in enumerate(self.itemList):

            #get attributes
            name = self.attributeName[idx]
            value = self.player.stats[name]
            maxValue = self.maxValue[idx]
            cost = self.player.upgradeCost[name]


            item.display(self.displaySurface, self.selectionIndex, name,value,maxValue,cost)

class Item:
    def __init__(self,x,y,width,height,index,font):
        self.rect = pygame.Rect(x,y,width,height)
        self.index = index
        self.font = font

        self.canTrigger = True
        self.triggerTime = 0

    def displayName(self,surface,name,cost,selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        #title
        titleSurface = self.font.render(name, False,color)
        titleRect = titleSurface.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        #cost
        costSurface = self.font.render(f'{int(cost)}', False, color)
        costRect = costSurface.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0,20))

        #draw
        surface.blit(titleSurface, titleRect)
        surface.blit(costSurface, costRect)

    def displayBar(self,surface,value,maxValue,selected):

        #setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        #bar setup
        fullHeight = bottom[1] - top[1]
        relativeNumber = (value / maxValue) * fullHeight
        valueRect = pygame.Rect(top[0] - 14,bottom[1] - relativeNumber,30,10)

        #draw
        pygame.draw.line(surface,color,top,bottom,10)
        pygame.draw.rect(surface,color,valueRect)

    def trigger(self,player):
        upgradeAttribute = list(player.stats.keys())[self.index]

        if player.skillPoint >= player.upgradeCost[upgradeAttribute] and player.stats[upgradeAttribute] < player.maxStats[upgradeAttribute] and self.canTrigger:
            player.skillPoint -= player.upgradeCost[upgradeAttribute]
            player.stats[upgradeAttribute] += player.upgradeAmount[upgradeAttribute]
            player.upgradeCost[upgradeAttribute] += 1
            self.triggerTime = pygame.time.get_ticks()
            self.canTrigger = False

        if player.stats[upgradeAttribute] > player.maxStats[upgradeAttribute]:
            player.stats[upgradeAttribute] = player.maxStats[upgradeAttribute]

    def triggerCooldown(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.triggerTime >=100:
            self.canTrigger = True


    def display(self, surface, selectionNum, name, value, maxValue, cost):

        if self.index == selectionNum:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR_ACTIVE,self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect, 4)
        # pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        self.displayName(surface, name,cost,self.index == selectionNum)
        self.displayBar(surface,value,maxValue,self.index == selectionNum)
