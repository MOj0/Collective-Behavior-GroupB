import math
import pygame as pg


def radBetween(a: pg.Vector2, b: pg.Vector2) -> float:
    c = perpDot2(a, b)
    d = a.dot(b)
    return math.atan2(c, d)


def perpDot(v: pg.Vector2) -> pg.Vector2:
    return pg.Vector2(-v.y, v.x)


def perpDot2(a: pg.Vector2, b: pg.Vector2) -> float:
    return a.x * b.y - a.y * b.x


def preyEscapeDir(
    weight: float, predatorVelocity: pg.Vector2, preyVelocity: pg.Vector2
):
    radAwayPred = -radBetween(predatorVelocity, preyVelocity)
    w = math.copysign(weight, radAwayPred)
    return perpDot(preyVelocity) * w
