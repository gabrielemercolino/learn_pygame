from attrs import asdict, define 
import pygame, json, ast

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
    position: tuple[int, int]


class Tilemap:
    def __init__(self, tile_size=16) -> None:
        self.tile_size = tile_size
        # the actual tile map with position relative to the tile size
        self.tilemap: dict[tuple[int, int], Tile] = dict()
        # other objects on the map with pixel position
        self.decorations: dict[tuple[int, int], Tile] = dict()

    def render(self, destination: pygame.Surface, offset: pygame.Vector2) -> None:
        # decorations behind actual grid
        for position in self.decorations:
            decoration = self.decorations[position]
            decoration_sprite = Assets.tiles[decoration.kind][decoration.variant]
            final_position = pygame.Vector2(*decoration.position) - offset
            destination.blit(decoration_sprite, final_position)

        # render tiles only actually in screen
        for x in range(int(offset.x) // self.tile_size - 1, (int(offset.x) + destination.width) // self.tile_size + 1):
            for y in range(int(offset.y) // self.tile_size - 1, (int(offset.y) + destination.height) // self.tile_size + 1):
                location = (x, y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    tile_sprite = Assets.tiles[tile.kind][tile.variant]
                    final_position = pygame.Vector2(*tile.position) * self.tile_size - offset
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

    def save(self, path: str) -> None:
        with open(f"{path}", 'w') as f:
            tiles = dict()
            decorations = dict()

            for key, value in self.tilemap.items():
                tiles[str(key)] = asdict(value)

            for key, value in self.decorations.items():
                decorations[str(key)] = asdict(value)

            contents = json.dumps(dict(tiles=tiles, decorations=decorations))
            f.write(contents)

    def load(self, path: str) -> None:
        with open(f"{path}", 'r') as f:
            tiles: dict[tuple[int, int], Tile] = dict()
            decorations: dict[tuple[int, int], Tile] = dict()

            data = json.load(f)
            
            _tiles: dict[str, dict] = data['tiles']
            _decorations: dict[str, dict] = data['decorations']

            for key, value in _tiles.copy().items():
                tiles[ast.literal_eval(key)] = Tile(kind=value['kind'], variant=value['variant'], position=tuple(value['position']))
            
            for key, value in _decorations.copy().items():
                decorations[ast.literal_eval(key)] = Tile(kind=value['kind'], variant=value['variant'], position=tuple(value['position']))

            self.tilemap = tiles
            self.decorations = decorations
