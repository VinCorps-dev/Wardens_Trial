import pygame
import pytmx
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1,1)]
PHYSICS_TILES = {'tiles'}
PLATFORM_TILES = {'platform'}

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.spawn_point = (50, 50)  # default FIRST
        self.load_tmx("Levels/Map 1.tmx")

    def tiles_around(self, position):
        tiles = []
        # Kunin ang saktong tile coordinate ng player
        tile_x = int(position[0] // self.tile_size)
        tile_y = int(position[1] // self.tile_size)

        # Imbes na range(-3, 4), gagamit tayo ng saktong 3x3 o 3x4 grid
        # para hindi masyadong malayo ang chine-check na tiles.
        for dx in range(-1, 2):  # Check left, center, right
            for dy in range(-1, 3):  # Check head, torso, feet, and floor
                check_x, check_y = tile_x + dx, tile_y + dy
                check_location = f"{check_x};{check_y}"
                if check_location in self.tilemap:
                    tiles.append(self.tilemap[check_location])
        return tiles

        # --- ILAGAY MO DITO SA BABA NG PHYSICS_RECTS O KAHIT SAANG DEF ---
    def get_goal_rect(self):
        return pygame.Rect(self.goal_pos[0], self.goal_pos[1], self.tile_size, self.tile_size)

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            # Siguraduhin na ang PHYSICS_TILES ay 'tiles' (base sa setup mo)
            if tile['type'] in PHYSICS_TILES or tile['type'] == 'solid':
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size,
                    tile['pos'][1] * self.tile_size,
                    self.tile_size,
                    self.tile_size
                ))
        return rects



    def render(self, surf, offset=(0, 0)):
        # draw using Tiled layer order
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue

                    image = self.tmx_data.get_tile_image_by_gid(gid)

                    if image:
                        surf.blit(
                            image,
                            (
                                x * self.tile_size - offset[0],
                                y * self.tile_size - offset[1]
                            )
                        )



    def load_tmx(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        tmx_data = self.tmx_data

        for layer in tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue


                    props = tmx_data.get_tile_properties_by_gid(gid) or {}

                    tile_type = props.get("type")

                    if isinstance(tile_type, str):
                        final_type = tile_type.strip().lower()
                    else:
                        final_type = ""

                    image = tmx_data.get_tile_image_by_gid(gid)

                    self.tilemap[f"{x};{y}"] = {
                        "type": final_type,
                        "image": image,
                        "pos": (x, y)
                    }

    # --- FIND SPAWN POINT ---
        for obj in self.tmx_data.objects:
            if obj.name == "spawn":
                self.spawn_point = (obj.x, obj.y)

        self.goal_pos = (0, 0)  # Default
        for obj in self.tmx_data.objects:
            if obj.name == "goal":
                self.goal_pos = (obj.x, obj.y)
                break


    def deadly_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] == 'deadly':
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size,
                    tile['pos'][1] * self.tile_size,
                    self.tile_size,
                    self.tile_size
                ))
        return rects