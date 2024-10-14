import pygame

from learn_pygame.assets import Assets


class PhysicsEntity:
    def __init__(self, tag, position: tuple[float, float], size: tuple[int, int]) -> None:
        self.tag = tag
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.FRect(*position, *size)
        self.collisions = dict(up=False, down=False, left=False, right=False)

        self.action = ''
        # TODO: remove this pls
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
    
    def set_action(self, action: str):
        if action != self.action:
            self.action = action
            self.animation = Assets.animations[self.tag][self.action].copy()

    def update(self, tilemap, movement: pygame.Vector2):
        # reset collisions
        self.collisions = dict(up=False, down=False, left=False, right=False)
        
        frame_movement = pygame.Vector2(self.velocity.xy) + movement
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

        if frame_movement.x > 0:
            self.flip = False
        elif frame_movement.x < 0:
            self.flip = True

        self.animation.update()

    def render(self, destination: pygame.Surface, offset: pygame.Vector2):
        position = (int(self.rect.x - offset.x + self.animation_offset[0]), int(self.rect.y - offset.y + self.animation_offset[1]))
        destination.blit(pygame.transform.flip(self.animation.get_frame(), self.flip, False), position)

class Player(PhysicsEntity):
    def __init__(self, position: tuple[float, float], size: tuple[int, int]) -> None:
        super().__init__('player', position, size)
        self.air_time = 0

    def update(self, tilemap, movement: pygame.Vector2):
        super().update(tilemap, movement)
        
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement.x != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
