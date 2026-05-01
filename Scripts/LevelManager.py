import pygame


class LevelManager:
    def __init__(self, game):
        self.game = game
        self.levels = {
            1: ["Levels/Map 1.tmx", "Makrothumia"],
            2: ["Levels/Map 2.tmx", "Peitharchia"],
            3: ["Levels/Map 1.tmx", "Atlas"]
        }
        self.current_level = 1
        self.unlocked_levels = [1,2]

    def is_unlocked(self, level_id):
        return level_id in self.unlocked_levels

    def load_level(self, level_id):
        if level_id in self.levels:
            self.current_level = level_id
            tmx_path, char_folder = self.levels[level_id]
            self.game.Tilemap.load_tmx(tmx_path)

            keys_to_remove = [k for k in self.game.assets.keys() if k.startswith('player/')]
            for k in keys_to_remove:
                del self.game.assets[k]

            from Scripts.Animation import load_character_animations
            new_assets = load_character_animations('player', f'Character/{char_folder}')
            self.game.assets.update(new_assets)

            if hasattr(self.game, 'player') and self.game.player:
                self.game.player.set_action('walk')
                self.game.player.pos = [self.game.Tilemap.spawn_point[0], self.game.Tilemap.spawn_point[1] - 32]
                self.game.player.velocity = [0, 0]
                self.game.scroll = [self.game.player.pos[0] - 160, self.game.player.pos[1] - 120]

            self.game.state = "playing"
            print(f"Level {level_id} Loaded with {char_folder} Successfully!")
        else:
            print(f"Error: Level {level_id} not found.")

    def unlock_next_level(self):
        next_lvl = self.current_level + 1
        if next_lvl in self.levels and next_lvl not in self.unlocked_levels:
            self.unlocked_levels.append(next_lvl)
            print(f"Level {next_lvl} is now UNLOCKED!")


# ==========================================
# STANDALONE FUNCTION (Wala sa loob ng class)
# ==========================================
def draw_parallax_background(game, surf, render_scroll):
    """Tinatayang nire-render ang iba't ibang parallax layers nang walang class constraint."""
    if game.level_manager.current_level == 2:
        layers = [
            {'name': 'back', 'speed': 0.1},
            {'name': 'far', 'speed': 0.2},
            {'name': 'middle', 'speed': 0.4},
            {'name': 'near', 'speed': 0.6},
            {'name': 'foreground', 'speed': 0.9}
        ]

        for layer in layers:
            img = game.assets.get(layer['name'])
            if img:
                img = pygame.transform.scale(img, (320, 240))
                scroll_x = (render_scroll[0] * layer['speed']) % img.get_width()

                for x in range(-1, 2):
                    surf.blit(img, (int(-scroll_x + x * img.get_width()), 0))
    else:
        # Default black background para sa ibang level
        surf.fill((0, 0, 0))