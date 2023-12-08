from abc import ABC
from enum import Enum
from pygame import Vector2, Surface, draw, SRCALPHA, transform

OCCLUSION_ANGLE = 2  # deg


class Boid(ABC):
    def __init__(
        self,
        size=(10, 6),
        color=(0, 0, 255),
        position=Vector2(0, 0),
        velocity=Vector2(0, 0),
        acceleration=Vector2(0, 0),
        cruise_velocity=200.0,
        max_velocity=500.0,
        max_acceleration=2000.0,
        base_acceleration=1200,
        max_rotation_angle=8,
    ) -> None:
        super().__init__()
        self._width, self._height = size
        self._boid_shape: Surface = Surface(size, SRCALPHA)
        draw.polygon(
            self._boid_shape,
            color,
            [(self._width, self._height / 2), (0, 0), (0, self._height)],
        )

        self._pos: Vector2 = position
        self._vel: Vector2 = velocity
        self._acc: tuple[Vector2, Vector2] = (acceleration, Vector2(0, 0))

        self.cruising_velocity = cruise_velocity
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.base_acceleration = base_acceleration

        self.max_rotation_angle = max_rotation_angle

    def getPosition(self) -> Vector2:
        return self._pos

    def getVelocity(self) -> Vector2:
        return self._vel

    def distance_sq_to(self, other: "Boid") -> float:
        return self.getPosition().distance_squared_to(other.getPosition())

    def angle_between(self, other: "Boid") -> float:
        diff = other.getPosition() - self.getPosition()
        angle = self.getVelocity().angle_to(diff) % 360
        return min(angle, 360 - angle)

    # Returns True if there is a neighbor between the `self` and `other` boid (potential neighbor)
    def is_occluded_by_neighbor(
        self, angle_between_other: float, dist_other_sq: float, neighbors: list["Boid"]
    ) -> bool:
        for neighbor in neighbors:
            if (
                abs(angle_between_other - self.angle_between(neighbor))
                < OCCLUSION_ANGLE
                and self.distance_sq_to(neighbor) < dist_other_sq
            ):
                return True

        return False

    # Returns indices of all neighbors which are occluded by the `other` boid
    def occludes_neighbors(
        self, angle_between_other: float, dist_other_sq: float, neighbors: list["Boid"]
    ) -> list[int]:
        occluded_neighbors_idx = []

        for i, n in enumerate(neighbors):
            if (
                abs(angle_between_other - self.angle_between(n)) < OCCLUSION_ANGLE
                and self.distance_sq_to(n) > dist_other_sq
            ):
                occluded_neighbors_idx.append(i)

        return occluded_neighbors_idx

    def setDesiredDir(self, dir: Vector2) -> None:
        new_acceleration = (
            dir.normalize() * self.base_acceleration
            if dir.length_squared() != 0
            else dir
        )

        angle = new_acceleration.angle_to(self._acc[0])
        if angle % 360 > self.max_rotation_angle:
            sign = 1 if angle > 0 and angle < 180 or angle < -180 else -1
            new_acceleration = new_acceleration.rotate(self.max_rotation_angle * sign)

        self._acc = (self._acc[0], new_acceleration)

    def _velocityCheck(self) -> None:
        speed: float = self._vel.length()
        if speed < self.cruising_velocity:
            self._vel.scale_to_length(self.cruising_velocity)
        elif speed > self.max_velocity:
            self._vel.scale_to_length(self.max_velocity)

    def rolloverAcc(self) -> None:
        self._acc = (self._acc[1], Vector2(0, 0))

    def update(self, dt: float) -> None:
        initialVelocity: float = self._vel

        self._vel += self._acc[1] * dt
        self._velocityCheck()

        self._pos += initialVelocity * dt + (self._acc[1] * dt**2) / 2

    def draw(self, surface: Surface, debug_draw: bool) -> None:
        _, heading = self._vel.as_polar()
        shape_rotated = transform.rotate(self._boid_shape, -heading)

        surface.blit(
            shape_rotated,
            self.getPosition() - (self._width / 2, self._height / 2),
        )

        if debug_draw:
            draw.line(
                surface,
                (255, 0, 0),
                self.getPosition(),
                self.getPosition() + self.getVelocity().normalize() * 50,
            )
