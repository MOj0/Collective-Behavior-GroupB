import pygame as pg
import random

from Constants import *
from SimEngine import SimEngine
from Boid import *
from Predator import Predator
from Behaviours.HoPePreyAvoidPosition import HoPePreyAvoidPosition
from Behaviours.HoPePreyAvoidDirection import HoPePreyAvoidDirection
from Behaviours.HoPePreyAvoidTurnTime import HoPePreyAvoidTurnTime
from Behaviours.HoPePreyAvoidTurnRandom import HoPePreyAvoidTurnRandom
from Behaviours.HoPePreyAvoidTurnGamma import HoPePreyAvoidTurnGamma
from Behaviours.HoPePreyAvoidZigZag import HoPePreyAvoidZigZag
from Behaviours.HoPePreyBehaviour import HoPePreyBehaviour
from Behaviours.PredatorAttackCentroid import PredatorAttackCentroid
from Behaviours.PredatorAttackNearest import PredatorAttackNearest
from Behaviours.PredatorAttackRandom import PredatorAttackRandom
from Behaviours.PredatorAttackMostPeripheral import PredatorAttackMostPeripheral
import Camera

pg.init()
pg.display.set_caption("Predator and Prey boid simulation")
screen = pg.display.set_mode([WIDTH, HEIGHT], pg.DOUBLEBUF)
clock = pg.time.Clock()
font = pg.font.SysFont("monospace", 22)


simEngine: SimEngine = SimEngine(
    HoPePreyAvoidTurnRandom(), PredatorAttackMostPeripheral(), toroidalCoords=True
)


# NOTE: `add_prey` and `add_predator` needs to be refactored to something more apropriate when necessary
def add_prey(n_prey):
    for i in range(n_prey):
        # random_velocity = pg.Vector2(
        #     random.uniform(-1, 1),
        #     random.uniform(-1, 1),
        # )
        # start_velocity = PREY_CRUISE_VELOCITY * random_velocity.normalize()
        simEngine.addPrey(
            Boid(
                i,
                size=(10 * 2, 6 * 2),
                color=(255, 255, 255),
                position=Vector2(
                    random.uniform(WIDTH / 4, 3 * WIDTH / 4),
                    random.uniform(HEIGHT / 4, HEIGHT / 2),
                ),
                velocity=Vector2(0, -1),
                cruise_velocity=PREY_CRUISE_VELOCITY,
                max_velocity=PREY_MAX_VELOCITY,
                max_acceleration=PREY_MAX_ACCELERATION,
                base_acceleration=PREY_BASE_ACCELERATION,
                max_rotation_angle=PREY_MAX_ROTATION_ANGLE,
                escape_reaction_time=PREY_ESCAPE_REACTION_TIME,
            )
        )


def add_predators(n_predators):
    for i in range(n_predators):
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
            Predator(
                -i - 1,
                size=(20 * 2, 12 * 2),
                color=(255, 0, 0),
                position=Vector2(WIDTH / 2, 4 * HEIGHT / 5),
                velocity=start_velocity,
                cruise_velocity=PREDATOR_CRUISE_VELOCITY,
                max_velocity=PREDATOR_MAX_VELOCITY,
                max_acceleration=PREDATOR_MAX_ACCELERATION,
                base_acceleration=PREDATOR_BASE_ACCELERATION,
                max_rotation_angle=PREDATOR_MAX_ROTATION_ANGLE,
            )
        )


def add_boids():
    add_prey(N_PREY)
    add_predators(N_PREDATORS)


add_boids()

running: bool = True
debug_draw: bool = False
is_update_on: bool = True
do_single_update: bool = True
follow_predator: bool = False
camera_zoom = 1
camera_view = Vector2(WIDTH * camera_zoom, HEIGHT * camera_zoom)
camera_center = Vector2(WIDTH / 2, HEIGHT / 2)
mouse_drag = False

camera = Camera.Camera(Camera.simple_camera, camera_view.x, camera_view.y)
camera.update(camera_center)

while running:
    mouseDelta = pg.mouse.get_rel()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_d:
                debug_draw = not debug_draw
            elif event.key == pg.K_r:
                simEngine.reset()
                add_boids()
            elif event.key == pg.K_SPACE:
                is_update_on = not is_update_on
            elif event.key == pg.K_RIGHT:
                do_single_update = True
            elif event.key == pg.K_s:
                pg.image.save(screen, f"boids_step_{simEngine.getSteps()-1}.jpg")
            elif event.key == pg.K_a:
                simEngine.plot()
            elif event.key == pg.K_p:
                follow_predator = not follow_predator
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_drag = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_drag = False
        elif event.type == pg.MOUSEWHEEL:
            camera_zoom -= event.y / 10
            camera_zoom = max(0.1, camera_zoom)

        if mouse_drag:
            camera_center -= Vector2(mouseDelta[0], mouseDelta[1])

    if is_update_on or do_single_update:
        simEngine.update(DT)
        do_single_update = False

    screen.fill((0, 0, 0))

    if follow_predator and len(simEngine._predators) > 0:
        camera.update(simEngine._predators[0].getPosition())
    else:
        camera.scale(camera_zoom)
        camera.update(camera_center)

    simEngine.draw(camera, screen, debug_draw)
    if debug_draw:
        screen.blit(
            font.render(f"FPS: {int(clock.get_fps())}", 1, (0, 255, 255)), (20, 20)
        )
        screen.blit(
            font.render(f"steps: {simEngine.getSteps()-1}", 1, (0, 255, 255)), (20, 50)
        )

    pg.display.flip()
    clock.tick(FPS)


pg.quit()
