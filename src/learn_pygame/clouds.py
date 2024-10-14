import random

from attr import define
import pygame

from learn_pygame.assets import Assets

@define(eq = True)
class Cloud:
    position: pygame.Vector2
    image: pygame.Surface
    speed: float
    depth: float

    def update(self):
        self.position.x += self.speed

    def render(self, destination: pygame.Surface, offset: pygame.Vector2):
        final_position = self.position - offset * self.depth
        final_position.x = final_position.x % (destination.width + self.image.width) - self.image.width
        final_position.y = final_position.y % (destination.height + self.image.width) - self.image.height
        destination.blit(self.image, (int(final_position.x), int(final_position.y)))


class Clouds:
    def __init__(self, cloud_count = 16) -> None:
        self.clouds = []

        for _ in range(cloud_count):
            position = pygame.Vector2(random.random() * 9999, random.random() * 9999)
            image = random.choice(Assets.clouds) 
            speed = random.random() * 0.05 + 0.05
            depth = random.random() * 0.06 + 0.02
            self.clouds.append(Cloud(position=position, image=image, speed=speed, depth=depth))

        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds: cloud.update()

    def render(self, destination: pygame.Surface, offset: pygame.Vector2):
        for cloud in self.clouds: cloud.render(destination=destination, offset=offset)
