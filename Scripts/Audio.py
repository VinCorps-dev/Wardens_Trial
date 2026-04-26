import pygame

class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

    def play_music(self, path, volume=0.5):
        if self.current_music == path:
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # loop forever
        self.current_music = path

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, path, volume=0.5):
        # Ang Sound object ay para sa maiikling effects (wav/ogg)
        sfx = pygame.mixer.Sound(path)
        sfx.set_volume(volume)
        sfx.play()