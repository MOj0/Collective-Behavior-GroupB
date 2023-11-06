from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2

class BasicPreyBehaviour(Behaviour):

    def __init__(self, perceptionRadius: float = 50, separationDistance: float = 25) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance

    def _get_neighbors(self, curBoid: Boid, boids: list[Boid]) -> list[Boid]:
        neighbors: list[Boid] = []
        for boid in boids:
            if boid is not curBoid:
                dist_sq = curBoid.getPosition().distance_squared_to(boid.getPosition())
                if dist_sq < self._perceptionRadius**2:
                    neighbors.append(boid)

        return neighbors

    def _separation(self, curBoid: Boid, neighbors: list[Boid]) -> Vector2:
        direction = Vector2(0, 0)
        for boid in neighbors:
            if (boid.getPosition() - curBoid.getPosition()).length_squared() \
                < self._separationDistance**2:
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
            direction.x = 10
        elif curBoid.getPosition().x >= self._maxBounds.x:
            direction.x = -10

        if curBoid.getPosition().y <= self._minBounds.y:
            direction.y = 10
        elif curBoid.getPosition().y >= self._maxBounds.y:
            direction.y = -10

        return direction

    def update(self, friendlies: list[Boid], enemies: list[Boid]) -> None:
        for boid in friendlies:
            neighbors = self._get_neighbors(boid, friendlies)
            s = self._separation(boid, neighbors)
            c = self._cohesion(boid, neighbors)
            a = self._alignment(boid, neighbors)
            b = self._bound_position(boid)
            boid.setDesiredDir((s + c + a + b) * 100)