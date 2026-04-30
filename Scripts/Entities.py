import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False

        self.set_action('walk')

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.jumps = 0
        self.max_jumps = 2
        self.drop_through = False

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + '/' + self.action].copy()
            self.animation.frame = 0

    def rect(self):
        return pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1])

    def update(self, Tilemap, movement=(0, 0), map_bounds=None):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        # 1. APPLY GRAVITY
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # 2. X-AXIS MOVEMENT
        frame_movement = [movement[0] + self.velocity[0], self.velocity[1]]
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

        # 3. Y-AXIS MOVEMENT
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 0
                    self.jumps = 0
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
                self.pos[1] = entity_rect.y

        # 4. PLATFORM LOGIC
        entity_rect = self.rect()
        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] == "platform":
                platform_rect = pygame.Rect(tile["pos"][0] * Tilemap.tile_size, tile["pos"][1] * Tilemap.tile_size, 16, 16)
                if entity_rect.colliderect(platform_rect):
                    if self.velocity[1] > 0 and not self.drop_through:
                        if entity_rect.bottom <= platform_rect.top + 10:
                            entity_rect.bottom = platform_rect.top
                            self.pos[1] = entity_rect.y
                            self.collisions['down'] = True
                            self.velocity[1] = 0
                            self.jumps = 0

        # 5. ANIMATION LOGIC
        if self.collisions['down']:
            if abs(movement[0]) > 0.1:
                self.set_action('walk')
                self.animation.update()
            else:
                self.set_action('walk')
                self.animation.frame = 0
        else:
            if self.velocity[1] < 0:
                self.set_action('jump')
            elif self.velocity[1] > 0.7:
                self.set_action('drop')
            self.animation.update()

        if movement[0] > 0: self.flip = False
        elif movement[0] < 0: self.flip = True

        # 6. GOAL & DEATH CHECKS
        goal_hitbox = pygame.Rect(Tilemap.goal_pos[0], Tilemap.goal_pos[1], 16, 16)
        if entity_rect.colliderect(goal_hitbox):
            self.game.level_manager.unlock_next_level()
            self.game.state = "level_complete"
            return

        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] == "deadly":
                d_rect = pygame.Rect(tile["pos"][0] * 16, tile["pos"][1] * 16, 16, 16)
                if entity_rect.colliderect(d_rect):
                    self.game.audio.play_sfx("Assets/Music/SFX/Death Sound.mp3", 0.4)
                    self.pos = [self.game.Tilemap.spawn_point[0], self.game.Tilemap.spawn_point[1] - 32]
                    self.velocity = [0, 0]

        if map_bounds:
            self.pos[0] = max(0, min(self.pos[0], map_bounds[0] - self.size[0]))
            self.pos[1] = max(0, min(self.pos[1], map_bounds[1] - self.size[1]))

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.flip(self.animation.img(), self.flip, False)
        rect = img.get_rect(midbottom=(
            self.pos[0] + self.size[0] // 2 - offset[0],
            self.pos[1] + self.size[1] - offset[1]
        ))
        surf.blit(img, rect)