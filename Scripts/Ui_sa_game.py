import pygame
import pygame_gui
import pygame_menu


class UserInterface:
    def __init__(self, game):
        self.game = game
        self.manager = pygame_gui.UIManager(self.game.screen.get_size())

        self.font = pygame.font.Font(pygame_menu.font.FONT_8BIT, 16)
        self.small_font = pygame.font.Font(pygame_menu.font.FONT_8BIT, 16)

        self.timer = 0.0

        # Pause Button
        raw_icon = pygame.image.load(
            'Assets/Menu Buttons/Square Buttons/Square Buttons/Pause Square Button.png').convert_alpha()
        self.pause_icon = pygame.transform.scale(raw_icon, (40, 40))
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-60, 10), (50, 50)),
            text='',
            manager=self.manager,
            anchors={'right': 'right', 'top': 'top'}
        )

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                self.game.state = "time_up"
                self.game.menu_manager.time_up_menu.enable()
        self.manager.update(dt)

    def draw_timer(self, surf, time_val, x, y, label="TIME"):
        """Helper method na Puti (White) ang kulay para sa Timer"""
        minutes = int(time_val) // 60
        seconds = int(time_val) % 60

        # 1. Render Label (White)
        label_text = self.font.render(label, True, (255, 255, 255))
        surf.blit(label_text, (x, y))

        # 2. Unang Colon (White)
        c1_x = x + label_text.get_width()
        pygame.draw.rect(surf, (255, 255, 255), (c1_x, y + 4, 3, 3))
        pygame.draw.rect(surf, (255, 255, 255), (c1_x, y + 10, 3, 3))

        # 3. Minutes (White)
        min_text = self.font.render(f"{minutes:02d}", True, (255, 255, 255))
        surf.blit(min_text, (c1_x + 10, y))

        # 4. Pangalawang Colon (White)
        c2_x = c1_x + 10 + min_text.get_width()
        pygame.draw.rect(surf, (255, 255, 255), (c2_x, y + 4, 3, 3))
        pygame.draw.rect(surf, (255, 255, 255), (c2_x, y + 10, 3, 3))

        # 5. Seconds (White)
        sec_text = self.font.render(f"{seconds:02d}", True, (255, 255, 255))
        surf.blit(sec_text, (c2_x + 10, y))

    def draw(self, surf):
        # 1. DRAW PROGRESS BAR
        start_x = self.game.Tilemap.spawn_point[0]
        end_x = self.game.Tilemap.goal_pos[0]
        total_dist = end_x - start_x
        current_travelled = self.game.player.pos[0] - start_x
        progress = max(0, min(current_travelled / total_dist, 1.0)) if total_dist > 0 else 0

        pygame.draw.rect(surf, (255, 255, 255), (10, 10, 202, 22), 2)
        pygame.draw.rect(surf, (255, 215, 0), (12, 12, int(198 * progress), 18))

        # 2. DRAW 8-BIT TEXTS
        progress_text = self.small_font.render("LEVEL PROGRESS", True, (255, 255, 255))
        surf.blit(progress_text, (10, 35))

        # 3. DRAW MAIN TIMER
        if self.timer > 0:
            self.draw_timer(surf, self.timer, 10, 60, "TIME")

        # 4. DRAW UI MANAGER
        self.manager.draw_ui(surf)
        button_rect = self.pause_button.get_abs_rect()
        surf.blit(self.pause_icon, (button_rect.x + 5, button_rect.y + 5))

    def process_events(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.pause_button:
            return "pause_clicked"
        return None