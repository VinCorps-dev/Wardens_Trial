import os

import pygame

BASE_IMG_PATH = 'Assets/'

def load_image(path):
    # Gamitin ang .convert_alpha() para basahin ang transparency ng PNG
    image = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return image

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


def load_spritesheet(filename, tile_size, spacing=0, margin=0):
    """
    Naglo-load ng tileset image at pinuputol ito sa tiles na may margin at spacing.
    """
    from Scripts.Utilities import load_image  # Kung saan naka-define ang base path

    # Siguraduhing tugma ang path mo (hal. 'Assets/' + filename)
    image_path = os.path.join('Assets', filename)
    try:
        sheet = pygame.image.load(image_path).convert_alpha()
    except FileNotFoundError:
        # Fallback kung nasa ibang path ang assets
        sheet = pygame.image.load(filename).convert_alpha()

    sheet_width, sheet_height = sheet.get_size()
    sprites = []

    for y in range(margin, sheet_height, tile_size + spacing):
        for x in range(margin, sheet_width, tile_size + spacing):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            # Gumawa ng surface para sa bawat tile
            sprite = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), rect)
            sprites.append(sprite)

    return sprites


