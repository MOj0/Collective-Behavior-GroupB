from Boid import Boid

class Telemetry:

    def __init__(self) -> None:
        self.prevVel: dict[int, float] = {}
        self.turnDurMap: dict[int, float] = {}

    def update(self, friendlies: list[Boid], enemies: list[Boid], dt: float):

        for f in friendlies:

            angle = f.getVelocity().angle_to(f.getAcceleration())

            if (f.getId() not in self.turnAngleMap) \
            and (f.getId() not in self.turnDurMap):
                self.turnAngleMap[f.getId()] = 
                self.turnDurMap[f.getId()] = 0
