from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from math import radians, copysign
from random import randrange
import utils
from Camera import Camera


class HoPePreyBehaviour(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREY_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREY_SEPARATION_DISTANCE,
        angleOfView: float = Constants.PREY_FOV,
        separationCoef: float = Constants.PREY_SEPARATION_COEFFICIENT,
        cohesionCoef: float = Constants.PREY_COHESION_COEFFICIENT,
        alignmentCoef: float = Constants.PREY_ALIGNMENT_COEFFICIENT,
        escapeCoef: float = Constants.PREY_ESCAPE_COEFFICIENT,
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angleOfView: float = angleOfView

        self._separationCoef: float = separationCoef
        self._cohesionCoef: float = cohesionCoef
        self._alignmentCoef: float = alignmentCoef
        self._escapeCoef: float = escapeCoef

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

    def align_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += boid.getVelocity()

        if len(neighbors) > 0:
            direction /= len(neighbors)
        direction -= curBoid.getVelocity()

        return direction

    def cohere_turn_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += curBoid.dirTo(boid).normalize()

        if len(neighbors) > 0:
            direction /= len(neighbors)
        return direction

    def cohere_speed_action(self, curBoid: Boid, neighbors: list[Boid]) -> float:
        speed = curBoid.getVelocity().magnitude()
        for boid in neighbors:
            speed += boid.getVelocity().magnitude()

        speed /= len(neighbors) + 1
        return speed

    def avoid_friendly_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            if curBoid.distance_sq_to(boid) < self._separationDistance**2:
                direction -= curBoid.dirTo(boid)

        return direction

    def wiggle_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = curBoid.getVelocity()
        randomAngle = radians(randrange(-5, 5) * 0.0001)
        return direction.rotate(randomAngle)

    # https://github.com/marinapapa/a-new-HoPE-model/blob/master/actions/avoid_pred_actions.hpp#L58-L98
    def avoid_enemy_action(self, curBoid: Boid, predators: list[Boid]) -> Vector2:
        direction = Vector2()

        for predator in predators:
            radAwayPred = -utils.radBetween(
                predator.getVelocity(), curBoid.getVelocity()
            )
            weight = copysign(self._escapeCoef, radAwayPred)

            direction += utils.perpDot(curBoid.getVelocity()) * weight

        return direction

    def update(self, friendlies: list[Boid], enemies: list[Boid]) -> None:
        for boid in friendlies:
            neighbors = self._get_neighbors(boid, friendlies)
            predators = self._get_neighbors(boid, enemies)
            boid.setPredation(len(predators) > 0)

            s = self.avoid_friendly_action(boid, neighbors) * self._separationCoef
            c = self.cohere_turn_action(boid, neighbors) * self.cohere_speed_action(
                boid, neighbors
            )
            a = self.align_action(boid, neighbors) * self._alignmentCoef
            w = self.wiggle_action(boid, neighbors)

            e = self.avoid_enemy_action(boid, predators)

            boid.setDesiredAcceleration(s + c + a + w + e)

    def debug_draw(self, camera: Camera, surface: Surface, boids: list[Boid]):
        for boid in boids:
            _, heading = boid.getVelocity().as_polar()
            heading = radians(heading)

            arcCenter = camera.apply(
                boid.getPosition()
                - Vector2(self._perceptionRadius, self._perceptionRadius)
            )

            draw.arc(
                surface,
                (150, 150, 150),
                (
                    *arcCenter,
                    camera.apply(2 * self._perceptionRadius),
                    camera.apply(2 * self._perceptionRadius),
                ),
                -heading - radians(self._angleOfView),
                -heading + radians(self._angleOfView),
            )
            draw.circle(
                surface,
                (255, 100, 100),
                camera.apply(boid.getPosition()),
                camera.apply(self._separationDistance),
                width=1,
            )
