from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from math import radians
from random import randrange

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

    def align_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += boid.getVelocity()

        if len(neighbors) > 0:
            direction /= len(neighbors)
        direction -= curBoid.getVelocity()

        return direction
    
    def chohere_turn_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction += (curBoid.getPosition() - boid.getPosition()).normalize()

        if len(neighbors) > 0:
            direction /= len(neighbors)
        return direction
    
    def cohere_speed_action(self, curBoid: Boid, neighbors: list[Boid]) -> float:
        speed = curBoid.getVelocity().magnitude()
        for boid in neighbors:
            speed += boid.getVelocity().magnitude()

        speed /= len(speed) + 1
        return speed
    
    def avoid_friendly_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            direction -= boid.getPosition() - curBoid.getPosition()
        return direction
    
    def wiggle_action(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = curBoid.getVelocity()
        randomAngle = randrange(-5, 5, 0.0001)
        return direction.rotate(randomAngle)
    
    def avoid_enemy_action(self, curBoid: Boid, predators: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in predators:
            direction -= boid.getPosition() - curBoid.getPosition()
        return direction

    def update(self, friendlies: list[Boid], enemies: list[Boid]) -> None:
        pass

    def debug_draw(self, surface: Surface, boids: list[Boid]):
        pass
