from typing import Optional
from abc import ABC, abstractmethod
from Boid import Boid
from pygame import Vector2, Surface
from Constants import *
from Camera import Camera


class Behaviour(ABC):
    def __init__(
        self,
        minBounds: Vector2 = Vector2(WIDTH * 0.05, HEIGHT * 0.05),
        maxBounds: Vector2 = Vector2(WIDTH * 0.95, HEIGHT * 0.95),
    ) -> None:
        super().__init__()
        self._minBounds: Vector2 = minBounds
        self._maxBounds: Vector2 = maxBounds
        self.selectedPrey: Optional[Boid] = None

    @abstractmethod
    def update(self, friendlies: list[Boid], enemies: list[Boid]) -> None:
        raise Exception("Missing implementation!")

    @abstractmethod
    def debug_draw(self, camera: Camera, surface: Surface, boids: list[Boid]) -> None:
        raise Exception("Missing implementation!")
