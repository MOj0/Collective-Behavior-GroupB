import pygame as pg
import random

from Constants import *
from SimEngine import SimEngine
from Boid import *
from Behaviours.BasicPreyBehaviour import BasicPreyBehaviour

pg.init()
screen = pg.display.set_mode([WIDTH, HEIGHT], pg.DOUBLEBUF)
clock = pg.time.Clock()

FPS = 60
DT = 1 / FPS

preyBehaviour: BasicPreyBehaviour = BasicPreyBehaviour()
simEngine: SimEngine = SimEngine(preyBehaviour, preyBehaviour)


def add_prey(n_prey):
    for _ in range(n_prey):
        random_velocity = pg.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
        )
        start_velocity = (
            (Boid.MIN_VELOCITY + Boid.MAX_VELOCITY)
            / 2
            * random_velocity
            / random_velocity.length()
        )
        simEngine.addPrey(
            Boid(
                Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)),
                start_velocity,
            )
        )


add_prey(N_PREY)

running: bool = True
debug_draw: bool = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_d:
                debug_draw = not debug_draw
            elif event.key == pg.K_r:
                simEngine.clear()
                add_prey(N_PREY)

    simEngine.update(DT)

    screen.fill((0, 0, 0))
    simEngine.draw(screen, debug_draw)
    pg.display.flip()
    clock.tick(FPS)


pg.quit()
