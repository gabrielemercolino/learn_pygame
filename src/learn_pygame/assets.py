import pygame
from learn_pygame.animations import Animation
from learn_pygame.utils import load_image, load_images

BLACK = (0, 0, 0)

class Assets:
    tiles: dict[str, list[pygame.Surface]]
    player: pygame.Surface
    background: pygame.Surface
    clouds: list[pygame.Surface]
    animations: dict[str, dict[str, Animation]]

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
        Assets.clouds = load_images("clouds", color_key=BLACK)
    
        Assets.animations = dict(
            player = dict(
                idle = Animation(images=load_images("entities/player/idle", color_key=BLACK), duration=6),
                run = Animation(images=load_images("entities/player/run", color_key=BLACK), duration=4),
                jump = Animation(images=load_images("entities/player/jump", color_key=BLACK)),
                slide = Animation(images=load_images("entities/player/slide", color_key=BLACK)),
                wall_slide = Animation(images=load_images("entities/player/wall_slide", color_key=BLACK)),
            )
        )
