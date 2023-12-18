from pygame import Rect, Vector2
from Constants import WIDTH, HEIGHT

class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.rect = Rect(0, 0, width, height)

    def apply(self, target: Vector2):
        view_range = Vector2(WIDTH / (self.rect.bottomright[0] - self.rect.topleft[0]), 
                            HEIGHT / (self.rect.bottomright[1] - self.rect.topleft[1]))
        transformed_target = (target - Vector2(self.rect.topleft)).elementwise() * view_range.elementwise()
        return Vector2(self.rect.topleft) + transformed_target

    # NOTE: Annotation `target: Boid` results in a crash (circular import)
    def update(self, target: Vector2):
        self.rect = self.camera_func(self.rect, target)


def simple_camera(camera: Rect, target: Vector2):
    x, y = target
    _, _, w, h = camera
    return Rect(-x + w // 2, -y + h // 2, w, h)
