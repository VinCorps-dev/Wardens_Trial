import pygame


# ==============================================================================
# BASE CLASS — PhysicsEntity
# Handles all shared physics logic. Does NOT contain game-specific behavior
# like death or goal reaching — those are handled by subclasses.
# ==============================================================================

class PhysicsEntity:

    # --- Constants (no more magic numbers) ---
    GRAVITY             = 0.1
    MAX_FALL_SPEED      = 5
    FALL_ANIM_THRESHOLD = 0.7
    PLATFORM_TOLERANCE  = 10
    GOAL_SIZE           = (32, 32)
    TILE_SIZE           = 16
    SPAWN_OFFSET_Y      = 32
    MOVE_THRESHOLD      = 0.1

    def __init__(self, game, e_type, pos, size):
        self.game    = game
        self.e_type  = e_type
        self.pos     = list(pos)
        self.size    = size
        self.velocity = [0, 0]

        self.action     = ''
        self.anim_offset = (-3, -3)
        self.flip       = False

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.jumps      = 0
        self.max_jumps  = 2
        self.drop_through = False

        self.set_action('walk')

    # --------------------------------------------------------------------------
    # PROPERTIES — Data abstraction over raw list access
    # --------------------------------------------------------------------------

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def on_ground(self):
        """True when the entity is standing on a solid surface."""
        return self.collisions['down']

    @property
    def can_jump(self):
        """True when the entity still has jumps remaining."""
        return self.jumps < self.max_jumps

    # --------------------------------------------------------------------------
    # CORE METHODS
    # --------------------------------------------------------------------------

    def set_action(self, action):
        if action != self.action:
            self.action = action
            try:
                self.animation = self.game.assets[self.e_type + '/' + self.action].copy()
            except KeyError:
                self.animation = self.game.assets[self.e_type + '/walk'].copy()
            self.animation.frame = 0

    def rect(self):
        return pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1])

    # --------------------------------------------------------------------------
    # MAIN UPDATE — Clean and readable; delegates to private methods
    # --------------------------------------------------------------------------

    def update(self, Tilemap, movement=(0, 0), map_bounds=None):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        # Apply gravity
        self.velocity[1] = min(self.MAX_FALL_SPEED, self.velocity[1] + self.GRAVITY)

        self._handle_x_collision(Tilemap, movement)
        self._handle_y_collision(Tilemap)
        self._handle_platform_collision(Tilemap)
        self._update_animation(movement)
        self._check_goal(Tilemap)
        self._check_deadly(Tilemap)
        self._apply_map_bounds(map_bounds)

    # --------------------------------------------------------------------------
    # PRIVATE METHODS — Each handles exactly one responsibility
    # --------------------------------------------------------------------------

    def _handle_x_collision(self, Tilemap, movement):
        """Move entity horizontally and resolve solid tile collisions."""
        frame_movement_x = movement[0] + self.velocity[0]
        self.pos[0] += frame_movement_x
        entity_rect = self.rect()

        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement_x > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement_x < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

    def _handle_y_collision(self, Tilemap):
        """Move entity vertically and resolve solid tile collisions."""
        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()

        for rect in Tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 0
                    self.jumps = 0
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
                self.pos[1] = entity_rect.y

    def _handle_platform_collision(self, Tilemap):
        """Handle one-way platform collision (drop-through supported)."""
        entity_rect = self.rect()

        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] != "platform":
                continue

            platform_rect = pygame.Rect(
                tile["pos"][0] * Tilemap.tile_size,
                tile["pos"][1] * Tilemap.tile_size,
                self.TILE_SIZE,
                self.TILE_SIZE
            )

            if not entity_rect.colliderect(platform_rect):
                continue

            falling       = self.velocity[1] > 0
            not_dropping  = not self.drop_through
            close_enough  = entity_rect.bottom <= platform_rect.top + self.PLATFORM_TOLERANCE

            if falling and not_dropping and close_enough:
                entity_rect.bottom  = platform_rect.top
                self.pos[1]         = entity_rect.y
                self.collisions['down'] = True
                self.velocity[1]    = 0
                self.jumps          = 0

    def _update_animation(self, movement):
        """Pick the correct animation frame based on movement state."""
        if self.on_ground:
            self.set_action('walk')
            if abs(movement[0]) > self.MOVE_THRESHOLD:
                self.animation.update()
            else:
                self.animation.frame = 0
        else:
            if self.velocity[1] < 0:
                self.set_action('jump')
            elif self.velocity[1] > self.FALL_ANIM_THRESHOLD:
                self.set_action('drop')
            self.animation.update()

        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

    def _check_goal(self, Tilemap):
        """Check if entity has reached the level goal."""
        if not Tilemap.goal_pos:
            return

        gx, gy = Tilemap.goal_pos
        goal_hitbox = pygame.Rect(gx, gy, *self.GOAL_SIZE)

        if self.rect().colliderect(goal_hitbox):
            self.on_goal_reached()

    def _check_deadly(self, Tilemap):
        """Check if entity has touched a deadly tile."""
        entity_rect = self.rect()

        for tile in Tilemap.tiles_around(self.pos):
            if tile["type"] != "deadly":
                continue

            d_rect = pygame.Rect(
                tile["pos"][0] * self.TILE_SIZE,
                tile["pos"][1] * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE
            )

            if entity_rect.colliderect(d_rect):
                self.on_deadly_hit()
                break  # one hit is enough per frame

    def _apply_map_bounds(self, map_bounds):
        """Clamp entity position within map boundaries."""
        if map_bounds:
            self.pos[0] = max(0, min(self.pos[0], map_bounds[0] - self.size[0]))
            self.pos[1] = max(0, min(self.pos[1], map_bounds[1] - self.size[1]))

    # --------------------------------------------------------------------------
    # HOOK METHODS — Override in subclasses for specific behavior
    # --------------------------------------------------------------------------

    def on_deadly_hit(self):
        """Called when entity touches a deadly tile. Override in subclasses."""
        pass

    def on_goal_reached(self):
        """Called when entity reaches the goal. Override in subclasses."""
        pass

    # --------------------------------------------------------------------------
    # RENDER
    # --------------------------------------------------------------------------

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.flip(self.animation.img(), self.flip, False)
        rect = img.get_rect(midbottom=(
            self.pos[0] + self.size[0] // 2 - offset[0],
            self.pos[1] + self.size[1] - offset[1]
        ))
        surf.blit(img, rect)


# ==============================================================================
# PLAYER — Subclass of PhysicsEntity
# Adds player-specific responses to game events (death, goal).
# ==============================================================================

class Player(PhysicsEntity):

    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

    def on_deadly_hit(self):
        """Player dies: play SFX and reset to spawn point."""
        self.game.audio.play_sfx("Assets/Music/SFX/Death Sound.mp3")
        spawn = self.game.Tilemap.spawn_point
        self.pos = [spawn[0], spawn[1] - self.SPAWN_OFFSET_Y]
        self.velocity = [0, 0]

    def on_goal_reached(self):
        """Player wins the level: unlock next and change state."""
        self.game.level_manager.unlock_next_level()
        self.game.state = "level_complete"
