from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from Camera import Camera
from math import radians
import utils


class HoPePreyAvoidZigZag(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREY_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREY_SEPARATION_DISTANCE,
        angleOfView: float = Constants.PREY_FOV,
        separationCoef: float = Constants.PREY_SEPARATION_COEFFICIENT,
        cohesionCoef: float = Constants.PREY_COHESION_COEFFICIENT,
        alignmentCoef: float = Constants.PREY_ALIGNMENT_COEFFICIENT,
        escapeCoef: float = Constants.PREY_ESCAPE_COEFFICIENT,
        escapeTurn: float = radians(30),
        zigZagTime: float = 0.7,  # sec
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angleOfView: float = angleOfView

        self._separationCoef: float = separationCoef
        self._cohesionCoef: float = cohesionCoef
        self._alignmentCoef: float = alignmentCoef

        self._escapeCoef: float = escapeCoef

        self._escapeTurn: float = escapeTurn
        self._zigZagTime: float = zigZagTime
        self._zigTimer: float = 0

    def __str__(self) -> str:
        return "HoPePreyAvoidZigZag" 

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

    def _zigzag_turn_pred(self, curBoid: Boid, predators: list[Boid]) -> Vector2:
        direction = Vector2()

        angularVelocity = 2 * self._escapeTurn / self._zigZagTime
        radius = curBoid.getVelocity().magnitude() / angularVelocity

        for predator in predators:
            dirAway = predator.dirTo(curBoid)
            sign = 1 if utils.perpDot2(curBoid.getVelocity(), dirAway) > 0 else -1

            if self._zigTimer > self._zigZagTime:
                sign *= -1

            turnDir = sign * utils.perpDot(curBoid.getVelocity())
            fz = curBoid.getVelocity().magnitude() ** 2 / radius

            direction += fz * turnDir

        return direction

    def update(self, friendlies: list[Boid], enemies: list[Boid], dt: float) -> None:
        for boid in friendlies:
            neighbors = self._get_neighbors(boid, friendlies)
            predators = self._get_neighbors(boid, enemies)
            boid.setPredation(len(predators) > 0)
            if not boid.getPredation():
                boid.setEvasion(False)

            if (
                boid.getEvasion()
                or boid.getPredation()
                and boid.get_curr_escape_reaction_time() <= 0
            ):
                e = self._zigzag_turn_pred(boid, predators)

                boid.setDesiredAcceleration(e)
                boid.setEvasion(True)

                boid.reset_curr_escape_reaction_time()
            else:
                boid.setEvasion(False)

                s = self._separation(boid, neighbors)
                c = self._cohesion(boid, neighbors)
                a = self._alignment(boid, neighbors)
                # b = self._bound_position(boid)

                boid.setDesiredAcceleration(s + c + a)

                if boid.getPredation():
                    boid.decrease_curr_escape_reaction_time(dt)

        if self._zigTimer > 2 * self._zigZagTime:
            self._zigTimer = 0
        else:
            self._zigTimer += dt

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
