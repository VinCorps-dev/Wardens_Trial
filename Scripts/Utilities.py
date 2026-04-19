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
