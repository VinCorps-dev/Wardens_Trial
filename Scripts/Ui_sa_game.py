import pygame
import pygame_gui


class UserInterface:
    def __init__(self, game):
        self.game = game
        self.manager = pygame_gui.UIManager(self.game.screen.get_size())

        # 1. Container para sa Progress Bar (Top-Left)
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

        # 2. PAUSE BUTTON (Top-Right)
        # Gagamit tayo ng anchor para laging nasa gilid kahit mag-resize ang window
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-60, 10), (50, 50)),  # -60 means 60 pixels mula sa kanan
            text='||',
            manager=self.manager,
            anchors={'right': 'right', 'top': 'top'}  # I-anchor sa top-right
        )

    def update(self, dt):
        # Progress logic mo (Working na ito base sa code mo)
        start_x = self.game.Tilemap.spawn_point[0]
        end_x = self.game.Tilemap.goal_pos[0]
        total_dist = end_x - start_x
        current_travelled = self.game.player.pos[0] - start_x

        if total_dist > 0:
            progress = max(0, min(current_travelled / total_dist, 1.0))
        else:
            progress = 0

        self.progress_bar.percent_full = progress

        # Mahalaga: I-update ang manager
        self.manager.update(dt)

    def draw(self, surf):
        self.manager.draw_ui(surf)

    # 3. Method para i-handle ang events ng UI
    def process_events(self, event):
        self.manager.process_events(event)

        # Check kung na-click ang pause button
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.pause_button:
                return "pause_clicked"  # I-return ito sa main loop
        return None