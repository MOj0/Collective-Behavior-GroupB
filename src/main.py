import pygame as pg
import random

from Constants import *
from SimEngine import SimEngine
from Boid import *
from Behaviours.BasicPreyBehaviour import BasicPreyBehaviour

pg.init()
screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

fps = 60
dt = 1 / fps

drawMode: BoidDrawMode = BoidDrawMode.BASIC
preyBehaviour: BasicPreyBehaviour = BasicPreyBehaviour()
simEngine: SimEngine = SimEngine(preyBehaviour, preyBehaviour)

for i in range(N_PREY):
    simEngine.addPrey(Boid(Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)),
                           Vector2(random.uniform(-10, 10), random.uniform(-10, 10))))

running: bool = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_d:
                drawMode = BoidDrawMode.DEBUG                

    simEngine.update(dt)

    screen.fill((0, 0, 0))
    simEngine.draw(screen, drawMode)
    pg.display.flip()
    clock.tick(fps)


pg.quit()
