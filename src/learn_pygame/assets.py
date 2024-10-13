import pygame
from learn_pygame.utils import load_image, load_images

BLACK = (0, 0, 0)

class Assets:
    tiles: dict[str, list[pygame.Surface]]
    player: pygame.Surface
    background: pygame.Surface

    @staticmethod
    def load():
        Assets.tiles = dict(
            grass       = load_images("tiles/grass", color_key=BLACK),
            stone       = load_images("tiles/stone", color_key=BLACK),
            decor       = load_images("tiles/decor", color_key=BLACK),
            large_decor = load_images("tiles/large_decor", color_key=BLACK)
        )
        Assets.player = load_image("entities/player.png", color_key=BLACK)
        Assets.background = load_image("background.png")
        
    
