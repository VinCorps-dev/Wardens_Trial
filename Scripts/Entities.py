import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = { 'up': False, 'down': False, 'left': False, 'right': False }
        self.jumps = 0
        self.max_jumps = 2
        self.drop_through = False

    def rect(self):
        return pygame.Rect(
            int(self.pos[0]),
            int(self.pos[1]),
            self.size[0],
            self.size[1]
        )

    def update(self, Tilemap, movement=(0, 0), map_bounds=None):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement =  (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement [0] # Movement ng X axis
        entity_rect = self.rect()
        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()

        for rect in Tilemap.physics_rects_around(self.pos):

            if entity_rect.colliderect(rect):

                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True

                elif frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                self.pos[1] = entity_rect.y


        for tile in Tilemap.tiles_around(self.pos): #Platform Logic

            if tile["type"] != "platform":
                continue

            tx, ty = tile["pos"]

            plat_rect = pygame.Rect(
                tx * Tilemap.tile_size,
                ty * Tilemap.tile_size,
                Tilemap.tile_size,
                Tilemap.tile_size
            )

            if entity_rect.colliderect(plat_rect):

                # ONLY LAND WHEN FALLING
                if (frame_movement[1] > 0
                        and entity_rect.bottom <= plat_rect.top + 6
                        and not self.drop_through):
                    entity_rect.bottom = plat_rect.top
                    self.pos[1] = entity_rect.y
                    self.collisions['down'] = True

        player_rect = self.rect()

        for tile in Tilemap.tilemap.values():

            if tile["type"] != "deadly":
                continue

            tx, ty = tile["pos"]

            deadly_rect = pygame.Rect(
                tx * Tilemap.tile_size,
                ty * Tilemap.tile_size,
                Tilemap.tile_size,
                Tilemap.tile_size
            )

            if player_rect.colliderect(deadly_rect):
                self.pos = list(self.game.Tilemap.spawn_point)
                self.velocity = [0, 0]
                return
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down']:
            self.velocity[1] = 0
            self.jumps = 0  # reset jumps when touching ground
        elif self.collisions['up']:
            self.velocity[1] = 0

        if map_bounds:
            map_w, map_h = map_bounds

            self.pos[0] = max(0, min(self.pos[0], map_w - self.size[0]))
            self.pos[1] = max(0, min(self.pos[1], map_h - self.size[1]))

    def render(self, surf, offset=(0, 0)):
        img = self.game.assets['player']

        rect = img.get_rect(midbottom=(
            self.pos[0] + self.size[0] / 2 - offset[0],
            self.pos[1] + self.size[1] - offset[1]
        ))

        surf.blit(img, rect)
