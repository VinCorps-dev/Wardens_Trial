import pygame
import os
import pygame
from Scripts.Utilities import load_images, BASE_IMG_PATH


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        self.frame += 1
            # Full cycle calculation para sa 16 frames
        full_cycle = self.img_duration * len(self.images)

        if self.loop:
                # Ito ang saktong modulo para hindi mag-skip ng frames
                self.frame %= full_cycle
        else:
            if self.frame >= full_cycle - 1:
                 self.frame = full_cycle - 1
                 self.done = True

    def img(self):
            # Siguraduhin na integer ang index at hindi lalampas sa list size
        img_index = int(self.frame / self.img_duration)
        return self.images[img_index % len(self.images)]

def load_character_animations(e_type, base_path):
    animations = {}
    actions = ['walk', 'jump', 'drop']
    for action in actions:
        full_path = base_path + '/' + action
        if os.path.exists(BASE_IMG_PATH + full_path):
            dict_key = e_type + '/' + action
                # 16 frames need a faster duration (3 or 4) to look smooth at 60fps
            dur = 4 if action == 'walk' else 8
            animations[dict_key] = Animation(load_images(full_path), img_dur=dur)
    return animations