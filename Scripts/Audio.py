import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.was_paused = False

        # 🔊 Dito natin ise-store ang volume settings mula sa slider
        self.music_volume = 0.5  # Default 50%
        self.sfx_volume = 0.4  # Default 40%

    def update_music(self, state, level=1):
        expected_track = None
        # Gamitin ang variable sa halip na hardcoded number
        volume = self.music_volume

        if state in ["main_menu", "level_select"]:
            expected_track = "Assets/Music/TItle screen.mp3"
        elif state == "playing":
            if level == 2:
                expected_track = "Assets/Music/Level 2 Music.mp3"
                # Gawing mas mahina ang level 2 music nang konti
                volume = self.music_volume * 0.8
            else:
                expected_track = "Assets/Music/Background Music.mp3"
        elif state == "paused":
            expected_track = self.current_music
            volume = self.music_volume

        # 🎵 SWITCH MUSIC
        if expected_track and expected_track != self.current_music:
            try:
                pygame.mixer.music.fadeout(300)
                pygame.mixer.music.load(expected_track)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.current_music = expected_track
            except Exception as e:
                print("Music load error:", e)

        # ✅ IMPORTANTE: I-update ang volume kahit hindi nagpapalit ng track
        # Para kapag ginalaw ang slider, maririnig agad ang pagbabago.
        if self.current_music:
            pygame.mixer.music.set_volume(volume)

        # ⏸ PAUSE/RESUME LOGIC
        if state == "paused":
            if not self.was_paused:
                pygame.mixer.music.pause()
                self.was_paused = True
        else:
            if self.was_paused:
                pygame.mixer.music.unpause()
                self.was_paused = False

    def play_sfx(self, path, volume=None):
        try:
            # Kung walang binigay na volume sa call, gamitin ang setting mula sa slider
            final_volume = volume if volume is not None else self.sfx_volume
            sfx = pygame.mixer.Sound(path)
            sfx.set_volume(final_volume)
            sfx.play()
        except Exception as e:
            print(f"SFX error: {e}")