from csv import reader
from os import walk

import pygame


def import_csv_layout(path):

    terrainMap = []
    with open(path) as levelMap:
        layout = reader(levelMap, delimiter=',')
        for row in layout:
            terrainMap.append(list(row))
        return terrainMap

def import_folder(path):
    surfaceList = []

    for filePath, _, imageFile in walk(path):
        for image in imageFile:

            fullPath = path + '/' + image
            # print(fullPath)
            imageSurface = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurface)
    return surfaceList


