from Boid import Boid
from Behaviours.Behaviour import Behaviour
from pygame import Surface


class SimEngine:
    def __init__(self, preyBehaviour: Behaviour, predatorBehaviour: Behaviour) -> None:
        self._preyBehaviour: Behaviour = preyBehaviour
        self._predatorBehaviour: Behaviour = predatorBehaviour
        self._prey: list[Boid] = []
        self._predators: list[Boid] = []

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
        self._preyBehaviour.update(self._prey, self._predators)
        self._predatorBehaviour.update(self._predators, self._prey)

        for p in self._prey:
            p.update(dt)
            p.rolloverAcc()
        for p in self._predators:
            p.update(dt)
            p.rolloverAcc()

    def draw(self, surface: Surface, debug_draw: bool):
        for p in self._prey:
            p.draw(surface, debug_draw)
        for p in self._predators:
            p.draw(surface, debug_draw)
        if debug_draw:
            self._preyBehaviour.debug_draw(surface, self._prey)
            self._predatorBehaviour.debug_draw(surface, self._predators)
