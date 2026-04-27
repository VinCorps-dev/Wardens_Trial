import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type  # e.g., 'player'
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False

        # CHANGED: Just ask for 'run'.
        # Combined with e_type ('player'), it will look for 'player/run'
        self.set_action('run')

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.jumps = 0
        self.max_jumps = 2
        self.drop_through = False



    def set_action(self, action):
        if action != self.action:
            self.action = action
            # This looks up 'player/run' in your assets and makes a fresh copy for this player
            self.animation = self.game.assets[self.e_type + '/' + self.action].copy()

    def rect(self):
        return pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1])

    def update(self, Tilemap, movement=(0, 0), map_bounds=None):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        # --- 1. X AXIS MOVEMENT ---
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
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

        # --- 2. Y AXIS MOVEMENT ---
        self.pos[1] += frame_movement[1]
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

        # --- 3. PLATFORM LOGIC (One-way) ---
        entity_rect = self.rect()
        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] == "platform":
                tx, ty = tile["pos"]
                platform_rect = pygame.Rect(tx * Tilemap.tile_size, ty * Tilemap.tile_size, Tilemap.tile_size,
                                            Tilemap.tile_size)

                if entity_rect.colliderect(platform_rect):
                    # Check kung pababa ka at hindi naka-pindot ng Down key
                    if self.velocity[1] > 0 and not self.drop_through:
                        if entity_rect.bottom <= platform_rect.top + 10:
                            entity_rect.bottom = platform_rect.top
                            self.pos[1] = entity_rect.y
                            self.collisions['down'] = True
                            self.velocity[1] = 0

        # --- 4. DEATH CHECK (Deadly Tiles) ---
        entity_rect = self.rect()
        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] == "deadly":
                tx, ty = tile["pos"]
                deadly_rect = pygame.Rect(tx * Tilemap.tile_size, ty * Tilemap.tile_size, Tilemap.tile_size,
                                          Tilemap.tile_size)
                if entity_rect.colliderect(deadly_rect):
                    self.game.audio.play_sfx("Assets/Music/SFX/Death Sound.mp3", 0.4)
                    # RESPAWN WITH OFFSET
                    self.pos = [self.game.Tilemap.spawn_point[0], self.game.Tilemap.spawn_point[1] - 32]
                    self.velocity = [0, 0]
                    return  # Exit update immediately on death

        if movement[0] != 0:
            # We are moving! Update the flip and play the animation
            if movement[0] > 0:
                self.flip = False
            elif movement[0] < 0:
                self.flip = True

            # This makes the legs move
            self.animation.update()
        else:
            # 2. If we AREN'T moving, reset to the first frame
            # so the character stands still.
            self.animation.frame = 0


        # --- 5. GRAVITY & TERMINAL VELOCITY ---
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down']:
            self.velocity[1] = 0
            self.jumps = 0
        elif self.collisions['up']:
            self.velocity[1] = 0

        # --- 6. MAP BOUNDS ---
        if map_bounds:
            self.pos[0] = max(0, min(self.pos[0], map_bounds[0] - self.size[0]))
            self.pos[1] = max(0, min(self.pos[1], map_bounds[1] - self.size[1]))

    def render(self, surf, offset=(0, 0)):
        # 1. Get the current frame
        img = self.animation.img()

        # 2. Handle the flip
        img_to_draw = pygame.transform.flip(img, self.flip, False)

        # 3. Use 'midbottom' alignment
        # We align the middle-bottom of the IMAGE to the middle-bottom of the HITBOX
        rect = img_to_draw.get_rect(midbottom=(
            self.pos[0] + self.size[0] // 2 - offset[0], # Center of hitbox X
            self.pos[1] + self.size[1] - offset[1]      # Bottom of hitbox Y
        ))

        # 4. Draw the rect
        surf.blit(img_to_draw, rect)
