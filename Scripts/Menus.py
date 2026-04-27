import pygame
import pygame_menu


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

        # --- 2. MAIN MENU ---
        self.main_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.my_theme, center_content=False
        )
        self.main_menu.add.vertical_margin(70)
        self.main_menu.add.label("WARDENS TRIAL", font_size=35, font_color=(255, 215, 0),
                                 background_color=(0, 0, 0, 130), padding=(10, 20))
        self.main_menu.add.vertical_margin(80)#Button margin
        self.main_menu.add.button('START GAME', self.start_game)
        self.main_menu.add.button('QUIT', pygame_menu.events.EXIT)

        # --- 3. PAUSE MENU ---
        # Gumamit tayo ng semi-transparent black para makita pa rin yung laro sa likod
        self.pause_theme = self.my_theme.copy()
        self.pause_theme.background_color = (0, 0, 0, 160)  # RGBA (160 = Semi-transparent)

        self.pause_menu = pygame_menu.Menu(
            title="", width=640, height=480,
            theme=self.pause_theme, center_content=True  # Center ito para maganda
        )

        self.pause_menu.add.label("PAUSED", font_size=40, font_color=(255, 215, 0))
        self.pause_menu.add.vertical_margin(20)
        self.pause_menu.add.button('RESUME', self.resume_game)
        self.pause_menu.add.button('BACK TO TITLE', self.back_to_title)
        self.pause_menu.disable()  # Off muna sa simula

        self.main_menu.enable()  # Siguraduhin na laging ON ito sa start
        self.pause_menu.disable()  # Ito lang ang OFF sa start

    # --- FUNCTIONS PARA SA BUTTONS ---

    def start_game(self):
        self.game.state = "playing"
        self.main_menu.disable()
        pygame.mixer.music.unpause()

    def resume_game(self):
        self.game.state = "playing"
        # ✅ Ituloy ang musika
        pygame.mixer.music.unpause()
        self.pause_menu.disable()

    def back_to_title(self):
        self.game.state = "main_menu"
        # ✅ Patayin nang tuluyan ang musika
        pygame.mixer.music.pause()
        self.pause_menu.disable()
        self.main_menu.enable()