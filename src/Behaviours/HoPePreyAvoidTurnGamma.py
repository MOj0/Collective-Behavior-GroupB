from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from Camera import Camera
from math import radians
import utils
import random


class HoPePreyAvoidTurnGamma(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREY_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREY_SEPARATION_DISTANCE,
        angleOfView: float = Constants.PREY_FOV,
        separationCoef: float = Constants.PREY_SEPARATION_COEFFICIENT,
        cohesionCoef: float = Constants.PREY_COHESION_COEFFICIENT,
        alignmentCoef: float = Constants.PREY_ALIGNMENT_COEFFICIENT,
        escapeCoef: float = Constants.PREY_ESCAPE_COEFFICIENT,
        escapeTurnMean: float = radians(30),
        escapeTurnSD: float = radians(20),
        escapeTimeMean: float = 2, # sec
        escapeTimeSD: float = 1, # sec
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angleOfView: float = angleOfView

        self._separationCoef: float = separationCoef
        self._cohesionCoef: float = cohesionCoef
        self._alignmentCoef: float = alignmentCoef

        self._escapeCoef: float = escapeCoef

        self._turnAlpha: float = (escapeTurnMean / escapeTurnSD) ** 2
        self._turnBeta: float = (escapeTurnSD ** 2) / escapeTurnMean

        self._timeAlpha: float = (escapeTimeMean / escapeTimeSD) ** 2
        self._timeBeta: float = (escapeTimeSD ** 2) / escapeTimeMean

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
            if curBoid.distance_sq_to(boid) < self._separationDistance**2:
                direction -= curBoid.dirTo(boid)

        return direction * self._separationCoef

    def _cohesion(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        if len(neighbors) == 0:
            return Vector2(0, 0)

        direction = Vector2()
        for boid in neighbors:
            direction += curBoid.dirTo(boid)
        direction /= len(neighbors)

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

    def _gamma_t_turn_pred(self, curBoid: Boid, predators: list[Boid]) -> Vector2:
        direction = Vector2()

        for predator in predators:

            turnTime = 0
            turnAmount = 0

            while (turnTime * turnAmount) <= 0:
                turnTime = random.gammavariate(self._timeAlpha, self._timeBeta)
                turnAmount = random.gammavariate(self._turnAlpha, self._turnBeta)

            angularVelocity = turnAmount / turnAmount
            radius = curBoid.getVelocity().magnitude() / angularVelocity

            dirAway = predator.dirTo(curBoid)
            sign = 1 if utils.perpDot2(curBoid.getVelocity(), dirAway) > 0 else -1

            turnDir = sign * utils.perpDot(curBoid.getVelocity())
            fz = curBoid.getVelocity().magnitude() ** 2 / radius

            direction += fz * turnDir

        return direction

    def update(self, friendlies: list[Boid], enemies: list[Boid], dt: float) -> None:
        for boid in friendlies:
            neighbors = self._get_neighbors(boid, friendlies)
            predators = self._get_neighbors(boid, enemies)
            boid.setPredation(len(predators) > 0)

            s = self._separation(boid, neighbors)
            c = self._cohesion(boid, neighbors)
            a = self._alignment(boid, neighbors)
            # b = self._bound_position(boid)

            e = self._gamma_t_turn_pred(
                boid, predators
            )

            boid.setDesiredAcceleration(s + c + a + e)

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
                    2 * self._perceptionRadius,
                    2 * self._perceptionRadius,
                ),
                -heading - radians(self._angleOfView),
                -heading + radians(self._angleOfView),
            )
            draw.circle(
                surface,
                (255, 100, 100),
                camera.apply(boid.getPosition()),
                self._separationDistance,
                width=1,
            )
