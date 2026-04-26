import pygame_gui
import pygame

class UserInterface:
    def __init__(self, game):
        self.game = game

        self.manager = pygame_gui.UIManager(self.game.screen.get_size())

        self.container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 10), (220, 60)),
            manager=self.manager,
            starting_height=1)

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

    def update(self, dt):
        # 1. Get the start and end points
        start_x = self.game.Tilemap.spawn_point[0]
        end_x = self.game.Tilemap.goal_pos[0]

        # 2. Total distance the player needs to travel
        total_dist = end_x - start_x

        # 3. How far the player has traveled from the start
        current_travelled = self.game.player.pos[0] - start_x

        # 4. Calculate progress
        if total_dist > 0:
            progress = max(0, min(current_travelled / total_dist, 1.0))
        else:
            progress = 0

        # 🔥 ITO ANG KULANG:
        self.progress_bar.percent_full = progress # I-set ang laman ng bar
        self.manager.update(dt) # I-update ang UI graphics

    def draw(self, surf):
            self.manager.draw_ui(surf)



