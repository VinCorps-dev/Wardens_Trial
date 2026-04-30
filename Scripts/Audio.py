import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None

    def update_music(self, state):
        """Centralized logic para sa music na may smooth transitions."""
        # 1. Tukuyin ang dapat na kanta
        if state in ["main_menu", "level_select"]:
            expected_track = "Assets/Music/TItle screen.mp3"
            volume = 0.4
        elif state in ["playing", "paused"]:
            expected_track = "Assets/Music/Background Music.mp3"
            volume = 0.4
        else:
            expected_track = None

        # 2. Logic para sa Fade Out at Pagpapalit
        if expected_track:
            if self.current_music != expected_track:
                # Kung may tumutugtog na ibang kanta, i-fade out muna (500ms = 0.5 seconds)
                if self.current_music is not None:
                    pygame.mixer.music.fadeout(500)
                    # Konting delay para matapos ang fade bago mag-load ng bago
                    # Note: Sa simple games, okay na ang diretso load pagkatapos ng command

                pygame.mixer.music.load(expected_track)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.current_music = expected_track

            # 3. Handling para sa Pause/Unpause (Instant ito, walang fade)
            if state == "paused":
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        else:
            # Pag walang kanta (eg. level complete), i-fade out din para swabe
            if self.current_music is not None:
                pygame.mixer.music.fadeout(1000)  # 1 second fade out
                self.current_music = None

    def play_sfx(self, path, volume=0.5):
        try:
            sfx = pygame.mixer.Sound(path)
            sfx.set_volume(volume)
            sfx.play()
        except Exception as e:
            print(f"SFX error: {e}")