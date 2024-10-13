import sys, threading
import pygame
from learn_pygame.assets import Assets
from learn_pygame.entities import PhysicsEntity
from learn_pygame.tilemap import Tilemap


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('sus')
        
        # the window
        self.screen = pygame.display.set_mode((640, 480))
        # the main surface for rendering
        # it is used for scaling and works well with pixel art
        self.display = pygame.Surface((320, 240))

        Assets.load()
        self.clock = pygame.time.Clock()
        self.input = dict(left=0, right=0)

        self.player = PhysicsEntity('player', (50, 50), (8, 15))
        self.tilemap = Tilemap()

        self.camera_offset = pygame.Vector2(0, 0)

        self.running = True

    def run(self) -> None:
        logic_thread = threading.Thread(target=self.update)
        logic_thread.start()

        while self.running:
            # clear screen
            #self.display.fill((14, 14, 14))
            self.display.blit(Assets.background, (0, 0))

            # check events like keyboard input
            self.check_events(events = pygame.event.get())

            # rendering
            self.camera_offset.x += int((self.player.rect.centerx - self.display.get_width() / 2 - self.camera_offset.x) / 15)
            self.camera_offset.y += int((self.player.rect.centery - self.display.get_height() / 2 - self.camera_offset.y) / 15)
            self.tilemap.render(destination=self.display, offset=self.camera_offset)
            self.player.render(destination=self.display, offset=self.camera_offset)
            
            # now show the frame
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()

            # wait until enough time has passed so 60fps can be archieved
            self.clock.tick(60)

        self.running = False # it theory is not needed but whatever
        logic_thread.join()
        sys.exit()

    def update(self) -> None:
        while self.running:
            self.player.update(self.tilemap, pygame.Vector2(self.input["right"]-self.input["left"], 0))

            pygame.time.Clock().tick(60)

    def check_events(self, events: list[pygame.Event]):
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYUP:
                    self.handle_input(event, False)
                case pygame.KEYDOWN:
                    self.handle_input(event, True)

    def handle_input(self, event: pygame.Event, is_down: bool) -> None:
        match event.key:
            case pygame.K_a:   
                self.input["left"] = is_down
            case pygame.K_d:   
                self.input["right"] = is_down
            case pygame.K_SPACE:
                if is_down: self.player.velocity[1] = -3


def main():
    Game().run()
