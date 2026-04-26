import math
import pygame
import sys

from Scripts.Entities import PhysicsEntity
from Scripts.Utilities import load_image, load_images
from Scripts.Tilemap import Tilemap
from Scripts.Utilities import load_spritesheet
from Scripts.Audio import Audio
from Scripts.Ui_sa_game import UserInterface

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Warden's Trial")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.ui = UserInterface(self)

        self.clock = pygame.time.Clock()

        self.movement = [False,False]

        self.assets ={
            'tiles': load_spritesheet('Tilesets/Dungeon Tile Set.png', 16),
            'player': load_image('Character/sprite.png')
        }

        self.Tilemap = Tilemap(self, tile_size= 16)

        # ✅ THEN GET SPAWN
        spawn = (self.Tilemap.spawn_point[0], self.Tilemap.spawn_point[1] - 32)  # Offset for height
        self.player = PhysicsEntity(self, 'player', spawn, (16, 32))

        self.scroll = [0, 0]

        self.scroll = [0, 0]

        self.audio = Audio()
        self.audio.play_music("Assets/Audio/Background#3_Level 3.mp3", 0.4)


    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            dt = self.clock.tick(60) / 1000.0

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            map_width = self.Tilemap.tmx_data.width * self.Tilemap.tile_size
            map_height = self.Tilemap.tmx_data.height * self.Tilemap.tile_size

            self.scroll[0] = max(0, min(self.scroll[0], map_width - self.display.get_width()))
            self.scroll[1] = max(0, min(self.scroll[1], map_height - self.display.get_height()))


            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # 3. Now you use 'render_scroll' for BOTH of these
            self.Tilemap.render(self.display, offset=render_scroll)

            map_w = self.Tilemap.tmx_data.width * self.Tilemap.tile_size
            map_h = self.Tilemap.tmx_data.height * self.Tilemap.tile_size


            self.player.update(
                self.Tilemap,
                (self.movement[1] - self.movement[0], 0),
                (map_w, map_h)
            )
            self.player.render(self.display, offset=render_scroll)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.ui.manager.process_events(event)


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jumps < self.player.max_jumps:
                            self.player.velocity[1] = -3
                            self.player.jumps += 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

                if event.type == pygame.KEYDOWN: # Platform na pwede bumababa
                    if event.key == pygame.K_DOWN:
                        self.player.drop_through = True

                if event.type == pygame.KEYUP:  # Platform na pwede bumaba
                    if event.key == pygame.K_DOWN:
                        self.player.drop_through = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.ui.update(dt)  # Ito yung magka-calculate ng progress bar
            self.ui.draw(self.screen)  # Draw directly to the big screen
            pygame.display.update()


Game().run()