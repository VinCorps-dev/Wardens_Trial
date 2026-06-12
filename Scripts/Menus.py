import pygame
import pygame_menu
import sys


class MenuManager:
    def __init__(self, game):
        self.game = game

        # --- 1. THEME SETUP ---
        bg_image = pygame_menu.baseimage.BaseImage(
            image_path='Assets/Background For Levels/Background for Title screen/Lamora HR.png',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
        )

        self.my_theme = pygame_menu.themes.THEME_DARK.copy()
        self.my_theme.background_color = bg_image
        self.my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        self.my_theme.widget_font = pygame_menu.font.FONT_8BIT
        self.my_theme.widget_font_size = 20

        # Gawing puti ang mga text button, red ang selection highlight
        self.my_theme.widget_font_color = (255, 255, 255)
        self.my_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        # --- 2. MAIN MENU ---
        self.main_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.my_theme, center_content=False
        )
        self.main_menu.add.vertical_margin(70)
        self.main_menu.add.label("WARDENS TRIAL", font_size=40, font_color=(255, 215, 0),
                                 background_color=(0, 0, 0, 0), padding=(10, 20))
        self.main_menu.add.vertical_margin(80)  # Button margin

        self.main_menu.add.button(
            'START',
            self.start_game,
            padding=(15, 60),
            margin=(0, 10)
        )

        self.main_menu.add.button(
            'OPTIONS',
            self.open_options,
            padding=(15, 52),
            margin=(0, 10)
        )

        self.main_menu.add.button(
            'QUIT',
            self.quit_program,
            padding=(15, 66),
            margin=(0, 10)
        )

        # --- 3. PAUSE MENU ---
        self.pause_theme = self.my_theme.copy()
        self.pause_theme.background_color = (0, 0, 0, 160)  # RGBA (Semi-transparent)
        self.pause_theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

        self.pause_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.pause_theme,
            center_content=False
        )

        # Pause buttons
        self.pause_menu.add.vertical_margin(130)
        self.pause_menu.add.label("PAUSED", font_size=40, font_color=(255, 215, 0))
        self.pause_menu.add.vertical_margin(20)

        self.pause_menu.add.button('RESUME', self.resume_game, padding=(12, 30))
        self.pause_menu.add.vertical_margin(10)
        self.pause_menu.add.button('OPTIONS', self.open_options_from_pause, padding=(12, 33))
        self.pause_menu.add.vertical_margin(10)
        self.pause_menu.add.button('BACK TO TITLE', self.back_to_title, padding=(12, 12))

        # --- 4. OPTIONS MENU SETUP ---
        self.options_theme = self.my_theme.copy()
        self.options_theme.background_color = (20, 20, 20, 240)
        self.options_theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

        self.options_theme.widget_font = pygame_menu.font.FONT_8BIT
        self.options_theme.widget_font_size = 28

        # Kulay puti ang mga text ng sliders, kulay ginto ang 'SETTINGS' title
        self.options_theme.widget_font_color = (255, 255, 255)
        self.options_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        self.options_theme.slider_color = (60, 60, 60)
        self.options_theme.slider_thickness = 12
        self.options_theme.cursor_color = (255, 215, 0)
        self.options_theme.cursor_selection_color = (200, 0, 0)

        self.options_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.options_theme,
            center_content=False
        )

        self.options_menu.add.vertical_margin(50)
        self.options_menu.add.label("SETTINGS", font_size=35, font_color=(255, 215, 0))
        self.options_menu.add.vertical_margin(30)

        # MUSIC SLIDER
        self.options_menu.add.range_slider(
            'MUSIC   ',
            default=30,
            range_values=(0, 100),
            increment=10,
            onchange=lambda x, **kwargs: self.set_music_volume(x / 100),
            slider_width=240,
            cursor_size=(20, 20),
            value_format=lambda x: f"{int(x)}",
            range_values_visibility=False
        )

        # SFX SLIDER
        self.options_menu.add.range_slider(
            'SFX       ',
            default=20,
            range_values=(0, 100),
            increment=10,
            onchange=lambda x, **kwargs: self.set_sfx_volume(x / 100),
            slider_width=240,
            cursor_size=(20, 20),
            value_format=lambda x: f"{int(x)}",
            range_values_visibility=False
        )

        self.options_menu.add.vertical_margin(40)
        self.options_menu.add.button('BACK', self.back_to_main_from_options, padding=(12, 12))
        self.options_menu.disable()

        # --- 5. LEVEL COMPLETE MENU ---
        self.complete_theme = self.my_theme.copy()
        self.complete_theme.background_color = (0, 0, 0, 180)

        self.complete_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.complete_theme,
            center_content=True
        )

        self.complete_menu.add.label("SHARD COLLECTED", font_size=40, font_color=(255, 215, 0))
        self.complete_menu.add.vertical_margin(40)

        self.complete_menu.add.button('LEVEL SELECT', self.back_to_select)
        self.complete_menu.add.button('BACK TO TITLE', self.back_to_title)
        self.complete_menu.disable()

        # --- 🔥 6. CHECKPOINT TEXT NOTIFICATION SETUP ---
        self.checkpoint_timer = 0
        # Gagamitin ang mismong font at kulay na gamit ng menus mo
        self.notification_font = pygame.font.Font(pygame_menu.font.FONT_8BIT, 30)

    # --- FUNCTIONS PARA SA BUTTONS AT ACTIONS ---

    def open_options(self):
        self.game.audio.play_sfx("Assets/Music/SFX/Button sound.mp3")
        self.game.last_state = self.game.state
        self.game.state = "options"
        self.main_menu.disable()
        self.options_menu.enable()

    def open_options_from_pause(self):
        self.game.audio.play_sfx("Assets/Music/SFX/Button sound.mp3")
        self.game.last_state = self.game.state
        self.game.state = "options"
        self.pause_menu.disable()
        self.options_menu.enable()

    def back_to_main_from_options(self):
        self.game.audio.play_sfx("Assets/Music/SFX/Button sound.mp3")
        self.options_menu.disable()

        if hasattr(self.game, 'last_state') and self.game.last_state == "paused":
            self.game.state = "paused"
            self.pause_menu.enable()
        else:
            self.game.state = "main_menu"
            self.main_menu.enable()

    def set_music_volume(self, value, **kwargs):
        self.game.audio.music_volume = value
        pygame.mixer.music.set_volume(value)

    def set_sfx_volume(self, value, **kwargs):
        self.game.audio.sfx_volume = value

    def back_to_select(self):
        self.game.state = "level_select"
        self.complete_menu.disable()
        pygame.mixer.music.pause()

    def start_game(self):
        self.game.audio.play_sfx("Assets/Music/SFX/Button sound.mp3")
        self.game.state = "level_select"
        self.main_menu.disable()

    def resume_game(self):
        self.game.state = "playing"
        pygame.mixer.music.unpause()
        self.pause_menu.disable()

    def back_to_title(self):
        self.game.state = "main_menu"
        pygame.mixer.music.pause()
        self.pause_menu.disable()
        self.complete_menu.disable()
        self.main_menu.enable()

    def quit_program(self):
        self.game.audio.play_sfx("Assets/Music/SFX/Button sound.mp3")
        pygame.quit()
        sys.exit()

    # --- 🔥 MGA BAGONG CHECKPOINT NOTIFICATION FUNCTIONS ---

    def trigger_checkpoint(self):
        """Tatawagin ito kapag nakabangga ng checkpoint."""
        self.checkpoint_timer = 2.0  # Oras kung gaano katagal sa screen (2 seconds)

    def draw_checkpoint_notification(self, surf, dt):
        """Tatawagin ito kada frame para i-draw ang text kung active ang timer."""
        if self.checkpoint_timer > 0:
            self.checkpoint_timer -= dt

            # Render ng text gamit ang kulay ginto/dilaw (255, 215, 0)
            text_surf = self.notification_font.render("CHECKPOINT REACHED", True, (255, 215, 0))

            # I-center ang text sa itaas na bahagi ng screen (y = 80)
            text_rect = text_surf.get_rect(center=(surf.get_width() // 2, 160))
            surf.blit(text_surf, text_rect)