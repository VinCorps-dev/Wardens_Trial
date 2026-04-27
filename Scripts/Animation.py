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
        if self.loop:
            # Cycle through frames: 17 frames * duration per frame
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        # Calculate which image index to show right now
        return self.images[int(self.frame / self.img_duration)]

def load_character_animations(e_type, base_path):
    animations = {}
    actions = ['run']

    for action in actions:
        full_path = base_path + '/' + action
        if os.path.exists(BASE_IMG_PATH + full_path):
            dict_key = e_type + '/' + action
                # Make sure this says 'Animation' with a capital A
            animations[dict_key] = Animation(load_images(full_path), img_dur=3)

    return animations