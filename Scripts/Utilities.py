import os

import pygame

BASE_IMG_PATH = 'Assets/'

def load_image(path):
    image = pygame.image.load(BASE_IMG_PATH + path).convert()
    image.set_colorkey((0, 0, 0))
    return image

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

def load_spritesheet(path, tile_size):
    sheet = pygame.image.load(BASE_IMG_PATH + path).convert()
    sheet.set_colorkey((0, 0, 0))

    images = []
    sheet_width, sheet_height = sheet.get_size()

    for y in range(0, sheet_height, tile_size):
        for x in range(0, sheet_width, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            image = sheet.subsurface(rect)
            images.append(image)

    return images