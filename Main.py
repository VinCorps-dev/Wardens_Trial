import math
import pygame
import sys

from Scripts.Menus import MenuManager
from Scripts.Entities import PhysicsEntity
from Scripts.Utilities import load_image, load_images, load_spritesheet
from Scripts.Tilemap import Tilemap
from Scripts.Audio import Audio
from Scripts.Ui_sa_game import UserInterface
from Scripts.Animation import Animation, load_character_animations
from Scripts.LevelManager import LevelManager
from Scripts.LevelSelector import LevelSelector


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Warden's Trial")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        self.audio = Audio()
        self.movement = [False, False]
        self.scroll = [0, 0]

        # 1. LOAD ASSETS
        self.assets = {
            'tiles': load_spritesheet('Tilesets/Dungeon Tile Set.png', 16),
            'goal': load_image('gems/atlas_gem.png'),
            'back_btn': load_image('Menu Buttons/Large Buttons/Large Buttons/Back Button.png'),
            'level_BG': load_image('Background For Levels/Background for Level Select/BG for level Select.png'),
            'Panel_BG': load_image('Background For Levels/Background for Level Select/Bg for Panels.png'),
            'btn_lvl1': load_image('Menu Buttons/Level buttons/Level 1.png'),
            'btn_lvl2': load_image('Menu Buttons/Level buttons/Level 2.png'),
            'btn_lvl3': load_image('Menu Buttons/Level buttons/Level 3.png'),
            'btn_lvl4': load_image('Menu Buttons/Level buttons/Level 4.png'),
            'btn_locked': load_image('Menu Buttons/Level buttons/Locked.png'),
            'gem1': load_image('gems/atlas_gem.png'),
            'gem2': load_image('gems/makrothumia_gem.png'),
            'gem3': load_image('gems/peitharchia_gem.png'),
            'gem4': load_image('gems/makrothumia_gem.png'),
        }

        # 2. INITIALIZE MANAGERS
        self.Tilemap = Tilemap(self, tile_size=16)
        self.level_manager = LevelManager(self)
        self.level_selector = LevelSelector(self)
        self.menu_manager = MenuManager(self)
        self.ui = UserInterface(self)

        # 3. INITIAL SETUP
        self.level_manager.load_level(1)
        spawn_pos = (self.Tilemap.spawn_point[0], self.Tilemap.spawn_point[1] - 32)
        self.player = PhysicsEntity(self, 'player', spawn_pos, (16, 32))

        # 🚀 4. STARTING STATE
        self.state = "main_menu"
        self.menu_manager.main_menu.enable()

    def start_level(self, level_id):
        self.movement = [False, False]
        self.level_manager.load_level(level_id)
        self.player.pos = [self.Tilemap.spawn_point[0], self.Tilemap.spawn_point[1] - 32]
        self.player.velocity = [0, 0]
        self.state = "playing"

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()

            # Update Music based on state
            self.audio.update_music(self.state)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # --- GLOBAL BUTTON SFX ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state in ["main_menu", "paused", "level_complete", "level_select"]:
                        self.audio.play_sfx("Assets/Music/SFX/Button sound.mp3", 0.4)

                # --- PLAYING INPUTS ---
                if self.state == "playing":
                    ui_action = self.ui.process_events(event)
                    if ui_action == "pause_clicked":
                        self.audio.play_sfx("Assets/Music/SFX/Button sound.mp3", 0.4)
                        self.state = "paused"
                        self.menu_manager.pause_menu.enable()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT: self.movement[0] = True
                        if event.key == pygame.K_RIGHT: self.movement[1] = True
                        if event.key == pygame.K_UP:
                            if self.player.jumps < self.player.max_jumps:
                                self.player.velocity[1] = -3
                                self.player.jumps += 1
                                self.audio.play_sfx("Assets/Music/SFX/Jump.wav", 0.3)
                        if event.key == pygame.K_DOWN: self.player.drop_through = True
                        if event.key == pygame.K_ESCAPE:
                            self.audio.play_sfx("Assets/Music/SFX/Button sound.mp3", 0.4)
                            self.state = "paused"
                            self.menu_manager.pause_menu.enable()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT: self.movement[0] = False
                        if event.key == pygame.K_RIGHT: self.movement[1] = False
                        if event.key == pygame.K_DOWN: self.player.drop_through = False

            # --- RENDER MACHINE ---

            if self.state == "main_menu":
                self.screen.fill((0, 0, 0))
                if self.menu_manager.main_menu.is_enabled():
                    self.menu_manager.main_menu.update(events)
                    if self.menu_manager.main_menu.is_enabled():
                        self.menu_manager.main_menu.draw(self.screen)
                else:
                    self.menu_manager.main_menu.enable()

            elif self.state == "level_select":
                self.level_selector.update(events)

            elif self.state == "playing":
                # Camera logic
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

                map_w = self.Tilemap.tmx_data.width * self.Tilemap.tile_size
                map_h = self.Tilemap.tmx_data.height * self.Tilemap.tile_size
                render_scroll = (int(max(0, min(self.scroll[0], map_w - 320))),
                                 int(max(0, min(self.scroll[1], map_h - 240))))

                self.player.update(self.Tilemap, (self.movement[1] - self.movement[0], 0), (map_w, map_h))

                self.display.fill((0, 0, 0))
                self.Tilemap.render(self.display, offset=render_scroll)

                gem_img = self.assets.get(f'gem{self.level_manager.current_level}', self.assets['goal'])
                self.display.blit(gem_img, (self.Tilemap.goal_pos[0] - render_scroll[0],
                                            self.Tilemap.goal_pos[1] - render_scroll[1] - 32))
                self.player.render(self.display, offset=render_scroll)

                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.ui.update(dt)
                self.ui.draw(self.screen)

            elif self.state == "paused":
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.ui.draw(self.screen)
                if self.menu_manager.pause_menu.is_enabled():
                    self.menu_manager.pause_menu.update(events)
                    if self.menu_manager.pause_menu.is_enabled():
                        self.menu_manager.pause_menu.draw(self.screen)
                else:
                    self.menu_manager.pause_menu.enable()

            elif self.state == "level_complete":
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                if self.menu_manager.complete_menu.is_enabled():
                    self.menu_manager.complete_menu.update(events)
                    if self.menu_manager.complete_menu.is_enabled():
                        self.menu_manager.complete_menu.draw(self.screen)
                else:
                    self.menu_manager.complete_menu.enable()

            pygame.display.update()


if __name__ == "__main__":
    Game().run()