from pygame import Rect, Vector2


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.rect = Rect(0, 0, width, height)

    def apply(self, target: Vector2):
        return target + Vector2(self.rect.topleft)

    # NOTE: Annotation `target: Boid` results in a crash (circular import)
    def update(self, target):
        self.rect = self.camera_func(self.rect, target.getPosition())


def simple_camera(camera: Rect, target: Vector2):
    x, y = target
    _, _, w, h = camera
    return Rect(-x + w // 2, -y + h // 2, w, h)
