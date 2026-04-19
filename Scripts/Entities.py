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

    def rect(self):
        return pygame.Rect(
            int(self.pos[0]),
            int(self.pos[1]),
            self.size[0],
            self.size[1]
        )

    def update(self, Tilemap, movement=(0, 0)):
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


        self.pos[1] += frame_movement [1] # Movement ng Y axis
        entity_rect = self.rect()
        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        player_rect = self.rect()

        for tile in Tilemap.tilemap.values():

            if tile["type"] != "deadly":
                continue

            tx, ty = tile["pos"]

            spike_rect = pygame.Rect(
                tx * Tilemap.tile_size,
                ty * Tilemap.tile_size,
                Tilemap.tile_size,
                Tilemap.tile_size
            )

            if player_rect.colliderect(spike_rect):

                self.pos = [50, 50]
                self.velocity = [0, 0]
                return
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down']:
            self.velocity[1] = 0
            self.jumps = 0  # reset jumps when touching ground
        elif self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf, offset=(0, 0)):
        render_x = self.pos[0] - offset[0]
        render_y = self.pos[1] - offset[1]
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
