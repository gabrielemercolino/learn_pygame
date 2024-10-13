import os
from typing import Optional
import pygame, importlib.resources


def load_image(name: str, color_key: Optional[tuple[int, int, int]]=None) -> pygame.Surface:
    image_path = importlib.resources.files('assets.images').joinpath(name)
    image = pygame.image.load(str(image_path)).convert()
    if (color_key): image.set_colorkey(color_key)
    return image

def load_images(dir: str, color_key: Optional[tuple[int, int, int]]=None) -> list[pygame.Surface]:
    images: list[pygame.Surface] = []
    images_dir = importlib.resources.files('assets.images').joinpath(dir)
    for image_name in sorted(os.listdir(str(images_dir))):
        images.append(load_image(f'{dir}/{image_name}', color_key))
    return images
