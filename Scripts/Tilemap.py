import pygame
import pytmx
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1,1)]
PHYSICS_TILES = {'tiles'}


class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.load_tmx("Levels/Map 1.tmx")

    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size)), (int(position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
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

        for layer in tmx_data:
            if hasattr(layer, "data"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue


                    props = tmx_data.get_tile_properties_by_gid(gid) or {}


                    tile_type = (props.get("type") or "").lower()
                    final_type = tile_type

                    image = tmx_data.get_tile_image_by_gid(gid)



                    self.tilemap[f"{x};{y}"] = {
                        "type": final_type,
                        "image": image,
                        "pos": (x, y)
                    }


    def deadly_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] == 'spike':
                rects.append(pygame.Rect(
                    tile['pos'][0] * self.tile_size,
                    tile['pos'][1] * self.tile_size,
                    self.tile_size,
                    self.tile_size
                ))
        return rects