import math
import pygame
import sys

from Scripts.Menus import MenuManager
from Scripts.Entities import PhysicsEntity
from Scripts.Utilities import load_image, load_images
from Scripts.Tilemap import Tilemap
from Scripts.Utilities import load_spritesheet
from Scripts.Audio import Audio
from Scripts.Ui_sa_game import UserInterface
from Scripts.Animation import Animation, load_character_animations

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Warden's Trial")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.ui = UserInterface(self)

        # Sa Game.__init__
        self.menu_manager = MenuManager(self)
        self.state = "main_menu"

        self.clock = pygame.time.Clock()

        self.movement = [False,False]

        self.assets ={
            'tiles': load_spritesheet('Tilesets/Dungeon Tile Set.png', 16),
            'goal': load_image('gems/atlas_gem.png'),
        }

        self.assets.update(load_character_animations('player', 'Character/Makrothumia'))

        self.Tilemap = Tilemap(self, tile_size= 16)

        # ✅ THEN GET SPAWN
        spawn = (self.Tilemap.spawn_point[0], self.Tilemap.spawn_point[1] - 32)  # Offset for height
        self.player = PhysicsEntity(self, 'player', spawn, (16, 32))

        self.scroll = [0, 0]

        self.scroll = [0, 0]

        self.audio = Audio()

    def run(self):
        while True:
            # 1. Timing at Events
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Ipasa ang events sa UI (Pause button) habang naglalaro
                if self.state == "playing":
                    self.ui.process_events(event)

            # ---------------------------------------------------------
            # CASE A: MAIN MENU
            # ---------------------------------------------------------
            if self.state == "main_menu":
                self.screen.fill((0, 0, 0))
                try:
                    if self.menu_manager.main_menu.is_enabled():
                        self.menu_manager.main_menu.update(events)
                        self.menu_manager.main_menu.draw(self.screen)
                    else:
                        self.menu_manager.main_menu.enable()
                except RuntimeError:
                    pass

            # ---------------------------------------------------------
            # CASE B: NAGLALARO (Fixed Indentation & Music)
            # ---------------------------------------------------------
            elif self.state == "playing":
                # Audio logic (Isang beses lang tatawagin)
                if not pygame.mixer.music.get_busy():
                    self.audio.play_music("Assets/Music/Background Music.mp3", 0.4)

                # Game Logic (Movement, Scroll, Update)
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

                map_w = self.Tilemap.tmx_data.width * self.Tilemap.tile_size
                map_h = self.Tilemap.tmx_data.height * self.Tilemap.tile_size
                self.scroll[0] = max(0, min(self.scroll[0], map_w - self.display.get_width()))
                self.scroll[1] = max(0, min(self.scroll[1], map_h - self.display.get_height()))
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                # Input Handling (Hiwalay sa Rendering)
                for event in events:
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
                            self.state = "paused"
                            pygame.mixer.music.pause()
                            self.menu_manager.pause_menu.enable()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT: self.movement[0] = False
                        if event.key == pygame.K_RIGHT: self.movement[1] = False
                        if event.key == pygame.K_DOWN: self.player.drop_through = False

                # Rendering (Dapat NAKALABAS ito sa for event loop)
                self.display.fill((0, 0, 0))
                self.Tilemap.render(self.display, offset=render_scroll)

                goal_rect = self.assets['goal'].get_rect(midbottom=(
                    self.Tilemap.goal_pos[0] + self.Tilemap.tile_size / 2 - render_scroll[0],
                    self.Tilemap.goal_pos[1] - render_scroll[1]
                ))
                self.display.blit(self.assets['goal'], goal_rect)

                self.player.update(self.Tilemap, (self.movement[1] - self.movement[0], 0), (map_w, map_h))
                self.player.render(self.display, offset=render_scroll)

                # Scaling to Main Screen
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.ui.update(dt)
                self.ui.draw(self.screen)

            # ---------------------------------------------------------
            # CASE C: PAUSED
            # ---------------------------------------------------------
            elif self.state == "paused":
                # Draw the last frame of the game
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.ui.draw(self.screen)

                try:
                    if self.menu_manager.pause_menu.is_enabled():
                        self.menu_manager.pause_menu.update(events)
                        self.menu_manager.pause_menu.draw(self.screen)
                    else:
                        self.menu_manager.pause_menu.enable()
                except RuntimeError:
                    pass

            # ISA LANG DAPAT ANG UPDATE SA PINAKABABA
            pygame.display.update()

Game().run()