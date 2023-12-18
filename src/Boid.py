from abc import ABC
from pygame import Vector2, Surface, draw, SRCALPHA, transform
from Camera import Camera
import math
from Constants import WIDTH, HEIGHT

OCCLUSION_ANGLE = 2  # deg


class Boid(ABC):
    def __init__(
        self,
        cruise_velocity: float,
        max_velocity: float,
        max_acceleration: float,
        base_acceleration: float,
        max_rotation_angle: float,
        size=(10, 6),
        color=(0, 0, 255),
        position=Vector2(0, 0),
        velocity=Vector2(0, 0),
        acceleration=Vector2(0, 0),
        predation=False,
    ) -> None:
        super().__init__()
        self._width, self._height = size
        self._boid_shape: Surface = Surface(size, SRCALPHA)
        draw.polygon(
            self._boid_shape,
            color,
            [(self._width, self._height / 2), (0, 0), (0, self._height)],
        )

        # Radius of circumcircle used for collision detection
        a = Vector2(self._width, self._height / 2).magnitude()
        b = Vector2(0, self._height).magnitude()
        c = (
            Vector2(self._width, self._height / 2) - Vector2(0, self._height)
        ).magnitude()
        self._r = (
            a * b * c / math.sqrt((a + b + c) * (b + c - a) * (c + a - b) * (a + b - c))
        )

        self._pos: Vector2 = position
        self._vel: Vector2 = velocity
        self._acc: tuple[Vector2, Vector2] = (acceleration, Vector2(0, 0))

        self.cruising_velocity = cruise_velocity
        self.max_velocity = max_velocity
        self.max_acceleration = max_acceleration
        self.base_acceleration = base_acceleration

        self.max_rotation_angle = max_rotation_angle

        # True if under predation (prey) or hunting (predator), False otherwise
        self._predation = predation

    def getPosition(self) -> Vector2:
        return self._pos

    def getVelocity(self) -> Vector2:
        return self._vel

    def getAcceleration(self) -> Vector2:
        return self._acc[0]

    def getPredation(self) -> bool:
        return self._predation

    def setPredation(self, predation):
        self._predation = predation

    def getCollisionRadius(self) -> float:
        return self._r

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

    def collide_with_others(self, others: list["Boid"]) -> list[int]:
        return [
            i
            for i, boid in enumerate(others)
            if (boid.getPosition() - self._pos).length_squared()
            <= (boid.getCollisionRadius() + self._r) ** 2
        ]

    def setDesiredAcceleration(self, new_acc: Vector2) -> None:
        if new_acc.length_squared() == 0:
            self._acc = (self._acc[0], new_acc)
            return

        new_acc.scale_to_length(
            self.base_acceleration if not self._predation else self.max_acceleration
        )

        heading_vec = self._acc[0] if self._acc[0].length_squared() != 0 else self._vel
        if heading_vec.length_squared() != 0:
            new_acc = (
                self._limit_rotation_angle(heading_vec.normalize(), new_acc.normalize())
                * new_acc.magnitude()
            )

        self._acc = (self._acc[0], new_acc)

    def _limit_rotation_angle(self, curr_heading: Vector2, new_dir: Vector2) -> Vector2:
        angle = math.degrees(
            math.atan2(new_dir.y, new_dir.x)
            - math.atan2(curr_heading.y, curr_heading.x)
        )

        min_angle = min(angle % 360, 360 - (angle % 360))
        if min_angle <= self.max_rotation_angle:
            return new_dir

        sign = -1 if -180.0 <= angle <= 0.0 or angle > 180 else 1
        return curr_heading.rotate(sign * self.max_rotation_angle)

    def _velocityCheck(self) -> None:
        speed = self._vel.length()
        if speed == 0:
            return

        if (
            speed < self.cruising_velocity
            or not self._predation
            and speed > self.cruising_velocity
        ):
            self._vel.scale_to_length(self.cruising_velocity)
        elif self._predation and speed > self.max_velocity:
            self._vel.scale_to_length(self.max_velocity)

    def rolloverAcc(self) -> None:
        self._acc = (self._acc[1], Vector2(0, 0))

    def rolloverCoords(self) -> None:
        x = ((self._pos.x + WIDTH/2) % WIDTH) - WIDTH/2
        y = ((self._pos.y + HEIGHT/2) % HEIGHT) - HEIGHT/2
        self._pos = Vector2(x,y)

    def update(self, dt: float) -> None:
        initialVelocity = self._vel

        self._vel += self._acc[1] * dt
        self._velocityCheck()

        self._pos += initialVelocity * dt + (self._acc[1] * dt**2) / 2

    def draw(self, camera: Camera, surface: Surface, debug_draw: bool) -> None:
        _, heading = self._vel.as_polar()
        shape_rotated = transform.rotate(self._boid_shape, -heading)

        surface.blit(
            shape_rotated,
            camera.apply(
                self.getPosition() - (self._width / 2, self._height / 2),
            ),
        )

        if debug_draw:
            draw.line(
                surface,
                (0, 255, 0),
                camera.apply(self.getPosition()),
                camera.apply(self.getPosition() + self.getVelocity() / 10),
            )
            draw.line(
                surface,
                (255, 0, 0),
                camera.apply(self.getPosition()),
                camera.apply(self.getPosition() + self.getAcceleration() / 10),
            )
