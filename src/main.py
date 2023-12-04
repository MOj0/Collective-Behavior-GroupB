import pygame as pg
import random

from Constants import *
from SimEngine import SimEngine
from Boid import *
from Behaviours.BasicPreyBehaviour import BasicPreyBehaviour
from Behaviours.BasicPredatorBehaviour import BasicPredatorBehaviour

pg.init()
pg.display.set_caption("Predator and Prey boid simulation")
screen = pg.display.set_mode([WIDTH, HEIGHT], pg.DOUBLEBUF)
clock = pg.time.Clock()
font = pg.font.SysFont("monospace", 22)

FPS = 60
DT = 1 / FPS

simEngine: SimEngine = SimEngine(BasicPreyBehaviour(), BasicPredatorBehaviour())


# NOTE: `add_prey` and `add_predator` needs to be refactored to something more apropriate when necessary
def add_prey(n_prey):
    for _ in range(n_prey):
        random_velocity = pg.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
        )
        min_velocity = 200.0
        max_velocity = 500.0
        max_acceleration = 2000.0
        start_velocity = (
            (min_velocity + max_velocity)
            / 2
            * random_velocity
            / random_velocity.length()
        )
        simEngine.addPrey(
            Boid(
                size=(10, 6),
                color=(0, 0, 255),
                position=Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)),
                velocity=start_velocity,
                min_velocity=min_velocity,
                max_velocity=max_velocity,
                max_acceleration=max_acceleration,
            )
        )


def add_predators(n_predators):
    for _ in range(n_predators):
        random_velocity = pg.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
        )
        min_velocity = 200.0
        max_velocity = 500.0
        start_velocity = (
            (min_velocity + max_velocity)
            / 2
            * random_velocity
            / random_velocity.length()
        )
        simEngine.addPredator(
            Boid(
                size=(20, 12),
                color=(255, 0, 0),
                position=Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)),
                velocity=start_velocity,
            )
        )


add_prey(N_PREY)
add_predators(N_PREDATORS)

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
                add_predators(N_PREDATORS)
                steps = 0
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
    if debug_draw:
        screen.blit(
            font.render(f"FPS: {int(clock.get_fps())}", 1, (0, 255, 255)), (20, 20)
        )
        screen.blit(font.render(f"steps: {steps-1}", 1, (0, 255, 255)), (20, 50))

    pg.display.flip()
    clock.tick(FPS)


pg.quit()
