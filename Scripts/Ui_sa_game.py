import pygame
import pygame_gui

class UserInterface:
    def __init__(self, game):
        self.game = game
        self.manager = pygame_gui.UIManager(self.game.screen.get_size())

        # 1. LOAD AND SCALE THE ICON
        # Nilagay natin sa 'self' para ma-access sa draw method mamaya
        raw_icon = pygame.image.load(
            'Assets/Menu Buttons/Square Buttons/Square Buttons/Pause Square Button.png').convert_alpha()
        self.pause_icon = pygame.transform.scale(raw_icon, (40, 40))

        # 2. CONTAINER PARA SA PROGRESS BAR (Top-Left)
        self.container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 10), (220, 60)),
            manager=self.manager,
            starting_height=1
        )

        self.progress_bar = pygame_gui.elements.UIStatusBar(
            relative_rect=pygame.Rect((10, 10), (200, 20)),
            manager=self.manager,
            container=self.container
        )

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 30), (200, 20)),
            text="Level Progress",
            manager=self.manager,
            container=self.container
        )

        # 3. PAUSE BUTTON (Top-Right)
        # Gagamit tayo ng UIButton para gumana pa rin ang UI_BUTTON_PRESSED event
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-60, 10), (50, 50)),
            text='',
            manager=self.manager,
            anchors={'right': 'right', 'top': 'top'}
        )

    def update(self, dt):
        # Progress logic (Working base sa code mo)
        start_x = self.game.Tilemap.spawn_point[0]
        end_x = self.game.Tilemap.goal_pos[0]
        total_dist = end_x - start_x
        current_travelled = self.game.player.pos[0] - start_x

        if total_dist > 0:
            progress = max(0, min(current_travelled / total_dist, 1.0))
        else:
            progress = 0

        self.progress_bar.percent_full = progress

        # Update ang manager
        self.manager.update(dt)

    def draw(self, surf):
        # I-draw muna ang lahat ng UI elements ng manager
        self.manager.draw_ui(surf)

        # 4. MANUAL BLIT NG ICON (THE HOVER FIX)
        # Kunin ang pwesto ng button at i-center ang icon sa loob nito (5px margin)
        button_rect = self.pause_button.get_abs_rect()
        icon_pos = (button_rect.x + 5, button_rect.y + 5)
        surf.blit(self.pause_icon, icon_pos)

    def process_events(self, event):
        self.manager.process_events(event)

        # Check kung na-click ang pause button
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.pause_button:
                return "pause_clicked"
        return None