from Behaviours.Behaviour import Behaviour
from Boid import Boid
from pygame import Vector2, Surface, draw
from Camera import Camera
import Constants
from math import radians


class BasicPredatorBehaviour(Behaviour):
    def __init__(
        self,
        perceptionRadius: float = Constants.PREDATOR_PERCEPTION_RADIUS,
        separationDistance: float = Constants.PREDATOR_SEPARATION_DISTANCE,
        angleOfView: float = Constants.PREDATOR_FOV,
    ) -> None:
        super().__init__()
        self._perceptionRadius: float = perceptionRadius
        self._separationDistance: float = separationDistance
        self._angleOfview: float = angleOfView

    def get_neighbor_prey(self, predator: Boid, prey: list[Boid]):
        neigh_prey: list[Boid] = []
        for p in prey:
            dist_sq = predator.distance_sq_to(p)

            if (
                dist_sq < self._perceptionRadius**2
                and predator.angle_between(p) <= self._angleOfview
            ):
                angle_between_boids = predator.angle_between(p)

                # Boid occlusion
                occluded_neighbors_idx = predator.occludes_neighbors(
                    angle_between_boids, dist_sq, neigh_prey
                )
                if len(occluded_neighbors_idx) > 0:
                    # Boid is in front of the neighbors
                    # Neighbors should be replaced by the boid
                    for i in reversed(occluded_neighbors_idx):
                        del neigh_prey[i]
                    neigh_prey.append(p)
                elif not predator.is_occluded_by_neighbor(
                    angle_between_boids, dist_sq, neigh_prey
                ):
                    # Boid is not occluded by any neighbor
                    neigh_prey.append(p)

        return neigh_prey

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
            prey = self.get_neighbor_prey(predator, prey)
            predator.setPredation(len(prey) > 0)

            c = self.find_centroid(predator, prey)
            b = self._bound_position(predator)

            direction = c + b
            predator.setDesiredAcceleration(direction)

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
                -heading - radians(self._angleOfview),
                -heading + radians(self._angleOfview),
            )
            draw.circle(
                surface,
                (255, 100, 100),
                camera.apply(boid.getPosition()),
                self._separationDistance,
                width=1,
            )
