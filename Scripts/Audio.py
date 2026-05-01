import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.was_paused = False

    def update_music(self, state, level=1):

        # 🎯 Decide what music should play
        if state in ["main_menu", "level_select"]:
            expected_track = "Assets/Music/TItle screen.mp3"
            volume = 0.4

        elif state == "playing":
            if level == 2:
                expected_track = "Assets/Music/Level 2 Music.mp3"
            else:
                expected_track = "Assets/Music/Background Music.mp3"
            volume = 0.4

        elif state == "paused":
            expected_track = self.current_music  # keep same music
            volume = 0.4
        else:
            expected_track = None
            volume = 0.4

        # 🎵 MUSIC SWITCH (ONLY WHEN NEEDED)
        if expected_track and expected_track != self.current_music:

            try:
                pygame.mixer.music.fadeout(300)
                pygame.mixer.music.load(expected_track)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)

                self.current_music = expected_track

            except Exception as e:
                print("Music load error:", e)

        # ⏸ SAFE PAUSE / RESUME (NO SPAM)
        if state == "paused":
            if not self.was_paused:
                pygame.mixer.music.pause()
                self.was_paused = True
        else:
            if self.was_paused:
                pygame.mixer.music.unpause()
                self.was_paused = False

        # 📴 STOP MUSIC CLEANLY (optional safety)
        if state not in ["main_menu", "level_select", "playing", "paused"]:
            pygame.mixer.music.fadeout(500)
            self.current_music = None
            self.was_paused = False

    def play_sfx(self, path, volume=0.5):
        try:
            sfx = pygame.mixer.Sound(path)
            sfx.set_volume(volume)
            sfx.play()
        except Exception as e:
            print(f"SFX error: {e}")