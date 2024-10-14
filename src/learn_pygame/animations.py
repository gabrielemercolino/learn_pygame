from attrs import define
import pygame


@define
class Animation:
    images: list[pygame.Surface]
    duration: float = 5
    loop: bool = True
    done: bool = False
    _frame_index: int = 0

    
    def copy(self):
        return Animation(images=self.images, duration=self.duration, loop=self.loop)

    def update(self):
        if self.loop:
            self._frame_index = int((self._frame_index + 1) % (self.duration * len(self.images)))
        else:
            last_index = int(self.duration * len(self.images) - 1)
            self._frame_index = min(self._frame_index + 1, last_index)
            if self._frame_index >= last_index:
                self.done = True

    def get_frame(self):
        return self.images[int(self._frame_index / self.duration)]
