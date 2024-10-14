import sys
from attrs import define, field
import pygame
from learn_pygame.assets import Assets
from learn_pygame.tilemap import Tilemap

RENDER_SCALE = 2.0

@define
class Menu:
    assets_list: list[list[pygame.Surface]]
    current_group: int = 0
    current_variant: int = 0
    position: pygame.Vector2 = field(factory=pygame.Vector2)


class Editor:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('editor')
        
        # the window
        self.screen = pygame.display.set_mode((640, 480))
        # the main surface for rendering
        # it is used for scaling and works well with pixel art
        self.display = pygame.Surface((320, 240))

        Assets.load()
        self.clock = pygame.time.Clock()
        self.input = dict(left=0, right=0, up=0, down=0)

        self.menu = Menu(assets_list=list(Assets.tiles.values())) 

        self.tilemap = Tilemap()

        self.camera_offset = pygame.Vector2(0, 0)

        self.running = True

    def run(self) -> None:
        while self.running:
            # clear screen
            self.display.fill((14, 14, 14))

            # check events like keyboard input
            self.check_events(events = pygame.event.get())

            self.camera_offset.x += self.input["right"]-self.input["left"]
            self.camera_offset.y += self.input["down"]-self.input["up"]

            # rendering
            self.tilemap.render(destination=self.display, offset=self.camera_offset)
            selected_asset = self.menu.assets_list[self.menu.current_group][self.menu.current_variant].copy()
            selected_asset.set_alpha(100)
            self.display.blit(selected_asset, self.menu.position)

            # now show the frame
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()

            # wait until enough time has passed so 60fps can be archieved
            self.clock.tick(60)

        sys.exit()

    def check_events(self, events: list[pygame.Event]):
        for event in events:
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYUP:
                    self.handle_keyboard_input(event, False)
                case pygame.KEYDOWN:
                    self.handle_keyboard_input(event, True)
                case pygame.MOUSEMOTION:
                    self.menu.position = pygame.Vector2(event.pos) // RENDER_SCALE
                    self.menu.position.y -= self.menu.assets_list[self.menu.current_group][self.menu.current_variant].height
                    self.menu.position.x -= self.menu.assets_list[self.menu.current_group][self.menu.current_variant].width // 2

    def handle_keyboard_input(self, event: pygame.Event, is_down: bool) -> None:
        match event.key:
            case pygame.K_a:   
                self.input["left"] = is_down
            case pygame.K_d:   
                self.input["right"] = is_down
            case pygame.K_w:
                self.input["up"] = is_down
            case pygame.K_s:
                self.input["down"] = is_down
            case pygame.K_UP:
                if is_down: 
                    self.menu.current_group = (self.menu.current_group + 1) % len(self.menu.assets_list)
                    self.menu.current_variant = 0
            case pygame.K_DOWN:
                if is_down:
                    self.menu.current_variant = (self.menu.current_variant + 1) % len(self.menu.assets_list[self.menu.current_group])


Editor().run()
