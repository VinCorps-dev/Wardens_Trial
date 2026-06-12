import pygame


class LevelSelector:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 24)
        self.level_titles = [
            "Trial of Patience",
            "Trial of Discipline",
            "Trial of Endurance",
            "Warden's Room"
        ]

        # Eksaktong sukat at pwesto ng panels
        self.panels = [
            pygame.Rect(10, 100, 140, 300),
            pygame.Rect(170, 100, 140, 300),
            pygame.Rect(330, 100, 140, 300),
            pygame.Rect(490, 100, 140, 300),
        ]
        self.levels = [1, 2, 3, 4]

    def update(self, events):
        # 1. DRAW BACKGROUND (Buong screen)
        bg_img = self.game.assets['level_BG']
        scaled_bg = pygame.transform.scale(bg_img, (640, 480))
        self.game.screen.blit(scaled_bg, (0, 0))

        # 2. DRAW BACK BUTTON (Top Left)
        back_img = self.game.assets['back_btn']
        back_img_small = pygame.transform.scale(back_img, (100, 40))
        back_rect = back_img_small.get_rect(topleft=(10, 10))
        self.game.screen.blit(back_img_small, back_rect)

        clickable = []

        # --- MGA ADJUSTMENT (Dito mo i-adjust ang taas/baba) ---
        text_y_offset = 30  # Distansya mula sa tuktok ng panel (Text)
        portrait_y_offset = 85  # Distansya mula sa tuktok ng panel (Pic)
        button_y_offset = 230  # Distansya mula sa tuktok ng panel (Button)

        for i, panel in enumerate(self.panels):
            lvl = self.levels[i]
            unlocked = self.game.level_manager.is_unlocked(lvl)

            # A. DRAW PANEL (Ang stone texture)
            panel_tex = self.game.assets['Panel_BG']
            scaled_panel = pygame.transform.scale(panel_tex, (panel.width, panel.height))
            self.game.screen.blit(scaled_panel, (panel.x, panel.y))

            # B. DRAW TEXT (Level Name)
            title = self.level_titles[i]
            text_surf = self.font.render(title, True, (255, 255, 255))
            tx = panel.centerx - (text_surf.get_width() // 2)
            ty = panel.y + text_y_offset

            # Text background (Para mas madaling basahin)
            bg_rect = pygame.Rect(tx - 5, ty - 2, text_surf.get_width() + 10, text_surf.get_height() + 4)
            pygame.draw.rect(self.game.screen, (20, 30, 60), bg_rect, border_radius=3)
            self.game.screen.blit(text_surf, (tx, ty))

            # C. DRAW CHARACTER PIC (Static frame lang)
            # Kukunin nito yung 'char1', 'char2', etc. sa assets mo
            gem_key = f'gem{lvl}'
            gem_img_raw = self.game.assets[gem_key]

            gem_w, gem_h = 80, 80
            px = panel.centerx - (gem_w // 2)
            py = panel.y + portrait_y_offset + 15

            # DITO KA MAG-INGAT: Siguraduhin na 'gem_img' ang pangalan nito
            gem_img = pygame.transform.scale(gem_img_raw, (gem_w, gem_h))

            # At 'gem_img' din dapat ang nandito sa blit:
            self.game.screen.blit(gem_img, (px, py))

            # D. DRAW BUTTON
            btn_w, btn_h = 100, 40
            bx = panel.centerx - (btn_w // 2)
            by = panel.y + button_y_offset
            btn_rect = pygame.Rect(bx, by, btn_w, btn_h)

            if unlocked:
                btn_img_raw = self.game.assets[f'btn_lvl{lvl}']
            else:
                btn_img_raw = self.game.assets['btn_locked']

            btn_img = pygame.transform.scale(btn_img_raw, (btn_w, btn_h))
            self.game.screen.blit(btn_img, (bx, by))

            # Listahan para sa click detection
            clickable.append((btn_rect, lvl))

        # 3. MOUSE EVENTS
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    self.game.state = "main_menu"
                for rect, lvl in clickable:
                    if rect.collidepoint(event.pos):
                        if self.game.level_manager.is_unlocked(lvl):
                            self.game.start_level(lvl)