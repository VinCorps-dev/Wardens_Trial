import pygame

class Animation:
    def __init__(self, images, img_dur=6, loop=True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop

        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % (len(self.images) * self.img_dur)

    def image(self):
        return self.images[int(self.frame / self.img_dur)]

    def reset(self):
        self.frame = 0