from Boid import Boid
from Behaviours.Behaviour import Behaviour
from Camera import Camera
from pygame import Surface, draw, Vector2, Rect
from Constants import WIDTH, HEIGHT

class SimEngine:
    def __init__(self, preyBehaviour: Behaviour, predatorBehaviour: Behaviour, toroidalCoords: bool = False) -> None:
        self._preyBehaviour: Behaviour = preyBehaviour
        self._predatorBehaviour: Behaviour = predatorBehaviour
        self._prey: list[Boid] = []
        self._predators: list[Boid] = []
        self.toroidalCoords: bool = toroidalCoords

    def addPrey(self, object: Boid) -> None:
        self._prey.append(object)

    def addPredator(self, object: Boid) -> None:
        self._predators.append(object)

    def clear(self) -> None:
        self.clearPrey()
        self.clearPredators()

    def clearPrey(self) -> None:
        self._prey.clear()

    def clearPredators(self) -> None:
        self._predators.clear()

    def update(self, dt: float):
        remove_prey_indices = set()
        for predator in self._predators:
            remove_prey_indices.update(predator.collide_with_others(self._prey))
        for remove_prey_idx in sorted(remove_prey_indices, reverse=True):
            del self._prey[remove_prey_idx]

        if len(remove_prey_indices) > 0:
            self._predatorBehaviour.selectedPrey = None

        self._preyBehaviour.update(self._prey, self._predators)
        self._predatorBehaviour.update(self._predators, self._prey)

        for p in self._prey:
            p.update(dt)
            p.rolloverAcc()
            if self.toroidalCoords:
                p.rolloverCoords()
        for p in self._predators:
            p.update(dt)
            p.rolloverAcc()
            if self.toroidalCoords:
                p.rolloverCoords()

    def _draw_bounds(self, camera: Camera, surface: Surface):
        bounds = (camera.apply(Vector2(0, 0)), camera.apply(Vector2(WIDTH, HEIGHT)))
        draw.rect(
                surface,
                (255, 255, 255),
                Rect(bounds[0], bounds[1] - bounds[0]),
                1
            )

    def draw(self, camera: Camera, surface: Surface, debug_draw: bool):
        self._draw_bounds(camera, surface)
        for p in self._prey:
            p.draw(camera, surface, debug_draw)
        for p in self._predators:
            p.draw(camera, surface, debug_draw)
        if debug_draw:
            self._preyBehaviour.debug_draw(camera, surface, self._prey)
            self._predatorBehaviour.debug_draw(camera, surface, self._predators)
