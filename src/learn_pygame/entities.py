from typing import Optional
import pygame

from learn_pygame.assets import Assets


class PhysicsEntity:
    def __init__(self, tag, position: tuple[float, float], size: tuple[int, int]) -> None:
        self.tag = tag
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.FRect(*position, *size)
        self.collisions = dict(up=False, down=False, left=False, right=False)

    def update(self, tilemap, movement: Optional[pygame.Vector2]):
        # reset collisions
        self.collisions = dict(up=False, down=False, left=False, right=False)
        
        frame_movement = pygame.Vector2(self.velocity.xy)
        if movement: frame_movement += movement
        tiles_to_check = tilemap.physics_rects_around(self.rect.center)

        self.rect.x += frame_movement.x
        for rect in tiles_to_check:
            if self.rect.colliderect(rect):
                if frame_movement.x > 0:
                    self.collisions['right'] = True
                    self.rect.right = rect.left
                elif frame_movement.x < 0:
                    self.collisions['left'] = True
                    self.rect.left = rect.right

        self.rect.y += frame_movement.y
        for rect in tiles_to_check:
            if self.rect.colliderect(rect):
                if frame_movement.y > 0:
                    self.collisions['down'] = True
                    self.rect.bottom = rect.top
                elif frame_movement.y < 0:
                    self.collisions['up'] = True
                    self.rect.top = rect.bottom

        # gravity
        self.velocity.y = min(5, self.velocity.y + 0.1)

        if self.collisions['up'] or self.collisions['down']:
            self.velocity.y = 0

    def render(self, destination: pygame.Surface, offset: pygame.Vector2):
        position = (int(self.rect.x - offset.x), int(self.rect.y - offset.y))
        destination.blit(Assets.player, position)
