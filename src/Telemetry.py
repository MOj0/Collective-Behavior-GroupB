from Boid import Boid
from copy import deepcopy
from numpy import sign
import matplotlib.pyplot as plt

class Telemetry:

    def __init__(self) -> None:
        self.turnSigma: float = 0.1
        self.minTurnDur: float = 0.1 #sec

        self._prevVel: dict[int, float] = {}
        self._turnAngleMap: dict[int, float] = {}
        self._turnDurMap: dict[int, float] = {}

        self.turnAngleLst: list[float] = []
        self.turnDurLst: list[float] = []

    def _initVars(self, boid: Boid):
        ID = boid.getId()
        if ID not in self._prevVel:
            self._prevVel[ID] = deepcopy(boid.getVelocity())
        if ID not in self._turnDurMap:
            self._turnDurMap[ID] = 0
        if ID not in self._turnAngleMap:
            self._turnAngleMap[ID] = 0

    def _addTurn(self, boid: Boid):
        ID = boid.getId()
        self.turnDurLst.append(self._turnDurMap[ID])
        self.turnAngleLst.append(self._turnAngleMap[ID])

    def _detectTurn(self, boid: Boid, dt: float):
        ID = boid.getId()
    
        angle = boid.getVelocity().angle_to(self._prevVel[ID])
        dur = self._turnDurMap[ID]
        if (abs(angle) < self.turnSigma) or \
            ((sign(self._turnAngleMap[ID]) != 0) and (sign(angle) != sign(self._turnAngleMap[ID]))):
            if (dur > self.minTurnDur):
                self._addTurn(boid)
            self._turnDurMap[ID] = 0
            self._turnAngleMap[ID] = 0
        else:
            self._turnAngleMap[ID] += angle
            self._turnDurMap[ID] += dt

        self._prevVel[ID] = deepcopy(boid.getVelocity())

    def update(self, friendlies: list[Boid], enemies: list[Boid], dt: float):
        for f in friendlies:
            self._initVars(f)
            self._detectTurn(f, dt)

    def _plotTurnDurFreq(self):
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.hist(self.turnDurLst)
        axs.set_xlabel('Turn duration (s)')
        axs.set_ylabel('Frequency')
        fig.show()

    def _plotTurnAngleFreq(self):
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.hist(self.turnAngleLst)
        axs.set_xlabel('Turn angle (deg)')
        axs.set_ylabel('Frequency')
        fig.show()


    def plotResults(self):
        self._plotTurnDurFreq()
        self._plotTurnAngleFreq()




