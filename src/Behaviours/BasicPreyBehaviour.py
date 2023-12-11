from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from math import radians


class BasicPreyBehaviour(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREY_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREY_SEPARATION_DISTANCE,
        angle_of_view: float = Constants.PREY_FOV,
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angle_of_view: float = angle_of_view

    def _get_neighbors(self, curBoid: Boid, boids: list[Boid]) -> list[Boid]:
        neighbors: list[Boid] = []
        for boid in boids:
            if boid is not curBoid:
                dist_sq = curBoid.distance_sq_to(boid)
                angle_between_boids = curBoid.angle_between(boid)

                if (
                    dist_sq < self._perceptionRadius**2
                    and angle_between_boids <= self._angle_of_view
                ):
                    # Boid occlusion
                    occluded_neighbors_idx = curBoid.occludes_neighbors(
                        angle_between_boids, dist_sq, neighbors
                    )
                    if len(occluded_neighbors_idx) > 0:
                        # Boid is in front of the neighbors
                        # Neighbors should be replaced by the boid
                        for i in reversed(occluded_neighbors_idx):
                            del neighbors[i]
                        neighbors.append(boid)
                    elif not curBoid.is_occluded_by_neighbor(
                        angle_between_boids, dist_sq, neighbors
                    ):
                        # Boid is not occluded by any neighbor
                        neighbors.append(boid)

        return neighbors

    def _separation(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            if (
                boid.getPosition() - curBoid.getPosition()
            ).length_squared() < self._separationDistance**2:
                direction -= boid.getPosition() - curBoid.getPosition()

        return direction

    def _cohesion(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        if len(neighbors) == 0:
            return Vector2(0, 0)
        direction = Vector2()
        for boid in neighbors:
            direction += boid.getPosition() - curBoid.getPosition()
        direction /= len(neighbors)
        return direction / 100  # Move 1% to the center

    def _alignment(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        if len(neighbors) == 0:
            return Vector2(0, 0)
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += boid.getVelocity()

        direction /= len(neighbors)
        direction -= curBoid.getVelocity()
        return direction / 8

    def _bound_position(self, curBoid: Boid):
        direction = Vector2(0, 0)
        if curBoid.getPosition().x <= self._minBounds.x:
            direction.x = 1
        elif curBoid.getPosition().x >= self._maxBounds.x:
            direction.x = -1

        if curBoid.getPosition().y <= self._minBounds.y:
            direction.y = 1
        elif curBoid.getPosition().y >= self._maxBounds.y:
            direction.y = -1

        return direction * 10

    def update(self, friendlies: list[Boid], enemies: list[Boid]) -> None:
        for boid in friendlies:
            neighbors = self._get_neighbors(boid, friendlies)
            s = self._separation(boid, neighbors)
            c = self._cohesion(boid, neighbors)
            a = self._alignment(boid, neighbors)
            b = self._bound_position(boid)
            direction = s + c + a + b
            boid.setDesiredDir(direction * 60 * 2)

    def debug_draw(self, surface: Surface, boids: list[Boid]):
        for boid in boids:
            _, heading = boid.getVelocity().as_polar()
            heading = radians(heading)

            draw.arc(
                surface,
                (150, 150, 150),
                (
                    *(
                        boid.getPosition()
                        - Vector2(self._perceptionRadius, self._perceptionRadius)
                    ),
                    2 * self._perceptionRadius,
                    2 * self._perceptionRadius,
                ),
                -heading - radians(self._angle_of_view),
                -heading + radians(self._angle_of_view),
            )
            draw.circle(
                surface,
                (255, 100, 100),
                boid.getPosition(),
                self._separationDistance,
                width=1,
            )
