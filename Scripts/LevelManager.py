import pygame
from Scripts.Entities import Makrothumia, Peitharchia, Atlas, Agnosia


class LevelManager:
    def __init__(self, game):
        self.game = game

        # CONFIGURATION: [File Path, Character Class, Has Parallax Background?]
        self.levels = {
            1: ["Levels/Map 1.tmx", "Makrothumia", False],
            2: ["Levels/Map 2.tmx", "Peitharchia", True],
            3: ["Levels/Map 3.tmx", "Atlas", True],  # Naka-True para sa mga bagong pic mo!
            4: ["Levels/Map 4.tmx", "Agnosia", False]
        }
        self.current_level = 1
        self.unlocked_levels = [1, 2, 3, 4]
        self.has_parallax = False  # Tagatanda kung may parallax ang map

    def is_unlocked(self, level_id):
        return level_id in self.unlocked_levels

    def load_level(self, level_id):
        if level_id in self.levels:
            self.current_level = level_id
            # TIMER SETTINGS
            if level_id == 3:
                self.game.ui.timer = 300
            elif level_id == 4:
                self.game.ui.timer = 300
            else:
                self.game.ui.timer = 0.0

            # Sinalo ang has_parallax setup mula sa self.levels config
            tmx_path, char_folder, self.has_parallax = self.levels[level_id]
            self.game.Tilemap.load_tmx(tmx_path)

            # Clear at dynamic update ng animation references
            keys_to_remove = [k for k in self.game.assets.keys() if k.startswith('player/')]
            for k in keys_to_remove:
                del self.game.assets[k]

            from Scripts.Animation import load_character_animations
            new_assets = load_character_animations('player', f'Character/{char_folder}')
            self.game.assets.update(new_assets)

            # Class Map Connector
            char_map = {
                "Makrothumia": Makrothumia,
                "Peitharchia": Peitharchia,
                "Atlas": Atlas,
                "Agnosia": Agnosia,
            }
            CharClass = char_map.get(char_folder, Makrothumia)

            # Dynamic Spawning at Coordinate Retrieval
            sp_x = int(float(self.game.Tilemap.spawn_point[0]))
            sp_y = int(float(self.game.Tilemap.spawn_point[1]))

            # Gagawa ng player gamit ang saktong class at coordinates
            self.game.player = CharClass(self.game, 'player', (sp_x, sp_y - 32), (16, 32))

            # CHECKPOINT RESET: Bagong posisyon ng checkpoint para sa bagong mapa
            if hasattr(self.game.Tilemap, 'checkpoint_pos'):
                self.game.Tilemap.checkpoint_pos = [sp_x, sp_y - 32]

            # Snap-lock ng camera frame sa simula ng level para walang itim na screen area
            self.game.scroll = [self.game.player.pos[0] - 160, self.game.player.pos[1] - 120]
            self.game.state = "playing"
            print(f"Level {level_id} Loaded with {char_folder} at Spawn Point ({sp_x}, {sp_y})")

    def unlock_next_level(self):
        next_lvl = self.current_level + 1
        if next_lvl in self.levels and next_lvl not in self.unlocked_levels:
            self.unlocked_levels.append(next_lvl)
            print(f"Level {next_lvl} is now UNLOCKED!")


# PINAGANDANG UTILITY FUNCTION PARA SA MAIN.PY
def draw_parallax_background(game, surf, render_scroll):
    if game.level_manager.has_parallax:
        current_lvl = game.level_manager.current_level
        layers = []

        # Kung Level 2 (Gagamit ng 5 layers)
        if current_lvl == 2:
            layers = [
                {'name': 'back', 'speed': 0.1},
                {'name': 'far', 'speed': 0.3},
                {'name': 'middle', 'speed': 0.5},
                {'name': 'near', 'speed': 0.7},
                {'name': 'foreground', 'speed': 0.9}
            ]

        # Kung Level 3 (3 layers na galing sa mga bago mong in-upload)
        elif current_lvl == 3:
            layers = [
                {'name': 'lvl3_night', 'speed': 0.05},  # Night.png
                {'name': 'lvl3_far forest', 'speed': 0.2},  # Far Forest.png
                {'name': 'lvl3_Dark Tree', 'speed': 0.6}  # Dark Tree.png
            ]

        # Render Loop para sa lahat ng napiling layers
        for layer in layers:
            img = game.assets.get(layer['name'])
            if img:
                img = pygame.transform.scale(img, (320, 240))
                scroll_x = (render_scroll[0] * layer['speed']) % img.get_width()
                for x in range(-1, 2):
                    surf.blit(img, (int(-scroll_x + x * img.get_width()), 0))
    else:
        # Default solid background kapag naka-False ang level
        surf.fill((0, 0, 0))