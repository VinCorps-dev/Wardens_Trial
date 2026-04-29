import pygame


class LevelManager:
    def __init__(self, game):
        self.game = game
        # format: level_id: [TMX_PATH, CHARACTER_FOLDER]
        self.levels = {
            1: ["Levels/Map 1.tmx", "Makrothumia"],
            2: ["Levels/Map 1.tmx", "Peitharchia"],
            3: ["Levels/Map 1.tmx", "Atlas"]
        }
        self.current_level = 1
        self.unlocked_levels = [1]

    def is_unlocked(self, level_id):
        return level_id in self.unlocked_levels

    def load_level(self, level_id):
        if level_id in self.levels:
            self.current_level = level_id

            # 1. KUNIN ANG TMX PATH AT CHARACTER FOLDER
            tmx_path, char_folder = self.levels[level_id]

            # 2. LOAD THE TMX FILE
            self.game.Tilemap.load_tmx(tmx_path)

            # 3. DYNAMIC CHARACTER LOADING
            from Scripts.Animation import load_character_animations
            new_assets = load_character_animations('player', f'Character/{char_folder}')
            self.game.assets.update(new_assets)

            # 4. SAFETY CHECK PARA SA PLAYER
            # Chine-check muna natin kung "buhay" na ang player object sa Game class
            if hasattr(self.game, 'player') and self.game.player:
                # Reset player position at action
                self.game.player.set_action('walk')
                self.game.player.pos = [self.game.Tilemap.spawn_point[0], self.game.Tilemap.spawn_point[1] - 32]
                self.game.player.velocity = [0, 0]

                # Reset Camera based sa bagong player position
                self.game.scroll = [self.game.player.pos[0] - 160, self.game.player.pos[1] - 120]

            # 5. STATE CHANGE
            self.game.state = "playing"
            print(f"Level {level_id} Loaded with {char_folder} Successfully!")
        else:
            print(f"Error: Level {level_id} not found.")

    def unlock_next_level(self):
        next_lvl = self.current_level + 1
        if next_lvl in self.levels and next_lvl not in self.unlocked_levels:
            self.unlocked_levels.append(next_lvl)
            print(f"Level {next_lvl} is now UNLOCKED!")