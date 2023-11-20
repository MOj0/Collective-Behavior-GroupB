import pygame as pg
import random

from Constants import *
from SimEngine import SimEngine
from Boid import *
from Behaviours.BasicPreyBehaviour import BasicPreyBehaviour

pg.init()
pg.display.set_caption("Predator and Prey boid simulation")
screen = pg.display.set_mode([WIDTH, HEIGHT], pg.DOUBLEBUF)
clock = pg.time.Clock()
font = pg.font.SysFont("monospace", 22)

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
is_update_on: bool = True
do_single_update: bool = True
steps = 0

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
            elif event.key == pg.K_SPACE:
                is_update_on = not is_update_on
            elif event.key == pg.K_COMMA:
                do_single_update = True
            elif event.key == pg.K_s:
                pg.image.save(screen, f"boids_step_{steps-1}.jpg")

    if is_update_on or do_single_update:
        simEngine.update(DT)
        do_single_update = False
        steps += 1

    screen.fill((0, 0, 0))
    simEngine.draw(screen, debug_draw)
    screen.blit(font.render(f"steps: {steps-1}", 1, (0, 255, 255)), (20, 20))

    pg.display.flip()
    clock.tick(FPS)


pg.quit()
