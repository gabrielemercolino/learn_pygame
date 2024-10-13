from dataclasses import dataclass
from typing import Optional
import pygame

from learn_pygame.assets import Assets

# for collisions
NEIGHBOUR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),  (0, 0),  (1, 0),
    (-1, 1),  (0, 1),  (1, 1)
]
PHYSICS_TILES_KINDS = {'grass', 'stone'}


@dataclass(slots=True, frozen=True, eq=True)
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
        self.tilemap: set[Tile] = set()
        # other objects on the map with pixel position
        self.decorations: set[Tile] = set()

        for i in range(10):
            position = pygame.Vector2(3+i, 10)
            self.tilemap.add(Tile(kind="grass", variant=1, position=position))
            
            position = pygame.Vector2(10, i+5)
            self.tilemap.add(Tile(kind="stone", variant=1, position=position))

    def render(self, destination: pygame.Surface, offset: Optional[pygame.Vector2]) -> None:
        # decorations behind actual grid
        for decoration in self.decorations:
            decoration_sprite = Assets.tiles[decoration.kind][decoration.variant]
            final_position = pygame.Vector2(decoration.position.xy)
            if offset: final_position -= offset
            destination.blit(decoration_sprite, final_position)

        for tile in self.tilemap:
            tile_sprite = Assets.tiles[tile.kind][tile.variant]
            final_position = pygame.Vector2(tile.position.xy) * self.tile_size
            if offset: final_position -= offset
            destination.blit(tile_sprite, final_position)

    def tiles_around(self, position: list[float]) -> list[Tile]:
        tiles: list[Tile]= []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for (x_offset, y_offset) in NEIGHBOUR_OFFSETS:
            position_to_check = (tile_location[0] + x_offset, tile_location[1] + y_offset)
            for tile in self.tilemap:
                if tile.position == position_to_check: tiles.append(tile)
        return tiles

    def physics_rects_around(self, position: list[float]):
        rects = []
        for tile in self.tiles_around(position):
            if tile.kind in PHYSICS_TILES_KINDS:
                tile_position = pygame.Vector2(tile.position[0], tile.position[1]) * self.tile_size
                rects.append(pygame.Rect(tile_position.x, tile_position.y, self.tile_size, self.tile_size))
        return rects
