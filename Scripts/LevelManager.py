import pygame


class LevelManager:
    def __init__(self, game):
        self.game = game
        # This list maps level numbers to actual file paths
        self.levels = {
            1: "Levels/Map 1.tmx",
            2: "Levels/Map 1.tmx",
            3: "Levels/Map 1.tmx",
            4: "Levels/Map 1.tmx",
        }
        self.current_level = 1

        # ✅ FIX: You MUST define this list here!
        # Without this, is_unlocked will keep crashing.
        self.unlocked_levels = [1]

    def is_unlocked(self, level_id):
        """Returns True if the level is in the unlocked list."""
        # Now this will work because 'self.unlocked_levels' is defined in __init__
        return level_id in self.unlocked_levels

    def load_level(self, level_id):
        if level_id in self.levels:
            self.current_level = level_id
            path = self.levels[level_id]

            # 1. Tell the Tilemap to load the new file
            self.game.Tilemap.load_tmx(path)

            # 2. Reset Player Position
            self.game.player.pos = [self.game.Tilemap.spawn_point[0], self.game.Tilemap.spawn_point[1] - 32]
            self.game.player.velocity = [0, 0]

            # 3. Reset Camera
            self.game.scroll = [self.game.player.pos[0], self.game.player.pos[1]]

            # 4. Change State to Playing
            self.game.state = "playing"
            print(f"Level {level_id} Loaded Successfully!")
        else:
            print(f"Error: Level {level_id} not found in LevelManager.")

            # Idagdag ito sa pinakababa ng LevelManager class:
    def unlock_next_level(self):
                # Alamin kung ano ang susunod na level base sa current_level
        next_lvl = self.current_level + 1

                # I-check kung may ganoong level sa dictionary at kung hindi pa ito unlocked
        if next_lvl in self.levels and next_lvl not in self.unlocked_levels:
            self.unlocked_levels.append(next_lvl)
            print(f"Level {next_lvl} is now UNLOCKED!")