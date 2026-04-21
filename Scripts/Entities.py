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
            int(self.pos[0]),  # 🔥 Integer X
            int(self.pos[1]),  # 🔥 Integer Y
            16,  # 🔥 Your width
            32  # 🔥 Your height
        )

    def update(self, Tilemap, movement=(0, 0), map_bounds=None):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # 🔥 STEP 2: X AXIS FIRST (Horizontal - No Jitter)
        self.pos[0] += frame_movement[0] * 0.8  # Slower X
        entity_rect = self.rect()
        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.pos[0] = rect.left - 16  # ← Exact 16px width snap
                    self.collisions['right'] = True
                else:  # < 0
                    self.pos[0] = rect.right  # ← Exact snap
                    self.collisions['left'] = True

        # 🔥 Y AXIS SECOND (Vertical)
        self.pos[1] += frame_movement[1] * 0.9  # Slower Y
        entity_rect = self.rect()
        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.pos[1] = rect.top - 32  # ← Exact 32px height snap
                    self.collisions['down'] = True
                else:  # < 0
                    self.pos[1] = rect.bottom  # ← Exact snap
                    self.collisions['up'] = True

        # 🔥 Your DEATH CHECK (keep as-is)
        player_rect = self.rect()
        for tile in Tilemap.tilemap.values():
            if tile["type"] != "deadly": continue
            tx, ty = tile["pos"]
            deadly_rect = pygame.Rect(tx * Tilemap.tile_size, ty * Tilemap.tile_size,
                                      Tilemap.tile_size, Tilemap.tile_size)
            if player_rect.colliderect(deadly_rect):
                self.pos = list(self.game.Tilemap.spawn_point)
                self.velocity = [0, 0]
                return

        # 🔥 Your PLATFORM LOGIC (keep as-is)
        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] != "platform": continue
            # ... your platform code stays exactly the same ...

        # 🔥 Gravity + Jumps (keep as-is)
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collisions['down']:
            self.velocity[1] = 0
            self.jumps = 0
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
