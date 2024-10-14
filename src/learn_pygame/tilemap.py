from attrs import define 
import pygame

from learn_pygame.assets import Assets

# for collisions
NEIGHBOUR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),  (0, 0),  (1, 0),
    (-1, 1),  (0, 1),  (1, 1)
]
PHYSICS_TILES_KINDS = {'grass', 'stone'}


@define(frozen=True, eq=True)
class Tile:
    kind: str
    variant: int
    position: pygame.Vector2

    def __hash__(self) -> int:
        return hash((self.kind, self.variant, self.position.x, self.position.y))


class Tilemap:
    def __init__(self, tile_size=16) -> None:
        self.tile_size = tile_size
        # the actual tile map with position relative to the tile size
        self.tilemap: dict[tuple[int, int], Tile] = dict()
        # other objects on the map with pixel position
        self.decorations: set[Tile] = set()

        for i in range(10):
            position = (3+i, 10)
            self.tilemap[position] = Tile(kind="grass", variant=1, position=pygame.Vector2(*position))
            
            position = (10, i+5)
            self.tilemap[position] = Tile(kind="stone", variant=1, position=pygame.Vector2(*position))

    def render(self, destination: pygame.Surface, offset: pygame.Vector2) -> None:
        # decorations behind actual grid
        for decoration in self.decorations:
            decoration_sprite = Assets.tiles[decoration.kind][decoration.variant]
            final_position = pygame.Vector2(decoration.position.xy) - offset
            destination.blit(decoration_sprite, final_position)

        # render tiles only actually in screen
        for x in range(int(offset.x) // self.tile_size - 1, (int(offset.x) + destination.width) // self.tile_size + 1):
            for y in range(int(offset.y) // self.tile_size - 1, (int(offset.y) + destination.height) // self.tile_size + 1):
                location = (x, y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    tile_sprite = Assets.tiles[tile.kind][tile.variant]
                    final_position = pygame.Vector2(tile.position.xy) * self.tile_size - offset
                    destination.blit(tile_sprite, final_position)


            
    def tiles_around(self, position: list[float]) -> list[Tile]:
        tiles: list[Tile]= []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for (x_offset, y_offset) in NEIGHBOUR_OFFSETS:
            position_to_check = (tile_location[0] + x_offset, tile_location[1] + y_offset)
            if position_to_check in self.tilemap:
                tiles.append(self.tilemap[position_to_check])
        return tiles

    def physics_rects_around(self, position: list[float]):
        rects = []
        for tile in self.tiles_around(position):
            if tile.kind in PHYSICS_TILES_KINDS:
                tile_position = pygame.Vector2(tile.position[0], tile.position[1]) * self.tile_size
                rects.append(pygame.Rect(tile_position.x, tile_position.y, self.tile_size, self.tile_size))
        return rects
