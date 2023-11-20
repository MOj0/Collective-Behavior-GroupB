from abc import ABC
from enum import Enum
from pygame import Vector2, Surface, draw, SRCALPHA, transform


class Boid(ABC):
    (BOID_WIDTH, BOID_HEIGHT) = (10, 6)
    BOID_SHAPE: Surface = Surface((BOID_WIDTH, BOID_HEIGHT), SRCALPHA)
    # Draw a triangle onto the boid_shape surface
    draw.polygon(
        BOID_SHAPE,
        (0, 0, 255),
        [(BOID_WIDTH, BOID_HEIGHT / 2), (0, 0), (0, BOID_HEIGHT)],
    )
    MIN_VELOCITY: float = 200.0
    MAX_VELOCITY: float = 500.0

    MAX_ACCELERATION: float = 2000.0
    MAX_TORQUE: float = 1.0

    def __init__(
        self, position=Vector2(0, 0), velocity=Vector2(0, 0), acceleration=Vector2(0, 0)
    ) -> None:
        super().__init__()
        self._pos: Vector2 = position
        self._vel: Vector2 = velocity
        self._acc: tuple[Vector2, Vector2] = (acceleration, Vector2(0, 0))

    def getPosition(self) -> Vector2:
        return self._pos

    def getVelocity(self) -> Vector2:
        return self._vel

    def setDesiredDir(self, value: Vector2) -> None:
        if value.length() > self.MAX_ACCELERATION:
            value.scale_to_length(self.MAX_ACCELERATION)
        self._acc = (self._acc[0], value)

    def _velocityCheck(self) -> None:
        speed: float = self._vel.length()
        if speed < self.MIN_VELOCITY:
            self._vel.scale_to_length(self.MIN_VELOCITY)
        elif speed > self.MAX_VELOCITY:
            self._vel.scale_to_length(self.MAX_VELOCITY)

    def rolloverAcc(self) -> None:
        self._acc = (self._acc[1], Vector2(0, 0))

    def update(self, dt: float) -> None:
        initialVelocity: float = self._vel

        self._vel += self._acc[1] * dt
        self._velocityCheck()

        self._pos += initialVelocity * dt + (self._acc[1] * dt**2) / 2

    def draw(self, surface: Surface, debug_draw: bool) -> None:
        _, heading = self._vel.as_polar()
        shape_rotated = transform.rotate(Boid.BOID_SHAPE, -heading)
        surface.blit(
            shape_rotated,
            self.getPosition() - (Boid.BOID_WIDTH / 2, Boid.BOID_HEIGHT / 2),
        )

        if debug_draw:
            draw.line(
                surface,
                (255, 0, 0),
                self.getPosition(),
                self.getPosition() + self.getVelocity().normalize() * 50,
            )