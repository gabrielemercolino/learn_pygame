import sys
from attrs import define
import pygame
from learn_pygame.assets import Assets
from learn_pygame.tilemap import Tile, Tilemap

RENDER_SCALE = 2.0

@define
class Menu:
    assets_list: list[list[pygame.Surface]]
    current_group: int = 0
    current_variant: int = 0


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
        self.input = dict(left=0, right=0, up=0, down=0, mouse_left_click=0, mouse_right_click=0, grid_mode=0, control=0)

        self.menu = Menu(assets_list=list(Assets.tiles.values())) 

        self.tilemap = Tilemap()
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

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

            
            self.tilemap.render(destination=self.display, offset=self.camera_offset)
            
            # positioning logic
            selected_asset = self.menu.assets_list[self.menu.current_group][self.menu.current_variant].copy()
            selected_asset.set_alpha(100)
            mouse_position = pygame.mouse.get_pos()
            mouse_position = (mouse_position[0] / RENDER_SCALE, mouse_position[1] / RENDER_SCALE)
            tile_position = (int((mouse_position[0] + self.camera_offset.x) // self.tilemap.tile_size), int((mouse_position[1] + self.camera_offset.y) // self.tilemap.tile_size))

            if self.input['grid_mode'] == 0:
                self.display.blit(selected_asset, (tile_position[0] * self.tilemap.tile_size - int(self.camera_offset.x), tile_position[1] * self.tilemap.tile_size - int(self.camera_offset.y)))
            else:
                self.display.blit(selected_asset, mouse_position)

            if self.input['mouse_left_click']:
                if self.input['grid_mode'] == 0:
                    self.tilemap.tilemap[tile_position] = Tile(kind=list(Assets.tiles.keys())[self.menu.current_group], variant=self.menu.current_variant,position=tile_position)
                else:
                    position = (int(mouse_position[0] + self.camera_offset.x), int(mouse_position[1] + self.camera_offset.y))
                    self.tilemap.decorations[position] = Tile(kind=list(Assets.tiles.keys())[self.menu.current_group], variant=self.menu.current_variant,position=position)
                    self.input['mouse_left_click'] = 0
            if self.input['mouse_right_click']:
                if self.input['grid_mode'] == 0:
                    if tile_position in self.tilemap.tilemap:
                        del self.tilemap.tilemap[tile_position]
                else:
                    position = (int(mouse_position[0] + self.camera_offset.x), int(mouse_position[1] + self.camera_offset.y))
                    for pos in list(self.tilemap.decorations.keys()):
                        tile = self.tilemap.decorations[pos]
                        sprite = Assets.tiles[tile.kind][tile.variant]
                        sprite_rect = pygame.Rect(pos[0] - self.camera_offset.x, pos[1] - self.camera_offset.y, sprite.width, sprite.height)
                        if sprite_rect.collidepoint(mouse_position):
                            del self.tilemap.decorations[pos]

            self.display.blit(selected_asset, (5, 5))


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
                case pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_input(event, True)
                case pygame.MOUSEBUTTONUP:
                    self.handle_mouse_input(event, False)

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
                if self.input["control"] == 1:
                    self.tilemap.save('map.json')
            case pygame.K_g:
                self.input["grid_mode"] = int(not bool(self.input["grid_mode"]))
            case pygame.K_LCTRL:
                self.input["control"] = is_down
            case pygame.K_UP:
                if is_down: 
                    self.menu.current_group = (self.menu.current_group + 1) % len(self.menu.assets_list)
                    self.menu.current_variant = 0
            case pygame.K_DOWN:
                if is_down:
                    self.menu.current_variant = (self.menu.current_variant + 1) % len(self.menu.assets_list[self.menu.current_group])

    def handle_mouse_input(self, event: pygame.Event, is_down: bool) -> None:
        match event.button:
            case 1:
                self.input['mouse_left_click'] = is_down
            case 3:
                self.input['mouse_right_click'] = is_down

Editor().run()
