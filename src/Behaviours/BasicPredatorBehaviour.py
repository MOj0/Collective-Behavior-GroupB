from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
import Constants
from math import radians


class BasicPredatorBehaviour(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREDATOR_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREDATOR_SEPARATION_DISTANCE,
        angle_of_view: float = Constants.PREDATOR_FOV,
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angle_of_view: float = angle_of_view

    def get_neighbor_prey(self, predator: Boid, prey: list[Boid]):
        neihg_prey: list[Boid] = []
        for p in prey:
            dist_sq = predator.distance_sq_to(p)
            angle_between_boids = predator.angle_between(p)

            if (
                dist_sq < self._perceptionRadius**2
                and angle_between_boids <= self._angle_of_view
            ):
                # Boid occlusion
                occluded_neighbors_idx = predator.occludes_neighbors(
                    angle_between_boids, dist_sq, neihg_prey
                )
                if len(occluded_neighbors_idx) > 0:
                    # Boid is in front of the neighbors
                    # Neighbors should be replaced by the boid
                    for i in reversed(occluded_neighbors_idx):
                        del neihg_prey[i]
                    neihg_prey.append(p)
                elif not predator.is_occluded_by_neighbor(
                    angle_between_boids, dist_sq, neihg_prey
                ):
                    # Boid is not occluded by any neighbor
                    neihg_prey.append(p)

        return neihg_prey

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

    def find_centroid(self, predator: Boid, others: list[Boid]) -> Vector2:
        if len(others) == 0:
            return Vector2(0, 0)

        centroid = Vector2()
        for p in others:
            centroid += p.getPosition() - predator.getPosition()
        return centroid / len(others)

    def update(self, friendlies: list[Boid], prey: list[Boid]) -> None:
        for predator in friendlies:
            c = self.find_centroid(predator, self.get_neighbor_prey(predator, prey))
            b = self._bound_position(predator)
            direction = c + b
            predator.setDesiredDir(direction * 5)

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
