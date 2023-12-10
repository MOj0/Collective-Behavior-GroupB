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
        angleOfView: float = Constants.PREY_FOV,
        separationCoef: float = Constants.PREY_SEPARATION_COEFFICIENT,
        cohesionCoef: float = Constants.PREY_COHESION_COEFFICIENT,
        alignmentCoef: float = Constants.PREY_ALIGNMENT_COEFFICIENT,
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angleOfView: float = angleOfView

        self._separationCoef: float = separationCoef
        self._cohesionCoef: float = cohesionCoef
        self._alignmentCoef: float = alignmentCoef

    def _get_neighbors(self, curBoid: Boid, boids: list[Boid]) -> list[Boid]:
        neighbors: list[Boid] = []
        for boid in boids:
            if boid is not curBoid:
                dist_sq = curBoid.distance_sq_to(boid)

                if (
                    dist_sq < self._perceptionRadius**2
                    and curBoid.angle_between(boid) <= self._angleOfView
                ):
                    neighbors.append(boid)

        return neighbors

    def _separation(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        if len(neighbors) == 0:
            return direction

        for boid in neighbors:
            if (
                boid.getPosition() - curBoid.getPosition()
            ).length_squared() < self._separationDistance**2:
                direction -= boid.getPosition() - curBoid.getPosition()

        return direction * self._separationCoef

    def _cohesion(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        if len(neighbors) == 0:
            return Vector2(0, 0)

        direction = Vector2()
        for boid in neighbors:
            direction += boid.getPosition()
        direction /= len(neighbors)
        direction -= curBoid.getPosition()

        return direction * self._cohesionCoef

    def _alignment(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        if len(neighbors) == 0:
            return Vector2(0, 0)
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += boid.getVelocity()

        direction /= len(neighbors)
        direction -= curBoid.getVelocity()

        return direction * self._alignmentCoef

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
            boid.setDesiredAcceleration(s + c + a + b)

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
                -heading - radians(self._angleOfView),
                -heading + radians(self._angleOfView),
            )
            draw.circle(
                surface,
                (255, 100, 100),
                boid.getPosition(),
                self._separationDistance,
                width=1,
            )
